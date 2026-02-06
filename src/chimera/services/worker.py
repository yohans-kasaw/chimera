from collections.abc import Sequence

from chimera.lib.logging import get_logger
from chimera.models.result import Result
from chimera.models.types import TenantId
from chimera.ports.llm import LLMPort
from chimera.ports.queue import TaskQueuePort

logger = get_logger(__name__)


class Worker:
    """Service for consuming and processing tasks.

    Uses an LLM backend to execute tasks and returns results.
    """

    def __init__(self, queue: TaskQueuePort, llm: LLMPort, worker_id: str):
        self._queue = queue
        self._llm = llm
        self._worker_id = worker_id

    async def process_batch(self, tenant_id: TenantId, batch_size: int = 1) -> Sequence[Result]:
        """Consume a batch of tasks and process them.

        Args:
            tenant_id: Target tenant.
            batch_size: Number of tasks to process.

        Returns:
            A sequence of produced Results.
        """
        raise NotImplementedError("Worker.process_batch is not implemented")
