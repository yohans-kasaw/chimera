# Tasks: MCP Client Integration

**Input**: Design documents from `/specs/001-mcp-client/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Strategy**: TDD Approach. This phase focuses ONLY on writing failing tests and establishing placeholder structures (interfaces/stubs). No logic implementation is allowed until these tasks are complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Phase 1: Setup (Scaffolding & Placeholders)

**Purpose**: Establish the project structure and placeholder interfaces for TDD.

- [ ] T001 Create placeholder models in `src/chimera/models/mcp.py` (Stubs for ToolDefinition, ToolResult)
- [ ] T002 Create MCPClientPort interface in `src/chimera/ports/mcp.py`
- [ ] T003 [P] Create skeletal MCPClient in `src/chimera/services/mcp_client.py` with `NotImplementedError` stubs
- [ ] T004 [P] Add `perceive` method stub to `src/chimera/services/worker.py` if not present

---

## Phase 2: User Story 1 - Reliable Tool Interactions (Priority: P1) 🎯 MVP

**Goal**: Verify that the client can connect via stdio and discover tools.

**Independent Test**: Standalone test runner executing `tests/chimera/unit/test_mcp_client.py` specifically for discovery methods.

### Tests for User Story 1 (Failing Tests)

- [ ] T005 [P] [US1] Write unit tests for `ToolDefinition` validation in `tests/chimera/unit/test_mcp_models.py`
- [ ] T006 [P] [US1] Write unit tests for `MCPClient` async context manager (connect/disconnect) in `tests/chimera/unit/test_mcp_client.py`
- [ ] T007 [P] [US1] Write unit tests for tool discovery (`list_tools`) in `tests/chimera/unit/test_mcp_client.py` using a mock transport
- [ ] T008 [P] [US1] Write unit tests for handshake protocol validation in `tests/chimera/unit/test_mcp_client.py`

---

## Phase 3: User Story 2 - Automated Tool Execution (Priority: P2)

**Goal**: Verify that tools can be executed and errors are handled correctly.

**Independent Test**: Execution tests in `tests/chimera/unit/test_mcp_client.py` with mock responses.

### Tests for User Story 2 (Failing Tests)

- [ ] T009 [P] [US2] Write unit tests for `ToolResult` validation in `tests/chimera/unit/test_mcp_models.py`
- [ ] T010 [P] [US2] Write unit tests for successful tool execution (`call_tool`) in `tests/chimera/unit/test_mcp_client.py`
- [ ] T011 [P] [US2] Write unit tests for JSON-RPC error mapping (e.g., method not found) in `tests/chimera/unit/test_mcp_client.py`
- [ ] T012 [P] [US2] Write unit tests for transport-level failure handling (e.g., process crash) in `tests/chimera/unit/test_mcp_client.py`

---

## Phase 4: User Story 3 - Perception Pipeline Integration (Priority: P3)

**Goal**: Verify that the Worker service correctly uses the MCPClient to augment its state.

**Independent Test**: Integration test in `tests/chimera/integration/test_worker_mcp_perception.py`.

### Tests for User Story 3 (Failing Tests)

- [ ] T013 [P] [US3] Write integration test in `tests/chimera/integration/test_worker_mcp_perception.py` verifying `Worker.perceive()` calls `MCPClient.list_tools()`
- [ ] T014 [US3] Write integration test verifying that a `fetch_data` tool result is correctly parsed and injected into the Worker's context
- [ ] T015 [US3] Write integration test verifying Worker behavior when the MCP server is unavailable during the perception phase

---

## Phase 5: Polish & Coverage Audit

**Purpose**: Ensure all tests satisfy the 100% coverage requirement (on stubs) and provide clear failure messages.

- [ ] T016 Run `uv run pytest --cov=src` and verify 100% missing coverage on the newly created placeholder files
- [ ] T017 Verify all tests fail with `NotImplementedError` or `AssertionError` as expected
- [ ] T018 Check that all public methods have Google-style docstrings (even if body is a stub)

## Dependencies

- All User Stories depend on Phase 1 (Setup).
- User Story 3 depends on User Story 1 and 2 interfaces.

## Parallel Execution

- T005, T006, T007, T008 (US1 Tests) can be written in parallel.
- T009, T010, T011, T012 (US2 Tests) can be written in parallel.
- T013, T014, T015 (US3 Tests) can be written in parallel.

## Implementation Strategy (TDD)

1. **Write Stubs**: Create the files with classes and methods but only `raise NotImplementedError()`.
2. **Write Tests**: Implement all the `tests/` mentioned above.
3. **Verify Failure**: Run the tests to confirm they fail.
4. **Implementation Phase (Next)**: Only after these tasks are marked as completed will logic be added to the stubs.
