# Research: AgentKit & MCP Alignment (Phase 0)

This research identifies how to integrate Coinbase AgentKit into Project Chimera while strictly adhering to Rule I (MCP-First) and Rule IV (Budget Governance).

## 1. Coinbase AgentKit MCP Integration

**Finding:** Coinbase provides an official MCP server implementation for AgentKit.
- **Reference:** `coinbase/agentkit-mcp-server` (Node.js/TypeScript) and evolving Python support.
- **Mechanism:** The server exposes AgentKit actions (e.g., `transfer_asset`, `get_balance`, `mint_nft`) as MCP Tools.
- **Recommendation:** Use the official `coinbase-mcp-server` via a `stdio` or `sse` transport.
- **Rule I Adherence:** Chimera's `Worker` MUST NOT import `coinbase_agentkit`. Instead, it connects to the MCP server. The `CommerceManager` acts as a high-level orchestrator that manages this connection and enforces policies.

## 2. CFO Judge Architecture

To satisfy Rule IV, a "Gatekeeper" pattern is required.

### Interceptor Pattern
The `CFO Judge` should be implemented as a middleware/interceptor within the `MCPClient` or a dedicated `CommerceService`.

**Workflow:**
1. **Agent Step:** LLM decides to call `transfer_asset(amount=50, asset="usdc")`.
2. **Pre-flight Check:** The `MCPClient` (or the `Worker` handling the call) identifies this as a "Financial Action".
3. **Judge Evaluation:** 
    - `CFO Judge` is invoked with `(tenant_id, tool_name, arguments)`.
    - `CFO Judge` fetches `current_spend` from Redis.
    - `CFO Judge` fetches `daily_limit` for the tenant (default $100).
4. **Decision:**
    - If `current_spend + request > daily_limit`: Return `ToolResult(is_error=True, content="Budget Exceeded")`.
    - Else: Execute actual MCP tool call.

## 3. Dry-Run & Safety Testing

**Best Practices for AgentKit:**
- **Network Selection:** Use `base-sepolia` for all development and non-production testing.
- **Wallet Faucets:** Utilize CDP's automated faucet tools for testnet assets.
- **Mocking at the Transport Layer:** Since we use MCP, we can mock the entire `MCPClientPort` in tests. We don't need to mock the blockchain provider directly if we can mock the Tool responses.
- **"Shadow" Mode:** Implement a configuration flag `CHIMERA_COMMERCE_DRY_RUN=true`. When enabled, the `CFO Judge` still validates, but the `MCPClient` logs the call and returns a success mock instead of calling the server.

## 4. Distributed Spend Limits (Implementation Detail)

To ensure consistency in a distributed environment:

### Hot State: Redis
- **Key:** `chimera:spend:{tenant_id}:{YYYY-MM-DD}`
- **Operation:** Use `WATCH` or a Lua script to ensure atomicity during `current_spend` update.
- **TTL:** 48 hours (to cover edge cases around day resets across timezones).

### Cold State: PostgreSQL (Audit Ledger)
- **Table:** `commerce_ledger`
- **Fields:** `trace_id`, `tenant_id`, `amount_usd`, `fee_usd`, `asset`, `status` (BLOCKED, EXECUTED, FAILED), `mcp_tool_call_id`.
- **Constraint:** Every entry in `commerce_ledger` must correlate to an MCP `call_tool` trace.

## 5. Summary Recommendation

1. **Deploy** `coinbase-mcp-server` as a sidecar or standalone service.
2. **Implement** `CommerceService` as the internal port for all financial logic.
3. **Implement** `@budget_check` decorator that wraps `CommerceService` methods, delegating to `CFO Judge`.
4. **Enforce** that all wallet interactions go through `CommerceService` -> `MCPClientPort`.
