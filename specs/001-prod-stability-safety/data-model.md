# Data Model: Production Stability & Safety

## Entities

### ReviewCard
Represents a task result that failed the automated safety gate and requires human intervention.

| Field | Type | Description |
|-------|------|-------------|
| review_id | UUID | Unique identifier. |
| task_id | TaskId | Reference to the original task. |
| result_id | ResultId | Reference to the proposed result. |
| reason | ReviewReason | Enum: LOW_CONFIDENCE, SENSITIVE_KEYWORD. |
| details | str | Explanation of the trigger (e.g., "Found keyword 'password'"). |
| status | ReviewStatus | Enum: PENDING, APPROVED, REJECTED. |
| operator_id | str? | ID of the human who performed the review. |
| timestamp | datetime | When the review was created. |
| resolution_at | datetime? | When the operator made a decision. |

### AgentHeartbeat
Tracking record for the 1,000+ cluster.

| Field | Type | Description |
|-------|------|-------------|
| agent_id | str | Unique agent identifier. |
| status | AgentStatus | ACTIVE, BUSY, IDLE, OFFLINE. |
| last_seen | datetime | Heartbeat timestamp. |
| metrics | dict | Agent-reported load/performance metrics. |

## State Transitions

### Task Lifecycle (Updated)
1. `QUEUED` -> `RUNNING` (Agent picks up)
2. `RUNNING` -> `NEEDS_REVIEW` (Orchestrator detects safety trigger)
3. `NEEDS_REVIEW` -> `APPROVED` (Human approves) -> Resume Flow
4. `NEEDS_REVIEW` -> `REJECTED` (Human rejects) -> Terminal Fail

### Review Lifecycle
1. `PENDING` -> `APPROVED`
2. `PENDING` -> `REJECTED`
