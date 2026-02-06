Here is my Loom Video explanation

https://drive.google.com/file/d/1akZ-9NEX8JVRHcahUTT1bbwNIusxNe9w/view?usp=sharing


 # Project Chimera: Autonomous Influencer Factory


## Project Status: The Orchestrator Phase (Day 3 Ready)

Project Chimera has transitioned from a concept to a robust "Factory" for autonomous agents. The infrastructure, specifications, and governance rails are in place to support safe, high-velocity development by an AI swarm.

### Key Achievements & Implementation Summary

*   **Spec-Driven Architecture**: Established a rigorous `specs/` hierarchy.
    *   **Master Index**: `specs/technical.md` links to executable contracts (OpenAPI) and data models (Mermaid/ERD).
    *   **Protocol**: `specs/openclaw_integration.md` defines our interface with the OpenClaw agent network.
*   **Test-Driven Development (TDD)**:
    *   Implemented a comprehensive test suite in `tests/` that defines the "empty slots" for the agents to fill.
    *   **Status**: Critical tests (Orchestrator, Judge, Commerce) are currently **FAILING** (as designed), providing clear goalposts for implementation.
*   **Skills Framework**:
    *   Built the core Skills architecture in `src/chimera/skills` using Pydantic for strict input/output contracts.
    *   Defined the Workflow engine to orchestrate deterministic agent actions.
*   **Infrastructure as Code**:
    *   **Dockerized**: Full development and testing environment defined in `Dockerfile` and `docker-compose.yml` (Postgres, Redis, Weaviate).
    *   **Governance**: CI/CD pipeline (`.github/workflows`) enforces linting, type-checking, and spec alignment on every push.
    *   **Safety**: `.coderabbit.yaml` and `.cursor/rules` configured to keep AI agents aligned with the Prime Directive: **"Spec First."**

---

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

## Skills, Workflows, and MCP
Project Chimera uses a Skills framework to bridge agent intent to executable workflows.

- Skills base + models: [src/chimera/skills](src/chimera/skills)
- Skills catalog (contracts): [skills.json](skills.json)
- Skills catalog schema: [skills.schema.json](skills.schema.json)
- Skills documentation: [specs/skills_catalog.md](specs/skills_catalog.md)
- Sample skills + workflow builder: [src/chimera/skills/samples.py](src/chimera/skills/samples.py)
- Workflow runner: [src/chimera/skills/workflow.py](src/chimera/skills/workflow.py)
- Pipeline wrapper: [src/chimera/pipelines/skills_workflow.py](src/chimera/pipelines/skills_workflow.py)
- MCP sample configuration: [mcp.sample.json](mcp.sample.json)

### MCP Configuration (Versioned)

- Primary MCP registry (committed): [mcp.json](mcp.json)
- Config schema (validation): [mcp.schema.json](mcp.schema.json)
- Documentation: [specs/mcp_configuration.md](specs/mcp_configuration.md)

The Skills workflow ties into the MCP client abstraction so tools remain externalized.
See the spec for the implementation contract and planned steps.

To enable local MCP tooling, ensure required env vars are set (see `specs/mcp_configuration.md`) and validate the config:

- `python scripts/validate_mcp_config.py`

To validate the skills contracts:

- `python scripts/validate_skills_manifest.py`

## Docker
- `docker build -t chimera-ci .`
- `docker run --rm chimera-ci`

## Docker Compose (Local Infra)
- `make compose-up` — start Redis, Postgres, and Weaviate
- `make compose-down` — stop and remove volumes
- Compose definition: [docker-compose.yml](docker-compose.yml)
