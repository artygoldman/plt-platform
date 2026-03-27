"""Dependency injection for FastAPI routes."""

from typing import AsyncGenerator
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection.

    Yields:
        AsyncSession: Database session for query execution.
    """
    async with get_session() as session:
        yield session


async def get_current_user() -> dict:
    """Get current authenticated user.

    TODO: Implement JWT authentication in Phase 4.
    Currently returns mock user data for development.

    Returns:
        dict: User object with id, email, and metadata.
    """
    # Mock user for development - will be replaced with JWT auth in Phase 4
    return {
        "id": uuid4(),
        "email": "user@example.com",
        "name": "Test User",
        "subscription_tier": "free",
    }
