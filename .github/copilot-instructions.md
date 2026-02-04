# Copilot Guidelines for Project Chimera

These rules govern the development of Project Chimera. All generated code must adhere to these standards.

## 1. Environment & Tooling
- **Manager**: Use `uv` for dependency management and running scripts.
- **Python Version**: 3.12+
- **Linter/Formatter**: `ruff`. Run `uv run ruff check .` and `uv run ruff format .` before committing.
- **Testing**: `pytest` with `pytest-asyncio`. Run `uv run pytest`.

## 2. Test-Driven Development (TDD)
**Strict Rule**: Tests MUST be written *before* the implementation code.
1.  **Red**: Write a failing test in `tests/`.
2.  **Green**: Write the minimal code in `src/` to pass the test.
3.  **Refactor**: Improve the code while keeping tests passing.

**Testing Standards**:
- Use `pytest` fixtures for setup (especially for async clients like Weaviate/Redis).
- Mock external API calls (MCP, Web Requests) using `unittest.mock` or `respx`.
- Aim for >90% code coverage.
- All tests for agents must be async.

## 3. Coding Style & Quality
- **Type Hints**: Strict type hints are MANDATORY. Use `mypy` to verify.
- **Pydantic**: Use `pydantic.BaseModel` for all data structures, request/response schemas, and configuration objects.
- **Docstrings**: Use Google-style docstrings for all functions and classes.
- **Async/Await**: Prefer `async/await` for all I/O bound operations (DB, API, MCP).
- **Error Handling**: Use custom exception classes inheriting from a base `ChimeraError`.

## 4. Architecture Standards
- **Global Imports**: Avoid circular imports. Use `if TYPE_CHECKING:` to import types purely for annotation.
- **Dependency Injection**: Pass dependencies (like database clients) into functions/classes rather than instantiating them globally.
- **Configuration**: Use `pydantic-settings` to load config from `.env` files.

## 5. Agentic Specifics
- **MCP**: When implementing MCP servers or clients, follow the official `@modelcontextprotocol/sdk` patterns.
- **FastRender Pattern**: Respect the `Planner` -> `Worker` -> `Judge` flow.
- **Safety**: Never hardcode credentials. Use environment variables.

## 6. Commit Messages
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
