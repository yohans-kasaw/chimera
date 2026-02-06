from datetime import UTC, datetime

import fakeredis.aioredis
import pytest

from chimera.lib.redis_queue import RedisTaskQueue
from chimera.models.task import Task


@pytest.mark.asyncio
async def test_worker_recovery_pending_entries() -> None:
    redis_client = fakeredis.aioredis.FakeRedis()
    queue = RedisTaskQueue(redis_client)
    tenant_id = "t_acme"
    worker_id = "worker_1"

    task = Task(
        tenant_id=tenant_id,
        trace_id="tr_1",
        task_id="tk_recovery",
        kind="test",
        input={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    await queue.enqueue(tenant_id, task)

    # Worker 1 retrieves but doesn't ACK (simulated crash)
    tasks = await queue.dequeue(tenant_id, batch_size=1, worker_id=worker_id)
    assert len(tasks) == 1

    # We'll implement a method to claim pending tasks in Phase 5
    # For now, this test will fail as dequeue with ">" won't return pending items for another worker

    # Simulate a second worker trying to recover
    # Use idle_time_ms=0 to claim immediately in tests
    recovered_tasks = await queue.dequeue_pending(tenant_id, worker_id="worker_2", idle_time_ms=0)
    assert len(recovered_tasks) == 1
    assert recovered_tasks[0].task_id == "tk_recovery"

    await redis_client.close()
