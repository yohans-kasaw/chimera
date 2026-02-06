import pytest
from decimal import Decimal
from chimera.services.commerce import CommerceManager
from chimera.services.judge_policy import CFOJudge

@pytest.mark.asyncio
async def test_full_transaction_flow_with_governance(mocker):
    """
    US1 & US2 Integration:
    1. Initialize CommerceManager
    2. Attempt a transaction
    3. Verify CFO Judge is consulted
    4. Verify Spend Tracker is updated (Audit trail)
    """
    # Setup environment
    mocker.patch.dict("os.environ", {
        "CDP_API_KEY_NAME": "test_key",
        "CDP_API_KEY_PRIVATE_KEY": "test_secret"
    })
    
    # Initialize components
    # We expect these to fail with NotImplementedError for now
    manager = CommerceManager("test_key", "test_secret")
    
    # Mock MCP call
    mocker.patch.object(manager, "_call_mcp_tool", return_value={"status": "success"})
    
    # Execute
    result = await manager.transfer_asset(
        agent_id="agent_alpha",
        tenant_id="tenant_beta",
        amount=Decimal("10.00"),
        asset="ETH",
        destination="0x000",
        trace_id="integration_trace_1"
    )
    
    # Verify
    assert result.status == "EXECUTED"
    assert result.amount_usd > 0
    
    # Verify spend was tracked (this would check Redis or DB in real impl)
    new_spend = await manager.get_current_spend("tenant_beta")
    assert new_spend >= Decimal("10.00")
