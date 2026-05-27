"""Tests for AuthService - TDD implementation."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest


def make_user_mock(
    id=None,
    email="admin@school.edu.ng",
    password_hash="$2b$12$dummy_hashed_password",
    first_name="Admin",
    last_name="User",
    role="school_admin",
    status="active",
    school_id=None,
    deleted_at=None,
    last_login_at=None,
):
    """Create a properly configured User mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = school_id or uuid4()
    mock.email = email
    mock.phone = None
    mock.password_hash = password_hash
    mock.first_name = first_name
    mock.last_name = last_name
    mock.role = role
    mock.status = status
    mock.last_login_at = last_login_at
    mock.mfa_enabled = False
    mock.mfa_secret = None
    mock.deleted_at = deleted_at
    mock.created_at = datetime(2026, 1, 15, tzinfo=UTC)
    mock.updated_at = datetime(2026, 1, 15, tzinfo=UTC)
    return mock


@pytest.fixture
def mock_repository():
    """Create a mock auth repository."""
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repository):
    """Create AuthService with mocked repository."""
    from edulafia.modules.auth.service import AuthService
    return AuthService(repository=mock_repository)


class TestAuthServiceLogin:
    """Test cases for AuthService.login()"""

    async def test_login_success(self, service, mock_repository):
        """Test successful login returns tokens and user."""
        user = make_user_mock(
            email="admin@school.edu.ng",
            role="school_admin",
        )
        mock_repository.get_by_email.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=True):
            result = await service.login("admin@school.edu.ng", "Password1!")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"
        assert result["expires_in"] == 15 * 60
        assert result["user"] == user
        mock_repository.update_last_login.assert_called_once_with(user.id)

    async def test_login_invalid_email(self, service, mock_repository):
        """Test login with non-existent email raises error."""
        from edulafia.modules.auth.exceptions import InvalidCredentialsError

        mock_repository.get_by_email.return_value = None

        with pytest.raises(InvalidCredentialsError):
            await service.login("nonexistent@school.edu.ng", "Password1!")

    async def test_login_wrong_password(self, service, mock_repository):
        """Test login with wrong password raises error."""
        from edulafia.modules.auth.exceptions import InvalidCredentialsError

        user = make_user_mock()
        mock_repository.get_by_email.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=False):
            with pytest.raises(InvalidCredentialsError):
                await service.login("admin@school.edu.ng", "WrongPass1!")

    async def test_login_disabled_account(self, service, mock_repository):
        """Test login with disabled account raises error."""
        from edulafia.modules.auth.exceptions import UserDisabledError

        user = make_user_mock(status="disabled")
        mock_repository.get_by_email.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=True):
            with pytest.raises(UserDisabledError):
                await service.login("admin@school.edu.ng", "Password1!")

    async def test_login_deleted_account(self, service, mock_repository):
        """Test login with deleted account raises error."""
        from edulafia.modules.auth.exceptions import UserDeletedError

        user = make_user_mock(deleted_at=datetime.now(UTC))
        mock_repository.get_by_email.return_value = user

        with pytest.raises(UserDeletedError):
            await service.login("admin@school.edu.ng", "Password1!")

    async def test_login_updates_last_login(self, service, mock_repository):
        """Test that successful login updates last_login_at."""
        user = make_user_mock()
        mock_repository.get_by_email.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=True):
            await service.login("admin@school.edu.ng", "Password1!")

        mock_repository.update_last_login.assert_called_once_with(user.id)


class TestAuthServiceRefresh:
    """Test cases for AuthService.refresh()"""

    async def test_refresh_success(self, service, mock_repository):
        """Test successful token refresh."""
        user = make_user_mock()
        mock_repository.get_by_id.return_value = user

        with patch("edulafia.modules.auth.service.decode_token") as mock_decode:
            mock_decode.return_value = {
                "sub": str(user.id),
                "role": "school_admin",
                "school_id": str(user.school_id),
                "type": "refresh",
            }

            result = await service.refresh("valid_refresh_token")

            assert "access_token" in result
            assert "refresh_token" in result
            assert result["token_type"] == "bearer"

    async def test_refresh_invalid_token(self, service, mock_repository):
        """Test refresh with invalid token raises error."""
        from edulafia.modules.auth.exceptions import InvalidTokenError

        with patch("edulafia.modules.auth.service.decode_token", side_effect=ValueError):
            with pytest.raises(InvalidTokenError):
                await service.refresh("invalid_token")

    async def test_refresh_wrong_token_type(self, service, mock_repository):
        """Test refresh with access token instead of refresh raises error."""
        from edulafia.modules.auth.exceptions import InvalidTokenError

        with patch("edulafia.modules.auth.service.decode_token") as mock_decode:
            mock_decode.return_value = {
                "sub": str(uuid4()),
                "role": "school_admin",
                "type": "access",
            }

            with pytest.raises(InvalidTokenError):
                await service.refresh("access_token_not_refresh")

    async def test_refresh_deleted_user(self, service, mock_repository):
        """Test refresh for deleted user raises error."""
        from edulafia.modules.auth.exceptions import InvalidTokenError

        mock_repository.get_by_id.return_value = None

        with patch("edulafia.modules.auth.service.decode_token") as mock_decode:
            mock_decode.return_value = {
                "sub": str(uuid4()),
                "role": "school_admin",
                "type": "refresh",
            }

            with pytest.raises(InvalidTokenError):
                await service.refresh("token_for_deleted_user")

    async def test_refresh_disabled_user(self, service, mock_repository):
        """Test refresh for disabled user raises error."""
        from edulafia.modules.auth.exceptions import UserDisabledError

        user = make_user_mock(status="disabled")
        mock_repository.get_by_id.return_value = user

        with patch("edulafia.modules.auth.service.decode_token") as mock_decode:
            mock_decode.return_value = {
                "sub": str(user.id),
                "role": "school_admin",
                "type": "refresh",
            }

            with pytest.raises(UserDisabledError):
                await service.refresh("token_for_disabled_user")


class TestAuthServiceChangePassword:
    """Test cases for AuthService.change_password()"""

    async def test_change_password_success(self, service, mock_repository):
        """Test successful password change."""
        user = make_user_mock()
        mock_repository.get_by_id.return_value = user

        with patch("edulafia.modules.auth.service.verify_password") as mock_verify:
            with patch("edulafia.modules.auth.service.hash_password", return_value="new_hash"):
                # First call: current password check (True)
                # Second call: new password same check (False)
                mock_verify.side_effect = [True, False]

                result = await service.change_password(
                    user_id=user.id,
                    current_password="OldPass1!",
                    new_password="NewPass2!",
                )

                assert result["message"] == "Password changed successfully"
                mock_repository.update_password.assert_called_once_with(user.id, "new_hash")

    async def test_change_password_wrong_current(self, service, mock_repository):
        """Test change password with wrong current password raises error."""
        from edulafia.modules.auth.exceptions import InvalidCredentialsError

        user = make_user_mock()
        mock_repository.get_by_id.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=False):
            with pytest.raises(InvalidCredentialsError):
                await service.change_password(
                    user_id=user.id,
                    current_password="WrongPass1!",
                    new_password="NewPass2!",
                )

    async def test_change_password_same_as_old(self, service, mock_repository):
        """Test change password with same password raises error."""
        from edulafia.modules.auth.exceptions import WeakPasswordError

        user = make_user_mock()
        mock_repository.get_by_id.return_value = user

        with patch("edulafia.modules.auth.service.verify_password", return_value=True):
            with pytest.raises(WeakPasswordError):
                await service.change_password(
                    user_id=user.id,
                    current_password="SamePass1!",
                    new_password="SamePass1!",
                )


class TestAuthServiceGetCurrentUser:
    """Test cases for AuthService.get_current_user()"""

    async def test_get_current_user_success(self, service, mock_repository):
        """Test getting current user by ID."""
        user = make_user_mock()
        mock_repository.get_by_id.return_value = user

        result = await service.get_current_user(user.id)

        assert result == user
        mock_repository.get_by_id.assert_called_once_with(user.id)

    async def test_get_current_user_not_found(self, service, mock_repository):
        """Test getting non-existent user returns None."""
        mock_repository.get_by_id.return_value = None

        result = await service.get_current_user(uuid4())

        assert result is None
