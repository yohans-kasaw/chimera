from typing import Sequence
from uuid import UUID

from chimera.models.review import ReviewCard, ReviewStatus
from chimera.models.types import TenantId


class ReviewService:
    """Manages Human-in-the-Loop review lifecycle."""

    async def create_review(self, tenant_id: TenantId, review: ReviewCard) -> None:
        """Persist a new review card."""
        raise NotImplementedError("ReviewService.create_review is not implemented")

    async def get_pending_reviews(self, tenant_id: TenantId) -> Sequence[ReviewCard]:
        """Fetch all PENDING review cards for a tenant."""
        raise NotImplementedError("ReviewService.get_pending_reviews is not implemented")

    async def submit_decision(
        self,
        tenant_id: TenantId,
        review_id: UUID,
        status: ReviewStatus,
        operator_id: str,
    ) -> ReviewCard:
        """Apply a human decision to a review card."""
        raise NotImplementedError("ReviewService.submit_decision is not implemented")
