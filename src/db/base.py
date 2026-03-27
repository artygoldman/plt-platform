"""Database base configuration and session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_database_url() -> str:
    """Get the async database URL from settings."""
    settings = get_settings()
    return settings.database_url


def create_engine_and_session():
    """Create async engine and session factory."""
    engine = create_async_engine(
        get_database_url(),
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
    )

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    return engine, session_factory


# Create engine and session factory at module load time
engine, AsyncSessionLocal = create_engine_and_session()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
