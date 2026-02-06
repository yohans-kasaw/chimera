# 🛠️ Copilot Instructions — Strict Python Standards

**Purpose:** Enforce a professional, strongly-typed, and test-driven codebase using **uv** as the primary project manager, alongside **Ruff**, **Mypy**, **Pytest**, and **Pydantic v2**.

---

## ✅ Mandatory Policies

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


* **Documentation**: Use **Google-style docstrings**. Every public-facing class, method, and function must be documented with `Args`, `Returns`, and `Raises` sections.

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

## ✅ PR Checklist

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

## 🧪 Testing & Async Patterns

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

## 📎 Technical Conventions

* **Python Version**: Specify in `pyproject.toml` using `requires-python = ">=3.12"`.
* **Project Structure**: Prefer a `src/` layout to ensure tests run against the installed package.
* **Scripts**: Define frequently used tasks in the `[tool.uv.scripts]` section of `pyproject.toml` for shortcuts like `uv run dev`.



