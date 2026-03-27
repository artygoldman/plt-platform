"""User authentication and profile management endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user, get_db
from src.api.schemas.user import (
    TokenResponse,
    UserLogin,
    UserProfileResponse,
    UserProfileUpdate,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Register a new user.

    Create a new user account with email, password, and basic health information.
    Returns JWT token for immediate authenticated access.

    Validation:
    - Email must be unique
    - Password must be at least 8 characters
    - Date of birth must be a valid date

    Args:
        request: User registration data with email, password, name, date_of_birth, sex
        db: Database session

    Returns:
        TokenResponse: JWT token and authenticated user details

    Raises:
        HTTPException: 400 if email already exists or validation fails
    """
    # TODO: Register user in DB
    # Implementation should:
    # - Check if user with this email already exists
    # - Raise 400 with detail="Email already registered" if exists
    # - Hash password using bcrypt
    # - Create user record in users table
    # - Generate JWT token (see auth utilities)
    # - Return TokenResponse with token and user details

    raise HTTPException(
        status_code=400,
        detail="User registration not yet implemented",
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Login and get JWT token.

    Authenticate user with email and password. Returns JWT token for
    subsequent authenticated requests.

    Args:
        request: Login credentials (email and password)
        db: Database session

    Returns:
        TokenResponse: JWT token and authenticated user details

    Raises:
        HTTPException: 401 if credentials invalid
    """
    # TODO: Authenticate user
    # Implementation should:
    # - Query user by email from users table
    # - Raise 401 with detail="Invalid email or password" if not found
    # - Verify password hash using bcrypt
    # - Raise 401 if password incorrect
    # - Generate JWT token
    # - Return TokenResponse with token and user

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password",
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user profile.

    Retrieve the profile of the currently authenticated user.
    Requires valid JWT token in Authorization header.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserResponse: User profile details

    Raises:
        HTTPException: 401 if not authenticated
    """
    user_id = current_user["id"]

    # TODO: Get user from DB
    # Implementation should:
    # - Query user where id = current_user["id"]
    # - Raise 404 if not found (shouldn't happen if auth is correct)
    # - Return UserResponse

    return UserResponse(
        id=user_id,
        email=current_user.get("email", ""),
        name=current_user.get("name", ""),
        date_of_birth=None,
        sex="",
        created_at=datetime.utcnow(),
        subscription_tier=current_user.get("subscription_tier", "free"),
    )


@router.patch("/me", response_model=UserResponse)
async def update_user_profile(
    update: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    """Update current user profile.

    Update user health profile information including height, weight,
    blood type, allergies, medications, genetic risks, and health goals.

    Args:
        update: Fields to update
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserResponse: Updated user details

    Raises:
        HTTPException: 401 if not authenticated
    """
    user_id = current_user["id"]

    # TODO: Update user in DB
    # Implementation should:
    # - Query user where id = current_user["id"]
    # - Update only provided fields
    # - Set updated_at = now()
    # - Return updated UserResponse

    return UserResponse(
        id=user_id,
        email=current_user.get("email", ""),
        name=current_user.get("name", ""),
        date_of_birth=None,
        sex="",
        created_at=datetime.utcnow(),
        subscription_tier=current_user.get("subscription_tier", "free"),
    )


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_health_profile(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserProfileResponse:
    """Get detailed health profile.

    Retrieve comprehensive health profile including allergies, medications,
    genetic risks, and health goals.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserProfileResponse: Detailed health profile

    Raises:
        HTTPException: 401 if not authenticated
    """
    user_id = current_user["id"]

    # TODO: Get health profile from DB
    # Implementation should:
    # - Query user_health_profile where user_id = current_user["id"]
    # - Return UserProfileResponse with all health details
    # - Return empty lists if no data

    return UserProfileResponse(
        height_cm=None,
        weight_kg=None,
        blood_type=None,
        allergies=[],
        medications=[],
        genetic_risks={},
        goals=[],
    )


@router.patch("/me/profile", response_model=UserProfileResponse)
async def update_health_profile(
    update: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserProfileResponse:
    """Update health profile.

    Update detailed health information: allergies, medications, genetic risks,
    physical measurements, and health goals.

    Args:
        update: Fields to update
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserProfileResponse: Updated health profile

    Raises:
        HTTPException: 401 if not authenticated
    """
    user_id = current_user["id"]

    # TODO: Update health profile in DB
    # Implementation should:
    # - Query or create user_health_profile for user_id = current_user["id"]
    # - Update only provided fields
    # - Set updated_at = now()
    # - Return updated UserProfileResponse

    return UserProfileResponse(
        height_cm=update.height_cm,
        weight_kg=update.weight_kg,
        blood_type=update.blood_type,
        allergies=update.allergies or [],
        medications=update.medications or [],
        genetic_risks=update.genetic_risks or {},
        goals=update.goals or [],
    )
