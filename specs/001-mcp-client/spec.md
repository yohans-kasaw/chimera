# Feature Specification: MCP Client Integration

**Feature Branch**: `001-mcp-client`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "Develop an MCPClient test suite that verifies connection to a local stdio process and correct handling of JSON-RPC capabilities. Write tests for tool discovery and execution, ensuring the client properly formats requests and handles errors from a mock MCP server. Implement the MCPClient to pass these tests, then integrate it into the Worker service. Create a specific test case where a Worker must use a tool to fetch data, validating the 'perception' pipeline. This ensures the agents can reliably interact with external resources like Twitter or Weaviate."

## Clarifications

### Session 2026-02-06
- Q: Which MCP version should be supported? → A: MCP 1.0 (Latest)
- Q: What type of data-fetching tool should be used for the perception test case? → A: Generic "Fetch" Mock
- Q: How should the client maintain its connection lifecycle? → A: Context Manager (async with)

## Acceptance Criteria (Gherkin)

### AC-001: Tool Discovery (Happy Path)
*   **Trace**: [FR-003], [FR-008]
*   **Scenario**: Retrieve Capabilities
    *   **Given** a running MCP 1.0 compliant server
    *   **When** the MCPClient connects via stdio
    *   **Then** the handshake completes successfully
    *   **And** `list_tools()` returns at least 1 validated `ToolDefinition`

### AC-002: Tool Execution (Happy Path)
*   **Trace**: [FR-004]
*   **Scenario**: Execute Fetch Tool
    *   **Given** a server providing tool `fetch_data`
    *   **When** I call `execute_tool("fetch_data", {"query": "test"})`
    *   **Then** the result is a `ToolResult` object
    *   **And** `result.is_error` is False
    *   **And** `result.content` matches the mock server response

### AC-003: Error Handling (Failure Mode)
*   **Trace**: [FR-005]
*   **Scenario**: Execute Unknown Tool
    *   **Given** a connected client
    *   **When** I call `execute_tool("missing_tool", {})`
    *   **Then** a `ToolNotFoundError` is raised
    *   **And** the error message contains "missing_tool"

### AC-004: Connection Lifecycle (Edge Case)
*   **Trace**: [FR-009]
*   **Scenario**: Server Crash
    *   **Given** an active MCP connection
    *   **When** the server process terminates unexpectedly
    *   **Then** the next client call raises `ConnectionError`
    *   **And** the context manager cleans up resources (pipes closed)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support MCP connection via standard input/output (stdio) pipelines.
- **FR-002**: System MUST implement JSON-RPC 2.0 protocol for all MCP message exchange patterns.
- **FR-003**: System MUST provide an interface for discovering available tools from a connected MCP server.
- **FR-004**: System MUST allow execution of discovered tools with arbitrary parameters passed as JSON.
- **FR-005**: System MUST handle and normalize MCP server errors (e.g., tool not found, execution failure, transport error).
- **FR-006**: Worker service MUST integrate the MCPClient to enable tool-based capabilities in its perception loop.
- **FR-007**: System MUST include a comprehensive test suite with a mock MCP server implementation for verification.
- **FR-008**: System MUST support MCP 1.0.
- **FR-009**: MCPClient MUST manage connection lifecycle using an asynchronous context manager to ensure resource cleanup.

### Key Entities *(include if feature involves data)*

- **MCPClient**: The core component managing the life-cycle of the connection and protocol logic.
- **ToolDefinition**: Pydantic model representing a tool's name, description, and input schema.
- **MCPConnection**: State-managed object handling the stdio streams and process management.
- **ToolResult**: Data structure containing the outcome of a tool execution (success or failure).

## Success Criteria
*(Superseded by Acceptance Criteria above)*

## Assumptions

- Stdio is the primary transport method for this initial implementation.
- The mock MCP server will be implemented as a separate Python script used during testing.
- Pydantic v2 will be used for all internal and external data models.

## Security & Compliance *(mandatory)*
This feature adheres to the [Master Security Architecture](../technical.md#7-security-architecture--compliance-rubric-pro).

*   **Authentication**: Uses standard OAuth2/JWT flow via the CommerceManager.
*   **Secrets Management**: All credentials managed via Vault/Env.
*   **Rate Limiting**: Enforces standard 60 req/min limit.
*   **Content Safety**: Subject to standard Moderation/Judge pipeline.
*   **Containment**: Strict Resource Limits apply (Execution Time, Token Budget).
