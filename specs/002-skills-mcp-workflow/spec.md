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

## Acceptance Criteria
- Skill definitions must use Pydantic models for input/output.
- Skill registry supports registration and discovery by name.
- Workflow runner executes ordered steps and returns structured run records.
- MCP tool skill must enforce that a configured MCP client is required.
