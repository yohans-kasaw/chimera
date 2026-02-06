# MCP Configuration (External Tools & Services)

This document defines the **formal, versioned configuration mechanism** for all external agent tools and services used by Chimera via **MCP (Model Context Protocol)**.

The authoritative, committed configuration is:

- `mcp.json` (server registry, connection details, and tool schemas)
- `mcp.schema.json` (JSON Schema for validating `mcp.json`)

The goal is to make the MCP layer **autonomous-agent friendly**: an AI agent can read these files and unambiguously connect to required external services.

## Files

- `mcp.json`
  - Versioned config (`config_version`) and MCP protocol target (`mcp_version`)
  - Declares each MCP server:
    - Connection details (stdio/http)
    - Authentication method (no secrets, only env var names)
    - Tool definitions, including `input_schema` and `output_schema`
    - Upstream dependencies (e.g., Weaviate, Twitter)
- `mcp.schema.json`
  - JSON Schema (draft 2020-12) for `mcp.json`
  - Enables CI and editors to validate structure and reduce ambiguity

## Design Rules

- **No secrets in git**: `mcp.json` only references environment variable names (e.g., `CDP_API_KEY_PRIVATE_KEY`), never literal tokens.
- **Self-documenting tools**: each tool entry MUST include a name, description, and both input/output JSON schemas.
- **Explicit transports**:
  - `transport: "stdio"` uses `stdio.command` + `stdio.args`
  - `transport: "http"` uses `http.url` (+ optional headers)
- **Auth is explicit**: every server MUST declare `auth.type` and list required vs optional credentials.
- **Docs are linkable**: every server MUST set `documentation_url` (typically this file or a relevant feature spec).

## Servers (Required)

Chimera currently declares four MCP servers in `mcp.json`:

- `chimera-memory`
  - Purpose: long-term memory and RAG functions
  - Upstream: Weaviate (`WEAVIATE_URL`, optional `WEAVIATE_API_KEY`)
  - Tools: `remember_fact`, `recall_context`, `search_knowledge_base`
- `chimera-commerce`
  - Purpose: wallet operations and transaction status
  - Upstream: Coinbase CDP AgentKit SDK (credentials via env)
  - Tools: `get_wallet_balance`, `transfer_asset`, `get_transaction_status`
- `chimera-social`
  - Purpose: social posting and feed reads
  - Upstreams: MoltBook + Twitter/X (credentials optional, per-platform)
  - Tools: `post_content`, `reply_to_post`, `fetch_feed`
- `chimera-dev-tools`
  - Purpose: sandboxed developer operations
  - Tools: `read_file`, `git_status`, `run_test`

## Environment Variables

All variables referenced by `mcp.json` are injected at runtime.

- Memory:
  - `WEAVIATE_URL` (required)
  - `WEAVIATE_API_KEY` (optional)
- Commerce:
  - `CDP_API_KEY_NAME` (required)
  - `CDP_API_KEY_PRIVATE_KEY` (required)
- Social:
  - `MOLTBOOK_API_KEY` (optional)
  - `TWITTER_BEARER_TOKEN` (optional)

## Validation

Recommended validation (local):

```bash
python scripts/validate_mcp_config.py
```

This validates `mcp.json` against `mcp.schema.json` and checks for common configuration mistakes.

## How an Agent Uses This

An autonomous agent can:

1. Read `mcp.json`.
2. For each server needed by a workflow:
   - Determine transport (`stdio` vs `http`).
   - Verify `auth.required` env vars exist.
   - Use `tools[*].input_schema` to construct valid tool calls.
3. Enforce local safety constraints (never log secrets; follow Judge/HITL requirements).
