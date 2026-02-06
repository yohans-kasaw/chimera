from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import fakeredis.aioredis
import pytest

from chimera.lib.redis_queue import RedisTaskQueue
from chimera.models.task import Task


@pytest.fixture
async def redis_client() -> AsyncGenerator[fakeredis.aioredis.FakeRedis, None]:
    client = fakeredis.aioredis.FakeRedis()
    yield client
    await client.flushall()
    await client.close()


@pytest.mark.asyncio
async def test_redis_queue_enqueue_dequeue(redis_client: fakeredis.aioredis.FakeRedis) -> None:
    queue = RedisTaskQueue(redis_client)
    task = Task(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        kind="test",
        input={"data": 1},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    await queue.enqueue("t_acme", task)

    tasks = await queue.dequeue("t_acme", batch_size=1, worker_id="w1")
    assert len(tasks) == 1
    assert tasks[0].task_id == "tk_1"
    assert tasks[0].tenant_id == "t_acme"


@pytest.mark.asyncio
async def test_redis_queue_ack(redis_client: fakeredis.aioredis.FakeRedis) -> None:
    queue = RedisTaskQueue(redis_client)
    task = Task(
        tenant_id="t_acme",
        trace_id="tr_1",
        task_id="tk_1",
        kind="test",
        input={"data": 1},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    await queue.enqueue("t_acme", task)
    tasks = await queue.dequeue("t_acme", batch_size=1, worker_id="w1")

    # Ack the task
    await queue.ack("t_acme", tasks[0], "w1")
