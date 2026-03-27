import asyncio
import os
from typing import AsyncGenerator, Generator

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.core.config import settings
from src.core.security import create_access_token
from src.db.base import Base


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    test_db_url = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite+aiosqlite:///:memory:",
    )

    if "sqlite" in test_db_url:
        engine = create_async_engine(
            test_db_url,
            echo=False,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = create_async_engine(
            test_db_url,
            echo=False,
        )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def auth_header() -> dict:
    user_id = "test-user-123"
    token = create_access_token(data={"sub": user_id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_list() -> list:
    users = [
        "test-user-1",
        "test-user-2",
        "test-user-3",
        "test-user-4",
        "test-user-5",
    ]
    headers_list = []
    for user_id in users:
        token = create_access_token(data={"sub": user_id})
        headers_list.append({"Authorization": f"Bearer {token}"})
    return headers_list


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        app=app,
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield client


@pytest.fixture
def redis_client():
    import redis

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    client = redis.from_url(redis_url, decode_responses=True)

    yield client

    client.flushdb()
    client.close()


@pytest.fixture(autouse=True)
async def cleanup_db(db_session: AsyncSession):
    yield
    await db_session.rollback()
