# 002: Skills + MCP Workflow Framework — Implementation Plan

## Phase 0: Spec Alignment
- Confirm Skills registry, workflow runner, and MCP tool binding requirements.
- Align user stories in [specs/functional.md](../functional.md).

## Phase 1: Core Models & Registry
- Implement `Skill` base class and `SkillRegistry`.
- Create `SkillContext` and run-record models.

## Phase 2: Workflow Runner
- Implement `WorkflowDefinition` and `SkillWorkflowRunner`.
- Capture structured outputs with timestamps for auditability.

## Phase 3: Sample Skills & Pipeline
- Add sample skills (`echo`, `normalize_handle`, `mcp_tool`).
- Provide a pipeline wrapper to execute workflows.

## Phase 4: MCP Configuration & Docs
- Add `mcp.sample.json` and document MCP setup in README.
- Link architecture and specs to Skills framework.

## Phase 5: Tests (Follow-on)
- Add tests validating registry discovery and workflow execution.
- Add integration test for MCP tool skill with mocked MCP client.
