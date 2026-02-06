# Tasks: Production Stability & Safety

**Input**: Design documents from `specs/001-prod-stability-safety/`
**Prerequisites**: [plan.md](specs/001-prod-stability-safety/plan.md), [spec.md](specs/001-prod-stability-safety/spec.md), [research.md](specs/001-prod-stability-safety/research.md), [data-model.md](specs/001-prod-stability-safety/data-model.md), [contracts/review_service.py](specs/001-prod-stability-safety/contracts/review_service.py)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Following TDD, tests are created FIRST and must FAIL before placeholders are filled.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure with placeholder files.

- [ ] T001 Create placeholder model for `ReviewCard` in `src/chimera/models/review.py`
- [ ] T002 Create placeholder model for `AgentHeartbeat` and `AgentRegistry` in `src/chimera/models/agent.py`
- [ ] T003 Create placeholder port for `AgentRegistryPort` in `src/chimera/ports/registry.py`
- [ ] T004 Create placeholder service for `SafetyService` in `src/chimera/services/safety.py`
- [ ] T005 Create placeholder service for `ReviewService` in `src/chimera/services/review_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [ ] T006 Implement placeholder `RedisAgentRegistry` in `src/chimera/lib/redis_registry.py`
- [ ] T007 Add `NEEDS_REVIEW` and `APPROVED` statuses to `TaskStatus` in `src/chimera/models/task.py`
- [ ] T008 [P] Initialize audit log configuration in `src/chimera/lib/logging.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Large Scale Agent Coordination (Priority: P1)

**Goal**: Orchestrator must manage 1,000 active agents simultaneously.

**Independent Test**: Running `tests/chimera/integration/test_load_orchestrator.py` with 1,000 mock agents and verifying heartbeat/task-pull response times < 200ms.

### Tests for User Story 1 (REQUIRED)

- [ ] T009 [US1] Integration test for 1,000 concurrent heartbeats in `tests/chimera/integration/test_load_orchestrator.py` (EXPECTED TO FAIL)
- [ ] T010 [US1] Integration test for distributed task locking across multiple orchestrator instances in `tests/chimera/integration/test_load_orchestrator.py` (EXPECTED TO FAIL)

### Implementation for User Story 1 (Placeholders Only)

- [ ] T011 [US1] Implement placeholder heartbeat logic in `src/chimera/services/orchestrator.py`
- [ ] T012 [P] [US1] Implement placeholder agent tracking in `src/chimera/lib/redis_registry.py`
- [ ] T013 [US1] Implement placeholder task distribution logic with Redis Streams `XREADGROUP` in `src/chimera/lib/redis_queue.py`

**Checkpoint**: US1 should have failing load tests and placeholder implementation ready for optimization.

---

## Phase 4: User Story 2 - Automated Safety Gate (Priority: P1)

**Goal**: Results with confidence < 0.7 or sensitive keywords must be routed to the review queue.

**Independent Test**: Mock a result with confidence 0.6 and verify it transitions to `NEEDS_REVIEW`. Mock a result with "password" and verify it transitions to `NEEDS_REVIEW`.

### Tests for User Story 2 (REQUIRED)

- [ ] T014 [P] [US1] Unit test for confidence threshold gating in `tests/chimera/unit/test_safety_filter.py` (EXPECTED TO FAIL)
- [ ] T015 [P] [US1] Unit test for sensitive keyword regex scanning in `tests/chimera/unit/test_safety_filter.py` (EXPECTED TO FAIL)
- [ ] T016 [US1] Integration test for Orchestrator routing result to `NEEDS_REVIEW` in `tests/chimera/integration/test_hitl_flow.py` (EXPECTED TO FAIL)

### Implementation for User Story 2 (Placeholders Only)

- [ ] T017 [US1] Implement placeholder `ConfidenceFilter` in `src/chimera/services/safety.py`
- [ ] T018 [US1] Implement placeholder `KeywordFilter` in `src/chimera/services/safety.py`
- [ ] T019 [US1] Update `Orchestrator.run_task` placeholder to include safety gate routing in `src/chimera/services/orchestrator.py`

**Checkpoint**: US2 should have failing safety tests and placeholder logic for gating.

---

## Phase 5: User Story 3 - Human-in-the-Loop Approval (Priority: P2)

**Goal**: ReviewCard API must update task status upon operator approval.

**Independent Test**: Post an approval to the ReviewCard API for a task in `NEEDS_REVIEW` and verify it moves to `APPROVED`.

### Tests for User Story 3 (REQUIRED)

- [ ] T020 [P] [US2] Unit test for `ReviewCard` state transitions in `tests/chimera/unit/test_review_models.py` (EXPECTED TO FAIL)
- [ ] T021 [US2] Integration test for human approval via `ReviewService` in `tests/chimera/integration/test_hitl_flow.py` (EXPECTED TO FAIL)

### Implementation for User Story 3 (Placeholders Only)

- [ ] T022 [US2] Implement placeholder `ReviewCard` creation in `src/chimera/services/review_service.py`
- [ ] T023 [US2] Implement placeholder `submit_decision` in `src/chimera/services/review_service.py`
- [ ] T024 [US2] Implement placeholder task resumption logic after approval in `src/chimera/services/orchestrator.py`

**Checkpoint**: US3 should have failing HITL tests and placeholder approval API.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Auditing and final stability checks.

- [ ] T025 [P] Implement placeholder audit logging for all human approvals in `src/chimera/services/review_service.py`
- [ ] T026 Final validation of 99.9% delivery guarantee under load in `tests/chimera/integration/test_load_orchestrator.py`

### Parallel Execution Examples
- [P] T014, T015, T020 (Unit tests for independent modules)
- [P] T012 (Agent tracking implementation)
