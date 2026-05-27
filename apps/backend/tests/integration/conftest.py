import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from edulafia.main import app


@pytest_asyncio.fixture
async def client(db_session):
    """Create an async test client with database session override."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
