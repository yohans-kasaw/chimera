# Research: Phase 4 Production Stability & Safety

## Scalability Analysis

### Decision: Distributed Task Locking with Redis Streams
- **Rationale**: The 1,000 concurrent agent requirement necessitates a robust, low-latency queuing system. Redis Streams provide consumer groups which handle task distribution and isolation natively.
- **Alternatives considered**: 
    - PostgreSQL + SKIP LOCKED: Solid but potentially higher latency for 1k concurrent pulls.
    - RabbitMQ: Feature-rich but adds infrastructure complexity. Redis is already in the stack.

### Decision: Orchestrator Statelessness
- **Rationale**: To support horizontal scaling, the Orchestrator must not maintain in-memory agent registries. All agent heartbeats and task metadata must reside in Redis.
- **Implementation**: `AgentRegistry` will use Redis Hashes with TTLs for heartbeat tracking.

## Safety & HITL Design

### Decision: Pre-Execution Gating logic
- **Rationale**: In accordance with the Constitution, any task result with confidence < 0.7 or sensitive keywords must be diverted before persistence or external publication.
- **Threshold**: 0.7 (as per spec).
- **Keywords**: "password", "secret key", "delete all", "override security", "PII", "SSN".

### Decision: ReviewCard API
- **Rationale**: A dedicated REST/gRPC endpoint to manage human approvals. Transitions tasks from `NEEDS_REVIEW` to `APPROVED` or `REJECTED`.
- **Persistence**: PostgreSQL for long-term audit logs of approvals, Redis for active review queue.

## Needs Clarification Status
- [x] Agent Registry Persistence -> Redis with persistence enabled or PostgreSQL backup. (Chosen: Redis for performance, mirroring metadata to Postgres for audit).
- [x] Keyword Filter Implementation -> Regex-based scanning of result payloads in the Orchestrator.
- [x] Failover handling -> Redis Streams `XREADGROUP` handles re-claiming pending tasks if an agent drops.
