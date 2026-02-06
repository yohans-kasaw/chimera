# Implementation Plan: Observable MCP Agent Swarm

**Branch**: `001-observable-mcp-swarm` | **Date**: 2026-02-06 | **Spec**: [specs/001-observable-mcp-swarm/spec.md](specs/001-observable-mcp-swarm/spec.md)
**Input**: Feature specification from `/specs/001-observable-mcp-swarm/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deliver a minimal but operational “brain” that orchestrates a tenant-isolated swarm with clear architectural boundaries:

- **Planner** creates validated `Task` payloads and pushes them to a Redis-backed queue.
- **Worker** consumes tasks atomically and produces validated `Result` payloads.
- **Judge** validates results, applies a gate decision (`approve`/`deny`/`hitl`), logs the outcome, and only then allows results to be committed to shared state.

This plan focuses on strict contracts + observability first, so autonomy can scale without leaking tenant data or allowing unsafe side effects.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12 (from `pyproject.toml`)  
**Primary Dependencies**: Pydantic v2, redis-py, structlog, MCP SDK (package: `mcp`)  
**Storage**: Redis (hot queues + episodic state). PostgreSQL is the long-term target for audit logs (per constitution), but not required for the MVP “brain” tests.  
**Testing**: pytest, pytest-asyncio, pytest-cov (coverage target ≥ 90%)  
**Target Platform**: Linux server (developer workstation + CI)  
**Project Type**: Single Python project (src layout)  
**Performance Goals**: Efficient task consumption under fan-out (baseline: consume in batches where possible; avoid per-task reconnect).  
**Constraints**: Strict typing (`mypy --strict`), strict schemas (`extra='forbid'`), no cross-tenant access; structured logging for all decisions.  
**Scale/Scope**: MVP supports 1 tenant, 1 session, and a small worker pool; architecture must generalize to many workers without changing contracts.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

PASS/PLAN (no open violations):

1. **MCP-First Integration (No Direct API Coupling)**
  - MVP “brain” performs no direct third-party API calls; skills/tooling integration is represented behind interfaces compatible with MCP tools.
2. **Swarm Roles Are Architectural Boundaries**
  - Planner/Worker/Judge are explicit boundaries with strict I/O contracts.
  - Workers are stateless/atomic: one task in → one result out.
  - Parallelism is via Redis fan-out (no worker-to-worker coordination).
3. **Safety + HITL Is Enforced Pre-Publication**
  - Judge is the single gate to committing results; decision + rationale are logged.
  - Confidence routing thresholds are defined at the policy layer; MVP wires the interfaces and logging, with policy behavior covered by tests.
4. **Economic Agency Requires Budget Governance**
  - Out of scope for MVP; architecture keeps “sensitive actions” behind Judge policies so a CFO policy layer can be added without changing task/result contracts.
5. **Python Quality, Reproducibility, and Type Safety**
  - All code must remain ruff/mypy/pytest clean, with ≥ 90% coverage.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── chimera/
  ├── __init__.py
  ├── models/
  │   ├── task.py
  │   └── result.py
  ├── ports/
  │   ├── llm.py
  │   ├── queue.py
  │   └── judge.py
  ├── services/
  │   ├── planner.py
  │   ├── worker.py
  │   ├── judge.py
  │   └── orchestrator.py
  └── lib/
    ├── logging.py
    └── redis_queue.py

tests/
└── chimera/
  ├── unit/
  │   ├── test_task_models.py
  │   ├── test_result_models.py
  │   ├── test_planner_queue_push.py
  │   ├── test_worker_queue_consume.py
  │   └── test_judge_validation_and_logging.py
  └── integration/
    └── test_orchestration_loop_with_mock_llm.py
```

**Structure Decision**: Single Python project using `src/chimera` package layout; tests mirror package structure under `tests/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phase 0: Research (complete)

Outputs:

- [specs/001-observable-mcp-swarm/research.md](specs/001-observable-mcp-swarm/research.md)

Decisions to lock:

- Redis queue primitive (Streams vs lists)
- Strict schema shape for `Task`/`Result` and JSON compatibility
- Testing strategy for Redis interactions without incurring external costs

## Phase 1: Design & Contracts (this change)

Outputs:

- [specs/001-observable-mcp-swarm/data-model.md](specs/001-observable-mcp-swarm/data-model.md)
- [specs/001-observable-mcp-swarm/contracts/openapi.yaml](specs/001-observable-mcp-swarm/contracts/openapi.yaml)
- [specs/001-observable-mcp-swarm/quickstart.md](specs/001-observable-mcp-swarm/quickstart.md)

Constitution Check (post-design): PASS

- Role boundaries and contract-first design are preserved.
- No direct external API coupling is introduced in the MVP plan.
- Judge remains the single gate for committing results, with auditable logs.

## Phase 2: Implementation Plan (next)

Implementation milestones (test-first):

1. Define Pydantic v2 models for `Task` and `Result` with `extra='forbid'` and strict field constraints.
2. Define typed interfaces (Protocols) for Planner/Worker/Judge plus ports for Redis queue + LLM backend.
3. Implement Redis-backed queue adapter and unit tests:
  - Planner pushes tasks to a tenant-scoped Redis stream.
  - Worker consumes via consumer groups and acks on success.
4. Implement Judge skeleton with strict result validation and logging; tests assert invalid results are rejected and outcomes are logged prior to any commit.
5. Implement orchestrator loop that wires Planner → queue → Worker → Judge using an injected/mock LLM backend.

