from abc import abstractmethod
from typing import Any, List
from contextlib import AbstractAsyncContextManager
from chimera.models.mcp import ToolDefinition, ToolResult

class MCPClientPort(AbstractAsyncContextManager["MCPClientPort"]):
    """Port defining the interface for a Model Context Protocol client."""

    @abstractmethod
    async def list_tools(self) -> List[ToolDefinition]:
        """List all available tools from the connected MCP server.

        Returns:
            List[ToolDefinition]: The list of tools discovered.
        
        Raises:
            RuntimeError: If the client is not connected or discovery fails.
        """
        pass

    @abstractmethod
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Call a specific tool on the MCP server.

        Args:
            name: The name of the tool to execute.
            arguments: Parameters for the tool.

        Returns:
            ToolResult: The outcome of the tool execution.
            
        Raises:
            ValueError: If the tool name is unknown.
            RuntimeError: If execution fails at the transport level.
        """
        pass
