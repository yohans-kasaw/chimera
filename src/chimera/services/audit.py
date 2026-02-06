from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from chimera.lib.logging import get_logger
from chimera.models.types import TenantId, TraceId

logger = get_logger(__name__)


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: TenantId
    trace_id: TraceId
    event_id: str
    event_type: str
    payload: dict[str, Any]
    created_at: datetime


class AuditService:
    """Minimal audit trail service for MVP.

    Logs events and stores them in memory.
    """

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def log_event(
        self, tenant_id: TenantId, trace_id: TraceId, event_type: str, payload: dict[str, Any]
    ) -> AuditEvent:
        raise NotImplementedError("AuditService.log_event is not implemented")
