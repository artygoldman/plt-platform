"""Longevity protocol endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.protocol import ProtocolResponse

router = APIRouter(prefix="/protocols", tags=["Protocols"])


@router.get("/active", response_model=ProtocolResponse)
async def get_active_protocol(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ProtocolResponse:
    """Get the currently active longevity protocol for the user.

    Retrieve the protocol that is currently in effect. A user has only one
    active protocol at a time. Protocol contains nutrition, supplements,
    fitness, sleep, environment, and medical action recommendations.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        ProtocolResponse: Active protocol with all components

    Raises:
        HTTPException: 404 if no active protocol found
    """
    user_id = current_user["id"]

    # TODO: Query active protocol from DB
    # Implementation should:
    # - Filter by user_id and status = "active"
    # - Ensure now() is between valid_from and valid_until
    # - Raise 404 if none found
    # - Return most recently activated protocol

    return ProtocolResponse(
        id=UUID(int=0),
        version=1,
        status="active",
        nutrition_plan=None,
        supplement_plan=None,
        fitness_plan=None,
        sleep_protocol=None,
        environment=None,
        medical_actions=None,
        valid_from=None,
        valid_until=None,
        approved_by=None,
        created_at=datetime.utcnow(),
    )


@router.get("/", response_model=list[ProtocolResponse])
async def list_protocols(
    skip: int = 0,
    limit: int = 50,
    status_filter: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[ProtocolResponse]:
    """List all protocols for the user.

    Retrieve paginated list of all protocols (active, archived, pending).
    Useful for viewing protocol history and comparing versions.

    Args:
        skip: Number of protocols to skip (pagination)
        limit: Maximum protocols to return (default 50)
        status_filter: Optional filter by status (active, archived, pending)
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[ProtocolResponse]: List of protocols ordered by most recent
    """
    user_id = current_user["id"]

    # TODO: Query all protocols from DB
    # Implementation should:
    # - Filter by user_id
    # - Apply status_filter if provided
    # - Order by created_at descending
    # - Apply pagination with skip/limit

    return []


@router.get("/{protocol_id}", response_model=ProtocolResponse)
async def get_protocol_detail(
    protocol_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ProtocolResponse:
    """Get detailed information about a specific protocol.

    Retrieve a single protocol with all components: nutrition plan,
    supplement recommendations, fitness program, sleep protocol, etc.

    Args:
        protocol_id: UUID of the protocol
        db: Database session
        current_user: Current authenticated user

    Returns:
        ProtocolResponse: Protocol details

    Raises:
        HTTPException: 404 if protocol not found
        HTTPException: 403 if protocol doesn't belong to current user
    """
    # TODO: Query protocol from DB
    # Implementation should:
    # - Query protocol where id = protocol_id and user_id = current_user["id"]
    # - Raise 404 if not found
    # - Return complete protocol with all nested objects

    raise HTTPException(status_code=404, detail="Protocol not found")


@router.post("/{protocol_id}/activate", response_model=dict, status_code=status.HTTP_200_OK)
async def activate_protocol(
    protocol_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Activate a protocol for the user.

    Switch from current active protocol to a different one. Deactivates
    the previous protocol and sets the new one as active. New contracts
    will be generated based on the activated protocol.

    Args:
        protocol_id: UUID of the protocol to activate
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Activation confirmation with new active protocol details

    Raises:
        HTTPException: 404 if protocol not found
        HTTPException: 403 if protocol doesn't belong to current user
    """
    user_id = current_user["id"]

    # TODO: Activate protocol in DB
    # Implementation should:
    # - Query protocol where id = protocol_id and user_id = current_user["id"]
    # - Raise 404 if not found
    # - Deactivate current active protocol (set status = "archived")
    # - Set new protocol status = "active" and activated_at = now
    # - Trigger contract generation for this user with new protocol
    # - Return confirmation with new protocol info

    return {
        "protocol_id": str(protocol_id),
        "status": "activated",
        "activated_at": datetime.utcnow().isoformat(),
        "message": "Protocol activated successfully. New contracts will be generated.",
    }
