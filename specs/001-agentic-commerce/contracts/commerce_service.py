from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Protocol, runtime_checkable
from pydantic import BaseModel

class TransactionRequest(BaseModel):
    agent_id: str
    tenant_id: str
    amount: Decimal
    asset: str
    destination_address: str
    trace_id: str

@runtime_checkable
class CommerceService(Protocol):
    """Protocol for the Commerce Service defining the contract for financial autonomy."""

    @abstractmethod
    async def transfer_asset(self, request: TransactionRequest) -> dict[str, Any]:
        """
        Executes an asset transfer after passing CFO Judge budget checks.
        
        Args:
            request: The transaction request details.
            
        Returns:
            dict: The result from the MCP tool call.
            
        Raises:
            BudgetExceededError: If the CFO Judge rejects the transaction.
            MCPError: If the underlying MCP call fails.
        """
        ...

    @abstractmethod
    async def get_balance(self, wallet_id: str, asset: str) -> Decimal:
        """
        Queries the current balance for a specific wallet and asset.
        
        Args:
            wallet_id: The unique identifier for the wallet.
            asset: The asset symbol (e.g., "ETH").
            
        Returns:
            Decimal: The current balance.
        """
        ...

    @abstractmethod
    async def get_current_spend(self, tenant_id: str) -> Decimal:
        """
        Retrieves the cumulative spend for the current day.
        
        Args:
            tenant_id: The tenant to check.
            
        Returns:
            Decimal: Cumulative USD spend.
        """
        ...
