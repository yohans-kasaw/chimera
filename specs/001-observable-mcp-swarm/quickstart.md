# Quickstart: Observable MCP Agent Swarm (MVP Brain)

This quickstart focuses on developer verification: run lint/typecheck/tests and (optionally) bring up Redis locally to exercise the queue-backed orchestration loop.

## Prerequisites

- Python 3.12+
- `uv`
- Redis 6+ recommended (Streams + Consumer Groups)

## Install

- `uv sync`

## Quality gates

- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run mypy .`
- Tests: `uv run pytest`

## Run Redis locally (optional)

If you have Redis installed:

- `redis-server`

If you prefer Docker:

- `docker run --rm -p 6379:6379 redis:7`

## Run the MVP brain (planned)

The implementation for this feature will include a minimal orchestrator loop that:

1. Planner enqueues a `Task` into a tenant-scoped Redis stream.
2. Worker reads from the stream (consumer group), processes using an injected LLM backend, and writes a `Result`.
3. Judge validates the `Result`, emits structured logs, and returns a gate decision.

Entry points will be finalized during implementation (Phase 2), but the tests will be runnable via `uv run pytest` and will validate:

- Planner enqueues correctly
- Worker consumes efficiently (batch reads where applicable)
- Judge rejects invalid results and logs outcomes prior to commit
- Orchestration loop can be exercised with a mocked LLM backend (no API costs)

## Troubleshooting

- If Redis is not running, integration-style tests may be skipped or configured to use an in-memory substitute (implementation choice in Phase 2).
- If coverage drops below 90%, add targeted unit tests for orchestration edge cases (invalid payloads, policy denies, retryable errors).