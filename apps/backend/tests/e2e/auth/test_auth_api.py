"""Tests for Auth API endpoints - TDD implementation."""

from uuid import uuid4

import pytest


class TestAuthAPI:
    """Test cases for Auth API endpoints."""

    def test_auth_router_exists(self):
        """Test that auth router is importable."""
        from edulafia.modules.auth.api.auth import router
        assert router is not None

    def test_login_endpoint_registered(self):
        """Test that POST /auth/login endpoint is registered."""
        from edulafia.modules.auth.api.auth import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('/login' in path for path in routes)

    def test_refresh_endpoint_registered(self):
        """Test that POST /auth/refresh endpoint is registered."""
        from edulafia.modules.auth.api.auth import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('/refresh' in path for path in routes)

    def test_logout_endpoint_registered(self):
        """Test that POST /auth/logout endpoint is registered."""
        from edulafia.modules.auth.api.auth import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('/logout' in path for path in routes)

    def test_change_password_endpoint_registered(self):
        """Test that POST /auth/change-password endpoint is registered."""
        from edulafia.modules.auth.api.auth import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('/change-password' in path for path in routes)

    def test_me_endpoint_registered(self):
        """Test that GET /auth/me endpoint is registered."""
        from edulafia.modules.auth.api.auth import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('/me' in path for path in routes)

    def test_auth_router_prefix(self):
        """Test that auth router has correct prefix."""
        from edulafia.modules.auth.api.auth import router
        assert router.prefix == "/auth"

    def test_auth_router_tags(self):
        """Test that auth router has correct tags."""
        from edulafia.modules.auth.api.auth import router
        assert "Authentication" in router.tags


class TestSecurityModule:
    """Test cases for core security functions."""

    def test_hash_password(self):
        """Test password hashing."""
        from edulafia.core.security import hash_password

        hashed = hash_password("TestPassword1!")
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        from edulafia.core.security import hash_password, verify_password

        password = "TestPassword1!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with wrong password."""
        from edulafia.core.security import hash_password, verify_password

        password = "TestPassword1!"
        hashed = hash_password(password)
        assert verify_password("WrongPassword1!", hashed) is False

    def test_create_access_token(self):
        """Test JWT access token creation."""
        from edulafia.core.security import create_access_token
        token = create_access_token({"sub": str(uuid4()), "role": "admin"})
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_refresh_token(self):
        """Test JWT refresh token creation."""
        from edulafia.core.security import create_refresh_token
        token = create_refresh_token({"sub": str(uuid4()), "role": "admin"})
        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_token(self):
        """Test JWT token decoding."""
        from edulafia.core.security import create_access_token, decode_token
        user_id = str(uuid4())
        token = create_access_token({"sub": user_id, "role": "admin"})
        payload = decode_token(token)
        assert payload["sub"] == user_id
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_decode_invalid_token(self):
        """Test decoding invalid token raises ValueError."""
        from edulafia.core.security import decode_token
        with pytest.raises(ValueError):
            decode_token("invalid.token.here")

    def test_create_user_token_payload(self):
        """Test user token payload creation."""
        from edulafia.core.security import create_user_token_payload
        user_id = uuid4()
        school_id = uuid4()
        payload = create_user_token_payload(
            user_id=user_id,
            role="school_admin",
            school_id=school_id,
        )
        assert payload["sub"] == str(user_id)
        assert payload["role"] == "school_admin"
        assert payload["school_id"] == str(school_id)
