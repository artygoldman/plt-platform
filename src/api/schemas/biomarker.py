from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BiomarkerCreate(BaseModel):
    """Schema for creating a new biomarker measurement."""

    source: Literal["blood_test", "oura", "apple_watch", "cgm", "manual"]
    category: str
    marker_name: str
    value: float
    unit: str
    reference_low: float | None = None
    reference_high: float | None = None
    optimal_low: float | None = None
    optimal_high: float | None = None


class BiomarkerResponse(BaseModel):
    """Schema for biomarker response."""

    id: UUID
    time: datetime
    source: str
    category: str
    marker_name: str
    value: float
    unit: str
    reference_low: float | None
    reference_high: float | None
    optimal_low: float | None
    optimal_high: float | None

    model_config = ConfigDict(from_attributes=True)


class BiomarkerHistory(BaseModel):
    """Schema for biomarker historical data."""

    marker_name: str
    unit: str
    data_points: list[dict]  # [{time, value}]
    trend: Literal["improving", "stable", "declining"] | None = None
