from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class AgentStatus(StrEnum):
    """Execution status of an individual agent."""

    ACTIVE = "active"
    BUSY = "busy"
    IDLE = "idle"
    OFFLINE = "offline"


class AgentHeartbeat(BaseModel):
    """Heartbeat record for an active agent."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    status: AgentStatus
    last_seen: datetime
    # justification: Metrics can be any agent-specific dynamic data
    metrics: dict[str, Any]
