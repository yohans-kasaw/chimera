from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator

from chimera.models.types import SessionId, TaskId, TenantId, TraceId


class TaskStatus(StrEnum):
    """Lifecycle stages of a task."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    TIMED_OUT = "timed_out"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"

    @property
    def is_terminal(self) -> bool:
        """Return True if the status is terminal."""
        raise NotImplementedError("TaskStatus.is_terminal is not implemented")


class Task(BaseModel):
    """A unit of requested work created by a Planner and processed by a Worker.

    Attributes:
        tenant_id: Strict isolation boundary ID.
        trace_id: Correlation ID across services.
        task_id: Unique task identifier.
        parent_task_id: Optional ID for decomposed tasks.
        session_id: Optional swarm session link.
        kind: Stable task type identifier (e.g., 'skill.invoke').
        input: JSON-serializable payload.
        status: Lifecycle status.
        priority: Execution priority (0-100).
        attempt: Current attempt count.
        max_attempts: Maximum allowed attempts.
        timeout_s: Optional timeout in seconds.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
        started_at: Execution start timestamp.
        completed_at: Completion timestamp.
    """

    model_config = ConfigDict(extra="forbid")

    tenant_id: TenantId
    trace_id: TraceId
    task_id: TaskId
    parent_task_id: TaskId | None = None
    session_id: SessionId | None = None
    kind: str
    # justification: Task input is dynamic JSON payload per skill contract
    input: dict[str, Any]
    status: TaskStatus = TaskStatus.QUEUED
    priority: int = Field(default=0, ge=0, le=100)
    attempt: int = Field(default=0, ge=0)
    max_attempts: int = Field(default=0, ge=0)
    timeout_s: int | None = Field(default=None, ge=1)

    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # internal storage for redis message id to enable XACK
    _raw_id: str | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def validate_terminal_status_completeness(self) -> "Task":
        """Ensure terminal status has completed_at set."""
        raise NotImplementedError("Task.validate_terminal_status_completeness is not implemented")

    @model_validator(mode="after")
    def validate_timestamp_ordering(self) -> "Task":
        """Verify timestamp sequence integrity."""
        raise NotImplementedError("Task.validate_timestamp_ordering is not implemented")
