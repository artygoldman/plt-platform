"""Data import and synchronization endpoints."""

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.biomarker import BiomarkerHistory, BiomarkerResponse

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Upload a PDF blood test or biomarker data file.

    Triggers background parsing via parse_blood_test_pdf service.
    Supports PDF blood test reports with automatic marker extraction.

    Args:
        file: File to upload (PDF, CSV, JSON)
        background_tasks: Background task queue
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Upload job status with ID for tracking
    """
    upload_id = str(uuid4())

    # Background task to parse file
    # background_tasks.add_task(parse_blood_test_pdf, upload_id, file, current_user["id"], db)

    return {
        "id": upload_id,
        "status": "processing",
        "filename": file.filename,
        "message": "File is being processed. Check /upload/{id} for status.",
    }


@router.post("/sync/oura", status_code=status.HTTP_202_ACCEPTED)
async def sync_oura_data(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Sync data from Oura Ring API.

    Retrieves sleep, activity, and readiness data from user's Oura account.
    Requires Oura API credentials in user profile.

    Args:
        background_tasks: Background task queue
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Sync status and data points ingested
    """
    sync_id = str(uuid4())

    # Background task to sync Oura data
    # background_tasks.add_task(sync_oura_service, sync_id, current_user["id"], db)

    return {
        "id": sync_id,
        "status": "syncing",
        "source": "oura",
        "message": "Oura Ring sync started",
    }


@router.post("/sync/apple-health", status_code=status.HTTP_202_ACCEPTED)
async def sync_apple_health(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Sync data from Apple Health.

    Processes exported Apple Health XML file to extract steps, heart rate,
    sleep, workouts, and other health metrics.

    Args:
        background_tasks: Background task queue
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Sync status and data points ingested
    """
    sync_id = str(uuid4())

    # Background task to sync Apple Health data
    # background_tasks.add_task(sync_apple_health_service, sync_id, current_user["id"], db)

    return {
        "id": sync_id,
        "status": "syncing",
        "source": "apple_health",
        "message": "Apple Health sync started",
    }


@router.get("/biomarkers", response_model=list[BiomarkerResponse])
async def get_biomarkers(
    category: str | None = None,
    marker_name: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[BiomarkerResponse]:
    """Get user's biomarkers with optional filters.

    Retrieve biomarker measurements with filtering by:
    - category (e.g., "blood_glucose", "lipids", "hormones")
    - marker_name (e.g., "HbA1c", "Total Cholesterol")
    - date range (start_date to end_date)

    Supports pagination with skip and limit.

    Args:
        category: Optional biomarker category filter
        marker_name: Optional specific marker name filter
        start_date: Optional start date for time range
        end_date: Optional end date for time range
        skip: Number of records to skip (pagination)
        limit: Maximum records to return (default 100)
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[BiomarkerResponse]: List of biomarker measurements matching filters
    """
    # TODO: Query actual biomarkers from DB with filters
    # Implementation should:
    # - Filter by user_id from current_user
    # - Apply category filter if provided
    # - Apply marker_name filter if provided
    # - Apply date range if start_date/end_date provided
    # - Apply pagination with skip/limit
    # - Order by time descending

    return []


@router.get("/biomarkers/{marker_name}/history", response_model=BiomarkerHistory)
async def get_biomarker_history(
    marker_name: str,
    days: int = 90,
    skip: int = 0,
    limit: int = 1000,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> BiomarkerHistory:
    """Get time series history for a specific biomarker.

    Retrieve all measurements for a specific marker (e.g., "Total Cholesterol")
    over a specified time period. Useful for trend analysis and visualization.

    Args:
        marker_name: Name of the biomarker (e.g., "Total Cholesterol", "HbA1c")
        days: Number of days to look back (default 90)
        skip: Number of records to skip (pagination)
        limit: Maximum records to return (default 1000)
        db: Database session
        current_user: Current authenticated user

    Returns:
        BiomarkerHistory: Time series data with trend analysis

    Raises:
        HTTPException: 404 if no data found for this marker
    """
    # TODO: Query actual biomarker history from DB
    # Implementation should:
    # - Filter by user_id and marker_name
    # - Filter by date range (now - days)
    # - Return data_points list with {time, value}
    # - Calculate trend (improving/stable/declining) from data

    return BiomarkerHistory(
        marker_name=marker_name,
        unit="mg/dL",
        data_points=[],
        trend=None,
    )
