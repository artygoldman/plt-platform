"""Agent, AgentSession, and AgentDecision models."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, String, Text, Integer, Boolean, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Agent(Base):
    """AI Agent configuration and system prompts."""
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # cmo, med_cardio, etc.
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-6
    specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[str] = mapped_column(String(100), default="claude-sonnet-4-6", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    sessions: Mapped[list["AgentSession"]] = relationship(
        "AgentSession",
        back_populates="agent",
    )
    decisions: Mapped[list["AgentDecision"]] = relationship(
        "AgentDecision",
        back_populates="agent",
    )


class AgentSession(Base):
    """Session record for an agent's execution."""
    __tablename__ = "agent_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # new_data, daily, user_query, alert
    trigger_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default="running",
        nullable=False,
    )  # running, completed, failed, vetoed
    langgraph_thread_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cost_usd: Mapped[Decimal] = mapped_column(Numeric(8, 4), default=0, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="agent_sessions",
    )
    decisions: Mapped[list["AgentDecision"]] = relationship(
        "AgentDecision",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    protocols: Mapped[list["Protocol"]] = relationship(
        "Protocol",
        back_populates="session",
    )


class AgentDecision(Base):
    """Individual decision made by an agent."""
    __tablename__ = "agent_decisions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agent_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    agent_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("agents.id"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    input_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    output_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 0-100
    was_vetoed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    veto_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    vetoed_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    session: Mapped["AgentSession"] = relationship(
        "AgentSession",
        back_populates="decisions",
    )
    agent: Mapped["Agent"] = relationship(
        "Agent",
        back_populates="decisions",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="agent_decisions",
    )
