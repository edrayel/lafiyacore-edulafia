from datetime import timezone, UTC, datetime
from uuid import uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Tests require proper school setup which is currently missing")

from edulafia.core.security import hash_password
from edulafia.modules.auth.exceptions import (
    InvalidCredentialsError,
    UserDeletedError,
    UserDisabledError,
    WeakPasswordError,
)
from edulafia.modules.auth.service import AuthService


@pytest.mark.asyncio
class TestAuthService:
    async def test_login_success(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="test@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Test",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)
        result = await service.login("test@test.com", "TestPass123!")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    async def test_login_invalid_email(self, db_session):
        from edulafia.modules.auth.repository import AuthRepository

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            await service.login("nonexistent@test.com", "password")

    async def test_login_wrong_password(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="wrong@test.com",
            password_hash=hash_password("CorrectPass123!"),
            first_name="Test",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
            await service.login("wrong@test.com", "WrongPass123!")

    async def test_login_disabled_user(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="disabled@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Disabled",
            last_name="User",
            role="school_admin",
            status="inactive",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(UserDisabledError, match="disabled"):
            await service.login("disabled@test.com", "TestPass123!")

    async def test_login_deleted_user(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="deleted@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Deleted",
            last_name="User",
            role="school_admin",
            status="active",
            deleted_at=datetime.now(UTC),
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(UserDeletedError, match="deleted"):
            await service.login("deleted@test.com", "TestPass123!")

    async def test_change_password_success(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="changepass@test.com",
            password_hash=hash_password("OldPass123!"),
            first_name="Change",
            last_name="Password",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        result = await service.change_password(user_id, "OldPass123!", "NewPass123!")
        assert result["message"] == "Password changed successfully"

    async def test_change_password_wrong_current(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="wrongcurrent@test.com",
            password_hash=hash_password("CorrectPass123!"),
            first_name="Test",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(InvalidCredentialsError, match="incorrect"):
            await service.change_password(user_id, "WrongPass123!", "NewPass123!")

    async def test_change_password_same_as_current(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="samepass@test.com",
            password_hash=hash_password("SamePass123!"),
            first_name="Test",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(WeakPasswordError, match="different"):
            await service.change_password(user_id, "SamePass123!", "SamePass123!")

    async def test_get_current_user(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="getme@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Get",
            last_name="Me",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        result = await service.get_current_user(user_id)
        assert result is not None
        assert result.email == "getme@test.com"

    async def test_refresh_success(self, db_session, mocker):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_refresh_token, create_user_token_payload

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="refresh@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Refresh",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        payload = create_user_token_payload(user_id=user_id, role="school_admin", school_id=school_id)
        refresh_token = create_refresh_token(payload)

        # Mock redis functions
        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=False)
        mocker.patch("edulafia.modules.auth.service.blacklist_token", return_value=None)

        result = await service.refresh(refresh_token)
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    async def test_refresh_invalid_token(self, db_session):
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.modules.auth.exceptions import InvalidTokenError

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(InvalidTokenError, match="Invalid refresh token"):
            await service.refresh("invalid.token.here")

    async def test_refresh_blacklisted_token(self, db_session, mocker):
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_refresh_token
        from edulafia.modules.auth.exceptions import InvalidTokenError

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        refresh_token = create_refresh_token({"sub": str(uuid4())})

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=True)

        with pytest.raises(InvalidTokenError, match="revoked"):
            await service.refresh(refresh_token)

    async def test_refresh_wrong_type(self, db_session, mocker):
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_access_token
        from edulafia.modules.auth.exceptions import InvalidTokenError

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        access_token = create_access_token({"sub": str(uuid4())})

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=False)

        with pytest.raises(InvalidTokenError, match="not a refresh token"):
            await service.refresh(access_token)

    async def test_refresh_user_disabled(self, db_session, mocker):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_refresh_token
        from edulafia.modules.auth.exceptions import UserDisabledError

        user_id = uuid4()
        user = User(
            id=user_id,
            school_id=uuid4(),
            email="refresh_disabled@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Refresh",
            last_name="Disabled",
            role="school_admin",
            status="inactive",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        refresh_token = create_refresh_token({"sub": str(user_id)})

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=False)

        with pytest.raises(UserDisabledError, match="disabled"):
            await service.refresh(refresh_token)

    async def test_reset_password_weak_password(self, db_session, mocker):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_access_token
        from edulafia.modules.auth.exceptions import WeakPasswordError

        user_id = uuid4()
        user = User(
            id=user_id,
            school_id=uuid4(),
            email="resetweak@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Reset",
            last_name="Weak",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        reset_token = create_access_token({"sub": str(user_id), "type": "reset"})

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=False)

        with pytest.raises(WeakPasswordError):
            await service.reset_password(reset_token, "weak")

    async def test_token_timezone_correctness(self, db_session):
        from edulafia.core.security import create_access_token, decode_token
        from datetime import datetime, timezone, timedelta
        
        # Ensure token expiration is exactly as expected in UTC
        data = {"sub": str(uuid4())}
        delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta=delta)
        
        decoded = decode_token(token)
        exp = decoded["exp"]
        
        # Get current time in UTC
        now = datetime.now(timezone.utc).timestamp()
        
        # Expiration should be ~15 minutes from now
        assert exp > now + 14 * 60
        assert exp < now + 16 * 60

    async def test_invalid_input_login(self, db_session):
        from edulafia.modules.auth.repository import AuthRepository
        repo = AuthRepository(db_session)
        service = AuthService(repo)
        
        with pytest.raises(InvalidCredentialsError):
            await service.login("", "")

    async def test_reset_password_invalid_token(self, db_session):
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.modules.auth.exceptions import InvalidTokenError

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        with pytest.raises(InvalidTokenError):
            await service.reset_password("badtoken", "StrongPass123!@#")

    async def test_reset_password_blacklisted_token(self, db_session, mocker):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_access_token
        from edulafia.modules.auth.exceptions import InvalidTokenError
        from datetime import timedelta

        user_id = uuid4()
        user = User(
            id=user_id,
            school_id=uuid4(),
            email="resetblacklisted@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Reset",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        reset_token = create_access_token(
            {"sub": str(user_id), "type": "reset"},
            expires_delta=timedelta(hours=1)
        )

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=True)

        with pytest.raises(InvalidTokenError, match="revoked"):
            await service.reset_password(reset_token, "NewPass123!@#")

    async def test_forgot_password(self, db_session):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository

        user_id = uuid4()
        user = User(
            id=user_id,
            school_id=uuid4(),
            email="forgot@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Forgot",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        result = await service.forgot_password("forgot@test.com")
        assert "If an account exists" in result["message"]

        # Even if user doesn't exist, we get the same message
        result2 = await service.forgot_password("nonexistent@test.com")
        assert "If an account exists" in result2["message"]

    async def test_reset_password_success(self, db_session, mocker):
        from edulafia.modules.auth.models import User
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_access_token
        from datetime import timedelta

        user_id = uuid4()
        user = User(
            id=user_id,
            school_id=uuid4(),
            email="reset@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Reset",
            last_name="User",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        reset_token = create_access_token(
            {"sub": str(user_id), "type": "reset"},
            expires_delta=timedelta(hours=1)
        )

        mocker.patch("edulafia.modules.auth.service.is_blacklisted", return_value=False)
        mocker.patch("edulafia.modules.auth.service.blacklist_token", return_value=None)

        result = await service.reset_password(reset_token, "NewPass123!@#")
        assert result["message"] == "Password reset successfully"

    async def test_logout_success(self, db_session, mocker):
        from edulafia.modules.auth.repository import AuthRepository
        from edulafia.core.security import create_access_token

        repo = AuthRepository(db_session)
        service = AuthService(repo)

        access_token = create_access_token({"sub": str(uuid4()), "type": "access"})
        refresh_token = create_access_token({"sub": str(uuid4()), "type": "refresh"})

        mocker.patch("edulafia.modules.auth.service.blacklist_token", return_value=None)

        result = await service.logout(access_token, refresh_token)
        assert result["message"] == "Logged out successfully"

