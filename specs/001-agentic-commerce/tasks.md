# Tasks: Agentic Commerce (Agency)

**Input**: Design documents from `/specs/001-agentic-commerce/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**TDD Approach**: This phase focuses on creating the structure and the tests that define success. All implementation tasks in this session are limited to **placeholders** (stubs that raise `NotImplementedError`).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure for commerce services and tests
- [x] T002 Organize commerce models and ports in `src/chimera/models/` and `src/chimera/ports/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 [P] Create placeholder Pydantic models in `src/chimera/models/commerce.py` (Wallet, Budget, Transaction)
- [x] T004 [P] Create `CommerceService` protocol in `src/chimera/ports/commerce.py`
- [x] T005 [P] Setup placeholder for persistent spend tracking in Redis/Postgres (schema stubs)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - Secure Wallet Initialization (Priority: P1)

**Goal**: Ensure `CommerceManager` initializes securely using environment variables.

**Independent Test**: Verify `CommerceManager` raises `ConfigurationError` when environment variables are missing.

### Tests for User Story 2

- [x] T006 [P] [US2] Create failing unit tests for `CommerceManager` initialization in `tests/unit/test_commerce_manager.py`

### Implementation for User Story 2 (Placeholders)

- [x] T007 [US2] Create `CommerceManager` class stub in `src/chimera/services/commerce.py` with `__init__` raising `NotImplementedError`

---

## Phase 4: User Story 1 - Financial Autonomy with Safety (Priority: P1) 🎯 MVP

**Goal**: Execute asset transfers securely within a defined budget.

**Independent Test**: Verify `transfer_asset` succeeds within budget and fails (rejection) when limit is exceeded.

### Tests for User Story 1

- [x] T008 [P] [US1] Create failing unit tests for `CFOJudge` logic in `tests/unit/test_cfo_judge.py`
- [x] T009 [P] [US1] Create failing unit tests for `transfer_asset` in `tests/unit/test_commerce_manager.py` (mocking blockchain)
- [x] T010 [US1] Create failing integration test for the full commerce workflow in `tests/integration/test_agentic_workflow.py`

### Implementation for User Story 1 (Placeholders)

- [x] T011 [US1] Create `CFOJudge` class stub in `src/chimera/services/judge_policy.py` (or extend existing)
- [x] T012 [US1] Implement `transfer_asset` and `get_balance` stubs in `src/chimera/services/commerce.py`

---

## Phase 5: User Story 3 - Budget-Aware Tool Execution (Priority: P2)

**Goal**: Use decorators to automatically enforce budget checks.

**Independent Test**: Verify that a decorated method is not executed when the budget check fails.

### Tests for User Story 3

- [x] T013 [P] [US3] Create failing unit tests for `@budget_check` decorator in `tests/unit/test_budget_decorator.py`

### Implementation for User Story 3 (Placeholders)

- [x] T014 [US3] Create placeholder for `@budget_check` decorator in `src/chimera/lib/decorators.py`

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T015 Verify all newly created tests fail as expected using `uv run pytest`
- [x] T016 Ensure `mypy --strict` passes for all placeholder files
- [ ] T017 Document any mock requirements for the next implementation phase in `specs/001-agentic-commerce/research.md`

## Dependencies

1. Foundation (Phase 2) -> All User Stories
2. US2 (Initialization) -> US1 (Transfers)
3. US1 (CFO Judge) -> US3 (Decorator)

## Parallel Execution Examples

- **Tests setup**: T006, T008, T013 can be written independently.
- **Models/Ports**: T003, T004 can be done in parallel.
- **Service Stubs**: T007, T011 can be created in parallel.

## Implementation Strategy

1. **Skeleton First**: Create all files and function signatures first.
2. **Contract Validation**: Ensure `CommerceManager` implements the `CommerceService` protocol even as a stub.
3. **Failing Baseline**: Run the tests to confirm they are indeed failing before any logic is added.
