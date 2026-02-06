"""Base classes for the Chimera skill framework."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar

from pydantic import BaseModel

from chimera.skills.models import SkillContext

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class Skill(Generic[InputT, OutputT], ABC):
    """Base class for an executable skill.

    Skills are the smallest reusable capability units that the planner can invoke.
    Each skill validates input/output using Pydantic models and executes within a
    shared execution context.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    name: ClassVar[str]
    description: ClassVar[str]
    input_model: ClassVar[type[InputT]]
    output_model: ClassVar[type[OutputT]]

    @abstractmethod
    async def run(self, payload: InputT, context: SkillContext) -> OutputT:
        """Run the skill using validated payload and execution context.

        Args:
            payload: Validated input data.
            context: Execution context for MCP access and tracing.

        Returns:
            The validated output model.
        """
        raise NotImplementedError
