from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, JSON
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

# -----------------------------------------------------------------------------
# Identity & Orchestration
# -----------------------------------------------------------------------------


class SwarmSession(SQLModel, table=True):
    """
    Represents a session of a swarm belonging to a tenant.
    """

    __tablename__ = "swarm_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(index=True, nullable=False)
    status: str = Field(index=True)  # e.g., "active", "completed"
    context: dict = Field(default={}, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="session")


class AgentProfile(SQLModel, table=True):
    """
    Configuration for an agent persona within a tenant.
    """

    __tablename__ = "agent_profiles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(index=True, nullable=False)
    name: str
    role: str
    tools_config: dict = Field(default={}, sa_column=Column(JSONB))

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="agent")


class Task(SQLModel, table=True):
    """
    A unit of work to be executed by an agent.
    """

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: Optional[UUID] = Field(default=None, foreign_key="swarm_sessions.id")
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agent_profiles.id")
    parent_task_id: Optional[UUID] = Field(default=None, foreign_key="tasks.id")

    type: str = Field(index=True)
    status: str = Field(index=True, default="QUEUED")
    input_payload: dict = Field(default={}, sa_column=Column(JSONB))
    priority: int = Field(default=0)
    attempt_count: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Relationships
    session: Optional[SwarmSession] = Relationship(back_populates="tasks")
    agent: Optional[AgentProfile] = Relationship(back_populates="tasks")
    parent: Optional["Task"] = Relationship(sa_relationship_kwargs={"remote_side": "Task.id"})
    results: List["TaskResult"] = Relationship(back_populates="task")
    transactions: List["Transaction"] = Relationship(back_populates="task")
    reviews: List["ReviewCard"] = Relationship(back_populates="task")


class TaskResult(SQLModel, table=True):
    """
    The output of a completed task.
    """

    __tablename__ = "task_results"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.id")
    status: str
    output_payload: dict = Field(default={}, sa_column=Column(JSONB))
    artifact_uri: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Task = Relationship(back_populates="results")


# -----------------------------------------------------------------------------
# Commerce Governance
# -----------------------------------------------------------------------------


class BudgetConfig(SQLModel, table=True):
    """
    Financial constraints for a tenant.
    """

    __tablename__ = "budget_configs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(index=True, nullable=False)
    daily_limit_usd: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    currency: str = Field(default="USD")
    is_active: bool = Field(default=True)

    # Relationships
    transactions: List["Transaction"] = Relationship(back_populates="budget")


class Transaction(SQLModel, table=True):
    """
    Immutable record of a financial operation.
    """

    __tablename__ = "transactions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    budget_id: UUID = Field(foreign_key="budget_configs.id")
    task_id: Optional[UUID] = Field(default=None, foreign_key="tasks.id")

    amount_usd: Decimal = Field(max_digits=12, decimal_places=2)
    asset_symbol: str
    status: str = Field(index=True)  # PENDING, EXECUTED, REJECTED
    metadata_json: dict = Field(
        default={}, sa_column=Column(JSONB, name="metadata")
    )  # 'metadata' is reserved in SQLModel
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    budget: BudgetConfig = Relationship(back_populates="transactions")
    task: Optional[Task] = Relationship(back_populates="transactions")


# -----------------------------------------------------------------------------
# Safety & Human-in-the-Loop
# -----------------------------------------------------------------------------


class ReviewCard(SQLModel, table=True):
    """
    A flagged item requiring human or high-level AI review.
    """

    __tablename__ = "review_cards"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.id")
    trigger_reason: str
    status: str = Field(default="OPEN")  # OPEN, RESOLVED, REJECTED
    reviewer_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

    # Relationships
    task: Task = Relationship(back_populates="reviews")
