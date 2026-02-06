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
