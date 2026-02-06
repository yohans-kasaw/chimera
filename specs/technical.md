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

## Database Architecture & Schema
The Master Data Specification defines the unified architecture across PostgreSQL, Redis, and Weaviate.

*   **Master Data Spec**: [data-architecture.md](./data-architecture.md)
*   **Backend Architecture & Agent Framework**: [backend-architecture.md](./backend-architecture.md)
*   **Frontend Architecture & Design System**: [frontend-architecture.md](./frontend-architecture.md)

### Domain-Specific Models (Reference)
The following diagrams provide focused views on specific domains, but are subordinate to the Master Data Spec.

*   **Commerce Data Model**: [data-model.mermaid](./001-agentic-commerce/data-model.mermaid)
*   **Swarm Data Model**: [data-model.mermaid](./001-observable-mcp-swarm/data-model.mermaid)
*   **Production Stability & Safety Data Model**: [data-model.md](./001-prod-stability-safety/data-model.md)

## Protocol Definitions
*   **OpenClaw Agent Protocol**: [contracts/openclaw.yaml](./001-observable-mcp-swarm/contracts/openclaw.yaml)

## MCP Configuration (External Tools)

Chimera's external tool/services layer is declared as a **versioned MCP server registry**.

*   **MCP Configuration**: [mcp_configuration.md](./mcp_configuration.md)
*   **Registry (JSON)**: [`mcp.json`](../mcp.json)
*   **Registry Schema**: [`mcp.schema.json`](../mcp.schema.json)

## Skills & Workflow Specifications
*   **Skills + MCP Workflow Spec**: [002-skills-mcp-workflow/spec.md](./002-skills-mcp-workflow/spec.md)

## Agent Skills Catalog (Runtime)

Chimera defines a formal, discoverable skills structure:

*   **Skills Catalog**: [skills_catalog.md](./skills_catalog.md)
*   **Skills Manifest (JSON)**: [`skills.json`](../skills.json)
*   **Skills Manifest Schema**: [`skills.schema.json`](../skills.schema.json)

## CI/CD & Governance
The CI/CD pipeline enforces spec fidelity, code quality, and security checks.

*   **CI workflow**: Lint, type-check, security checks, and tests run on every push/PR via [ .github/workflows/main.yml](../.github/workflows/main.yml)
*   **Coverage workflow**: Produces `coverage.xml` artifacts via [ .github/workflows/coverage.yml](../.github/workflows/coverage.yml)
*   **Docker parity**: Tests are executed in Docker to ensure environment consistency (see [Dockerfile](../Dockerfile))
*   **Local infra**: Development dependencies run via Docker Compose (see [docker-compose.yml](../docker-compose.yml))
*   **AI review policy**: Automated review guidance for spec alignment and security is defined in [ .coderabbit.yaml](../.coderabbit.yaml)

## Security Architecture & Compliance (Rubric: Pro)
This section defines the mandatory security layer for all Chimera agents.

### Authentication & Authorization Strategy
*   **Strategy**: Federated OAuth2 with JWT (JSON Web Tokens).
*   **Implementation**:
    *   **Service-to-Service**: Mutual TLS (mTLS) or Signed JWTs via `internal_keys`.
    *   **User-to-Agent**: Bearer Tokens (OAuth2) validated against the Identity Provider (IdP).
*   **Enforcement**: All API Contracts (see Section 1) must define `securitySchemes` in their OpenAPI specs.
    *   *Constraint*: No endpoint may be `public` without explicit justification in `specs/functional.md`.

### Secrets Management
*   **Vault**: All high-entropy secrets (Private Keys, API Tokens) must be stored in the **CommerceManager Vault** (HashiCorp Vault compatible) or injected via **Environment Variables** (`os.getenv`).
*   **Forbidden**: Hardcoding secrets in source code is strictly prohibited and detected by `bandit`.

### Rate Limiting & Resource Containment
*   **Per-Endpoint Limits**: All APIs must enforce strict rate limits (Token Bucket algorithm).
    *   *Default*: 60 requests/minute per Tenant.
    *   *Commerce*: 10 transactions/minute.
*   **Agent Containment**:
    *   **Execution Time**: Max 60s per reasoning loop.
    *   **Token Budget**: Max 8k input tokens / 2k output tokens per turn.
    *   **Recursion Limit**: Max depth of 5 sub-tasks.

### Content Safety & Moderation
*   **The Judge**: A mandatory "Safety Layer" (see `specs/001-prod-stability-safety`) intercepts all Agent outputs.
*   **Pipeline**:
    1.  **Input Guard**: Regex/Keyword filter for PII (SSN, Email) sanitization.
    2.  **Logic Core**: LLM generation.
    3.  **Output Guard**: Semantic evaluation (Confidence < 0.7 -> REJECT).
*   **Escalation**: Any content flagged as "Harmful" triggers a `HUMAN_INTERVENTION_REQUIRED` event.

### Sensitive Data Handling
*   **PII Policy**: No PII (Personally Identifiable Information) may be stored in `Weaviate` (Long-term memory).
*   **Token Redaction**: Logs must mask all tokens (e.g., `sk-****`).
