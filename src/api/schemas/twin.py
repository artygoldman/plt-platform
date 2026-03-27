from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SystemStatus(BaseModel):
    """Status of a biological system."""

    score: int  # 0-100
    trend: Literal["improving", "stable", "declining"]
    alerts: list[str] = []


class DigitalTwinResponse(BaseModel):
    """Schema for digital twin response."""

    user_id: UUID
    biological_age: float
    chronological_age: float
    dunedin_pace: float
    longevity_score: int
    healthspan_forecast_years: float
    mortality_risk_score: float
    systems_status: dict[str, SystemStatus]
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)
