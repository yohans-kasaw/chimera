from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from chimera.models.result import Result, ResultStatus
from chimera.models.task import Task
from chimera.ports.llm import LLMPort
from chimera.ports.queue import TaskQueuePort
from chimera.services.worker import Worker


@pytest.mark.asyncio
async def test_worker_consumes_and_processes_task() -> None:
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
    )

    mock_queue.dequeue.return_value = [task]
    mock_llm.generate_result.return_value = Result(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        status=ResultStatus.SUCCEEDED,
        output={"answer": 42},
        completed_at=datetime.now(UTC),
    )

    results = await worker.process_batch(tenant_id="t_acme", batch_size=1)

    assert len(results) == 1
    assert results[0].output == {"answer": 42}

    # Verify ack was called
    mock_queue.ack.assert_called_once_with("t_acme", task, "w1")
