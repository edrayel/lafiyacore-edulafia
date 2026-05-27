from __future__ import annotations
"""Inspection tracking repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.inspection_tracking.models import SchoolInspection


class SchoolInspectionRepository:
    """Repository for school inspection database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SchoolInspection:
        """Create a new school inspection."""
        inspection = SchoolInspection(**data)
        self.db.add(inspection)
        await self.db.flush()
        await self.db.refresh(inspection)
        return inspection

    async def get_by_id(self, inspection_id: UUID) -> SchoolInspection | None:
        """Get a school inspection by ID."""
        stmt = select(SchoolInspection).where(SchoolInspection.id == inspection_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[SchoolInspection]:
        """List all inspections for a school."""
        stmt = select(SchoolInspection).where(
            SchoolInspection.school_id == school_id
        ).order_by(SchoolInspection.inspection_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_status(self, status: str) -> Sequence[SchoolInspection]:
        """List inspections by status."""
        stmt = select(SchoolInspection).where(
            SchoolInspection.status == status
        ).order_by(SchoolInspection.inspection_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, inspection: SchoolInspection, data: dict) -> SchoolInspection:
        """Update a school inspection."""
        for key, value in data.items():
            if value is not None:
                setattr(inspection, key, value)
        await self.db.flush()
        await self.db.refresh(inspection)
        return inspection

    async def delete(self, inspection: SchoolInspection) -> None:
        """Delete a school inspection."""
        await self.db.delete(inspection)
        await self.db.flush()
