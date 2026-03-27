"""Agent execution and session management endpoints."""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.agent import AgentDecisionResponse, AgentRunRequest, AgentSessionResponse

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def run_agent_pipeline(
    request: AgentRunRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Trigger the full agent pipeline execution.

    Initiates a multi-tier agent orchestration for comprehensive health analysis
    and recommendation generation. Runs asynchronously in background.

    Trigger types:
    - "new_data": Triggered by new biomarker data
    - "daily": Scheduled daily analysis
    - "user_query": User-initiated query
    - "alert": Triggered by health alert threshold

    Args:
        request: Agent run configuration with trigger type and data
        background_tasks: Background task queue for async execution
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Session ID for tracking pipeline progress

    Raises:
        HTTPException: 403 if user_id doesn't match current user
    """
    if request.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    session_id = uuid4()

    # Background task to run agent pipeline
    # background_tasks.add_task(runner.run_agent_pipeline, session_id, request.user_id, request.trigger_type, request.trigger_data, db)

    return {
        "session_id": str(session_id),
        "status": "queued",
        "trigger_type": request.trigger_type,
        "message": "Agent pipeline has been queued for execution",
    }


@router.get("/sessions", response_model=list[AgentSessionResponse])
async def list_agent_sessions(
    skip: int = 0,
    limit: int = 50,
    status_filter: Literal["running", "completed", "failed"] | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[AgentSessionResponse]:
    """List recent agent sessions for current user.

    Retrieve paginated list of agent execution sessions with optional status filtering.

    Args:
        skip: Number of sessions to skip (pagination)
        limit: Maximum sessions to return (default 50)
        status_filter: Optional filter by session status
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[AgentSessionResponse]: List of agent sessions ordered by most recent
    """
    user_id = current_user["id"]

    # TODO: Query agent sessions from DB
    # Implementation should:
    # - Filter by user_id
    # - Apply status_filter if provided (running/completed/failed)
    # - Order by started_at descending
    # - Apply pagination with skip/limit
    # - Populate decisions list for each session (or keep empty for list view)

    return []


@router.get("/sessions/{session_id}", response_model=AgentSessionResponse)
async def get_session_details(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> AgentSessionResponse:
    """Get full session details including all agent decisions.

    Retrieve a complete agent session with all decisions made by each tier
    in the agent hierarchy. Includes confidence scores and any vetoes.

    Args:
        session_id: UUID of the agent session
        db: Database session
        current_user: Current authenticated user

    Returns:
        AgentSessionResponse: Session details with all decisions

    Raises:
        HTTPException: 404 if session not found
        HTTPException: 403 if session doesn't belong to current user
    """
    # TODO: Query actual session from DB
    # Implementation should:
    # - Query agent_session where id = session_id and user_id = current_user["id"]
    # - Raise 404 if not found
    # - Query all agent_decisions for this session_id
    # - Populate decisions list with full AgentDecisionResponse objects
    # - Return complete session

    return AgentSessionResponse(
        id=session_id,
        status="completed",
        trigger_type="daily",
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
        total_tokens=0,
        decisions=[],
    )


@router.get("/sessions/{session_id}/decisions", response_model=list[AgentDecisionResponse])
async def list_session_decisions(
    session_id: UUID,
    skip: int = 0,
    limit: int = 100,
    agent_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[AgentDecisionResponse]:
    """List all agent decisions within a session.

    Get paginated decisions from an agent session, optionally filtered by agent tier.
    Decisions are ordered by execution order in the agent hierarchy.

    Args:
        session_id: UUID of the agent session
        skip: Number of decisions to skip (pagination)
        limit: Maximum decisions to return (default 100)
        agent_id: Optional filter by agent tier (e.g., "tier1_aggregator", "tier2_metabolologist")
        db: Database session
        current_user: Current authenticated user

    Returns:
        list[AgentDecisionResponse]: Agent decisions from the session

    Raises:
        HTTPException: 404 if session not found or doesn't belong to user
    """
    # TODO: Query agent decisions from DB
    # Implementation should:
    # - Verify session exists and belongs to current_user
    # - Query agent_decisions where session_id = session_id
    # - Apply agent_id filter if provided
    # - Order by execution_order or created_at
    # - Apply pagination with skip/limit

    return []


@router.get("/decisions/{decision_id}", response_model=AgentDecisionResponse)
async def get_decision_details(
    decision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> AgentDecisionResponse:
    """Get details of a specific agent decision.

    Retrieve full information about a single agent's decision including
    confidence score, reasoning, output data, and veto status.

    Args:
        decision_id: UUID of the agent decision
        db: Database session
        current_user: Current authenticated user

    Returns:
        AgentDecisionResponse: Single decision details

    Raises:
        HTTPException: 404 if decision not found
        HTTPException: 403 if decision doesn't belong to current user's session
    """
    # TODO: Query decision from DB
    # Implementation should:
    # - Query agent_decision where id = decision_id
    # - Verify the session belongs to current_user
    # - Raise 404 if not found
    # - Return complete decision with all fields

    raise HTTPException(status_code=404, detail="Decision not found")
