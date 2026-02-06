"""Sample workflow definitions.

Note: skill implementations live in `chimera.skills.skills.*` (one module per skill).
This module keeps helper functions that register built-ins and build example workflows.
"""

from __future__ import annotations

from chimera.models.types import TenantId, TraceId
from chimera.skills.models import SkillContext
from chimera.skills.registry import SkillRegistry
from chimera.skills.skills import EchoSkill, McpToolSkill, NormalizeHandleSkill
from chimera.skills.workflow import WorkflowDefinition, WorkflowStep


def register_sample_skills(registry: SkillRegistry) -> None:
    """Register built-in sample skills.

    Args:
        registry: Registry to update.

    Returns:
        None.

    Raises:
        ValueError: If a skill is registered more than once.
    """
    registry.register(EchoSkill)
    registry.register(NormalizeHandleSkill)
    registry.register(McpToolSkill)


def build_sample_workflow(
    tenant_id: TenantId, trace_id: TraceId
) -> tuple[WorkflowDefinition, SkillContext]:
    """Build a sample workflow and context.

    Args:
        tenant_id: Tenant identifier.
        trace_id: Trace identifier.

    Returns:
        Tuple of workflow definition and execution context.

    Raises:
        None.
    """
    workflow = WorkflowDefinition(
        workflow_id="sample.handle.normalize",
        steps=[
            WorkflowStep(skill_name="echo", input={"message": "Prepare handle"}),
            WorkflowStep(skill_name="normalize_handle", input={"handle": "chimera_ai"}),
        ],
    )
    context = SkillContext(tenant_id=tenant_id, trace_id=trace_id)
    return workflow, context
