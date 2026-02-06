from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from chimera.models.result import Result, ResultStatus


def test_result_creation_valid() -> None:
    """Test creating a valid result."""
    result = Result(
        tenant_id="t_acme",
        trace_id="tr_123",
        task_id="tk_456",
        status=ResultStatus.SUCCEEDED,
        output={"success": True},
        completed_at=datetime.now(UTC),
    )
    assert result.status == ResultStatus.SUCCEEDED


def test_result_failure_requires_error() -> None:
    """Test that failed result requires error field."""
    with pytest.raises(ValidationError):
        Result(
            tenant_id="t_acme",
            trace_id="tr_123",
            task_id="tk_456",
            status=ResultStatus.FAILED,
            output={},
            completed_at=datetime.now(UTC),
            # error missing
        )


def test_result_success_no_error() -> None:
    """Test that succeeded result should not have error."""
    with pytest.raises(ValidationError):
        Result(
            tenant_id="t_acme",
            trace_id="tr_123",
            task_id="tk_456",
            status=ResultStatus.SUCCEEDED,
            output={"ok": True},
            error={"msg": "wrong"},
            completed_at=datetime.now(UTC),
        )
