"""Shared models for skills and workflows."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from chimera.models.types import TenantId, TraceId
from chimera.ports.mcp import MCPClientPort


class SkillContext(BaseModel):
    """Execution context provided to every skill.

    Attributes:
        tenant_id: Tenant boundary for the execution.
        trace_id: Correlation ID for observability.
        mcp_client: Optional MCP client for tool calls.
        metadata: String metadata for additional coordination.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    tenant_id: TenantId
    trace_id: TraceId
    mcp_client: MCPClientPort | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class SkillRunStatus(StrEnum):
    """Status of a skill execution step."""

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    SUCCEEDED = "succeeded"
    FAILED = "failed"


class SkillRunRecord(BaseModel):
    """Record of a single skill execution.

    Attributes:
        skill_name: Skill identifier.
        status: Outcome status.
        output: Output payload captured as a dict.
        error: Optional error message for failures.
        completed_at: Completion timestamp.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """

    model_config = ConfigDict(extra="forbid")

    skill_name: str
    status: SkillRunStatus
    output: dict[str, object]
    error: str | None = None
    completed_at: datetime
