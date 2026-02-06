from decimal import Decimal
from typing import Protocol, runtime_checkable

from chimera.models.result import Result
from chimera.ports.judge import Decision


@runtime_checkable
class JudgePolicy(Protocol):
    """Protocol for security gate policies."""

    def evaluate(self, result: Result) -> tuple[Decision, str]:
        """Evaluate a result and return a decision and reason.

        Args:
            result: The result to evaluate.

        Returns:
            A tuple of (Decision, reason_code).
        """
        ...


class DefaultJudgePolicy:
    """A simple policy for the MVP."""

    def evaluate(self, result: Result) -> tuple[Decision, str]:
        raise NotImplementedError("DefaultJudgePolicy.evaluate is not implemented")


class CFOJudge:
    """Policy for financial budget enforcement."""

    def __init__(self, daily_limit: Decimal = Decimal("100.00")):
        self.daily_limit = daily_limit

    def validate_transaction(self, amount_usd: Decimal, current_spend: Decimal) -> bool:
        """
        Validate if a transaction fits within the daily budget.
        
        Args:
            amount_usd: The amount of the transaction in USD.
            current_spend: The total amount spent today in USD.
            
        Returns:
            bool: True if approved, False otherwise.
        """
        raise NotImplementedError("CFOJudge.validate_transaction is not implemented")
