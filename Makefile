SHELL := /bin/bash

.PHONY: setup lint format typecheck test security spec-check pre-commit ci compose-up compose-down

setup:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

test:
	uv run pytest

security:
	uv run ruff check . --select S

pre-commit:
	uv run pre-commit run --all-files

spec-check:
	uv run python scripts/spec_check.py

ci: lint typecheck security spec-check test pre-commit

compose-up:
	docker compose up -d

compose-down:
	docker compose down -v
