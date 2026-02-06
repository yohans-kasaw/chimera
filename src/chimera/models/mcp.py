from typing import Any
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    """Placeholder for MCP Tool definition."""
    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A description of what the tool does")
    input_schema: dict[str, Any] = Field(..., description="JSON schema for the tool inputs")

class ToolResult(BaseModel):
    """Placeholder for MCP Tool execution result."""
    # justification: external tool output is dynamic by nature; safety is handled by downstream validation
    content: Any = Field(..., description="The output content from the tool")
    is_error: bool = Field(default=False, description="Whether the result represents an error")
