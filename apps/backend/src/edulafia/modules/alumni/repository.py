from __future__ import annotations
"""Alumni repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.alumni.models import AlumniProfile


class AlumniRepository:
    """Repository for alumni database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AlumniProfile:
        """Create a new alumni profile."""
        profile = AlumniProfile(**data)
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def get_by_id(self, profile_id: UUID) -> AlumniProfile | None:
        """Get an alumni profile by ID."""
        stmt = select(AlumniProfile).where(AlumniProfile.id == profile_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, profile_id: UUID, school_id: UUID) -> AlumniProfile | None:
        """Get an alumni profile by ID scoped to school."""
        stmt = select(AlumniProfile).where(
            AlumniProfile.id == profile_id,
            AlumniProfile.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_and_school(self, student_id: UUID, school_id: UUID) -> AlumniProfile | None:
        """Get an alumni profile by student ID scoped to school."""
        stmt = select(AlumniProfile).where(
            AlumniProfile.student_id == student_id,
            AlumniProfile.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[AlumniProfile]:
        """List all alumni profiles for a school."""
        stmt = select(AlumniProfile).where(
            AlumniProfile.school_id == school_id
        ).order_by(AlumniProfile.graduation_year.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, profile: AlumniProfile, data: dict) -> AlumniProfile:
        """Update an alumni profile."""
        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def delete(self, profile: AlumniProfile) -> None:
        """Delete an alumni profile."""
        await self.db.delete(profile)
        await self.db.flush()
