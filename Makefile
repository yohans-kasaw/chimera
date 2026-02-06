SHELL := /bin/bash

.PHONY: setup lint format typecheck test security ci compose-up compose-down

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

ci: lint typecheck security test

compose-up:
	docker compose up -d

compose-down:
	docker compose down -v
