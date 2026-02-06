from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Protocol, runtime_checkable
from chimera.models.commerce import TransactionRecord

@runtime_checkable
class CommercePort(Protocol):
    """Protocol for financial operations."""

    @abstractmethod
    async def transfer_asset(
        self, 
        agent_id: str, 
        tenant_id: str, 
        amount: Decimal, 
        asset: str, 
        destination: str,
        trace_id: str
    ) -> TransactionRecord:
        """Execute asset transfer."""
        ...

    @abstractmethod
    async def get_balance(self, wallet_id: str, asset: str) -> Decimal:
        """Get account balance."""
        ...

    @abstractmethod
    async def get_current_spend(self, tenant_id: str) -> Decimal:
        """Get total spend for the current day."""
        ...
