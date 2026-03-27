"""Digital Twin model for user health snapshot."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Numeric, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class DigitalTwin(Base):
    """Aggregated health snapshot from agent analysis."""
    __tablename__ = "digital_twin"

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
    biological_age: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=True)
    chronological_age: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=True)
    dunedin_pace: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=True)
    longevity_score: Mapped[Integer] = mapped_column(Integer, nullable=True)  # 0-100
    healthspan_forecast_years: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=True)
    mortality_risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 3), nullable=True)
    systems_status: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="digital_twin",
    )
