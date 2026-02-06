# Feature Specification: Observable MCP Agent Swarm

**Feature Branch**: `001-observable-mcp-swarm`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "Project Chimera is an observable, MCP-integrated swarm of autonomous agents. By leveraging a modular Skills framework, the system enforces strict contracts and Judge-led security gates, enabling a single operator to manage a multi-tenant, fault-tolerant influencer network with guaranteed state integrity."

## Technical Specifications *(mandatory)*

### Protocols & Data Models
*   **OpenClaw Protocol**: [contracts/openclaw.yaml](./contracts/openclaw.yaml) - Defines the message structure for Swarm/Agent communication.
*   **Data Model**: [data-model.mermaid](./data-model.mermaid) - Entity Relationship Diagram for Swarm, Tenants, and Tasks.
*   **OpenAPI Contract**: [contracts/openapi.yaml](./contracts/openapi.yaml) - API definitions for Swarm management.

## Acceptance Criteria (Gherkin)

### AC-001: Operate Tenant Swarm (Happy Path)
*   **Trace**: [FR-002], [FR-003], [API-POST-/swarm/session]
*   **Scenario**: Operator Starts Session
    *   **Given** a valid tenant "Tenant-A" exists
    *   **When** the operator submits `POST /swarm/session` with tenant_id="Tenant-A"
    *   **Then** the response status is 201 (Created)
    *   **And** the session state is "ACTIVE"
    *   **And** the Swarm Dashboard displays the new session within 500ms

### AC-002: Security Gate Enforcement (Failure Mode)
*   **Trace**: [FR-007], [FR-008]
*   **Scenario**: Judge Rejects Policy Violation
    *   **Given** an active agent proposes action `tweet("hacked")`
    *   **And** the active security policy forbids the keyword "hacked"
    *   **When** the Judge evaluates the proposal
    *   **Then** the action is rejected with reason "Policy Violation: Forbidden Keyword"
    *   **And** an Audit Event is created with `decision="DENY"`
    *   **And** no side effects (tweets) occur

### AC-003: Cross-Tenant Isolation (Edge Case)
*   **Trace**: [FR-001], [FR-009]
*   **Scenario**: Prevent Cross-Tenant Access
    *   **Given** Agent-A belongs to Tenant-A
    *   **When** Agent-A attempts to read data belonging to Tenant-B
    *   **Then** the database layer raises a `TenantIsolationError`
    *   **And** the attempt is logged as a security incident

### AC-004: Fault Tolerance
*   **Trace**: [FR-010]
*   **Scenario**: Single Agent Failure
    *   **Given** Agent-X is executing Task-Y
    *   **When** Agent-X crashes (process termination)
    *   **Then** the Swarm Supervisor detects the failure within 1000ms
    *   **And** Task-Y state is reset to "PENDING"
    *   **And** Agent-X is marked "RESTARTING"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support a multi-tenant operating model where tenant data, execution, and audit history are isolated by default. (Acceptance: attempts to access another tenant’s data or actions are blocked and recorded.)
- **FR-002**: System MUST allow a single operator to create, start, pause, and stop a swarm session for a specific tenant. (Acceptance: an operator can transition a session through these states and observe the state change.)
- **FR-003**: System MUST provide continuous observability for swarm sessions, including agent status, task progress, decisions made, and outcomes. (Acceptance: for any session, the operator can view live status plus a durable history of key events.)
- **FR-004**: System MUST integrate with MCP-compatible interfaces so skills and tools can be invoked through a consistent, contract-driven mechanism. (Acceptance: at least one MCP-compatible tool/skill can be invoked end-to-end with validated inputs/outputs.)
- **FR-005**: System MUST provide a modular Skills framework where each skill has an explicit contract defining required inputs, outputs, and allowed side effects. (Acceptance: contracts are visible to the operator and are enforced for execution.)
- **FR-006**: System MUST validate that skill invocations conform to the declared contract before execution. (Acceptance: invalid invocations are rejected with actionable validation errors and no side effects.)
- **FR-007**: System MUST enforce Judge-led security gates for actions that are sensitive, policy-controlled, or cross-trust-boundary. (Acceptance: gated actions produce an explicit approve/deny decision before any effects occur.)
- **FR-008**: System MUST record every security gate decision (approve/deny) with reason codes and enough context to audit after the fact. (Acceptance: an operator can retrieve the full decision record for any gated action.)
- **FR-009**: System MUST prevent cross-tenant data access and cross-tenant action execution, including via indirect agent-to-agent coordination. (Acceptance: simulated cross-tenant attempts are denied and produce audit events.)
- **FR-010**: System MUST provide fault-tolerant execution such that individual agent failures do not corrupt committed state. (Acceptance: induced single-agent failure preserves committed history and leads to controlled resume or halt.)
- **FR-011**: System MUST maintain state integrity such that all committed state changes are traceable to an authorized decision and can be reconciled to a consistent final state. (Acceptance: an operator can reconcile state snapshots against the event history without unexplained deltas.)
- **FR-012**: System MUST allow the operator to review a tenant’s influencer-network activity as a set of managed entities, tasks, and outcomes. (Acceptance: the operator can list entities, see associated tasks, and review outcomes for a selected time range.)

### Assumptions & Dependencies

- The operator is an authorized user with permission to manage one or more tenants.
- Tenants may have different security policies; defaults exist for new tenants.
- Influencer-network operations may involve external systems; such interactions are always policy-controlled and auditable.
- This feature defines the core platform guarantees (observability, skill contracts, security gates, isolation, and integrity) and does not define tenant billing, influencer acquisition strategy, or content/campaign creative direction.

### Key Entities *(include if feature involves data)*

- **Tenant**: A customer/account boundary; owns all data, policies, and execution history.
- **Operator**: The human responsible for initiating sessions, submitting tasks, and reviewing outcomes.
- **Swarm Session**: A time-bounded operating context for one tenant’s work; includes participating agents and the executed task history.
- **Agent**: An autonomous actor that performs tasks using available skills; has status, identity, and assigned work.
- **Skill**: A modular capability used by agents; has a contract describing inputs/outputs and allowed side effects.
- **Skill Contract**: The explicit specification for a skill’s interface and constraints used for validation and safe composition.
- **Judge Policy**: A set of rules that define what is allowed, denied, or requires additional review.
- **Gate Decision**: A recorded outcome of Judge evaluation for a proposed action.
- **Task**: A unit of requested work; may decompose into steps and skill invocations.
- **Audit Event**: An immutable record of significant system events (decisions, state changes, failures, approvals).
- **State Snapshot**: A point-in-time representation of the tenant/session state used for reconciliation and integrity checks.
- **Influencer Profile**: A managed entity representing an influencer account, constraints, and engagement goals.
- **Campaign**: A set of objectives and tasks executed against one or more influencer profiles.

## Security & Compliance *(mandatory)*

This feature adheres to the [Master Security Architecture](../technical.md#7-security-architecture--compliance-rubric-pro).

*   **Authentication**: Uses standard OAuth2/JWT flow via the CommerceManager.
*   **Secrets Management**: All credentials managed via Vault/Env.
*   **Rate Limiting**: Enforces standard 60 req/min limit.
*   **Content Safety**: Subject to standard Moderation/Judge pipeline.
*   **Containment**: Strict Resource Limits apply (Execution Time, Token Budget).
