"""Echo skill.

Deterministic, side-effect free skill used as a checkpoint and runtime smoke test.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from chimera.skills.base import Skill
from chimera.skills.models import SkillContext


class EchoInput(BaseModel):
    """Input payload for the echo skill."""

    message: str = Field(..., description="Message to echo.")


class EchoOutput(BaseModel):
    """Output payload for the echo skill."""

    message: str = Field(..., description="Echoed message.")


class EchoSkill(Skill[EchoInput, EchoOutput]):
    """Return the input message unchanged."""

    name = "echo"
    description = "Echo back a provided message."
    input_model = EchoInput
    output_model = EchoOutput

    async def run(self, payload: EchoInput, context: SkillContext) -> EchoOutput:
        _ = context
        return EchoOutput(message=payload.message)
