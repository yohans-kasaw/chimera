from typing import Protocol, runtime_checkable

from chimera.models.result import Result
from chimera.models.task import Task


@runtime_checkable
class LLMPort(Protocol):
    """Port for LLM backend interactions.

    Used by workers to process tasks.
    """

    async def generate_result(self, task: Task) -> Result:
        """Process a task through the LLM and produce a result.

        Args:
            task: The task to be processed.

        Returns:
            A validated Result model.
        """
        ...
