# Data Model: Agentic Commerce

## Entities

### BudgetConfiguration (Pydantic Model)
Defines the spending constraints for a specific entity (tenant or agent).
- `id`: UUID
- `tenant_id`: str
- `daily_limit_usd`: Decimal (Default: 100.00)
- `currency`: str (Default: "USD")
- `is_active`: bool

### TransactionRecord (PostgreSQL / SQLModel)
Audit trail for every financial request (Rule IV.4).
- `id`: UUID (Primary Key)
- `trace_id`: str (Correlation ID for the task)
- `agent_id`: str
- `timestamp`: DateTime (UTC)
- `tool_name`: str (e.g., "transfer_asset")
- `amount_asset`: Decimal
- `asset_symbol`: str (e.g., "ETH", "USDC")
- `amount_usd`: Decimal (Calculated at time of transaction)
- `network_fee_usd`: Decimal
- `status`: TransactionStatus (PENDING, APPROVED, REJECTED, EXECUTED, FAILED)
- `rejection_reason`: str?
- `mcp_response`: JSON? (Raw response from MCP server)

### SpendTracker (Redis State)
Hot state for real-time budget enforcement.
- **Key**: `chimera:spend:{tenant_id}:{YYYYMMDD}`
- **Value**: Decimal (Cumulative USD spend)
- **TTL**: 48h

## Enums

### TransactionStatus
- `PENDING`: Request received by CFO Judge.
- `APPROVED`: Passed budget check, sent to MCP.
- `REJECTED`: Blocked by CFO Judge due to budget.
- `EXECUTED`: Successfully signed/confirmed on-chain.
- `FAILED`: MCP server returned an error or blockchain failure.

## Relationships
- A `BudgetConfiguration` applies to a `tenant_id`.
- Every `TransactionRecord` belongs to a `tenant_id` and `agent_id`.
- Every `TransactionRecord` correlates to an entry in the `SpendTracker`.
