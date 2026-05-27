from __future__ import annotations
"""Clubs repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.clubs.models import Club, ClubMembership


class ClubRepository:
    """Repository for club database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Club:
        """Create a new club."""
        club = Club(**data)
        self.db.add(club)
        await self.db.flush()
        await self.db.refresh(club)
        return club

    async def get_by_id(self, club_id: UUID) -> Club | None:
        """Get a club by ID."""
        stmt = select(Club).where(Club.id == club_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, club_id: UUID, school_id: UUID) -> Club | None:
        """Get a club by ID scoped to school."""
        stmt = select(Club).where(
            Club.id == club_id,
            Club.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[Club]:
        """List all clubs for a school."""
        stmt = select(Club).where(
            Club.school_id == school_id
        ).order_by(Club.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, club: Club, data: dict) -> Club:
        """Update a club."""
        for key, value in data.items():
            if value is not None:
                setattr(club, key, value)
        await self.db.flush()
        await self.db.refresh(club)
        return club

    async def delete(self, club: Club) -> None:
        """Delete a club."""
        await self.db.delete(club)
        await self.db.flush()


class ClubMembershipRepository:
    """Repository for club membership database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ClubMembership:
        """Create a new club membership."""
        membership = ClubMembership(**data)
        self.db.add(membership)
        await self.db.flush()
        await self.db.refresh(membership)
        return membership

    async def get_by_id(self, membership_id: UUID) -> ClubMembership | None:
        """Get a membership by ID."""
        stmt = select(ClubMembership).where(ClubMembership.id == membership_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_club_and_student(self, club_id: UUID, student_id: UUID) -> ClubMembership | None:
        """Get a membership by club and student."""
        stmt = select(ClubMembership).where(
            ClubMembership.club_id == club_id,
            ClubMembership.student_id == student_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_club(self, club_id: UUID) -> Sequence[ClubMembership]:
        """List all memberships for a club."""
        stmt = select(ClubMembership).where(
            ClubMembership.club_id == club_id
        ).order_by(ClubMembership.joined_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_student(self, student_id: UUID) -> Sequence[ClubMembership]:
        """List all memberships for a student."""
        stmt = select(ClubMembership).where(
            ClubMembership.student_id == student_id
        ).order_by(ClubMembership.joined_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, membership: ClubMembership, data: dict) -> ClubMembership:
        """Update a club membership."""
        for key, value in data.items():
            if value is not None:
                setattr(membership, key, value)
        await self.db.flush()
        await self.db.refresh(membership)
        return membership

    async def delete(self, membership: ClubMembership) -> None:
        """Delete a club membership."""
        await self.db.delete(membership)
        await self.db.flush()
