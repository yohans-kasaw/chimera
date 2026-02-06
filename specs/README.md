# Project Chimera Specifications

This directory contains the specifications for Project Chimera, structured by feature.

## Feature Specifications

*   **[001-agentic-commerce](./001-agentic-commerce/spec.md)**: Specifications for the "Agency" phase, covering financial autonomy, wallet management, and budget governance.
*   **[001-observable-mcp-swarm](./001-observable-mcp-swarm/spec.md)**: Specifications for the core swarm architecture, observability, and tenant isolation.
*   **[001-mcp-client](./001-mcp-client/spec.md)**: Specifications for the MCP Client integration.
*   **[001-prod-stability-safety](./001-prod-stability-safety/spec.md)**: Specifications for production stability and safety mechanisms.
*   **[002-skills-mcp-workflow](./002-skills-mcp-workflow/spec.md)**: Specifications for the Skills framework, workflows, and MCP tool bindings.

## Executable Specifications

The following executable specifications are defined and linked within the feature specs:

*   **API Schemas (OpenAPI)**:
    *   [Agentic Commerce API](./001-agentic-commerce/contracts/openapi.yaml)
    *   [Swarm Brain API](./001-observable-mcp-swarm/contracts/openapi.yaml)
    *   [HITL Review Service API](./001-prod-stability-safety/contracts/review_api.yaml)
*   **Protocol Definitions**:
    *   [OpenClaw Agent Protocol](./001-observable-mcp-swarm/contracts/openclaw.yaml)
*   **Data Models (ERD)**:
    *   [Swarm Data Model (Mermaid)](./001-observable-mcp-swarm/data-model.mermaid)
    *   [Commerce Data Model (Mermaid)](./001-agentic-commerce/data-model.mermaid)
    *   [Production Stability & Safety Data Model](./001-prod-stability-safety/data-model.md)
