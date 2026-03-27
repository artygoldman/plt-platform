"""Supplement inventory management endpoints."""

from datetime import date, datetime, timedelta
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.inventory import (
    SupplementCreate,
    SupplementResponse,
    SupplementUpdate,
)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=list[SupplementResponse])
async def list_supplements(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[SupplementResponse]:
    """List all supplements in the user's inventory.

    Retrieve paginated list of all supplements currently in inventory,
    regardless of expiry status or quantity.

    Args:
        skip: Number of supplements to skip (pagination)
        limit: Maximum supplements to return (default 100)
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[SupplementResponse]: List of supplements with details
    """
    user_id = current_user["id"]

    # TODO: Query supplements from DB
    # Implementation should:
    # - Filter by user_id
    # - Order by name ascending
    # - Apply pagination with skip/limit

    return []


@router.post("/", response_model=SupplementResponse, status_code=status.HTTP_201_CREATED)
async def add_supplement(
    supplement: SupplementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> SupplementResponse:
    """Add a new supplement to inventory.

    Create a new supplement entry with name, brand, dosage, quantity, expiry date,
    and auto-reorder preference. Returns created supplement with ID.

    Args:
        supplement: Supplement data to create
        db: Database session
        current_user: Current authenticated user

    Returns:
        SupplementResponse: Created supplement with ID and timestamp
    """
    user_id = current_user["id"]

    # TODO: Create supplement in DB
    # Implementation should:
    # - Create new supplement record with user_id = current_user["id"]
    # - Set created_at and updated_at to now()
    # - Return created supplement

    supplement_id = uuid4()
    return SupplementResponse(
        id=supplement_id,
        name=supplement.name,
        brand=supplement.brand,
        dosage_per_unit=supplement.dosage_per_unit,
        units_remaining=supplement.units_remaining,
        expiry_date=supplement.expiry_date,
        auto_reorder=supplement.auto_reorder,
        updated_at=datetime.utcnow(),
    )


@router.patch("/{supplement_id}", response_model=SupplementResponse)
async def update_supplement(
    supplement_id: UUID,
    update: SupplementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> SupplementResponse:
    """Update a supplement in inventory.

    Update supplement quantity, expiry date, or auto-reorder preference.
    Only fields provided in the request are updated.

    Args:
        supplement_id: UUID of the supplement
        update: Fields to update (units_remaining, expiry_date, auto_reorder)
        db: Database session
        current_user: Current authenticated user

    Returns:
        SupplementResponse: Updated supplement

    Raises:
        HTTPException: 404 if supplement not found
        HTTPException: 403 if supplement doesn't belong to current user
    """
    # TODO: Update supplement in DB
    # Implementation should:
    # - Query supplement where id = supplement_id and user_id = current_user["id"]
    # - Raise 404 if not found
    # - Update only provided fields
    # - Set updated_at = now()
    # - Return updated supplement

    return SupplementResponse(
        id=supplement_id,
        name="",
        brand=None,
        dosage_per_unit=None,
        units_remaining=update.units_remaining,
        expiry_date=update.expiry_date,
        auto_reorder=update.auto_reorder or False,
        updated_at=datetime.utcnow(),
    )


@router.delete("/{supplement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplement(
    supplement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> None:
    """Remove a supplement from inventory.

    Delete a supplement entry from the user's inventory.

    Args:
        supplement_id: UUID of the supplement
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: 404 if supplement not found
        HTTPException: 403 if supplement doesn't belong to current user
    """
    # TODO: Delete supplement from DB
    # Implementation should:
    # - Query supplement where id = supplement_id and user_id = current_user["id"]
    # - Raise 404 if not found
    # - Delete supplement record
    # - Return 204 No Content


@router.get("/expiring")
async def list_expiring_supplements(
    days: int = 30,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[SupplementResponse]:
    """Get supplements expiring within N days.

    Retrieve supplements that will expire within the specified number of days.
    Useful for identifying items to use up or replace soon.

    Args:
        days: Days until expiry to include (default 30)
        skip: Number of supplements to skip (pagination)
        limit: Maximum supplements to return (default 100)
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[SupplementResponse]: List of soon-to-expire supplements
    """
    user_id = current_user["id"]
    expiry_cutoff = date.today() + timedelta(days=days)

    # TODO: Query supplements from DB
    # Implementation should:
    # - Filter by user_id
    # - Filter where expiry_date IS NOT NULL
    # - Filter where expiry_date <= today + days
    # - Filter where expiry_date > today (not already expired)
    # - Order by expiry_date ascending
    # - Apply pagination

    return []


@router.get("/reorder")
async def list_reorder_needed(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[SupplementResponse]:
    """Get supplements that need reorder.

    Retrieve supplements that are running low (units_remaining below threshold)
    or that have auto_reorder enabled and are below minimum quantity.

    Args:
        skip: Number of supplements to skip (pagination)
        limit: Maximum supplements to return (default 100)
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[SupplementResponse]: List of supplements needing reorder
    """
    user_id = current_user["id"]

    # TODO: Query supplements from DB
    # Implementation should:
    # - Filter by user_id
    # - Filter where auto_reorder = True and units_remaining < threshold (e.g., 10)
    # - OR filter where units_remaining = 0
    # - Order by units_remaining ascending
    # - Apply pagination

    return []
