# Agent Skills Structure (Runtime Capability Catalog)

This document defines Chimera's **reusable runtime skills**: the small, typed capability units invoked by agents and workflows.

The catalog is **formal and discoverable**:

- Machine-readable manifest: `skills.json`
- Manifest schema: `skills.schema.json`
- Runtime implementation package: `src/chimera/skills/`
- Per-skill modules (one file per skill): `src/chimera/skills/skills/`

The manifest contracts are precise enough for an AI agent to implement skills and their invocations without ambiguity.

## Design Rules

- Every skill MUST have:
  - `purpose`
  - `input_schema` and `output_schema` (JSON Schema objects)
  - explicit `dependencies` (context + MCP requirements)
  - explicit `error_cases` (what happens; raise vs return error)
- Skills are invoked by `skill_name` and validated with Pydantic at runtime.

## Discoverability

- Human-readable: this file + `specs/002-skills-mcp-workflow/spec.md`
- Machine-readable: `skills.json`
- Runtime discovery: `SkillRegistry.list_names()` plus `register_sample_skills()`

## Skill List (Minimum Required)

The repository defines at least 3 skills:

- `echo` (deterministic checkpoint)
- `normalize_handle` (canonicalization)
- `mcp_tool` (bridge to MCP tool calls)

Their authoritative I/O contracts, error cases, and dependencies are defined in `skills.json`.

## Dependencies

Common dependencies referenced by skills:

- `SkillContext.tenant_id` (tenant boundary)
- `SkillContext.trace_id` (correlation / observability)
- `SkillContext.mcp_client` (required only for `mcp_tool`)

MCP server/tool contracts live in `mcp.json` / `specs/mcp_configuration.md`.

## Implementation Notes

- Runtime code: `src/chimera/skills/base.py`, `src/chimera/skills/registry.py`, `src/chimera/skills/workflow.py`
- Built-in skills (one file per skill): `src/chimera/skills/skills/`
- Sample workflow builders and registration helpers: `src/chimera/skills/samples.py`

## Validation

Recommended validation (local):

```bash
python scripts/validate_skills_manifest.py
```

This validates `skills.json` against `skills.schema.json` and checks for duplicates and missing required fields.
