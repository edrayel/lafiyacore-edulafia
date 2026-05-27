"""Tests for Auth schemas - TDD implementation."""

import pytest
from pydantic import ValidationError


class TestLoginRequest:
    """Test cases for LoginRequest schema."""

    def test_valid_login_request(self):
        """Test valid login request."""
        from edulafia.modules.auth.schemas import LoginRequest

        data = LoginRequest(email="admin@school.edu.ng", password="Password1!")
        assert data.email == "admin@school.edu.ng"
        assert data.password == "Password1!"

    def test_login_request_requires_email(self):
        """Test that login request requires valid email."""
        from edulafia.modules.auth.schemas import LoginRequest

        with pytest.raises(ValidationError):
            LoginRequest(email="", password="Password1!")

    def test_login_request_requires_password(self):
        """Test that login request requires password."""
        from edulafia.modules.auth.schemas import LoginRequest

        with pytest.raises(ValidationError):
            LoginRequest(email="admin@school.edu.ng", password="")

    def test_login_request_invalid_email_format(self):
        """Test that login request rejects invalid email format."""
        from edulafia.modules.auth.schemas import LoginRequest

        with pytest.raises(ValidationError):
            LoginRequest(email="not-an-email", password="Password1!")


class TestTokenResponse:
    """Test cases for TokenResponse schema."""

    def test_valid_token_response(self):
        """Test valid token response."""
        from edulafia.modules.auth.schemas import TokenResponse

        data = TokenResponse(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh",
            expires_in=900,
        )
        assert data.access_token.startswith("eyJ")
        assert data.token_type == "bearer"
        assert data.expires_in == 900

    def test_token_response_default_type(self):
        """Test that token type defaults to bearer."""
        from edulafia.modules.auth.schemas import TokenResponse

        data = TokenResponse(
            access_token="token",
            refresh_token="refresh",
        )
        assert data.token_type == "bearer"


class TestChangePasswordRequest:
    """Test cases for ChangePasswordRequest schema."""

    def test_valid_password_change(self):
        """Test valid password change request."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        data = ChangePasswordRequest(
            current_password="OldPass1!",
            new_password="NewPass2@",
        )
        assert data.new_password == "NewPass2@"

    def test_password_requires_uppercase(self):
        """Test that password requires uppercase letter."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        with pytest.raises(ValidationError):
            ChangePasswordRequest(
                current_password="OldPass1!",
                new_password="newpass2@",
            )

    def test_password_requires_lowercase(self):
        """Test that password requires lowercase letter."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        with pytest.raises(ValidationError):
            ChangePasswordRequest(
                current_password="OldPass1!",
                new_password="NEWPASS2@",
            )

    def test_password_requires_digit(self):
        """Test that password requires digit."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        with pytest.raises(ValidationError):
            ChangePasswordRequest(
                current_password="OldPass1!",
                new_password="NewPass!@",
            )

    def test_password_requires_special_char(self):
        """Test that password requires special character."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        with pytest.raises(ValidationError):
            ChangePasswordRequest(
                current_password="OldPass1!",
                new_password="NewPass23",
            )

    def test_password_minimum_length(self):
        """Test that password must be at least 8 characters."""
        from edulafia.modules.auth.schemas import ChangePasswordRequest

        with pytest.raises(ValidationError):
            ChangePasswordRequest(
                current_password="OldPass1!",
                new_password="Np1!",
            )


class TestRefreshRequest:
    """Test cases for RefreshRequest schema."""

    def test_valid_refresh_request(self):
        """Test valid refresh request."""
        from edulafia.modules.auth.schemas import RefreshRequest

        data = RefreshRequest(refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test")
        assert data.refresh_token.startswith("eyJ")

    def test_refresh_request_requires_token(self):
        """Test that refresh request requires token."""
        from edulafia.modules.auth.schemas import RefreshRequest

        with pytest.raises(ValidationError):
            RefreshRequest(refresh_token="")


class TestUserResponse:
    """Test cases for UserResponse schema."""

    def test_valid_user_response(self):
        """Test valid user response."""
        from uuid import uuid4

        from edulafia.modules.auth.schemas import UserResponse

        data = UserResponse(
            id=uuid4(),
            email="admin@school.edu.ng",
            first_name="Admin",
            last_name="User",
            role="school_admin",
            status="active",
        )
        assert data.email == "admin@school.edu.ng"
        assert data.role == "school_admin"
