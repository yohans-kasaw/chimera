import pytest
from pydantic import ValidationError
from chimera.models.mcp import ToolDefinition, ToolResult

def test_tool_definition_validation() -> None:
    """Test that ToolDefinition validates its fields."""
    # Valid model
    tool = ToolDefinition(
        name="test_tool",
        description="A test tool",
        input_schema={"type": "object", "properties": {"foo": {"type": "string"}}}
    )
    assert tool.name == "test_tool"
    
    # Missing fields
    with pytest.raises(ValidationError):
        ToolDefinition(name="incomplete") # type: ignore

def test_tool_result_validation() -> None:
    """Test that ToolResult validates its fields."""
    # Valid success result
    res = ToolResult(content={"data": "hello"}, is_error=False)
    assert res.content == {"data": "hello"}
    assert not res.is_error
    
    # Valid error result
    err = ToolResult(content="something went wrong", is_error=True)
    assert err.is_error
    assert err.content == "something went wrong"
