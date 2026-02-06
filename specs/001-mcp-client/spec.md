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

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reliable Tool Interactions (Priority: P1)

As an agent developer, I want my agents to connect to external MCP servers via stdio so they can discover and use tools reliably.

**Why this priority**: Core infrastructure for any external capability. Without connection and discovery, no tools can be used.

**Independent Test**: Can be fully tested by running a standalone client against a mock stdio server and verifying tool list retrieval.

**Acceptance Scenarios**:

1. **Given** a mock MCP server binary, **When** the MCPClient initiates a connection via stdio, **Then** the client should successfully handshake and receive server capabilities.
2. **Given** an established connection, **When** the client requests the tool list, **Then** it should return a list of validated tool definitions matching the server's manifest.

---

### User Story 2 - Automated Tool Execution (Priority: P2)

As an autonomous worker, I want to execute a tool on a remote MCP server so I can fetch external data needed for my task.

**Why this priority**: Enables agents to take action and retrieve specific data points, moving beyond static knowledge.

**Independent Test**: Can be tested by invoking a specific tool (e.g., 'echo' or 'fetch') on a mock server and validating the result payload.

**Acceptance Scenarios**:

1. **Given** a mock server with a 'fetch_data' tool, **When** the client executes the tool with valid parameters, **Then** it should return the correct JSON-RPC response containing the data.
2. **Given** a tool execution request, **When** the server returns a JSON-RPC error (e.g., invalid params), **Then** the client should catch and structure the error for consumer handling.

---

### User Story 3 - Perception Pipeline Integration (Priority: P3)

As a Chimera Worker, I want to use the MCPClient to augment my perception of the world so I can use tools like search or social media APIs.

**Why this priority**: Ties the low-level client into the high-level agent workflow, validating the "perception" aspect of the swarm.

**Independent Test**: A worker integration test that triggers a generic "fetch_data" tool execution and verifies the returned JSON-RPC payload flows into the worker's perception context.

**Acceptance Scenarios**:

1. **Given** a Worker assigned a data-fetching task, **When** the Worker uses the MCPClient to execute a mock `fetch_data` tool, **Then** the perception pipeline should capture the result and update the worker's visible state with the fetched data.

### Edge Cases

- **Process Crash**: How does the client handle the stdio process or mock server unexpectedly terminating?
- **Protocol Mismatch**: What happens if the server sends a malformed JSON-RPC message or uses an unsupported MCP version?
- **Stalled Connection**: How does the client handle a server that accepts the connection but never responds to the handshake?

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

1.  **Tool Discovery Speed**: Retrieve tool definitions from a local mock MCP server in under 100ms.
2.  **Execution Reliability**: Maintain 100% success rate for 'no-op' tool executions over 100 iterations.
3.  **Data Integrity**: 100% of tool results MUST pass Pydantic validation before being consumed by the Worker.
4.  **Error Mapping**: 100% of standard JSON-RPC error codes are mapped to internal exception classes.

## Assumptions

- Stdio is the primary transport method for this initial implementation.
- The mock MCP server will be implemented as a separate Python script used during testing.
- Pydantic v2 will be used for all internal and external data models.
