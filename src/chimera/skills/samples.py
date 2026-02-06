"""Sample skills and workflow definitions."""

from __future__ import annotations

from pydantic import BaseModel, Field

from chimera.models.types import TenantId, TraceId
from chimera.skills.base import Skill
from chimera.skills.models import SkillContext
from chimera.skills.registry import SkillRegistry
from chimera.skills.workflow import WorkflowDefinition, WorkflowStep


class EchoInput(BaseModel):
    """Input payload for the echo skill.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    message: str = Field(..., description="Message to echo.")


class EchoOutput(BaseModel):
    """Output payload for the echo skill.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    message: str = Field(..., description="Echoed message.")


class EchoSkill(Skill[EchoInput, EchoOutput]):
    """Return the input message unchanged.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    name = "echo"
    description = "Echo back a provided message."
    input_model = EchoInput
    output_model = EchoOutput

    async def run(self, payload: EchoInput, context: SkillContext) -> EchoOutput:
        """Return the payload unchanged.

        Args:
            payload: Echo input payload.
            context: Execution context (unused).

        Returns:
            EchoOutput with the same message.

        Raises:
            None.
        """
        _ = context
        return EchoOutput(message=payload.message)


class NormalizeHandleInput(BaseModel):
    """Input payload for handle normalization.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    handle: str = Field(..., description="Social handle to normalize.")


class NormalizeHandleOutput(BaseModel):
    """Normalized social handle output.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    handle: str = Field(..., description="Normalized handle.")


class NormalizeHandleSkill(Skill[NormalizeHandleInput, NormalizeHandleOutput]):
    """Normalize social handles into a canonical format.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    name = "normalize_handle"
    description = "Normalize a social handle into a canonical format."
    input_model = NormalizeHandleInput
    output_model = NormalizeHandleOutput

    async def run(
        self, payload: NormalizeHandleInput, context: SkillContext
    ) -> NormalizeHandleOutput:
        """Normalize leading @ and whitespace.

        Args:
            payload: Normalization payload.
            context: Execution context (unused).

        Returns:
            Normalized handle output.

        Raises:
            None.
        """
        _ = context
        normalized = payload.handle.strip()
        if not normalized.startswith("@"):  # simple canonicalization
            normalized = f"@{normalized}"
        return NormalizeHandleOutput(handle=normalized)


class McpToolInput(BaseModel):
    """Input payload for MCP tool execution.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    tool_name: str = Field(..., description="Name of the MCP tool to invoke.")
    # justification: MCP tool arguments are dynamic JSON payloads.
    arguments: dict[str, object] = Field(default_factory=dict)


class McpToolOutput(BaseModel):
    """Output payload from an MCP tool invocation.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    # justification: MCP tool outputs are dynamic JSON payloads.
    response: dict[str, object] = Field(default_factory=dict)


class McpToolSkill(Skill[McpToolInput, McpToolOutput]):
    """Invoke an MCP tool through the active MCP client.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    name = "mcp_tool"
    description = "Invoke an MCP tool using the active MCP client."
    input_model = McpToolInput
    output_model = McpToolOutput

    async def run(self, payload: McpToolInput, context: SkillContext) -> McpToolOutput:
        """Call a tool using the MCP client.

        Args:
            payload: MCP tool payload.
            context: Execution context containing an MCP client.

        Returns:
            MCP tool output.

        Raises:
            RuntimeError: If no MCP client is configured.
        """
        if context.mcp_client is None:
            raise RuntimeError("MCP client is required for mcp_tool skill")
        result = await context.mcp_client.call_tool(payload.tool_name, payload.arguments)
        return McpToolOutput(response={"content": result.content, "is_error": result.is_error})


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


def build_sample_workflow(tenant_id: TenantId, trace_id: TraceId) -> tuple[WorkflowDefinition, SkillContext]:
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
