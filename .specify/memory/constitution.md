# Project Chimera Constitution

This constitution defines the non-negotiable engineering and governance rules for Project Chimera (Autonomous Influencer Network). Where this document conflicts with other docs, this document wins.

## Core Principles

### I. MCP-First Integration (No Direct API Coupling)
All interactions with external systems (social platforms, web/news, vector DB, wallets/chain) MUST occur through Model Context Protocol (MCP) Resources and Tools.

Rules:
1. Agent core logic MUST NOT call third-party SDKs or REST APIs directly.
2. Integration changes MUST be isolated to MCP servers; agent logic remains stable.
3. All MCP tools MUST support safe operation modes where applicable (e.g., dry-run, rate limiting) and MUST produce structured logs.

### II. Swarm Roles Are Architectural Boundaries
The system is a hierarchical swarm (FastRender pattern): Planner (strategy), Worker (execution), Judge (validation/gating).

Rules:
1. Workers are stateless and atomic: one task in, one artifact out.
2. Workers do not coordinate with each other directly; parallelism comes from queue fan-out.
3. Judges are the single gate to committing results to shared state or publishing externally.
4. State updates MUST be protected with Optimistic Concurrency Control (OCC) (e.g., state_version checks) to prevent committing stale work.

### III. Safety + HITL Is Enforced Pre-Publication
The Judge is the safety firewall. Nothing reaches the public internet (or executes irreversible actions) without passing a Judge decision.

Rules:
1. Confidence routing MUST be implemented and consistently applied:
	- > 0.90: auto-approve
	- 0.70–0.90: queue for asynchronous human approval
	- < 0.70: reject + retry (with feedback)
2. Sensitive topics (politics, health advice, financial advice, legal claims) MUST always route to HITL regardless of score.
3. Agents MUST disclose their AI nature when asked, overriding persona/brand voice.
4. Platform-native AI labeling MUST be used whenever available.

### IV. Economic Agency Requires Budget Governance
Agents may transact and manage resources, but must do so safely.

Rules:
1. Financial actions (wallet operations, on-chain transactions, paid API calls above thresholds) MUST be reviewed by a dedicated “CFO Judge” policy layer.
2. Budget limits MUST be explicit and enforced (e.g., max daily spend). Exceeding limits MUST halt execution and require HITL approval.
3. Private keys/credentials MUST NOT be stored in code or logs. They MUST be sourced from a secrets manager and injected at runtime.
4. Ledger/audit records MUST be immutable and queryable for every financial action.

### V. Python Quality, Reproducibility, and Type Safety
The codebase is a professional Python system with strict quality gates.

Rules:
1. Dependency management uses `uv` exclusively. Never use `pip`, `poetry`, or `conda`.
2. Typing is mandatory. `mypy --strict` MUST pass.
3. `Any` is forbidden unless it includes a `justification:` comment on the same declaration.
4. Schemas/config MUST use Pydantic v2. Prefer `Annotated` types for constraints/metadata.
5. Lint/format uses Ruff. The repo stays formatted and lint-clean.
6. Tests use pytest and live under `tests/`, mirroring `src/`. Coverage MUST remain ≥ 90%.
7. Public-facing functions/classes MUST have Google-style docstrings with `Args`, `Returns`, `Raises`.

## Architecture and Data Constraints

### System Topology
1. The orchestrator is the hub; swarms are spokes. Services communicate via well-defined queues and schemas.
2. Multi-tenancy isolation is mandatory: no cross-tenant memory, data, or financial access.

### Storage Strategy
1. PostgreSQL is the system of record for relational metadata and audit logs (ACID required).
2. Redis is for hot queues and short-term/episodic state.
3. Weaviate is for semantic memory and persona retrieval.
4. Large assets (images/video) live in object storage; databases store references and metadata.

### Observability and Auditability
1. All tool calls and publication attempts MUST be logged with correlation identifiers.
2. Every external action must be attributable to: agent_id, tenant_id, campaign_id, and a trace/task id.
3. Failures should be self-healing by default (retry with backoff, re-queue, circuit breakers). Escalate to HITL only on policy/safety/edge cases.

### Performance and Scalability
1. Design for horizontal scaling of workers and judges.
2. Target operation at 1,000+ concurrent agents without orchestrator degradation (stateless where feasible).
3. High-priority interaction latency targets must be defined per workflow; anything safety-gated can exclude human review time.

## Development Workflow and Quality Gates

### Definition of Done (DoD)
1. `uv sync` works from a clean checkout and keeps `uv.lock` consistent.
2. `uv run ruff format .` produces no diffs.
3. `uv run ruff check .` passes (or `--fix` was applied and re-checked).
4. `uv run mypy .` passes in strict mode.
5. `uv run pytest` passes and coverage remains ≥ 90%.
6. Public API changes include updated docstrings and relevant tests.

### Change Discipline
1. Prefer small PRs: one capability or policy change at a time.
2. Any change that affects:
	- tool contracts (MCP)
	- task/result schemas
	- Judge policy thresholds
	- persona/SOUL parsing
	- finance/budget enforcement
	MUST include tests and a short migration note.
3. Breaking changes require a written upgrade path.

### Security Practices
1. Never log secrets. Redact by default.
2. Treat agent-generated content as untrusted input when it flows into tools.
3. Use least privilege for MCP servers and credentials.

## Governance

1. This constitution supersedes all other project practices and should be referenced during reviews.
2. Exceptions are allowed only with:
	- a written rationale
	- scope + time limit
	- an explicit rollback plan
	- approval by the maintainer/super-orchestrator
3. Amendments require updating this file and noting the change in the “Last Amended” date.

**Version**: 0.1.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
