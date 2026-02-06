from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from chimera.models.task import Task
from chimera.ports.llm import LLMPort
from chimera.ports.queue import TaskQueuePort
from chimera.services.worker import Worker


@pytest.mark.asyncio
async def test_worker_retries_on_failure() -> None:
    mock_queue = AsyncMock(spec=TaskQueuePort)
    mock_llm = AsyncMock(spec=LLMPort)
    worker = Worker(queue=mock_queue, llm=mock_llm, worker_id="w1")

    task = Task(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        kind="test",
        input={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        attempt=0,
        max_attempts=2,
    )

    mock_queue.dequeue.return_value = [task]
    # Simulate LLM failure
    mock_llm.generate_result.side_effect = RuntimeError("LLM Down")

    # The task says: "Add worker retry/backoff + idempotency hooks"

    with pytest.raises(RuntimeError):
        await worker.process_batch(tenant_id="t_acme", batch_size=1)

    # Verify ack was NOT called
    mock_queue.ack.assert_not_called()
