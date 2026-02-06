from enum import StrEnum
from typing import Protocol, runtime_checkable

from chimera.models.result import Result
from chimera.models.types import TaskId, TenantId, TraceId


class Decision(StrEnum):
    """Judge decision outcome."""

    APPROVE = "approve"
    DENY = "deny"
    HITL = "hitl"


@runtime_checkable
class JudgePort(Protocol):
    """Port for Judge security gate evaluation."""

    async def evaluate_result(self, tenant_id: TenantId, result: Result) -> Decision:
        """Evaluate a result against security policies.

        Args:
            tenant_id: Target tenant.
            result: The result to evaluate.

        Returns:
            The decision made by the judge.
        """
        ...

    async def log_decision(
        self,
        tenant_id: TenantId,
        trace_id: TraceId,
        task_id: TaskId,
        decision: Decision,
        reason: str,
    ) -> None:
        """Durable log of a judge decision.

        Args:
            tenant_id: Target tenant.
            trace_id: Correlation ID.
            task_id: Task ID.
            decision: Outcome.
            reason: Rationale for the decision.
        """
        ...
