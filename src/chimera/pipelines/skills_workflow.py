"""Pipeline for executing skill workflows."""

from __future__ import annotations

from chimera.skills.models import SkillContext
from chimera.skills.registry import SkillRegistry
from chimera.skills.samples import register_sample_skills
from chimera.skills.workflow import SkillWorkflowRunner, WorkflowDefinition, WorkflowRunResult


class SkillsWorkflowPipeline:
    """High-level pipeline that executes skill workflows.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, registry: SkillRegistry | None = None) -> None:
        self._registry = registry or SkillRegistry()
        register_sample_skills(self._registry)
        self._runner = SkillWorkflowRunner(self._registry)

    async def run(self, definition: WorkflowDefinition, context: SkillContext) -> WorkflowRunResult:
        """Run the workflow definition using the registered skills.

        Args:
            definition: Workflow definition to execute.
            context: Execution context.

        Returns:
            Workflow run results.

        Raises:
            pydantic.ValidationError: If a step payload fails input validation.
        """
        return await self._runner.run(definition, context)
