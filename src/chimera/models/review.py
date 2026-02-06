from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from chimera.models.types import ResultId, TaskId


class ReviewReason(StrEnum):
    """Reasons why a task result was flagged for review."""

    LOW_CONFIDENCE = "low_confidence"
    SENSITIVE_KEYWORD = "sensitive_keyword"


class ReviewStatus(StrEnum):
    """Status of a human-in-the-loop review."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewCard(BaseModel):
    """Holds information for human intervention on a flagged result."""

    model_config = ConfigDict(extra="forbid")

    review_id: UUID
    task_id: TaskId
    result_id: ResultId
    reason: ReviewReason
    details: str
    status: ReviewStatus = ReviewStatus.PENDING
    operator_id: str | None = None
    timestamp: datetime
    resolution_at: datetime | None = None
