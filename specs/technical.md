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
