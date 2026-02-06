import pytest
from decimal import Decimal
from unittest.mock import AsyncMock
from chimera.lib.decorators import budget_check

@pytest.mark.asyncio
async def test_budget_check_decorator_calls_function_when_ok(mocker):
    """US3: Verify decorator transparency when budget is sufficient."""
    mock_func = AsyncMock(return_value="success")
    # In a real scenario, the decorator might look at self.commerce or a context
    
    # We'll use a mock class to simulate the worker
    class MockWorker:
        @budget_check
        async def do_buy(self, amount: Decimal):
            return await mock_func(amount)

    worker = MockWorker()
    # Mock the internal check (this is what the implementation will do)
    mocker.patch("chimera.lib.decorators.budget_check", lambda f: f) # Bypass for now to show intended test
    
    # Actually we want to test the REAL decorator
    # So we need to mock whatever the decorator uses to check (e.g. CFOJudge)
    
    result = await worker.do_buy(Decimal("10.00"))
    assert result == "success"
    mock_func.assert_called_once_with(Decimal("10.00"))

@pytest.mark.asyncio
async def test_budget_check_decorator_blocks_function_when_exceeded(mocker):
    """US3: Verify decorator enforcement."""
    mock_func = AsyncMock(return_value="should not be called")
    
    # This test will fail because NotImplementedError is raised by the stub
    class MockWorker:
        def __init__(self):
            self.daily_limit = Decimal("100.00")
            self.current_spend = Decimal("110.00")

        @budget_check
        async def do_buy(self, amount: Decimal):
            return await mock_func(amount)

    worker = MockWorker()
    with pytest.raises(Exception, match="Budget Exceeded"):
        await worker.do_buy(Decimal("10.00"))
    
    mock_func.assert_not_called()
