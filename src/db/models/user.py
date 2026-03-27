"""User and UserProfile models."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, Date, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class User(Base):
    """User profile and account information."""
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(20), nullable=False)  # 'male' or 'female'
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    subscription_tier: Mapped[str] = mapped_column(String(50), default="premium", nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), default="UTC", nullable=False)

    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    biomarkers: Mapped[list["Biomarker"]] = relationship(
        "Biomarker",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    digital_twin: Mapped[Optional["DigitalTwin"]] = relationship(
        "DigitalTwin",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    files: Mapped[list["UserFile"]] = relationship(
        "UserFile",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    agent_sessions: Mapped[list["AgentSession"]] = relationship(
        "AgentSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    agent_decisions: Mapped[list["AgentDecision"]] = relationship(
        "AgentDecision",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    protocols: Mapped[list["Protocol"]] = relationship(
        "Protocol",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    daily_contracts: Mapped[list["DailyContract"]] = relationship(
        "DailyContract",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    supplement_inventory: Mapped[list["SupplementInventory"]] = relationship(
        "SupplementInventory",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserProfile(Base):
    """Detailed user health profile."""
    __tablename__ = "user_profiles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    height_cm: Mapped[Optional[float]] = mapped_column(nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(nullable=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    allergies: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    medications: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    contraindications: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    genetic_risks: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    goals: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )
