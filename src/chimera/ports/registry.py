from typing import Protocol, Sequence

from chimera.models.agent import AgentHeartbeat


class AgentRegistryPort(Protocol):
    """Port for distributed agent tracking."""

    async def register_heartbeat(self, heartbeat: AgentHeartbeat) -> None:
        """Record or update an agent heartbeat."""
        ...

    async def get_active_agents(self) -> Sequence[AgentHeartbeat]:
        """Retrieve all agents currently marked as active."""
        ...
