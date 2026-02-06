 # chimera
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/yohans-kasaw/chimera?utm_source=oss&utm_medium=github&utm_campaign=yohans-kasaw%2Fchimera&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)

## CI/CD & Governance
- **CI pipeline**: Lint, type-check, security checks, spec alignment checks, pre-commit hooks, and tests run on every push/PR via [ .github/workflows/main.yml](.github/workflows/main.yml).
- **Spec governance**: [scripts/spec_check.py](scripts/spec_check.py) enforces the presence of core specs, executable contracts, and a test mapping for each feature spec.
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
- `make pre-commit` — run all pre-commit hooks across the repo
- `make spec-check` — verify specs, contracts, and test coverage mapping

## Docker
- `docker build -t chimera-ci .`
- `docker run --rm chimera-ci`

## Docker Compose (Local Infra)
- `make compose-up` — start Redis, Postgres, and Weaviate
- `make compose-down` — stop and remove volumes
- Compose definition: [docker-compose.yml](docker-compose.yml)
