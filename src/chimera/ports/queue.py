from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from chimera.models.task import Task
from chimera.models.types import TenantId


@runtime_checkable
class TaskQueuePort(Protocol):
    """Port for task queue operations.

    All operations must be tenant-scoped.
    """

    async def enqueue(self, tenant_id: TenantId, task: Task) -> None:
        """Add a task to the queue for a specific tenant."""
        ...

    async def dequeue(
        self, tenant_id: TenantId, batch_size: int = 1, worker_id: str = "default_worker"
    ) -> Sequence[Task]:
        """Retrieve tasks from the queue for a specific tenant.

        Args:
            tenant_id: Target tenant.
            batch_size: Maximum number of tasks to retrieve.
            worker_id: Identifier for the consumer.

        Returns:
            A sequence of tasks assigned to the worker.
        """
        ...

    async def ack(self, tenant_id: TenantId, task: Task, worker_id: str) -> None:
        """Acknowledge successful processing of a task."""
        ...

    async def dequeue_pending(
        self, tenant_id: TenantId, worker_id: str, idle_time_ms: int = 10000
    ) -> Sequence[Task]:
        """Claim and retrieve pending (unacknowledged) tasks from the queue.

        Args:
            tenant_id: Target tenant.
            worker_id: The claiming worker.
            idle_time_ms: Minimum time since last delivery.

        Returns:
            A sequence of claimed tasks.
        """
        ...
