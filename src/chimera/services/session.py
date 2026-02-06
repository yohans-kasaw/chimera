import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from chimera.models.types import SessionId, TenantId


class SessionState(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class SwarmSession(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: SessionId
    tenant_id: TenantId
    state: SessionState = SessionState.CREATED
    created_at: datetime
    updated_at: datetime


class SessionService:
    """Minimal in-memory session helper for MVP.

    This will eventually use a real database.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, SwarmSession] = {}

    def create_session(self, tenant_id: TenantId) -> SwarmSession:
        raise NotImplementedError("SessionService.create_session is not implemented")

    def get_session(self, session_id: str) -> SwarmSession | None:
        raise NotImplementedError("SessionService.get_session is not implemented")
