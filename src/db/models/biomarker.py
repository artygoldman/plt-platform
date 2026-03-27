"""Biomarker model for time-series health data."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, String, Numeric, Index, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Biomarker(Base):
    """Time-series biomarker measurements.

    Note: This table is designed to be converted to a TimescaleDB hypertable
    with (time, user_id) as the primary dimensions.
    """
    __tablename__ = "biomarkers"
    __table_args__ = (
        Index(
            "idx_biomarkers_user_marker",
            "user_id",
            "marker_name",
            postgresql_using="btree",
        ),
        Index(
            "idx_biomarkers_time",
            "time",
            postgresql_using="btree",
        ),
        Index(
            "idx_biomarkers_user_time",
            "user_id",
            "time",
            postgresql_using="btree",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # blood_test, oura, apple_watch, cgm
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # lipids, hormones, inflammation, sleep
    marker_name: Mapped[str] = mapped_column(String(100), nullable=False)  # ApoB, testosterone, hsCRP, HRV
    value: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    reference_low: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    reference_high: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    optimal_low: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    optimal_high: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    metadata_: Mapped[dict] = mapped_column(
        JSON,
        name="metadata",
        default=dict,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="biomarkers",
    )
