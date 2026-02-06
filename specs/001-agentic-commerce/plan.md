# Implementation Plan: Agentic Commerce (Agency)

**Branch**: `001-agentic-commerce` | **Date**: 2026-02-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-agentic-commerce/spec.md`

## Summary

This feature implements the "Agency" phase of Project Chimera, enabling autonomous agents to execute financial transactions with strict budget governance. The core components include a `CommerceManager` for wallet lifecycle, a `CFO Judge` for real-time budget enforcement against a `daily_spend` limit, and a `@budget_check` decorator for seamless integration. All blockchain interactions will aim to align with the project's MCP-first architecture.

## Technical Context

**Language/Version**: Python 3.12 (as per `pyproject.toml`)  
**Primary Dependencies**: `coinbase-agentkit-python` (Tentative), `pydantic`, `pytest`, `pytest-asyncio`  
**Storage**: Redis (Spend Tracker / Hot state), PostgreSQL (Immutable Ledger / Audit)  
**Testing**: `pytest` with `pytest-mock` and `mocker` fixture  
**Target Platform**: Linux (Dockerized workers)
**Project Type**: Single project (Source layout: `src/chimera/`)  
**Performance Goals**: Budget validation latency < 200ms  
**Constraints**: 
- `mypy --strict` compliance.
- 0% violation rate for `daily_spend` limit.
- No sensitive credentials in logs or code.
- 90%+ test coverage.
**Scale/Scope**: Initial support for CD P (Coinbase Developer Platform) assets; extensible to other chains via MCP.

## Constitution Check

*GATE: Passed. Re-checked after Phase 1 design.*

- **Rule I (MCP-First)**: ✅ COMPLIANT. Design has pivoted to using the standalone `coinbase-mcp-server`. `CommerceManager` will be an MCP client, not a direct SDK consumer.
- **Rule IV.1 (CFO Judge)**: ✅ COMPLIANT. Interceptor pattern in `CommerceManager`/`MCPClient` gates all financial tool calls.
- **Rule IV.2 (Budget Limits)**: ✅ COMPLIANT. Redis-backed `daily_spend` limit enforced with atomic increments.
- **Rule IV.3 (No Keys in Code)**: ✅ COMPLIANT. Environment variables used; CD P sensitive data injected into MCP server context, not worker code.
- **Rule IV.4 (Immutable Ledger)**: ✅ COMPLIANT. `TransactionRecord` entity added to Postgres schema for immutable audit trail.
- **Rule V.6 (Testing/Coverage)**: ✅ COMPLIANT. Planned test suite using mocks and standard Chimera testing patterns.

## Project Structure

### Documentation (this feature)

```text
specs/001-agentic-commerce/
├── plan.md              # This file
├── research.md          # Research into MCP-AgentKit alignment
├── data-model.md        # Entities: Wallet, Budget, Transaction, Ledger
├── quickstart.md        # Setup guide
├── contracts/           # API/Service interfaces
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/chimera/
├── models/
│   ├── commerce.py      # Pydantic models for transactions/budgets
├── ports/
│   ├── commerce.py      # Abstract interface for wallet operations
├── services/
│   ├── commerce.py      # CommerceManager implementation
│   ├── judge_policy.py  # CFO Judge (adding to existing judge service)
├── lib/
│   ├── decorators.py    # @budget_check implementation
└── adapters/
    ├── mcp/
        └── commerce.py  # MCP Client for wallet tools (if following Rule I)

tests/
├── unit/
│   ├── test_commerce_manager.py
│   ├── test_cfo_judge.py
│   ├── test_budget_decorator.py
├── integration/
│   ├── test_agentic_workflow.py
```

**Structure Decision**: Single project layout matching existing `src/chimera` structure. New `commerce` models and services will be added.

## Complexity Tracking

| Violation | Justification | Mitigation |
|-----------|---------------|------------|
| Rule I (MCP-First) | AgentKit provides high-level agentic tools that may not yet be standardized in a generic MCP server for Chimera. | Research Phase 0 will evaluate wrapping AgentKit in an internal MCP server or implementing a compliant Adapter pattern. |

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
