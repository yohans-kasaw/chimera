from __future__ import annotations

from dataclasses import dataclass, field

from chimera.judge import GateDecision, JudgeOutcome, JudgeService, JudgeUnitOfWork, ResultEnvelope


@dataclass
class RecordingLogger:
    calls: list[tuple[str, str]] = field(default_factory=list)

    def info(self, event: str, **kwargs: object) -> None:  # noqa: ARG002
        self.calls.append(("log", event))

    def warning(self, event: str, **kwargs: object) -> None:  # noqa: ARG002
        self.calls.append(("log", event))


@dataclass
class RecordingUoW(JudgeUnitOfWork):
    calls: list[tuple[str, str]]
    committed: bool = False
    outcomes: list[JudgeOutcome] = field(default_factory=list)

    def record_outcome(self, outcome: JudgeOutcome) -> None:
        self.calls.append(("uow", "record_outcome"))
        self.outcomes.append(outcome)

    def commit(self) -> None:
        self.calls.append(("uow", "commit"))
        self.committed = True

    def rollback(self) -> None:
        self.calls.append(("uow", "rollback"))

    def __enter__(self) -> RecordingUoW:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:
        if exc is not None:
            self.rollback()


class AllowAllPolicy:
    def decide(self, result: ResultEnvelope) -> tuple[GateDecision, str]:
        return (GateDecision.APPROVE, "ok")


def test_invalid_result_is_rejected_and_not_committed() -> None:
    timeline: list[tuple[str, str]] = []
    logger = RecordingLogger(calls=timeline)

    def uow_factory() -> RecordingUoW:
        return RecordingUoW(calls=timeline)

    judge = JudgeService(policy=AllowAllPolicy(), uow_factory=uow_factory, logger=logger)

    # Missing required fields => invalid.
    outcome = judge.judge_payload({"tenant_id": "t_acme"})

    assert outcome.decision == GateDecision.DENY
    assert outcome.reason == "invalid_result"
    assert timeline == [("log", "judge.invalid_result")]


def test_log_emitted_before_commit_for_valid_result() -> None:
    timeline: list[tuple[str, str]] = []
    logger = RecordingLogger(calls=timeline)
    policy = AllowAllPolicy()

    def uow_factory() -> RecordingUoW:
        return RecordingUoW(calls=timeline)

    judge = JudgeService(policy=policy, uow_factory=uow_factory, logger=logger)

    outcome = judge.judge_payload(
        {
            "tenant_id": "t_acme",
            "trace_id": "trace-123",
            "task_id": "task-123",
            "kind": "publish",
            "status": "succeeded",
            "output": {"url": "https://example.com"},
        }
    )

    assert outcome.decision == GateDecision.APPROVE
    assert timeline == [
        ("uow", "record_outcome"),
        ("log", "judge.outcome"),
        ("uow", "commit"),
    ]
