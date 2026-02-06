# Implementation Plan: MCP Client Integration

**Branch**: `001-mcp-client` | **Date**: 2026-02-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mcp-client/spec.md`

## Summary

This feature implements a robust `MCPClient` based on the Model Context Protocol 1.0. It supports stdio transport, JSON-RPC 2.0 communication, tool discovery, and execution. The implementation follows a strict TDD approach, starting with failing tests and placeholder interfaces.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `mcp` (official SDK), `pydantic`, `anyio`  
**Storage**: N/A (Stateless client)  
**Testing**: `pytest`, `pytest-asyncio`, `fakeredis` (for worker integration)  
**Target Platform**: Linux/MacOS (Stdio-compatible environments)
**Project Type**: Python Library Integration  
**Performance Goals**: Tool discovery < 100ms, 100% execution reliability.  
**Constraints**: MCP 1.0 strictly, No direct API coupling per Constitution Principle I.  
**Scale/Scope**: Support for multiple concurrent MCP server connections.

## Constitution Check

- **I. MCP-First Integration**: PASSED. This feature is the foundation for following this principle.
- **V. Python Quality**: PASSED. Using `uv`, `mypy --strict`, `ruff`, and `pytest` with 90%+ coverage goal.

## Project Structure

### Documentation

```text
specs/001-mcp-client/
├── plan.md              # This file
├── checklists/
│   └── requirements.md
└── spec.md              # Feature specification
```

### Source Code

```text
src/chimera/
├── models/
│   └── mcp.py           # Pydantic models for ToolDefinition, ToolResult
├── ports/
│   └── mcp.py           # MCPClientPort interface
├── services/
│   └── mcp_client.py    # MCPClient implementation (context manager)
└── worker.py            # Updated to use MCPClient in perception loop

tests/chimera/
├── unit/
│   ├── test_mcp_models.py
│   └── test_mcp_client.py
└── integration/
    └── test_worker_mcp_perception.py
```

**Structure Decision**: Integrated into existing Chimera service architecture. Adding `ports/mcp.py` to define the boundary and `models/mcp.py` for protocol-specific data structures.

## Implementation Strategy

### TDD Phase (Current)
1. Define Pydantic models in `models/mcp.py` (placeholders).
2. Define `MCPClientPort` interface in `ports/mcp.py`.
3. Create `src/chimera/services/mcp_client.py` with empty class/methods.
4. Write failing unit tests for model validation.
5. Write failing unit tests for `MCPClient` handshake, discovery, and execution using a mock transport.
6. Write failing integration test for `Worker` perception loop using a dummy tool.

### MVP Scope
- Stdio transport only.
- Basic tool discovery and execution.
- Integration into `Worker.perceive()`.
