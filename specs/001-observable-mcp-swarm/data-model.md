# Data Model: Observable MCP Agent Swarm (MVP)

This model is intentionally minimal: it defines the durable contracts for the “brain” (Planner/Worker/Judge) and the audit/observability surface needed to operate safely.

## Entities

### Tenant

Represents a strict isolation boundary.

Fields:

- `tenant_id` (string, required): constrained ID (e.g., `t_acme`).
- `created_at` (datetime, required)

Rules:

- All other entities must carry `tenant_id`.

### SwarmSession

A time-bounded operating context for a tenant’s work.

Fields:

- `session_id` (string, required)
- `tenant_id` (string, required)
- `state` (enum: `created|running|paused|stopped`, required)
- `created_at`, `updated_at` (datetime, required)

Relationships:

- Tenant 1 → N SwarmSessions

### Task

A unit of requested work created by a Planner and processed by a Worker.

Fields (core):

- `tenant_id` (string, required)
- `trace_id` (string, required): correlation across services
- `task_id` (string, required)
- `parent_task_id` (string, optional): for decomposition
- `session_id` (string, optional)
- `kind` (string, required): stable task type identifier (e.g., `skill.invoke`)
- `input` (object, required): JSON-serializable payload

Fields (execution/metadata):

- `status` (enum): lifecycle (`queued|running|succeeded|failed|cancelled|blocked|timed_out`)
- `priority` (int 0–100)
- `attempt` (int ≥ 0)
- `max_attempts` (int ≥ 0)
- `timeout_s` (int, optional)

Fields (timing):

- `created_at`, `updated_at` (datetime, required)
- `started_at`, `completed_at` (datetime, optional)

Validation rules:

- `extra` fields forbidden (schema drift prevention).
- `tenant_id` required and validated for format.
- Timestamp ordering must be consistent (`updated_at >= created_at`, etc.).
- Terminal `status` implies `completed_at` is set.

Relationships:

- SwarmSession 1 → N Tasks (optional link; tasks may exist outside sessions in early MVP)

### Result

A terminal outcome for a `Task`. Produced by a Worker and evaluated by a Judge.

Fields:

- `tenant_id`, `trace_id`, `task_id` (required)
- `status` (enum: `succeeded|failed|cancelled|blocked|timed_out`, required)
- `output` (object, required; empty allowed)
- `error` (object, optional): required for non-success statuses
- `produced_by` (string, optional): worker/agent id
- `completed_at` (datetime, required)

Validation rules:

- `completed_at` required.
- Success results must not include `error`.
- Non-success results must include `error`.

Relationships:

- Task 1 → 0/1 Result

### GateDecision

Judge evaluation outcome for a proposed action or for a `Result` being committed.

Fields:

- `tenant_id`, `trace_id`, `task_id` (required)
- `decision` (enum: `approve|deny|hitl`, required)
- `reason_code` (string, required)
- `confidence` (float 0–1, optional)
- `created_at` (datetime, required)

Rules:

- All decisions must be durable and retrievable.

### AuditEvent

Immutable, append-only record of significant events.

Fields:

- `tenant_id`, `trace_id` (required)
- `event_id` (string, required)
- `event_type` (string, required): e.g., `task.queued`, `worker.consumed`, `judge.outcome`
- `payload` (object, required)
- `created_at` (datetime, required)

Rules:

- Must include correlation identifiers for observability.

## State transitions

### SwarmSession

`created → running → paused → running → stopped`

### Task

Typical:

`queued → running → (succeeded|failed|blocked|timed_out)`

Retries:

- `failed` + `retryable` error can produce a new task (or re-queue with incremented `attempt`) while preserving audit trail.

## Isolation

All persistent keys (Redis, future Postgres) must be tenant-scoped:

- `tenant:{tenant_id}:...`

This ensures cross-tenant collisions are structurally impossible even under programming mistakes.