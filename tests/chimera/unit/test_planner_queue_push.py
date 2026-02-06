from unittest.mock import AsyncMock

import pytest

from chimera.ports.queue import TaskQueuePort
from chimera.services.planner import Planner


@pytest.mark.asyncio
async def test_planner_creates_and_pushes_task() -> None:
    mock_queue = AsyncMock(spec=TaskQueuePort)
    planner = Planner(queue=mock_queue)

    task_input = {"action": "greet", "name": "world"}
    task = await planner.create_task(tenant_id="t_acme", kind="skill.invoke", task_input=task_input)

    assert task.tenant_id == "t_acme"
    assert task.input == task_input
    assert task.kind == "skill.invoke"

    # Verify it was enqueued
    mock_queue.enqueue.assert_called_once_with("t_acme", task)
