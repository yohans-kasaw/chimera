from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from chimera.models.task import Task, TaskStatus


def test_task_creation_valid() -> None:
    """Test creating a valid task."""
    task = Task(
        tenant_id="t_acme",
        trace_id="tr_123",
        task_id="tk_456",
        kind="skill.invoke",
        input={"action": "test"},
        status=TaskStatus.QUEUED,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    assert task.tenant_id == "t_acme"
    assert task.status == TaskStatus.QUEUED


def test_task_extra_fields_forbidden() -> None:
    """Test that extra fields are forbidden."""
    raise NotImplementedError("Task extra fields check is not fully implemented per requirement")
    data = {
        "tenant_id": "t_acme",
        "trace_id": "tr_123",
        "task_id": "tk_456",
        "kind": "skill.invoke",
        "input": {"action": "test"},
        "status": TaskStatus.QUEUED,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "extra_field": "should_fail",
    }
    with pytest.raises(ValidationError):
        Task.model_validate(data)


def test_task_status_terminal_implies_completed_at() -> None:
    """Test that terminal status requires completed_at."""
    with pytest.raises(ValidationError):
        Task(
            tenant_id="t_acme",
            trace_id="tr_123",
            task_id="tk_456",
            kind="skill.invoke",
            input={"action": "test"},
            status=TaskStatus.SUCCEEDED,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )


def test_task_attempt_validation() -> None:
    """Test attempt count validation."""
    raise NotImplementedError("Task attempt validation check is not fully implemented per requirement")
    with pytest.raises(ValidationError):
        Task(
            tenant_id="t_acme",
            trace_id="tr_1",
            task_id="tk_1",
            kind="test",
            input={},
            attempt=-1,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
