---

description: "Task list for feature implementation"

---

# Tasks: Observable MCP Agent Swarm

**Input**: Design documents from `/specs/001-observable-mcp-swarm/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: INCLUDED (explicitly requested: unit tests for Planner/Worker/Judge, plus an orchestration loop test with mocked LLM backend).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- All tasks include explicit file paths

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Add Redis test dependency via `pyproject.toml` + `uv.lock` (e.g., `fakeredis` or equivalent)
- [ ] T002 [P] Create package skeleton under `src/chimera/models/`, `src/chimera/ports/`, `src/chimera/services/`, `src/chimera/lib/` (add `__init__.py` files)
- [ ] T003 [P] Create test skeleton under `tests/chimera/unit/` and `tests/chimera/integration/` (add `__init__.py` files)

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T004 [P] Define shared JSON/value types + ID types in `src/chimera/models/types.py`
- [ ] T005 [P] Define strict `Task` Pydantic schema in `src/chimera/models/task.py`
- [ ] T006 [P] Define strict `Result` Pydantic schema in `src/chimera/models/result.py`
- [ ] T007 [P] Add model unit tests for Task invariants in `tests/chimera/unit/test_task_models.py`
- [ ] T008 [P] Add model unit tests for Result invariants in `tests/chimera/unit/test_result_models.py`
- [ ] T009 [P] Define queue port interfaces in `src/chimera/ports/queue.py` (enqueue/dequeue/ack; tenant-scoped)
- [ ] T010 [P] Define LLM port interface in `src/chimera/ports/llm.py` (mockable backend for Worker)
- [ ] T011 [P] Define Judge port interfaces in `src/chimera/ports/judge.py` (policy + unit-of-work + logger ports)
- [ ] T012 Implement Redis Streams queue adapter in `src/chimera/lib/redis_queue.py` (XADD/XREADGROUP/XACK)
- [ ] T013 [P] Add Redis queue adapter unit tests in `tests/chimera/unit/test_redis_queue_adapter.py`
- [ ] T014 Add structured logging helper (structlog wrapper) in `src/chimera/lib/logging.py`

**Checkpoint**: Core contracts + ports exist, and models/queue adapter are test-covered.

---

## Phase 3: User Story 1 — Operate a Tenant Swarm (Priority: P1) 🎯 MVP

**Goal**: Create a tenant-scoped swarm session, submit at least one skill-driven task, and observe end-to-end execution status.

**Independent Test**: Create one tenant + one session, enqueue one task, consume it with a Worker using a mocked LLM backend, and return a terminal Result.

### Tests for User Story 1 (write first)

- [ ] T015 [P] [US1] Add Planner queue-push unit test in `tests/chimera/unit/test_planner_queue_push.py`
- [ ] T016 [P] [US1] Add Worker consumption efficiency test (batch read / minimal round-trips) in `tests/chimera/unit/test_worker_queue_consume.py`
- [ ] T017 [P] [US1] Add orchestration loop test with mocked LLM backend in `tests/chimera/integration/test_orchestration_loop_with_mock_llm.py`

### Implementation for User Story 1

- [ ] T018 [US1] Implement Planner interface + service in `src/chimera/services/planner.py` (create validated Task, enqueue to Redis stream)
- [ ] T019 [US1] Implement Worker interface + service in `src/chimera/services/worker.py` (consume tasks in batches, call LLM port, emit validated Result)
- [ ] T020 [US1] Implement orchestrator loop in `src/chimera/services/orchestrator.py` (wire Planner → Queue → Worker; no external API calls)
- [ ] T021 [US1] Add tenant/session minimal state helpers in `src/chimera/services/session.py` (IDs + lifecycle; in-memory MVP)

**Checkpoint**: US1 runs end-to-end locally with Redis + mocked LLM backend.

---

## Phase 4: User Story 2 — Enforce Judge-Led Security Gates (Priority: P2)

**Goal**: Ensure sensitive or risky actions are gated, rejected/approved deterministically, and auditable.

**Independent Test**: Submit an invalid Result and confirm Judge rejects it (no side effects), logs the outcome, and returns a deny decision.

### Tests for User Story 2 (write first)

- [ ] T022 [P] [US2] Add Judge invalid-result rejection tests in `tests/chimera/unit/test_judge_validation_and_logging.py`
- [ ] T023 [P] [US2] Add Judge log-before-commit ordering test in `tests/chimera/unit/test_judge_validation_and_logging.py`

### Implementation for User Story 2

- [ ] T024 [US2] Implement Judge service skeleton in `src/chimera/services/judge.py` (validate Result schema, decision enum, structured logging)
- [ ] T025 [US2] Implement default Judge policy in `src/chimera/services/judge_policy.py` (approve/deny/hitl; confidence routing hooks)
- [ ] T026 [US2] Integrate Judge into orchestrator loop in `src/chimera/services/orchestrator.py` (Judge must gate before any commit)

**Checkpoint**: US2 blocks invalid results and produces auditable Judge outcomes.

---

## Phase 5: User Story 3 — Recover from Failures Without State Corruption (Priority: P3)

**Goal**: Keep tenant state consistent when a worker fails mid-task; enable controlled resume or halt.

**Independent Test**: Simulate a worker crash after reading a task but before ack; verify the task remains pending and can be recovered and processed by another worker.

### Tests for User Story 3 (write first)

- [ ] T027 [P] [US3] Add pending-entry recovery integration test in `tests/chimera/integration/test_worker_recovery_pending_entries.py`
- [ ] T028 [P] [US3] Add retry/backoff behavior unit test in `tests/chimera/unit/test_worker_retry_policy.py`

### Implementation for User Story 3

- [ ] T029 [US3] Extend queue adapter with pending-claim support in `src/chimera/lib/redis_queue.py` (XAUTOCLAIM/XCLAIM strategy)
- [ ] T030 [US3] Add worker retry/backoff + idempotency hooks in `src/chimera/services/worker.py` (at-least-once safe)
- [ ] T031 [US3] Add audit event emission stubs in `src/chimera/services/audit.py` (in-memory MVP + structlog; no DB yet)

**Checkpoint**: US3 demonstrates recovery without losing or corrupting committed state.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T032 [P] Tighten docstrings to Google style for public classes/functions in `src/chimera/models/task.py`, `src/chimera/models/result.py`, `src/chimera/services/planner.py`, `src/chimera/services/worker.py`, `src/chimera/services/judge.py`, `src/chimera/services/orchestrator.py`
- [ ] T033 Update quickstart with real entrypoints and env vars in `specs/001-observable-mcp-swarm/quickstart.md`
- [ ] T034 Run and fix quality gates (`ruff`, `mypy`, `pytest`, coverage ≥ 90%) and document any skips in `README.md`

---

## Dependencies & Execution Order

- Setup (T001–T003) → Foundational (T004–T014) → US1 (T015–T021) → US2 (T022–T026) → US3 (T027–T031) → Polish (T032–T034)

## Parallel opportunities (examples)

- Phase 2: T004–T011 can be developed in parallel (separate files)
- US1 tests (T015–T017) can be written in parallel
- US2 tests (T022–T023) can be written in parallel
- US3 tests (T027–T028) can be written in parallel

## Parallel execution examples per story

### User Story 1

```bash
Task: "Add Planner queue-push unit test in tests/chimera/unit/test_planner_queue_push.py"
Task: "Add Worker consumption efficiency test in tests/chimera/unit/test_worker_queue_consume.py"
Task: "Add orchestration loop test in tests/chimera/integration/test_orchestration_loop_with_mock_llm.py"
```

### User Story 2

```bash
Task: "Add Judge invalid-result rejection tests in tests/chimera/unit/test_judge_validation_and_logging.py"
Task: "Add Judge log-before-commit ordering test in tests/chimera/unit/test_judge_validation_and_logging.py"
```

### User Story 3

```bash
Task: "Add pending-entry recovery integration test in tests/chimera/integration/test_worker_recovery_pending_entries.py"
Task: "Add retry/backoff behavior unit test in tests/chimera/unit/test_worker_retry_policy.py"
```

## Implementation strategy (two manageable chunks)

- **Chunk A (Contracts + Queue + US1 MVP)**: T001–T021
- **Chunk B (Judge + Recovery + Polish)**: T022–T034
