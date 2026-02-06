import pytest
from decimal import Decimal
from chimera.services.judge_policy import CFOJudge

def test_cfo_judge_approves_within_limit():
    """US1: Verify CFO Judge approves when limit is not reached."""
    judge = CFOJudge(daily_limit=Decimal("100.00"))
    assert judge.validate_transaction(
        amount_usd=Decimal("50.00"),
        current_spend=Decimal("20.00")
    ) is True

def test_cfo_judge_rejects_over_limit():
    """US1: Verify CFO Judge rejects when limit is exceeded."""
    judge = CFOJudge(daily_limit=Decimal("100.00"))
    assert judge.validate_transaction(
        amount_usd=Decimal("60.00"),
        current_spend=Decimal("50.00")
    ) is False

def test_cfo_judge_rejects_exactly_at_limit():
    """US1: Verify threshold handling."""
    judge = CFOJudge(daily_limit=Decimal("100.00"))
    # If limit is 100, and we try to spend 1, when we already spent 100
    assert judge.validate_transaction(
        amount_usd=Decimal("1.00"),
        current_spend=Decimal("100.00")
    ) is False
