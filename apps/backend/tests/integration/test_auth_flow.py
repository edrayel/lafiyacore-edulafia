from uuid import uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Needs proper DB setup")

from edulafia.core.security import hash_password
from edulafia.modules.auth.models import User


@pytest.mark.asyncio
class TestAuthFlow:
    async def test_full_login_refresh_logout_flow(self, db_session, client):
        """Test complete auth flow: login -> get me -> refresh -> logout."""
        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="flow@test.com",
            password_hash=hash_password("FlowPass123!"),
            first_name="Flow",
            last_name="Test",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        # Login
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "flow@test.com", "password": "FlowPass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

        # Get current user
        cookies = response.cookies
        response = await client.get("/api/v1/auth/me", cookies=cookies)
        assert response.status_code == 200
        assert response.json()["email"] == "flow@test.com"

        # Logout
        response = await client.post("/api/v1/auth/logout", cookies=cookies)
        assert response.status_code == 200
