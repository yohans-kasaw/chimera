from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from chimera.models.result import Result, ResultStatus
from chimera.ports.judge import Decision
from chimera.services.judge import JudgeService


@pytest.mark.asyncio
async def test_judge_rejects_invalid_result() -> None:
    judge = JudgeService()

    # Simulating a result that might be "risky" per our policy
    result = Result(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        status=ResultStatus.SUCCEEDED,
        output={"action": "delete_all_files"},
        completed_at=datetime.now(UTC),
    )

    # We'll implement a policy that denies "delete_all_files"
    decision = await judge.evaluate_result("t_acme", result)
    assert decision == Decision.DENY


@pytest.mark.asyncio
async def test_judge_logs_before_return() -> None:
    judge = JudgeService()
    result = Result(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        status=ResultStatus.SUCCEEDED,
        output={"ok": True},
        completed_at=datetime.now(UTC),
    )

    with patch("chimera.services.judge.logger") as mock_logger:
        await judge.evaluate_result("t_acme", result)
        # Check that logger was called with the decision
        args, kwargs = mock_logger.info.call_args
        assert args[0] == "judge_decision"
        assert kwargs["tenant_id"] == "t_acme"
        assert kwargs["decision"] == Decision.APPROVE
