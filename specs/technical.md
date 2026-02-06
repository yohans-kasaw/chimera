# Technical Specifications

This document is the central index for all executable specifications used by
Project Chimera. Specs in this file are treated as the source of truth for
API contracts, data models, and external protocols.

## API Contracts (Executable)
The following contracts define the JSON inputs/outputs for the agents and
supporting services.

*   **Commerce Manager API**: [contracts/openapi.yaml](./001-agentic-commerce/contracts/openapi.yaml)
*   **Swarm Management API**: [contracts/openapi.yaml](./001-observable-mcp-swarm/contracts/openapi.yaml)
*   **Review Service API (HITL)**: [contracts/review_api.yaml](./001-prod-stability-safety/contracts/review_api.yaml)

## Database Schema (ERD)
The following Entity Relationship Diagrams and data models define the core
data structures for the system.

*   **Commerce Data Model**: [data-model.mermaid](./001-agentic-commerce/data-model.mermaid)
*   **Swarm Data Model**: [data-model.mermaid](./001-observable-mcp-swarm/data-model.mermaid)
*   **Production Stability & Safety Data Model**: [data-model.md](./001-prod-stability-safety/data-model.md)

## Protocol Definitions
*   **OpenClaw Agent Protocol**: [contracts/openclaw.yaml](./001-observable-mcp-swarm/contracts/openclaw.yaml)

## Skills & Workflow Specifications
*   **Skills + MCP Workflow Spec**: [002-skills-mcp-workflow/spec.md](./002-skills-mcp-workflow/spec.md)

## CI/CD & Governance
The CI/CD pipeline enforces spec fidelity, code quality, and security checks.

*   **CI workflow**: Lint, type-check, security checks, and tests run on every push/PR via [ .github/workflows/main.yml](../.github/workflows/main.yml)
*   **Coverage workflow**: Produces `coverage.xml` artifacts via [ .github/workflows/coverage.yml](../.github/workflows/coverage.yml)
*   **Docker parity**: Tests are executed in Docker to ensure environment consistency (see [Dockerfile](../Dockerfile))
*   **Local infra**: Development dependencies run via Docker Compose (see [docker-compose.yml](../docker-compose.yml))
*   **AI review policy**: Automated review guidance for spec alignment and security is defined in [ .coderabbit.yaml](../.coderabbit.yaml)
