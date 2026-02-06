# Research: Observable MCP Swarm “Brain” (Planner/Worker/Judge)

This Phase 0 research locks the technical choices needed to implement a minimal but operational orchestration loop with strong contracts and observability.

## Decision 1: Redis queue primitive

- Decision: Use **Redis Streams + Consumer Groups** for task fan-out.
- Rationale:
  - Native **acknowledgement** (`XACK`) and crash recovery via the Pending Entries List (PEL).
  - Efficient worker scaling with consumer groups (no worker-to-worker coordination).
  - Better observability than lists (stream entries are inspectable).
- Alternatives considered:
  - Redis Lists (`LPUSH`/`BRPOP`): simplest but no ack; tasks can be lost on worker crash.
  - Lists + processing list (`BRPOPLPUSH`): at-least-once possible, but requires custom reaper/inflight bookkeeping.

Notes:

- Recovery strategy: MVP uses consumer-group ack; later add `XAUTOCLAIM`/reaper for stuck pending tasks if needed.

## Decision 2: Task/Result schema strictness

- Decision: Pydantic v2 models with `extra="forbid"` and **strict primitives** (e.g., `StrictStr`, `StrictInt`) plus explicit `Annotated` constraints.
- Rationale:
  - Prevent silent schema drift across services.
  - Maintain JSON compatibility for Redis transport.
- Alternatives considered:
  - `ConfigDict(strict=True)`: often too strict for JSON transport where timestamps/IDs arrive as strings.

Schema requirements to enforce:

- Multi-tenancy: `tenant_id` on every `Task` and `Result`.
- Observability: `trace_id` + `task_id`, and timestamps.
- Validation invariants:
  - timezone-aware timestamps (`AwareDatetime`)
  - terminal statuses require `completed_at`
  - success results must not contain `error`; failure-like results must contain `error`

## Decision 3: Testing strategy for Redis interactions

- Decision: Unit tests should use an in-memory Redis substitute **when feasible**, but the plan expects at least one **real-Redis integration path** for Streams semantics if the substitute is incomplete.
- Rationale:
  - Streams consumer group behavior and blocking reads can differ in fakes; correctness of ack/PEL handling matters.
- Alternatives considered:
  - Fake Redis only (e.g., fakeredis): fast but may not fully support `XREADGROUP` semantics depending on version.
  - Real Redis only: highest fidelity but slower; may require Docker in CI.

## Decision 4: Judge boundary + logging invariants

- Decision: Model Judge as a pure “validation + decision” boundary with injected ports:
  - `JudgePolicy` (pure policy), `JudgeUnitOfWork` (persistence), and a structlog-compatible logger.
- Rationale:
  - Judge is the safety firewall: it must reject invalid results deterministically and emit auditable logs.
  - Port-based design makes it testable without external systems.
- Alternatives considered:
  - Inlining persistence and policy decisions: makes tests slow/flaky and blurs boundaries.

Judge test invariants:

- Invalid `Result` payloads are rejected and logged (no side effects).
- Outcomes are logged **before** commit, to ensure auditability even on commit failure.

