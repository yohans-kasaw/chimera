from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime

class BudgetConfiguration(BaseModel):
    """Configuration for spending limits."""
    id: UUID = Field(default_factory=uuid4)
    tenant_id: str
    daily_limit_usd: Decimal = Decimal("100.00")
    currency: str = "USD"
    is_active: bool = True

class TransactionRecord(BaseModel):
    """Record of a financial transaction."""
    id: UUID = Field(default_factory=uuid4)
    trace_id: str
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_name: str
    amount_asset: Decimal
    asset_symbol: str
    amount_usd: Decimal
    network_fee_usd: Decimal = Decimal("0.00")
    status: str = "PENDING"
    rejection_reason: Optional[str] = None
    mcp_response: Optional[dict] = None

class WalletInfo(BaseModel):
    """Basic wallet information."""
    wallet_id: str
    address: str
    network_id: str
