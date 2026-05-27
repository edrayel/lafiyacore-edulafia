"""Pytest configuration and shared fixtures."""

import asyncio
import os
from collections.abc import AsyncGenerator, Generator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from edulafia.core.security import create_access_token, create_user_token_payload
from edulafia.database import Base
from edulafia.modules.guardians.student_guardian import StudentGuardian

# Test database URL - configurable via environment variable
# CI must set TEST_DATABASE_URL; the fallback is for local dev only
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://edulafia:edulafia@localhost:5432/edulafia_test",
)


def _check_db_available():
    """Check if the test database is available."""
    import asyncio
    async def _check():
        try:
            engine = create_async_engine(TEST_DATABASE_URL)
            async with engine.connect() as conn:
                await conn.close()
            await engine.dispose()
            return True
        except Exception:
            return False
    return asyncio.run(_check())


DB_AVAILABLE = _check_db_available()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Create a test database engine."""
    if not DB_AVAILABLE:
        pytest.skip("Test database is not available")

    from sqlalchemy.pool import NullPool

    engine = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session with automatic rollback."""
    TestSession = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestSession() as session, session.begin():
        yield session
        await session.rollback()


@pytest.fixture(scope="session")
def sample_school_id():
    """Generate a sample school ID."""
    return uuid4()

@pytest.fixture(scope="session")
def sample_user_id():
    """Generate a sample user ID."""
    return uuid4()


@pytest.fixture
def auth_token(sample_user_id, sample_school_id):
    """Create a test authentication token."""
    payload = create_user_token_payload(
        user_id=sample_user_id,
        role="school_admin",
        school_id=sample_school_id,
    )
    return create_access_token(payload)


@pytest.fixture
def auth_headers(auth_token):
    """Create authentication headers for test requests."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def teacher_auth_token(sample_school_id):
    """Create a test authentication token for a teacher."""
    payload = create_user_token_payload(
        user_id=uuid4(),
        role="teacher",
        school_id=sample_school_id,
    )
    return create_access_token(payload)


@pytest.fixture
def teacher_auth_headers(teacher_auth_token):
    """Create authentication headers for teacher test requests."""
    return {"Authorization": f"Bearer {teacher_auth_token}"}
