from __future__ import annotations
"""Discipline repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.discipline.models import DisciplineRecord


class DisciplineRecordRepository:
    """Repository for discipline record database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> DisciplineRecord:
        """Create a new discipline record."""
        record = DisciplineRecord(**data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_by_id(self, record_id: UUID) -> DisciplineRecord | None:
        """Get a discipline record by ID."""
        stmt = select(DisciplineRecord).where(DisciplineRecord.id == record_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_student(self, student_id: UUID) -> Sequence[DisciplineRecord]:
        """List all discipline records for a student."""
        stmt = select(DisciplineRecord).where(
            DisciplineRecord.student_id == student_id
        ).order_by(DisciplineRecord.date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_open(self) -> Sequence[DisciplineRecord]:
        """List all open discipline records."""
        stmt = select(DisciplineRecord).where(
            DisciplineRecord.status == "open"
        ).order_by(DisciplineRecord.date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, record: DisciplineRecord, data: dict) -> DisciplineRecord:
        """Update a discipline record."""
        for key, value in data.items():
            if value is not None:
                setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def delete(self, record: DisciplineRecord) -> None:
        """Delete a discipline record."""
        await self.db.delete(record)
        await self.db.flush()
