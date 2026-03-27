from typing import Literal

from pydantic import BaseModel


class LongevityScoreResponse(BaseModel):
    """Schema for longevity score and health metrics."""

    longevity_score: int  # 0-100
    biological_age: float
    chronological_age: float
    age_delta: float  # bio - chrono (negative is good)
    dunedin_pace: float
    healthspan_forecast_years: float
    mortality_risk_score: float
    trend_30d: Literal["improving", "stable", "declining"] | None = None
    projected_lifespan: float | None = None
