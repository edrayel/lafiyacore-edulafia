from __future__ import annotations
"""WAEC bulk repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.waec_bulk.models import WAECBulkRegistration


class WAECBulkRegistrationRepository:
    """Repository for WAEC bulk registration database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> WAECBulkRegistration:
        """Create a new WAEC bulk registration."""
        registration = WAECBulkRegistration(**data)
        self.db.add(registration)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def get_by_id(self, registration_id: UUID) -> WAECBulkRegistration | None:
        """Get a WAEC bulk registration by ID."""
        stmt = select(WAECBulkRegistration).where(WAECBulkRegistration.id == registration_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, registration_id: UUID, school_id: UUID) -> WAECBulkRegistration | None:
        """Get a WAEC bulk registration by ID scoped to school."""
        stmt = select(WAECBulkRegistration).where(
            WAECBulkRegistration.id == registration_id,
            WAECBulkRegistration.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[WAECBulkRegistration]:
        """List all WAEC bulk registrations for a school."""
        stmt = select(WAECBulkRegistration).where(
            WAECBulkRegistration.school_id == school_id
        ).order_by(WAECBulkRegistration.exam_year.desc(), WAECBulkRegistration.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_school_and_year(self, school_id: UUID, exam_year: int) -> Sequence[WAECBulkRegistration]:
        """List WAEC bulk registrations for a school by year."""
        stmt = select(WAECBulkRegistration).where(
            WAECBulkRegistration.school_id == school_id,
            WAECBulkRegistration.exam_year == exam_year,
        ).order_by(WAECBulkRegistration.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, registration: WAECBulkRegistration, data: dict) -> WAECBulkRegistration:
        """Update a WAEC bulk registration."""
        for key, value in data.items():
            if value is not None:
                setattr(registration, key, value)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def delete(self, registration: WAECBulkRegistration) -> None:
        """Delete a WAEC bulk registration."""
        await self.db.delete(registration)
        await self.db.flush()
