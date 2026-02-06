# Project Chimera Agent Rules

This file is the primary rules + operating manual for AI agents working in this repository.

## 1) Project Context (Non-Negotiable)

Project Chimera is an autonomous agent platform (“influencer factory”) built **spec-first**.

Source of truth:

- Specs: `specs/` (feature specs, architecture, executable contracts)
- Tooling layer: `mcp.json` + `specs/mcp_configuration.md`
- Skills layer: `skills.json` + `specs/skills_catalog.md`

## 2) Prime Directive: Spec-First Enforcement

You MUST read the relevant specs before proposing or writing code.

Minimum spec reads for any implementation work:

- `specs/technical.md`
- The relevant feature spec under `specs/00*-*/spec.md`

If a request is ambiguous or contradicts specs:

- Do not guess.
- Do not “make it up”.
- Do the non-blocked work (discovery, outlining options), then ask ONE targeted question.

## 3) Traceability (Always)

Every meaningful change MUST be traceable to a spec and/or acceptance criteria.

Rules:

- In your response, cite the exact spec file paths you’re implementing.
- When adding tests, include the spec acceptance criteria ID(s) in the test docstring.
- When updating contracts/manifests, keep them versioned and validated.

Trace tokens to use:

- `Spec:` `specs/<...>`
- `AC:` `AC-###`
- `FR:` `FR-###`

## 4) Structured State Block (Required Output Format)

For any non-trivial task (more than a one-liner), include a block like this in your response:

```text
STATE
Context: <1 sentence>
Spec: <paths>
Plan: <1-5 steps>
Changes: <files touched>
Verification: <commands run + result>
Open Questions: <only if blocked>
```

## 5) Coding Standards (Chimera-Specific)

- Python: 3.12+
- Dependency manager: `uv` (no pip/poetry/conda)
- Data contracts: Pydantic v2
- Lint/format: Ruff
- Typing: mypy strict; avoid `Any` unless required, annotate with `# justification:`
- Tests: pytest (+ pytest-asyncio)

## 6) File/Module Conventions

- Source layout: `src/` is canonical import root.
- Specs:
  - Feature spec: `specs/<id-name>/spec.md`
  - New specs must include: Acceptance Criteria (Gherkin) + Security & Compliance
- Skills:
  - Contracts manifest: `skills.json` (validated by `skills.schema.json`)
  - One file per built-in skill: `src/chimera/skills/skills/<skill>.py`
- MCP:
  - Registry: `mcp.json` (validated by `mcp.schema.json`)

## 7) Safety & Repo Hygiene

- Never commit secrets. Config files reference env var names only.
- Avoid destructive git commands unless explicitly requested.
- Keep changes minimal and spec-aligned.

## 8) Required Verification (Pick What Applies)

- Spec governance: `python scripts/spec_check.py`
- MCP config: `python scripts/validate_mcp_config.py`
- Skills manifest: `python scripts/validate_skills_manifest.py`
- Tests: `make test` (or `uv run pytest`)
- Lint/type: `make lint` / `make typecheck`

## 9) Iterative Refinement Log

This section records intentional improvements to agent rules over time.

- 2026-02-06: Initial rules consolidated into `AGENT.md`; added structured STATE block and explicit traceability tokens.
