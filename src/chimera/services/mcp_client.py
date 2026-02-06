from typing import Any, List, Optional, Type
from types import TracebackType
from chimera.ports.mcp import MCPClientPort
from chimera.models.mcp import ToolDefinition, ToolResult

class MCPClient(MCPClientPort):
    """Implementation of MCP Client using stdio transport.
    
    This client manages the lifecycle of a connection to an MCP server
    running as a local process.
    """

    def __init__(self, command: str, args: List[str]):
        """Initialize the client.
        
        Args:
            command: The executable to run.
            args: Arguments for the executable.
        """
        self.command = command
        self.args = args

    async def __aenter__(self) -> "MCPClient":
        """Start the stdio process and perform handshake.
        
        Raises:
            NotImplementedError: Always, during TDD phase.
        """
        raise NotImplementedError("MCPClient.__aenter__ is not implemented")

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Terminate the stdio process and cleanup resources.
        
        Raises:
            NotImplementedError: Always, during TDD phase.
        """
        raise NotImplementedError("MCPClient.__aexit__ is not implemented")

    async def list_tools(self) -> List[ToolDefinition]:
        """Discovery tools from the MCP server.
        
        Raises:
            NotImplementedError: Always, during TDD phase.
        """
        raise NotImplementedError("MCPClient.list_tools is not implemented")

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Call a tool on the MCP server.
        
        Raises:
            NotImplementedError: Always, during TDD phase.
        """
        raise NotImplementedError("MCPClient.call_tool is not implemented")
