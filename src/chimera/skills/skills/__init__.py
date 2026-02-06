"""Built-in skills.

Each skill is defined in its own module to keep contracts and dependencies
explicit and easy to discover.
"""

from chimera.skills.skills.echo import EchoInput, EchoOutput, EchoSkill
from chimera.skills.skills.mcp_tool import McpToolInput, McpToolOutput, McpToolSkill
from chimera.skills.skills.normalize_handle import (
    NormalizeHandleInput,
    NormalizeHandleOutput,
    NormalizeHandleSkill,
)

__all__ = [
    "EchoInput",
    "EchoOutput",
    "EchoSkill",
    "NormalizeHandleInput",
    "NormalizeHandleOutput",
    "NormalizeHandleSkill",
    "McpToolInput",
    "McpToolOutput",
    "McpToolSkill",
]
