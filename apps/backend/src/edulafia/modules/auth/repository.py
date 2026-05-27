from __future__ import annotations
"""Authentication repository for user database operations."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.auth.models import User


class AuthRepository:
    """Repository for user authentication database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email address."""
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_last_login(self, user_id: UUID) -> None:
        """Update user's last login timestamp."""
        user = await self.get_by_id(user_id)
        if user:
            user.last_login_at = datetime.now(UTC)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

    async def update_password(self, user_id: UUID, password_hash: str) -> None:
        """Update user's password hash."""
        user = await self.get_by_id(user_id)
        if user:
            user.password_hash = password_hash
            self.session.add(user)
