# Backend Architecture & Agent Framework Specification

## 1. Architectural Overview

Project Chimera utilizes a **Modular Monolith** architecture powered by **Python 3.12+** and **FastAPI**. It is designed to host a high-velocity swarm of autonomous agents that interact with external protocols (OpenClaw) and social networks (MoltBook).

### Core Layers
1.  **Interface Layer**: Exposes REST endpoints (FastAPI) and WebSocket/Streams (OpenClaw/MoltBook adapters).
2.  **Orchestration Layer**: Manages the lifecycle of swarms, tasks, and state persistence.
3.  **Agent Runtime (The "Brain")**: A specialized loop that resolves Intent -> Skills -> Tools.
4.  **Skill Registry**: A library of atomic, typed capabilities (Tools) that agents can invoke.
5.  **Infrastructure**: PostgreSQL (State), Redis (Queues/Cache), Weaviate (Memory).

---

## 2. Agent Framework Implementation

We do not use off-the-shelf frameworks like AutoGen or LangChain directly. Instead, we implement a **lightweight, type-safe Agent Loop** using **Pydantic** and **LLM Function Calling**.

### 2.1. The "Think-Act-Observe" Loop
The core agent runtime (`src/chimera/agent/runtime.py`) implements this state machine:

1.  **Observe**: Fetch `Task` input + `AgentMemory` (Weaviate) + Current Context.
2.  **Think**: Send prompt + available `Skills` (as tools) to the LLM.
3.  **Act**:
    *   If LLM requests a Tool Call -> Execute `Skill`.
    *   If LLM returns text -> Update `Task` status.
4.  **Loop**: Feed Tool Result back to "Observe" until `Task` is complete or max turns reached.

### 2.2. Skills & Tool Integration
*   **Definition**: Skills are Python classes inheriting from `BaseSkill` with Pydantic `input_model` and `output_model`.
*   **MCP Integration**: The `MCPSkill` wrapper allows any Model Context Protocol (MCP) server to be exposed as a native Agent Skill.

```python
# Conceptual Implementation
class BaseSkill(ABC):
    name: str
    description: str
    input_model: Type[BaseModel]
    
    async def execute(self, context: AgentContext, params: BaseModel) -> Result:
        ...
```

---

## 3. Integration Specifications

### 3.1. OpenClaw (Agent Network)
*   **Protocol**: WebSockets / HTTP Webhooks.
*   **Role**: The "Public Face" of the swarm.
*   **Implementation**: `src/chimera/integrations/openclaw.py`
    *   **Listener**: Subscribes to `agent.assign` topic.
    *   **Publisher**: Pushes heartbeat and status updates.

### 3.2. MoltBook (Social Network)
*   **Role**: The primary "Work Environment" for influencer agents.
*   **Implementation**: `src/chimera/integrations/moltbook.py`
*   **Capabilities**:
    *   `MoltBookPost`: Create content.
    *   `MoltBookReply`: Interact with users.
    *   `MoltBookAnalytics`: Fetch engagement metrics.
*   **Authentication**: Uses API Key injection via `CommerceManager` (secure wallet/vault).

---

## 4. API Contracts & I/O Schemas

All backend services must expose OpenAPI 3.1 compliant schemas.

### 4.1. Swarm Management API
*   **Path**: `/api/v1/swarm`
*   **Spec**: `specs/001-observable-mcp-swarm/contracts/openapi.yaml`

### 4.2. Commerce API
*   **Path**: `/api/v1/commerce`
*   **Spec**: `specs/001-agentic-commerce/contracts/openapi.yaml`

### 4.3. MoltBook Connect API (New)
*   **Path**: `/api/v1/integrations/moltbook`
*   **Schema**:
    ```json
    {
      "POST /connect": {
        "description": "Link a MoltBook account to a Tenant",
        "body": { "api_key": "sk_...", "handle": "@agent_x" }
      },
      "GET /status": {
        "response": { "connected": true, "last_sync": "iso-8601" }
      }
    }
    ```

---

## 5. Testing & Quality Assurance

### 5.1. Test Pyramid Strategy
1.  **Unit Tests (60%)**: Test `Skills` logic and `Pydantic` validation in isolation.
    *   *Tool*: `pytest`
2.  **Integration Tests (30%)**: Test API endpoints against real Dockerized DBs (Postgres/Redis).
    *   *Tool*: `pytest-asyncio` + `testcontainers` (or docker-compose services).
3.  **Agent Simulation Tests (10%)**: Deterministic replay of agent runs.
    *   *Strategy*: Mock the LLM via `vcrpy` or a custom `MockLLM` that returns pre-defined tool calls for specific prompts.
    *   *Goal*: Ensure the "Think-Act" loop handles tool outputs correctly without burning tokens.

### 5.2. Acceptance Criteria
*   **Code**: Python 3.12+, 100% Type Annotated (`mypy strict`).
*   **Docs**: All public modules must have docstrings.
*   **Coverage**: Minimum 80% line coverage.
*   **Safety**: No secrets in code (enforced by `bandit` and `pre-commit`).
