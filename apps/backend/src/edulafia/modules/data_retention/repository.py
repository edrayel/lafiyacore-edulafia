from __future__ import annotations
"""Data retention repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.data_retention.models import DataArchive, RetentionPolicy


class RetentionPolicyRepository:
    """Repository for retention policy database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> RetentionPolicy:
        """Create a new retention policy."""
        policy = RetentionPolicy(**data)
        self.db.add(policy)
        await self.db.flush()
        await self.db.refresh(policy)
        return policy

    async def get_by_id(self, policy_id: UUID) -> RetentionPolicy | None:
        """Get a retention policy by ID."""
        stmt = select(RetentionPolicy).where(RetentionPolicy.id == policy_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_school_and_type(self, school_id: UUID, data_type: str) -> RetentionPolicy | None:
        """Get a retention policy by school and data type."""
        stmt = select(RetentionPolicy).where(
            RetentionPolicy.school_id == school_id,
            RetentionPolicy.data_type == data_type,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[RetentionPolicy]:
        """List all retention policies for a school."""
        stmt = select(RetentionPolicy).where(
            RetentionPolicy.school_id == school_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, policy: RetentionPolicy, data: dict) -> RetentionPolicy:
        """Update a retention policy."""
        for key, value in data.items():
            if value is not None:
                setattr(policy, key, value)
        await self.db.flush()
        await self.db.refresh(policy)
        return policy

    async def delete(self, policy: RetentionPolicy) -> None:
        """Delete a retention policy."""
        await self.db.delete(policy)
        await self.db.flush()


class DataArchiveRepository:
    """Repository for data archive database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> DataArchive:
        """Create a new data archive."""
        archive = DataArchive(**data)
        self.db.add(archive)
        await self.db.flush()
        await self.db.refresh(archive)
        return archive

    async def get_by_id(self, archive_id: UUID) -> DataArchive | None:
        """Get a data archive by ID."""
        stmt = select(DataArchive).where(DataArchive.id == archive_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[DataArchive]:
        """List all data archives for a school."""
        stmt = select(DataArchive).where(
            DataArchive.school_id == school_id
        ).order_by(DataArchive.archived_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_status(self, status: str) -> Sequence[DataArchive]:
        """List data archives by status."""
        stmt = select(DataArchive).where(
            DataArchive.status == status
        ).order_by(DataArchive.archived_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, archive: DataArchive, data: dict) -> DataArchive:
        """Update a data archive."""
        for key, value in data.items():
            if value is not None:
                setattr(archive, key, value)
        await self.db.flush()
        await self.db.refresh(archive)
        return archive

    async def delete(self, archive: DataArchive) -> None:
        """Delete a data archive."""
        await self.db.delete(archive)
        await self.db.flush()
