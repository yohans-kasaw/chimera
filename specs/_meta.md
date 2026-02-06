# Project Chimera: The Autonomous Influencer Factory

## Mission
Architect the "Factory" that builds the "Autonomous Influencer." This is not a prototype; it is a robust engineering environment where Intent (Specs) is the source of truth, and Infrastructure (CI/CD, Tests, Docker) ensures reliability.

## The Problem
Most AI projects fail because they rely on fragile prompts and messy codebases. When scaling, they hallucinate or break.

## The Solution
A robust engineering environment where:
1.  **Spec-Driven Development (SDD)**: We do not write code until the Specification is ratified.
2.  **Infrastructure as Code**: CI/CD, Tests, and Docker ensure reliability.
3.  **Traceability**: Every action is logged and observable.

## CI/CD Governance
The repository enforces automated governance through GitHub Actions and AI review rules:
*   **CI workflows**: [ .github/workflows/main.yml](../.github/workflows/main.yml) and [ .github/workflows/coverage.yml](../.github/workflows/coverage.yml)
*   **Dockerized tests**: [Dockerfile](../Dockerfile)
*   **AI review policy**: [ .coderabbit.yaml](../.coderabbit.yaml)

## The Goal
A repository so well-architected, specified, and tooled that a swarm of AI agents could enter the codebase and build the final features with minimal human conflict.

---

# Agent Governance & Rules Specification

**Status**: ACTIVE  
**Audience**: AI Agents (Cursor, Windsurf, OpenClaw), Human Developers, and Governance Bots.

This section defines the **comprehensive intent and blueprint** for generating the functional rules file (e.g., `.cursorrules`, `.windsurfrules`). Any AI agent operating on this codebase must internalize these directives before modifying code.

## 1. Project Context & Identity
*   **Name**: Project Chimera
*   **Type**: Modular Monolith (Python 3.12+ / FastAPI) with React Frontend.
*   **Core Logic**: An "Agent Runtime" that executes `Skills` (tools) based on `Intent`.
*   **Philosophy**: "Code is a liability; Specs are assets."
*   **Critical Path**: All changes must trace back to a specific feature spec in `specs/`.

## 2. The Prime Directive: Spec-First Development
**NO CODE may be written or modified without a corresponding ratified specification.**
*   **Verification**: Before writing code, the Agent must READ the relevant `specs/{feature-id}/spec.md`.
*   **Deviation**: If the code requires a deviation from the Spec, the Spec must be updated FIRST.
*   **Citation**: All Commit Messages and Pull Request descriptions must reference the Spec ID (e.g., `feat(001-commerce): implement wallet logic`).

## 3. Behavioral Rules (The "Laws")

### 3.1. Forbidden Actions (Hard Constraints)
The Agent is **strictly prohibited** from:
1.  **Hallucinating Dependencies**: Do NOT import libraries not listed in `pyproject.toml` or `package.json`.
2.  **Secret Leakage**: NEVER hardcode API keys, tokens, or passwords. Use `os.getenv` or the `CommerceManager` vault.
3.  **Bypassing Tests**: NEVER disable tests or run with `--no-verify` unless explicitly instructed by a Human Admin.
4.  **Deleting Data**: NEVER execute `DROP TABLE` or recursive `rm` on non-temp directories without confirmation.
5.  **Phantom Files**: Do not create files outside the `specs/` or `src/` hierarchy defined in the Architecture docs.

### 3.2 Security Specification Standards 
All new Features and Architecture changes MUST include a dedicated Security Section addressing:
1.  **AuthN/AuthZ**: Formal strategy (OAuth2/JWT) linked to specific API contracts/endpoints.
2.  **Secrets Management**: Explicit Vault/Env-var strategy.
3.  **Rate Limiting**: Defined per-endpoint limits.
4.  **Content Safety**: Detailed moderation pipeline (input/output filters).
5.  **Agent Containment**:
    *   *Resource Limits*: Budget/Token caps.
    *   *Forbidden Actions*: Hard boundaries.
    *   *Escalation*: Human intervention triggers.
6.  **Data Privacy**: PII and Token handling protocols.

### 3.3. Ambiguity Handling & Escalation
If an Agent encounters ambiguity (e.g., missing type definition, vague business logic):
1.  **SEARCH**: Glob `specs/` for keywords.
2.  **ANALYZE**: Check existing patterns in `src/`.
3.  **HALT**: If still ambiguous, **STOP**.
4.  **ASK**: Issue a question to the User/Human with:
    *   *Context*: "I am trying to implement X."
    *   *Blocker*: "The spec does not define Y."
    *   *Proposal*: "I recommend doing Z based on pattern W."

### 3.3. Coding Standards & Conventions
*   **Language**: Python 3.12+ (Backend), TypeScript 5+ (Frontend).
*   **Typing**: Strict typing is MANDATORY. No `Any` allowed without explicit inline justification.
*   **Docs**: Google-style Docstrings for all functions/classes.
*   **Async**: All I/O bound operations must be `async/await`.
*   **Testing**:
    *   Unit Tests (Pytest) for logic.
    *   Integration Tests (Testcontainers) for DB interactions.

### 3.4. Traceability & Observability
*   **Logging**: Use `src.chimera.lib.logging`. Do NOT use `print()`.
*   **Structure**: `logger.info("event_name", extra={"context": "value"})`.
*   **Reasoning**: Every significant logic branch must emit a log.

## 4. Spec-Referencing Patterns
Agents must generate commits and artifacts using this format:
*   **Commit**: `type(scope): message [Ref: Spec-ID]`
    *   *Example*: `feat(commerce): add wallet deduction logic [Ref: 001-agentic-commerce]`
*   **TODOs**: `# TODO(Spec-ID): description`

## 5. Evolution of Rules
This document is the Source of Truth.
1.  **Bootstrap**: This file generates the initial `.cursorrules`.
2.  **Learning**: As the project matures, "Lessons Learned" must be added to a `docs/lessons_learned.md` (or similar) and critical rules back-ported here.
3.  **Versioning**: Changes to this section require a PR and review by the Lead Architect.

## 6. Testability of Intent
An Agent reading this section must be able to output a JSON object representing the rules:
```json
{
  "project_name": "Chimera",
  "allowed_languages": ["python", "typescript"],
  "forbidden_patterns": ["hardcoded_secrets", "any_type", "print_statements"],
  "required_workflow": "spec_first"
}
```
If an Agent cannot deterministically generate this config, this Spec is considered "Ambiguous" and must be refined.
