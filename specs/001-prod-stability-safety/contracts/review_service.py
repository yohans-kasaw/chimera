from typing import Protocol, Sequence
from uuid import UUID
from chimera.models.review import ReviewCard, ReviewStatus
from chimera.models.types import TenantId

class ReviewServicePort(Protocol):
    """Port for managing human-in-the-loop review cards."""

    async def create_review(self, tenant_id: TenantId, review: ReviewCard) -> None:
        """Create a new review card for a flagged task result."""
        ...

    async def get_pending_reviews(self, tenant_id: TenantId) -> Sequence[ReviewCard]:
        """Retrieve all reviews currently in PENDING status."""
        ...

    async def submit_decision(
        self, 
        tenant_id: TenantId, 
        review_id: UUID, 
        status: ReviewStatus, 
        operator_id: str
    ) -> ReviewCard:
        """Update a review card with a human decision (APPROVE/REJECT)."""
        ...
