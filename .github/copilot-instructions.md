# Copilot Instructions - Project Chimera (Spec-First)

These instructions tailor Copilot to Project Chimera.

Required directives are explicitly included:

- Project context
- Spec-first enforcement
- Traceability

Authoritative agent manual: `AGENT.md`.

---

## Project Context

Project Chimera is an autonomous agent platform built from executable specs.

Source of truth:

- Specs: `specs/`
- MCP registry: `mcp.json` (docs: `specs/mcp_configuration.md`)
- Skills manifest: `skills.json` (docs: `specs/skills_catalog.md`)

## Spec-First Enforcement (Mandatory)

Before writing code:

1. Read `specs/technical.md`
2. Read the relevant `specs/<feature>/spec.md`
3. Ensure acceptance criteria + security requirements exist; if missing, update specs first.

## Traceability (Mandatory)

In code reviews, commits, PR descriptions, and explanations, always cite:

- `Spec:` `specs/<...>`
- `AC:` `AC-###` and/or `FR:` `FR-###`

Tests should reference the relevant `AC-###` in docstrings.

## Mandatory Policies

* **Dependency Management**: Use **uv** exclusively.
* Never use `pip`, `poetry`, or `conda`.
* Add packages via `uv add <package>` and dev-dependencies via `uv add --dev <package>`.
* The `uv.lock` file must be committed and kept in sync with `pyproject.toml`.


* **Typing**: Use the `typing` module for all interfaces.
* Run **mypy** in `--strict` mode.
* **No `Any` is permitted** without a specific `justification:` comment (see policy below).


* **Linting & Formatting**: Use **Ruff**.
* Configure `ruff` to handle both linting (including import sorting) and formatting.
* Set `target-version` to match the project's Python version in `pyproject.toml`.


* **Data Validation**: Use **Pydantic v2** for all schema definitions and environment configurations. Prefer `Annotated` types for metadata and reuse.
* **Testing**: Use **pytest**.
* Async tests require `pytest-asyncio`.
* Coverage must be maintained at **90%+**.
* Tests must reside in `tests/` and mirror the `src/` directory structure.


* **Documentation**: Use clear docstrings for public APIs. Prefer short, accurate docstrings over boilerplate.

---

## ✍️ The "No-Stray-Any" Policy

If a type cannot be narrowed and `Any` is required, it **must** be documented immediately.

> **Rule:** Any usage of `Any` without a `justification:` token will trigger a CI failure.

```python
from typing import Any

# justification: external API response is dynamic; type safety handled by Pydantic model_validate
raw_data: Any = external_api.get_unstructured_json()

```

---

## PR Checklist

| Task | Command |
| --- | --- |
| **Sync Environment** | `uv sync` |
| **Run Tests** | `uv run pytest` |
| **Strict Type Check** | `uv run mypy .` |
| **Lint & Fix** | `uv run ruff check . --fix` |
| **Format Code** | `uv run ruff format .` |
| **Verify Coverage** | `uv run pytest --cov=src` |

---

## 🔧 CI/CD Standards (GitHub Actions)

When setting up CI, use the official `astral-sh/setup-uv` action. Ensure the environment is reproducible using the `--frozen` flag.

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: astral-sh/setup-uv@v5
    with:
      enable-cache: true
  - name: Install dependencies
    run: uv sync --frozen
  - name: Lint and Type Check
    run: |
      uv run ruff check .
      uv run mypy .
  - name: Run Tests
    run: uv run pytest --cov --cov-report=xml

```

---

## Testing & Async Patterns

* **Mocking**: Use `pytest-mock` (mocker fixture) instead of standard `unittest.mock` for cleaner syntax.
* **Async**: Annotate async tests with `@pytest.mark.asyncio`.
* **Pydantic Integration**: Use `model_validate` within tests to ensure mock data matches production schemas.

```python
import pytest
from pydantic import ValidationError

@pytest.mark.asyncio
async def test_item_creation(mock_db):
    # Ensure Pydantic validation is part of the test flow
    with pytest.raises(ValidationError):
        Item(name="Incomplete Data")

```

---

## Technical Conventions

* **Python Version**: Specify in `pyproject.toml` using `requires-python = ">=3.12"`.
* **Project Structure**: Prefer a `src/` layout to ensure tests run against the installed package.
* **Scripts**: Define frequently used tasks in the `[tool.uv.scripts]` section of `pyproject.toml` for shortcuts like `uv run dev`.

## Structured State Blocks (Preferred)

For non-trivial tasks, format your response using the STATE block described in `AGENT.md`.

## Iterative Refinement

Keep these instructions aligned with repo evolution (new manifests, new governance scripts, new specs). When a rule changes, update `AGENT.md` first, then sync this file.
