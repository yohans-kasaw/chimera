# Domain Architecture Strategy

## 1. Executive Summary
This document defines the architectural strategy for Project Chimera, translating the high-level requirements from the SRS into concrete structural decisions. The focus is on scalability, safety, and data integrity for a swarm of autonomous influencer agents.

## 2. Agent Pattern: Hierarchical Swarm (FastRender Pattern)

### Decision
We select the **Hierarchical Swarm** pattern (specifically the "FastRender" implementation detailed in the SRS) over a Sequential Chain (e.g., LangChain chains).

### Rationale
*   **Parallelism vs. Latency:** Sequential chains are blocking; if step 2 fails, the whole chain stops. A swarm allows multiple "Workers" to execute tasks in parallel (e.g., generating 50 replies simultaneously).
*   **Specialization:** By decoupling "Planning" (Strategy) from "Working" (Execution) and "Judging" (Review), we prevent context pollution. A Worker doesn't need to know the entire campaign history, only the specific task at hand.
*   **Resilience:** If one Worker fails, the Planner simply re-queues the task. The system is self-healing.

### Architecture Diagram

```mermaid
graph TD
    User((Human Operator)) -->|Sets Goal| Planner[Planner Agent]
    
    subgraph "The FastRender Swarm"
        Planner -->|Decomposes| TaskQueue[(Redis Task Queue)]
        
        TaskQueue -->|Polls| Worker1[Worker Agent 1]
        TaskQueue -->|Polls| Worker2[Worker Agent 2]
        TaskQueue -->|Polls| Worker3[Worker Agent 3]
        
        Worker1 -->|Output| ReviewQueue[(Review Queue)]
        Worker2 -->|Output| ReviewQueue
        Worker3 -->|Output| ReviewQueue
        
        ReviewQueue -->|Polls| Judge[Judge Agent]
    end
    
    Judge -->|Validates| Decision{Confidence > 0.9?}
    Decision -->|Yes| GlobalState[(Global State)]
    Decision -->|No| Planner
    Decision -->|Unsure/Sensitive| HITL[Human Review]
```

## 3. Human-in-the-Loop (HITL): The Safety Layer

### Location of Approval
The Human-in-the-Loop safety layer is strictly enforced at the **Post-Generation / Pre-Publication** stage, managed by the **Judge Agent**.

### Implementation Strategy
The "Judge" is the architectural bottleneck designed to prevent unsafe content from leaking to the public internet. It functions as a specialized firewall.

1.  **Confidence-Based Routing:**
    *   **High Confidence (>0.9):** Automated pass.
    *   **Medium Confidence (0.7-0.9):** Routed to **Orchestrator Dashboard** for async human approval.
    *   **Low Confidence (<0.7):** Auto-reject and retry.
2.  **Mandatory Filters:** Any content triggering "Sensitive Topic" classifiers (politics, finance) bypasses the confidence score and goes straight to HITL.

### Governance Workflow

```mermaid
sequenceDiagram
    participant W as Worker Agent
    participant J as Judge Agent
    participant DB as Postgres/Redis
    participant H as Human Moderator
    participant Pub as Social Platform

    W->>J: Submit Draft Content
    J->>J: Analyze Safety & Consistency
    
    alt High Confidence
        J->>Pub: Publish via MCP
        J->>DB: Log Success
    else Medium Confidence / Sensitive
        J->>DB: Queue for Approval (Status: PENDING)
        H->>DB: Fetch Pending Items
        H->>DB: Approve Item
        DB->>Pub: Trigger Publication
    else Low Confidence
        J->>W: Reject (Feedback Loop)
    end
```

## 4. Database Strategy: SQL (PostgreSQL) for Metadata

### Decision
We select **SQL (PostgreSQL)** as the primary store for high-velocity video metadata and operational logs, supplemented by **Redis** for the immediate ingestion queue.

### Rationale
*   **Relational Integrity:** Video metadata (file paths, duration, prompts, timestamps) is not isolated; it is deeply relational. It must link to a specific `AgentID`, a `CampaignID`, and a `LedgerTransactionID` (cost tracking). SQL ensures these relationships are enforced (Referential Integrity).
*   **JSONB Flexibility:** Modern PostgreSQL supports `JSONB`, allowing us to store flexible/unstructured metadata (e.g., varying API responses from generative video tools) while identifying it with structured columns.
*   **Transactional Accuracy:** The SRS emphasizes "Agentic Commerce" and "Budget Governance". We cannot risk "eventual consistency" (common in some NoSQL) when tracking the financial cost of video generation. We need ACID compliance to ensure that if a video is generated, the cost is deducted from the budget atomically.
*   **Operational Logs:** The "high-velocity" aspect is handled by the **Redis** layer for the `TaskQueue` and `Episodic Memory`. Once the task is complete (video generated), the final robust record is written to PostgreSQL.

### Data Topology

| Data Type | Storage Engine | Purpose |
| :--- | :--- | :--- |
| **Transactional/Metadata** | **PostgreSQL** | User accounts, Campaign config, Video Metadata (Asset Library), Financial Audit Logs. |
| **Hot Queue/State** | **Redis** | Task queues, Short-term conversation history, Rate limits. |
| **Semantic Knowledge** | **Weaviate** | Long-term memory, Persona definitions that need semantic search. |
| **Video Assets** | **S3 / Blob Storage** | The actual video files (referenced by URL in Postgres). |

## 5. Project Decomposition: Autonomous Workstreams

To execute this architecture efficiently, we decompose the system into 5 independent workstreams suitable for parallel development by autonomous teams.

### Workstream A: The Cognitive Swarm (Core Logic)
**Objective:** Build the central nervous system—the decision-making loop and task execution engine.
*   **Key Components:** `Planner Service`, `Worker Pool`, `Judge Service`, `Task Queue (Redis)`.
*   **Specific Tasks:**
    *   **Planner Agent:** Decompose `Campaign Goals` into a DAG of tasks using `Gemini 3 Pro`.
    *   **Worker Agent:** Atomic task execution agent that consumes `TaskQueue`.
    *   **Judge Agent:** Review logic using **Harm Perception** and validation against `GlobalState`.
    *   **Queue Infra:** `pydantic` schemas for `Task` and `Result` over Redis.
*   **Boundaries:** Owns the logic of *how* an agent thinks. Interfaces with MCP tools (via standard protocols) and Memory.

### Workstream B: Perception & Memory (Data Layer)
**Objective:** Provide identity, history, and context awareness (`RAG` & `SOUL`).
*   **Key Components:** `Cognitive Core`, `Weaviate Ops`, `Persona Loader`, `PostgreSQL Metadata`.
*   **Specific Tasks:**
    *   **Persona Engine:** Parser for `SOUL.md` (GitOps personality management).
    *   **RAG Pipeline:** `assemble_context()` logic fetching from Weaviate.
    *   **Memory Lifecycle:** Summarization loop writing back to Long-term memory.
    *   **SQL Schema:** Designs for User, Campaign, and Asset tables.
*   **Boundaries:** Owns the "Context Window" construction.

### Workstream C: Connectivity & Tools (MCP Layer)
**Objective:** Build the "Hands & Eyes" by wrapping external APIs into standardized MCP Servers.
*   **Key Components:** `MCP Servers`, `Tool Definitions`.
*   **Specific Tasks:**
    *   **Social Wrappers:** `mcp-server-twitter`, `mcp-server-instagram`.
    *   **Safety Middleware:** "Dry Run" modes and Rate Limiting logic.
    *   **Trend Spotter:** RSS/API pollers for new tasks.
*   **Boundaries:** Owns all 3rd party API integrations. Exposes standard JSON-RPC tools.

### Workstream D: Agentic Commerce (FinOps)
**Objective:** Enable financial autonomy and budget governance.
*   **Key Components:** `Coinbase AgentKit`, `CFO Judge`, `Ledger`.
*   **Specific Tasks:**
    *   **Wallet Integration:** `CdpEvmWalletProvider` for persistent wallets.
    *   **CFO Judge:** Intercepts financial tool calls to enforce `daily_spend` limits.
    *   **Transaction Tools:** `transfer_asset`, `check_balance`.
*   **Boundaries:** Owns the private keys and the ledger.

### Workstream E: Control Plane (Dashboard & HITL)
**Objective:** Management interface and the human safety layer.
*   **Key Components:** `Orchestrator Dashboard`, `ReviewQueue UI`, `Fleet Status API`.
*   **Specific Tasks:**
    *   **Mission Control:** React dashboard for Agent Status and Wallet Bounds.
    *   **HITL Review:** Interactive cards for approving flagged tasks.
    *   **API Gateway:** REST API for the frontend over Postgres/Redis.
*   **Boundaries:** Owns the UX and Manual Override.

## 6. High-Level Project Roadmap

The dependency structure implies a "Core-First" rollout strategy.

### Phase 1: Genesis (Weeks 1-2)
*   **Goal:** A functioning "Brain" in a jar.
*   **Key Deliverables:**
    *   [A] Basic Planner-Worker loop running against Mock Tools.
    *   [B] Database setup (Postgres/Weaviate) & `SOUL` parser.
    *   [C] `mcp-server-sqlite` for testing tool interfaces.
    *   [D] Wallet key management setup.
    *   [E] CLI-based dashboard.

### Phase 2: Connectivity (Weeks 3-4)
*   **Goal:** The Brain gets Senses.
*   **Key Deliverables:**
    *   [A] Judge logic implementation (Consistency checks).
    *   [B] RAG pipeline fully integrated into System Prompt.
    *   [C] `mcp-server-twitter` (Read-only) & RSS pollers connected.
    *   [D] `get_balance` tools integrated.
    *   [E] Read-only Web Dashboard (Fleet view).

### Phase 3: Agency (Weeks 5-6)
*   **Goal:** The Agent can Act.
*   **Key Deliverables:**
    *   [A] Full Swarm scaling (Multiple workers).
    *   [B] Long-term memory writing (writing back to Weaviate).
    *   [C] Write-access social tools enabled.
    *   [D] `transfer_asset` tools & CFO Judge enforcement.
    *   [E] HITL "Approve/Reject" buttons live in UI.

### Phase 4: Production (Weeks 7-8)
*   **Goal:** Stability and Safety.
*   **Key Deliverables:**
    *   End-to-end load testing.
    *   Rate limit tuning across all MCP servers.
    *   Security audits (Wallet & Injection attacks).
    *   "Trend Spotter" fully automated automation.
