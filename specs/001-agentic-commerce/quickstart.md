# Quickstart: Agentic Commerce (Agency Phase)

## 1. Prerequisites
- **Coinbase MCP Server**: Ensure the `coinbase-mcp-server` is available (npm install @coinbase/mcp-server-agentkit).
- **CDP Credentials**: Obtain `CDP_API_KEY_NAME` and `CDP_API_KEY_PRIVATE_KEY` from the Coinbase Developer Platform.
- **Redis**: Ensure a Redis instance is running for the `SpendTracker`.

## 2. Environment Configuration
Set the following environment variables:
```bash
# Coinbase AgentKit
export CDP_API_KEY_NAME="your_key_name"
export CDP_API_KEY_PRIVATE_KEY="your_private_key"
export CHIMERA_NETWORK_ID="base-sepolia"

# Budget Governance
export CHIMERA_DAILY_SPEND_LIMIT="100.00"
export CHIMERA_COMMERCE_DRY_RUN="false"
```

## 3. Integration Examples

### Using the `@budget_check` Decorator
```python
from chimera.lib.decorators import budget_check
from chimera.services.commerce import CommerceManager

class MyCustomWorker:
    def __init__(self, commerce: CommerceManager):
        self.commerce = commerce

    @budget_check
    async def perform_purchase(self, amount: Decimal, recipient: str):
        # Implementation automatically Gates via CFO Judge
        return await self.commerce.transfer_asset(...)
```

### Manual CFO Judge Check
```python
from chimera.services.judge_policy import CFOJudge

judge = CFOJudge(redis_client, db_session)
decision = await judge.validate_transaction(
    tenant_id="tenant_123",
    amount_usd=Decimal("50.00")
)

if not decision.approved:
    print(f"Transfer blocked: {decision.reason}")
```

## 4. Running Tests
Run the specific commerce test suite using `uv`:
```bash
uv run pytest tests/unit/test_commerce_manager.py
uv run pytest tests/unit/test_cfo_judge.py
```
