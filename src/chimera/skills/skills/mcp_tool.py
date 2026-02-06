"""MCP tool bridge skill.

Provides a consistent skill surface for invoking arbitrary MCP tools.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from chimera.skills.base import Skill
from chimera.skills.models import SkillContext


class McpToolInput(BaseModel):
    """Input payload for MCP tool execution."""

    tool_name: str = Field(..., description="Name of the MCP tool to invoke.")
    # justification: MCP tool arguments are dynamic JSON payloads.
    arguments: dict[str, object] = Field(default_factory=dict)


class McpToolOutput(BaseModel):
    """Output payload from an MCP tool invocation."""

    # justification: MCP tool outputs are dynamic JSON payloads.
    response: dict[str, object] = Field(default_factory=dict)


class McpToolSkill(Skill[McpToolInput, McpToolOutput]):
    """Invoke an MCP tool through the active MCP client."""

    name = "mcp_tool"
    description = "Invoke an MCP tool using the active MCP client."
    input_model = McpToolInput
    output_model = McpToolOutput

    async def run(self, payload: McpToolInput, context: SkillContext) -> McpToolOutput:
        if context.mcp_client is None:
            raise RuntimeError("MCP client is required for mcp_tool skill")

        result = await context.mcp_client.call_tool(payload.tool_name, payload.arguments)
        return McpToolOutput(response={"content": result.content, "is_error": result.is_error})
