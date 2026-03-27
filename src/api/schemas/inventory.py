from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SupplementCreate(BaseModel):
    """Schema for adding a new supplement."""

    name: str
    brand: str | None = None
    dosage_per_unit: str | None = None
    units_remaining: int | None = None
    expiry_date: date | None = None
    auto_reorder: bool = False


class SupplementResponse(BaseModel):
    """Schema for supplement response."""

    id: UUID
    name: str
    brand: str | None = None
    dosage_per_unit: str | None = None
    units_remaining: int | None = None
    expiry_date: date | None = None
    auto_reorder: bool
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupplementUpdate(BaseModel):
    """Schema for updating supplement data."""

    units_remaining: int | None = None
    expiry_date: date | None = None
    auto_reorder: bool | None = None
