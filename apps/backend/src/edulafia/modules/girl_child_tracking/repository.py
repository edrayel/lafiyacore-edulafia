from __future__ import annotations
"""Girl child tracking repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.girl_child_tracking.models import GirlChildRecord


class GirlChildRecordRepository:
    """Repository for girl child record database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> GirlChildRecord:
        """Create a new girl child record."""
        record = GirlChildRecord(**data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_by_id(self, record_id: UUID) -> GirlChildRecord | None:
        """Get a girl child record by ID."""
        stmt = select(GirlChildRecord).where(GirlChildRecord.id == record_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_id(self, student_id: UUID) -> GirlChildRecord | None:
        """Get a girl child record by student ID."""
        stmt = select(GirlChildRecord).where(
            GirlChildRecord.student_id == student_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_dropout_risk(self, risk_level: str) -> Sequence[GirlChildRecord]:
        """List girl child records by dropout risk level."""
        stmt = select(GirlChildRecord).where(
            GirlChildRecord.dropout_risk == risk_level
        ).order_by(GirlChildRecord.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, record: GirlChildRecord, data: dict) -> GirlChildRecord:
        """Update a girl child record."""
        for key, value in data.items():
            if value is not None:
                setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def delete(self, record: GirlChildRecord) -> None:
        """Delete a girl child record."""
        await self.db.delete(record)
        await self.db.flush()
