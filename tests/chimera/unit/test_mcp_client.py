import pytest
from unittest.mock import AsyncMock, patch
from chimera.services.mcp_client import MCPClient
from chimera.models.mcp import ToolDefinition, ToolResult

@pytest.mark.asyncio
async def test_mcp_client_context_manager() -> None:
    """Test that the client can be used as an async context manager."""
    async with MCPClient(command="mock-server", args=[]) as client:
        assert isinstance(client, MCPClient)

@pytest.mark.asyncio
async def test_mcp_client_list_tools() -> None:
    """Test that the client can list tools from the server."""
    async with MCPClient(command="mock-server", args=[]) as client:
        tools = await client.list_tools()
        assert len(tools) > 0
        assert isinstance(tools[0], ToolDefinition)

@pytest.mark.asyncio
async def test_mcp_client_call_tool_success() -> None:
    """Test that the client can call a tool successfully."""
    async with MCPClient(command="mock-server", args=[]) as client:
        result = await client.call_tool("echo", {"msg": "hello"})
        assert isinstance(result, ToolResult)
        assert result.content == {"msg": "hello"}
        assert not result.is_error

@pytest.mark.asyncio
async def test_mcp_client_call_tool_error() -> None:
    """Test that the client handles tool errors correctly."""
    async with MCPClient(command="mock-server", args=[]) as client:
        result = await client.call_tool("error_tool", {})
        assert result.is_error
        assert "error" in str(result.content).lower()

@pytest.mark.asyncio
async def test_mcp_client_handshake_failure() -> None:
    """Test that the client handles handshake failure."""
    raise NotImplementedError("MCP handshake failure check is not fully implemented per requirement")
    # This might require complex mocking of the transport
    pass # Placeholder for more specific tests if needed
