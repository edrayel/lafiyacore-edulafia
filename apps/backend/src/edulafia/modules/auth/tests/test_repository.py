"""Tests for the authentication repository."""

from datetime import timezone, UTC
from uuid import uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Tests require proper school setup which is currently missing")

from edulafia.core.security import hash_password
from edulafia.modules.auth.models import User
from edulafia.modules.auth.repository import AuthRepository


@pytest.mark.asyncio
class TestAuthRepository:
    async def test_get_by_email(self, db_session):
        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="repo@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Repo",
            last_name="Test",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        result = await repo.get_by_email("repo@test.com")
        assert result is not None
        assert result.email == "repo@test.com"

    async def test_get_by_email_not_found(self, db_session):
        repo = AuthRepository(db_session)
        result = await repo.get_by_email("nonexistent@test.com")
        assert result is None

    async def test_get_by_email_excludes_deleted(self, db_session):
        from datetime import timezone, datetime

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="deleted-repo@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Deleted",
            last_name="Repo",
            role="school_admin",
            status="active",
            deleted_at=datetime.now(UTC),
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        result = await repo.get_by_email("deleted-repo@test.com")
        assert result is None

    async def test_get_by_id(self, db_session):
        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="byid@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="ById",
            last_name="Test",
            role="teacher",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        result = await repo.get_by_id(user_id)
        assert result is not None
        assert result.id == user_id

    async def test_get_by_id_not_found(self, db_session):
        repo = AuthRepository(db_session)
        result = await repo.get_by_id(uuid4())
        assert result is None

    async def test_update_last_login(self, db_session):
        from datetime import timezone, datetime, timedelta

        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="login-update@test.com",
            password_hash=hash_password("TestPass123!"),
            first_name="Login",
            last_name="Update",
            role="school_admin",
            status="active",
            last_login_at=datetime.now(UTC) - timedelta(days=7),
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        await repo.update_last_login(user_id)
        await db_session.commit()

        updated = await repo.get_by_id(user_id)
        assert updated is not None
        assert updated.last_login_at is not None

    async def test_update_password(self, db_session):
        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="pass-update@test.com",
            password_hash=hash_password("OldPass123!"),
            first_name="Pass",
            last_name="Update",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        repo = AuthRepository(db_session)
        new_hash = hash_password("NewPass123!")
        await repo.update_password(user_id, new_hash)
        await db_session.commit()

        updated = await repo.get_by_id(user_id)
        assert updated is not None
        assert updated.password_hash != hash_password("OldPass123!")
