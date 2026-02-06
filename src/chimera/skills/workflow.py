"""Workflow orchestration for skills."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from chimera.skills.models import SkillContext, SkillRunRecord, SkillRunStatus
from chimera.skills.registry import SkillRegistry


class WorkflowStep(BaseModel):
    """A single step within a workflow.

    Attributes:
        skill_name: Skill identifier.
        input: Raw input payload for the skill.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    model_config = ConfigDict(extra="forbid")

    skill_name: str
    input: dict[str, object] = Field(default_factory=dict)


class WorkflowDefinition(BaseModel):
    """Definition of a multi-step workflow.

    Attributes:
        workflow_id: Unique workflow identifier.
        steps: Ordered list of steps.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    steps: list[WorkflowStep]


class WorkflowRunResult(BaseModel):
    """Captured outputs for a workflow execution.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    steps: list[SkillRunRecord]


class SkillWorkflowRunner:
    """Executes workflow definitions using the skill registry.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, registry: SkillRegistry) -> None:
        self._registry = registry

    async def run(self, definition: WorkflowDefinition, context: SkillContext) -> WorkflowRunResult:
        """Run the workflow sequentially.

        Args:
            definition: Workflow definition to execute.
            context: Skill execution context.

        Returns:
            WorkflowRunResult containing outputs of each step.

        Raises:
            pydantic.ValidationError: If a step payload fails input validation.
        """
        results: list[SkillRunRecord] = []
        for step in definition.steps:
            skill = self._registry.create(step.skill_name)
            payload = skill.input_model.model_validate(step.input)
            try:
                output = await skill.run(payload, context)
                results.append(
                    SkillRunRecord(
                        skill_name=step.skill_name,
                        status=SkillRunStatus.SUCCEEDED,
                        output=output.model_dump(),
                        completed_at=datetime.utcnow(),
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive capture
                results.append(
                    SkillRunRecord(
                        skill_name=step.skill_name,
                        status=SkillRunStatus.FAILED,
                        output={},
                        error=str(exc),
                        completed_at=datetime.utcnow(),
                    )
                )
                break
        return WorkflowRunResult(workflow_id=definition.workflow_id, steps=results)
