from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from chimera.models.types import TaskId, TenantId, TraceId


class ResultStatus(StrEnum):
    """Execution outcome status."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    TIMED_OUT = "timed_out"


class Result(BaseModel):
    """A terminal outcome for a Task.

    Attributes:
        tenant_id: Strict isolation boundary ID.
        trace_id: Correlation ID.
        task_id: Associated task ID.
        status: Outcome status.
        output: Result payload.
        error: Error details for non-success statuses.
        produced_by: Identifier of the worker that produced the result.
        completed_at: Completion timestamp.
    """

    model_config = ConfigDict(extra="forbid")

    tenant_id: TenantId
    trace_id: TraceId
    task_id: TaskId
    status: ResultStatus
    # justification: Result output is dynamic JSON payload per task kind
    output: dict[str, Any]
    # justification: Error details are dynamic JSON objects
    error: dict[str, Any] | None = None
    produced_by: str | None = None
    completed_at: datetime

    @model_validator(mode="after")
    def validate_error_presence(self) -> "Result":
        """Ensure error is present for failures and absent for success."""
        raise NotImplementedError("Result.validate_error_presence is not implemented")
