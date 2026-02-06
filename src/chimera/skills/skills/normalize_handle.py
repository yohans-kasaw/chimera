"""Handle normalization skill.

Canonicalizes social handles into an '@handle' string.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from chimera.skills.base import Skill
from chimera.skills.models import SkillContext


class NormalizeHandleInput(BaseModel):
    """Input payload for handle normalization."""

    handle: str = Field(..., description="Social handle to normalize.")


class NormalizeHandleOutput(BaseModel):
    """Normalized social handle output."""

    handle: str = Field(..., description="Normalized handle.")


class NormalizeHandleSkill(Skill[NormalizeHandleInput, NormalizeHandleOutput]):
    """Normalize social handles into a canonical format."""

    name = "normalize_handle"
    description = "Normalize a social handle into a canonical format."
    input_model = NormalizeHandleInput
    output_model = NormalizeHandleOutput

    async def run(
        self, payload: NormalizeHandleInput, context: SkillContext
    ) -> NormalizeHandleOutput:
        _ = context
        normalized = payload.handle.strip()
        if not normalized.startswith("@"):  # simple canonicalization
            normalized = f"@{normalized}"
        return NormalizeHandleOutput(handle=normalized)
