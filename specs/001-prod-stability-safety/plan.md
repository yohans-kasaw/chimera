# Implementation Plan: Production Stability & Safety

**Branch**: `001-prod-stability-safety` | **Date**: 2026-02-06 | **Spec**: [specs/001-prod-stability-safety/spec.md](specs/001-prod-stability-safety/spec.md)

## Summary
The goal is to scale the system to 1,000 concurrent agents and implement a comprehensive Human-in-the-Loop (HITL) safety framework. This involves optimizing the Orchestrator for statelessness, using Redis Streams for high-concurrency task distribution, and creating a ReviewCard system to gate high-risk or low-confidence agent results.

## Technical Context

**Language/Version**: Python 3.12+ (as per Copilot instructions)  
**Primary Dependencies**: Pydantic v2, Redis, structlog, pytest, ruff, mypy  
**Storage**: Redis (Hot queues & registry), PostgreSQL (Audit logs & persistent models)  
**Testing**: pytest (unit/integration), custom-script (load testing)  
**Target Platform**: Kubernetes/Linux (Distributed environment)  
**Project Type**: Python backend service  
**Performance Goals**: 1,000 concurrent agents, <200ms p95 latency for registry operations.  
**Constraints**: Constitution compliance (Safety + HITL), 90% coverage mandatory.

## Constitution Check

*GATE: Must pass before Phase 2 tasks.*

1. **MCP-First Integration**: Verified. Review logic is internal to orchestrator, no direct calls to external APIs.
2. **Swarm Roles**: Verified. Orchestrator remains the hub; Worker/Judge boundaries preserved.
3. **Safety + HITL**: Verified. Implements routing for < 0.70 confidence and sensitive topics as mandated by Rule III.
4. **Economic Agency**: N/A for this phase, but Audit logs (Rule IV.4) are incorporated.
5. **Python Quality**: Verified. uv, Ruff, Mypy, and Pydantic v2 are the standard.

## Project Structure

### Source Code

```text
src/chimera/
├── models/
│   ├── review.py        # New: ReviewCard and ReviewStatus models
│   ├── agent.py         # New: AgentHeartbeat and Registry models
├── services/
│   ├── safety.py        # New: Keyword and confidence filtering logic
│   ├── review_service.py # New: ReviewCard management
├── ports/
│   ├── registry.py      # New: Interface for agent tracking
└── lib/
    ├── redis_registry.py # New: Redis implementation of AgentRegistry
```

### Tests

```text
tests/chimera/
├── integration/
│   ├── test_hitl_flow.py      # End-to-end review lifecycle
│   ├── test_load_orchestrator.py # Simulation of 1,000 agents
├── unit/
│   ├── test_safety_filter.py  # Regex and confidence checks
│   ├── test_review_models.py
```

## Phase 0: Research Findings
- **Findings**: Documented in [specs/001-prod-stability-safety/research.md](specs/001-prod-stability-safety/research.md)
- **Resolved**: Distributed locking via Redis Streams, Stateless Orchestrator, ReviewCard gating logic.

## Phase 1: Design Artifacts
- **Data Model**: [specs/001-prod-stability-safety/data-model.md](specs/001-prod-stability-safety/data-model.md)
- **Contracts**: To follow in `/contracts/`.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
