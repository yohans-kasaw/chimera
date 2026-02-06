 # chimera

## CI/CD & Governance
- **CI pipeline**: Lint, type-check, security checks, and tests run on every push/PR via [ .github/workflows/main.yml](.github/workflows/main.yml).
- **Dockerized tests**: CI builds and runs the test suite inside Docker to prevent "works on my machine" drift.
- **Coverage**: A dedicated workflow generates `coverage.xml` artifacts in [ .github/workflows/coverage.yml](.github/workflows/coverage.yml).
- **AI review policy**: [ .coderabbit.yaml](.coderabbit.yaml) enforces spec alignment, security checks, and strict typing.

## Local Commands (uv + Make)
- `make setup` — sync dependencies with uv
- `make lint` — Ruff lint
- `make format` — Ruff format
- `make typecheck` — mypy strict
- `make security` — Ruff security (Bandit rules)
- `make test` — pytest

## Docker
- `docker build -t chimera-ci .`
- `docker run --rm chimera-ci`

## Docker Compose (Local Infra)
- `make compose-up` — start Redis, Postgres, and Weaviate
- `make compose-down` — stop and remove volumes
- Compose definition: [docker-compose.yml](docker-compose.yml)
