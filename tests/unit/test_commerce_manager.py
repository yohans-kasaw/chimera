import pytest
import os
from decimal import Decimal
from chimera.services.commerce import CommerceManager

def test_commerce_manager_init_fails_with_missing_env_vars():
    """US2: Verify initialization fails when credentials are not provided."""
    if "CDP_API_KEY_NAME" in os.environ:
        del os.environ["CDP_API_KEY_NAME"]
    if "CDP_API_KEY_PRIVATE_KEY" in os.environ:
        del os.environ["CDP_API_KEY_PRIVATE_KEY"]
    
    with pytest.raises(ValueError, match="Missing credentials"):
        # Currently raises NotImplementedError, which is also a type of failure
        CommerceManager(
            cdp_key_name=os.getenv("CDP_API_KEY_NAME", ""),
            cdp_private_key=os.getenv("CDP_API_KEY_PRIVATE_KEY", "")
        )

@pytest.mark.asyncio
async def test_transfer_asset_within_budget(mocker):
    """US1: Verify transfer succeeds when budget allows."""
    # Mocking the blockchain provider and existing spend
    manager = CommerceManager("key", "secret")
    mocker.patch.object(manager, "get_current_spend", return_value=Decimal("10.00"))
    
    # This should call the CFOJudge internally
    result = await manager.transfer_asset(
        agent_id="agent_1",
        tenant_id="tenant_1",
        amount=Decimal("50.00"),
        asset="USDC",
        destination="0x123",
        trace_id="trace_1"
    )
    
    assert result.status == "EXECUTED"
    assert result.amount_usd == Decimal("50.00")

@pytest.mark.asyncio
async def test_transfer_asset_exceeds_budget(mocker):
    """US1: Verify transfer is rejected when budget is exceeded."""
    manager = CommerceManager("key", "secret")
    mocker.patch.object(manager, "get_current_spend", return_value=Decimal("95.00"))
    
    with pytest.raises(Exception, match="Budget Exceeded"):
        await manager.transfer_asset(
            agent_id="agent_1",
            tenant_id="tenant_1",
            amount=Decimal("10.00"),
            asset="USDC",
            destination="0x123",
            trace_id="trace_2"
        )
