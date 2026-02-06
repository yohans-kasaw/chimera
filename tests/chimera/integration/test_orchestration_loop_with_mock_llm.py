from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from chimera.models.result import Result, ResultStatus
from chimera.ports.llm import LLMPort
from chimera.services.orchestrator import Orchestrator
from chimera.services.planner import Planner
from chimera.services.worker import Worker


@pytest.mark.asyncio
async def test_full_orchestration_loop() -> None:
    # Use a real queue adapter with fakeredis for integration test
    import fakeredis.aioredis

    from chimera.lib.redis_queue import RedisTaskQueue

    redis_client = fakeredis.aioredis.FakeRedis()
    queue = RedisTaskQueue(redis_client)
    mock_llm = AsyncMock(spec=LLMPort)

    # Use real JudgeService for integration test
    from chimera.services.judge import JudgeService

    judge = JudgeService()

    planner = Planner(queue=queue)
    worker = Worker(queue=queue, llm=mock_llm, worker_id="test_worker")
    orchestrator = Orchestrator(planner=planner, worker=worker, judge=judge)

    # Mock LLM response
    mock_llm.generate_result.side_effect = lambda task: Result(
        tenant_id=task.tenant_id,
        trace_id=task.trace_id,
        task_id=task.task_id,
        status=ResultStatus.SUCCEEDED,
        output={"status": "done"},
        completed_at=datetime.now(UTC),
    )

    # Execute loop
    result = await orchestrator.run_task(
        tenant_id="t_acme", kind="test.job", payload={"foo": "bar"}
    )

    assert result.status == ResultStatus.SUCCEEDED
    assert result.output == {"status": "done"}

    await redis_client.close()
