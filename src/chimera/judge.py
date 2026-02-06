"""Judge service for validating Results and enforcing gate decisions.

This module defines a small, mockable Judge boundary:

- Accept an untrusted Result payload.
- Validate it using Pydantic v2.
- Apply a policy to yield a gate decision (approve/deny/hitl).
- Persist the outcome via a Unit of Work.
- Emit structured logs (structlog-compatible) *before* committing.

All interfaces are Protocol-based to enable isolated unit tests under mypy strict.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic.types import StrictStr  # noqa: TC002


class GateDecision(StrEnum):
    """Gate decision emitted by the Judge."""

    APPROVE = "approve"
    DENY = "deny"
    HITL = "hitl"


class JudgeOutcome(BaseModel):
    """Outcome produced by the Judge for a given Result payload."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decision: GateDecision
    reason: StrictStr
    tenant_id: StrictStr | None = None
    trace_id: StrictStr | None = None
    task_id: StrictStr | None = None


class ResultEnvelope(BaseModel):
    """Validated Result payload (untrusted input normalized into a strict model)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: StrictStr
    trace_id: StrictStr
    task_id: StrictStr
    kind: StrictStr = Field(min_length=1)
    status: StrictStr = Field(min_length=1)
    output: Mapping[str, object] = Field(default_factory=dict)


class EventLogger(Protocol):
    """Minimal logger interface compatible with structlog bound loggers."""

    def info(self, event: str, **kwargs: object) -> None:
        """Emit an informational structured event."""

    def warning(self, event: str, **kwargs: object) -> None:
        """Emit a warning structured event."""


class JudgePolicy(Protocol):
    """Policy for deciding whether a validated Result passes the gate."""

    def decide(self, result: ResultEnvelope) -> tuple[GateDecision, str]:
        """Return (decision, reason) for a validated Result."""


class JudgeUnitOfWork(Protocol):
    """Persistence boundary for recording judge outcomes."""

    def record_outcome(self, outcome: JudgeOutcome) -> None:
        """Stage outcome for persistence."""

    def commit(self) -> None:
        """Commit staged changes."""

    def rollback(self) -> None:
        """Rollback staged changes."""

    def __enter__(self) -> Self:  # pragma: no cover
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:  # pragma: no cover
        if exc is None:
            return
        self.rollback()


class JudgeUoWFactory(Protocol):
    """Factory for creating a new Unit of Work per judge operation."""

    def __call__(self) -> JudgeUnitOfWork:
        """Create a new Unit of Work."""


class JudgeService:
    """Service that validates results, enforces gate decisions, and persists outcomes."""

    def __init__(
        self,
        *,
        policy: JudgePolicy,
        uow_factory: JudgeUoWFactory,
        logger: EventLogger,
    ) -> None:
        """Initialize the JudgeService.

        Args:
            policy: Gate policy used to determine approve/deny/hitl.
            uow_factory: Creates a unit-of-work used for persistence.
            logger: Structlog-compatible logger used for outcome logs.
        """

        self._policy = policy
        self._uow_factory = uow_factory
        self._logger = logger

    def judge_payload(self, payload: object) -> JudgeOutcome:
        """Validate and judge an untrusted payload.

        The payload may be a `dict`-like mapping or a JSON string.

        The Judge always logs an outcome event. On successful persistence,
        it guarantees that the log event is emitted before the commit.

        Args:
            payload: Untrusted result payload.

        Returns:
            JudgeOutcome describing the decision and reason.
        """

        result = self._validate_payload(payload)
        if result is None:
            outcome = JudgeOutcome(decision=GateDecision.DENY, reason="invalid_result")
            self._logger.warning("judge.invalid_result", reason=outcome.reason)
            return outcome

        decision, reason = self._policy.decide(result)
        outcome = JudgeOutcome(
            decision=decision,
            reason=reason,
            tenant_id=result.tenant_id,
            trace_id=result.trace_id,
            task_id=result.task_id,
        )

        with self._uow_factory() as uow:
            uow.record_outcome(outcome)

            # Ordering invariant: emit the outcome log before committing.
            self._logger.info(
                "judge.outcome",
                decision=outcome.decision,
                reason=outcome.reason,
                tenant_id=outcome.tenant_id,
                trace_id=outcome.trace_id,
                task_id=outcome.task_id,
            )

            uow.commit()

        return outcome

    @staticmethod
    def _validate_payload(payload: object) -> ResultEnvelope | None:
        """Convert untrusted payload into a validated `ResultEnvelope`.

        Args:
            payload: Untrusted payload, usually `dict` or JSON string.

        Returns:
            A validated `ResultEnvelope`, or None if validation fails.
        """

        try:
            if isinstance(payload, str):
                return ResultEnvelope.model_validate_json(payload)
            if isinstance(payload, Mapping):
                # Pydantic will validate keys/values; we keep type surface `object`.
                return ResultEnvelope.model_validate(payload)
        except ValidationError:
            return None

        return None
