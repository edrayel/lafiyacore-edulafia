from __future__ import annotations
"""Accreditation repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.accreditation.models import AccreditationChecklist


class AccreditationChecklistRepository:
    """Repository for accreditation checklist database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AccreditationChecklist:
        """Create a new accreditation checklist."""
        checklist = AccreditationChecklist(**data)
        self.db.add(checklist)
        await self.db.flush()
        await self.db.refresh(checklist)
        return checklist

    async def get_by_id(self, checklist_id: UUID) -> AccreditationChecklist | None:
        """Get an accreditation checklist by ID."""
        stmt = select(AccreditationChecklist).where(AccreditationChecklist.id == checklist_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[AccreditationChecklist]:
        """List all checklists for a school."""
        stmt = select(AccreditationChecklist).where(
            AccreditationChecklist.school_id == school_id
        ).order_by(AccreditationChecklist.category, AccreditationChecklist.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_school_and_category(self, school_id: UUID, category: str) -> Sequence[AccreditationChecklist]:
        """List checklists for a school by category."""
        stmt = select(AccreditationChecklist).where(
            AccreditationChecklist.school_id == school_id,
            AccreditationChecklist.category == category,
        ).order_by(AccreditationChecklist.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, checklist: AccreditationChecklist, data: dict) -> AccreditationChecklist:
        """Update an accreditation checklist."""
        for key, value in data.items():
            if value is not None:
                setattr(checklist, key, value)
        await self.db.flush()
        await self.db.refresh(checklist)
        return checklist

    async def delete(self, checklist: AccreditationChecklist) -> None:
        """Delete an accreditation checklist."""
        await self.db.delete(checklist)
        await self.db.flush()
