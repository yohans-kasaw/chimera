# Feature Specification: Agentic Commerce (Agency)

**Feature Branch**: `001-agentic-commerce`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "Write tests for a CommerceManager class, ensuring it correctly initializes with environment variables for the Coinbase AgentKit. Create a specific test for the CFO Judge logic that strictly enforces a daily_spend limit, rejecting any transaction that exceeds it. Mock the blockchain provider to verify transfer_asset and get_balance calls without spending real funds. Implement the wallet integration and budget decorators to pass these safety checks. This phase guarantees financial autonomy with rigid safety guardrails."

## Technical Specifications *(mandatory)*

### API & Schemas
*   **OpenAPI Contract**: [contracts/openapi.yaml](./contracts/openapi.yaml) - Defines the CommerceManager API surface.
*   **Data Model**: [data-model.mermaid](./data-model.mermaid) - Entity Relationship Diagram for commerce entities.

## Acceptance Criteria (Gherkin)

### AC-001: Financial Autonomy (Happy Path)
*   **Trace**: [FR-001], [FR-002], [API-POST-/transfer]
*   **Scenario**: Successful Asset Transfer
    *   **Given** the CommerceManager is initialized with valid AgentKit credentials
    *   **And** the wallet balance is > $50 USD
    *   **And** the daily spend is $0 / $100
    *   **When** I request a transfer of $50 USD via `POST /transfer`
    *   **Then** the response status code is 200 (OK)
    *   **And** the response body contains a valid `tx_hash`
    *   **And** the daily spend is updated to $50

### AC-002: Safety Guardrails (Failure Mode)
*   **Trace**: [FR-005], [FR-006]
*   **Scenario**: Reject Transaction Exceeding Daily Limit
    *   **Given** a wallet with a daily limit of $100
    *   **And** the current daily spend is $90
    *   **When** I request a transfer of $11 via `POST /transfer`
    *   **Then** the response status code is 402 (Payment Required)
    *   **And** the response body error is "Daily spend limit exceeded"
    *   **And** the transaction state is recorded as "REJECTED" in the ledger

### AC-003: Secure Initialization (Edge Case)
*   **Trace**: [FR-001]
*   **Scenario**: Missing Credentials
    *   **Given** the environment variable `CDP_API_KEY_NAME` is unset
    *   **When** the `CommerceManager` attempts to initialize
    *   **Then** a `ConfigurationError` is raised
    *   **And** the system logs a critical error "Missing Wallet Credentials" (masked)

### AC-004: Performance Latency
*   **Trace**: [FR-005]
*   **Scenario**: Budget Check Overhead
    *   **Given** a valid transfer request
    *   **When** the `@budget_check` decorator executes
    *   **Then** the latency added to the call is < 200ms

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST initialize `CommerceManager` using configuration from environment variables compatible with Coinbase AgentKit.
- **FR-002**: System MUST support asset transfers through a blockchain provider interface.
- **FR-003**: System MUST provide a mechanism to query account balances.
- **FR-004**: System MUST maintain a persistent record of daily spending.
- **FR-005**: CFO Judge MUST validate every transaction against a configurable `daily_spend` limit.
- **FR-006**: System MUST reject any transaction that would cause the daily spend to exceed the limit.
- **FR-007**: System MUST provide a `@budget_check` decorator for transparent enforcement of spending limits.
- **FR-008**: System MUST support a "dry run" or mock mode for testing without real-world funds.

### Key Entities *(include if feature involves data)*

- **Wallet**: Represents the cryptographic identity, providing access to asset transfers and balance checks.
- **Transaction**: Represents a request to move a specific amount of an asset to a destination.
- **Budget Policy**: Defines the constraints (e.g., $100/day limit, reset frequency).
- **Spend Tracker**: Keeps track of the total amount spent within the current budget period.
- **CFO Judge**: The logic engine that decides if a transaction complies with the Budget Policy.

## Assumptions


- Coinbase AgentKit is the primary integration point for blockchain interactions.
- Daily spend limits are denominated in USD (or equivalent stablecoin value).
- The "day" for limit calculations is defined as a UTC calendar day.
- Network/gas fees are small enough to be either ignored or handled separately from the main asset transfer amount.

## Security & Compliance *(mandatory)*
This feature adheres to the [Master Security Architecture](../technical.md#7-security-architecture--compliance-rubric-pro).

*   **Authentication**: Uses standard OAuth2/JWT flow via the CommerceManager.
*   **Secrets Management**: All credentials managed via Vault/Env.
*   **Rate Limiting**: Enforces standard 60 req/min limit.
*   **Content Safety**: Subject to standard Moderation/Judge pipeline.
*   **Containment**: Strict Resource Limits apply (Execution Time, Token Budget).
