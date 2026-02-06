# 002: Skills + MCP Workflow Framework

## Overview
Project Chimera needs a formal Skills framework that translates agent intent into deterministic workflows and MCP tool calls. Skills provide typed input/output contracts, while workflows orchestrate multi-step logic with traceable execution.

## Goals
- Establish a Skills registry with Pydantic input/output contracts.
- Provide a workflow runner that executes ordered skill steps.
- Connect skills to MCP tools through the MCP client abstraction.
- Ensure traceability with structured run records.

## Non-Goals
- Implement production MCP servers (handled in Workstream C).
- Replace Planner/Worker orchestration (skills integrate with them, not replace them).
- Provide a full UI for skill execution.

## Architecture
The Skills framework sits between agent intent and pipeline execution:

```
Agent Intent
  -> Skill Invocation
    -> Workflow Runner
      -> MCP Client / Providers
```

### Key Components
- **Skill Base Class**: Defines the execution interface and contracts.
- **Skill Registry**: Registers and discovers skills by name.
- **Workflow Runner**: Executes steps sequentially with structured results.
- **MCP Tool Skill**: Standard wrapper for MCP tool execution.

## Data Contracts
### Skill Definition
| Field | Type | Description |
| --- | --- | --- |
| name | string | Unique skill identifier. |
| description | string | Human-readable skill intent. |
| input_model | Pydantic model | Input validation contract. |
| output_model | Pydantic model | Output validation contract. |

### Workflow Step
| Field | Type | Description |
| --- | --- | --- |
| skill_name | string | Skill identifier. |
| input | object | Raw input payload for the skill. |

### Workflow Run Record
| Field | Type | Description |
| --- | --- | --- |
| skill_name | string | Skill identifier. |
| status | enum | succeeded/failed. |
| output | object | Output payload. |
| error | string? | Error message if failed. |
| completed_at | datetime | Completion timestamp. |

## Sample Workflows
### 1. Handle Normalization
1. `echo` (optional checkpoint)
2. `normalize_handle` (canonicalize social handle)

### 2. MCP Tool Invocation
1. `mcp_tool` (call MCP tool with dynamic payload)

## Implementation Mapping
- Skills package: [src/chimera/skills](../../src/chimera/skills)
- Workflow pipeline: [src/chimera/pipelines/skills_workflow.py](../../src/chimera/pipelines/skills_workflow.py)
- MCP sample configuration: [mcp.sample.json](../../mcp.sample.json)

## Acceptance Criteria (Gherkin)

### AC-001: Skill Registration (Happy Path)
*   **Trace**: [Data Contract]
*   **Scenario**: Valid Skill Registration
    *   **Given** a Python class inheriting from `BaseSkill`
    *   **And** it defines valid Pydantic input/output models
    *   **When** I call `registry.register(MySkill)`
    *   **Then** the skill is retrievable by name "MySkill"

### AC-002: Workflow Execution (Happy Path)
*   **Trace**: [Workflow Step]
*   **Scenario**: Multi-step Execution
    *   **Given** a workflow with steps `[echo, normalize]`
    *   **When** the workflow runner executes
    *   **Then** step 1 output is passed to step 2
    *   **And** the final result matches the normalized string
    *   **And** a run record is created with `status="succeeded"`

### AC-003: Validation Failure (Failure Mode)
*   **Trace**: [Skill Definition]
*   **Scenario**: Invalid Input Data
    *   **Given** a skill requiring `email: EmailStr`
    *   **When** I invoke it with `email="not-an-email"`
    *   **Then** a `PydanticValidationError` is raised
    *   **And** the workflow halts immediately

### AC-004: MCP Tool Integration (Edge Case)
*   **Trace**: [MCP Tool Skill]
*   **Scenario**: Missing Client
    *   **Given** an `MCPSkill` configured for tool "weather"
    *   **When** I execute it without an active `MCPClient`
    *   **Then** a `RuntimeError` is raised "MCP Client not configured"

## Security & Compliance *(mandatory)*
This feature adheres to the [Master Security Architecture](../technical.md#7-security-architecture--compliance-rubric-pro).

*   **Authentication**: Uses standard OAuth2/JWT flow via the CommerceManager.
*   **Secrets Management**: All credentials managed via Vault/Env.
*   **Rate Limiting**: Enforces standard 60 req/min limit.
*   **Content Safety**: Subject to standard Moderation/Judge pipeline.
*   **Containment**: Strict Resource Limits apply (Execution Time, Token Budget).
