from typing import Any

from chimera.lib.logging import get_logger
from chimera.models.agent import AgentHeartbeat
from chimera.models.result import Result
from chimera.models.types import TenantId
from chimera.ports.judge import JudgePort
from chimera.services.planner import Planner
from chimera.services.worker import Worker

logger = get_logger(__name__)


class Orchestrator:
    """Orchestrates the flow between Planner and Worker for a tenant.

    This is the top-level 'brain' entry point for the swarm.
    """

    def __init__(self, planner: Planner, worker: Worker, judge: JudgePort | None = None):
        self._planner = planner
        self._worker = worker
        self._judge = judge

    async def register_agent_heartbeat(self, heartbeat: AgentHeartbeat) -> None:
        """Register agent presence in the distributed registry."""
        raise NotImplementedError("Orchestrator.register_agent_heartbeat is not implemented")

    async def run_task(self, tenant_id: TenantId, kind: str, payload: dict[str, Any]) -> Result:
        """Execute a task end-to-end.

        Args:
            tenant_id: Target tenant.
            kind: Task type.
            payload: Input data.

        Returns:
            The terminal Result.
        """
        raise NotImplementedError("Orchestrator.run_task is not implemented")
