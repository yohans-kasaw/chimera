from typing import Any

from chimera.lib.logging import get_logger
from chimera.models.task import Task
from chimera.models.types import TenantId
from chimera.ports.queue import TaskQueuePort

logger = get_logger(__name__)


class Planner:
    """Service for creating and enqueuing tasks.

    Acts as the entry point for work into the swarm.
    """

    def __init__(self, queue: TaskQueuePort):
        self._queue = queue

    async def create_task(self, tenant_id: TenantId, kind: str, task_input: dict[str, Any]) -> Task:
        """Create a validated task and push it to the queue.

        Args:
            tenant_id: Target tenant.
            kind: Task type.
            task_input: Payload.

        Returns:
            The created Task instance.
        """
        raise NotImplementedError("Planner.create_task is not implemented")
