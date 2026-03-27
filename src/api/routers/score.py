"""Longevity score and metrics endpoints."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.score import LongevityScoreResponse

router = APIRouter(prefix="/score", tags=["Score"])


@router.get("/", response_model=LongevityScoreResponse)
async def get_longevity_score(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> LongevityScoreResponse:
    """Get the current Longevity Score and breakdown.

    Returns the comprehensive longevity score (0-100) along with component
    metrics: biological age, Dunedin pace, healthspan forecast, and mortality risk.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        LongevityScoreResponse: Comprehensive longevity metrics with breakdown
    """
    user_id = current_user["id"]

    # TODO: Calculate actual score from biomarkers and twin data
    # Implementation should:
    # - Query latest biomarker data for user
    # - Calculate biological age from DunedinPACE algorithm
    # - Calculate longevity_score from weighted biomarkers
    # - Calculate healthspan_forecast from mortality models
    # - Determine trend_30d from score history (improving/stable/declining)

    return LongevityScoreResponse(
        longevity_score=72,
        biological_age=42.5,
        chronological_age=45.0,
        age_delta=-2.5,
        dunedin_pace=0.95,
        healthspan_forecast_years=35.0,
        mortality_risk_score=18.5,
        trend_30d="improving",
        projected_lifespan=92.5,
    )


@router.get("/history")
async def get_score_history(
    days: int = 365,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get longevity score history (time series).

    Retrieve historical Longevity Score values to visualize trends over time.
    Useful for assessing progress and identifying improvement patterns.

    Args:
        days: Number of days to look back (default 365)
        skip: Number of records to skip (pagination)
        limit: Maximum records to return (default 100)
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Historical score data with time series points
    """
    user_id = current_user["id"]
    start_date = datetime.utcnow() - timedelta(days=days)

    # TODO: Query score history from DB
    # Implementation should:
    # - Query longevity_score_history where user_id = user_id and timestamp >= start_date
    # - Order by timestamp ascending
    # - Apply pagination with skip/limit
    # - Return data_points list with {timestamp, score, age_delta, trend}

    return {
        "user_id": user_id,
        "period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": datetime.utcnow().isoformat(),
        "data_points": [],
        "average_score": 0,
        "min_score": 0,
        "max_score": 0,
        "trend": None,
    }


@router.get("/forecast")
async def get_longevity_forecast(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get longevity forecast and life expectancy projection.

    Returns predicted lifespan and healthspan based on current biomarkers,
    genetics, lifestyle, and medical history. Includes confidence intervals
    and scenarios for different intervention outcomes.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Forecast data with lifespan and healthspan projections
    """
    user_id = current_user["id"]

    # TODO: Calculate forecast from biomarkers and models
    # Implementation should:
    # - Get current biological_age, mortality_risk_score
    # - Apply longevity prediction model (e.g., Lee-Carter, Gompertz)
    # - Calculate multiple scenarios: baseline, optimistic, pessimistic
    # - Calculate healthspan_forecast_years (disease-free lifespan)
    # - Return confidence intervals (95% CI)
    # - Include intervention recommendations with projected impact

    return {
        "user_id": user_id,
        "current_age_biological": 42.5,
        "current_age_chronological": 45.0,
        "projections": {
            "baseline": {
                "expected_lifespan": 92.5,
                "healthspan_years": 35.0,
                "confidence_interval": {
                    "lower": 88.0,
                    "upper": 97.0,
                },
            },
            "optimistic": {
                "expected_lifespan": 98.0,
                "healthspan_years": 40.5,
                "description": "With strict protocol adherence and interventions",
            },
            "pessimistic": {
                "expected_lifespan": 87.0,
                "healthspan_years": 30.0,
                "description": "If current trajectories continue",
            },
        },
        "key_interventions": [
            {
                "intervention": "Improve sleep quality",
                "projected_impact_years": 2.5,
                "priority": "high",
            },
        ],
        "calculated_at": datetime.utcnow().isoformat(),
    }
