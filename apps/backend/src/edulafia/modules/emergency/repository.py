from __future__ import annotations
"""Emergency repository for database operations."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.emergency.models import EmergencyMode


class EmergencyModeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active(self, school_id: UUID) -> EmergencyMode | None:
        stmt = select(EmergencyMode).where(
            EmergencyMode.school_id == school_id,
            EmergencyMode.status == "active",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> EmergencyMode:
        mode = EmergencyMode(**data)
        self.db.add(mode)
        await self.db.flush()
        await self.db.refresh(mode)
        return mode

    async def deactivate(self, mode_id: UUID) -> EmergencyMode | None:
        mode = await self.get_by_id(mode_id)
        if mode:
            mode.status = "resolved"
            self.db.add(mode)
        return mode

    async def get_by_id(self, mode_id: UUID) -> EmergencyMode | None:
        stmt = select(EmergencyMode).where(EmergencyMode.id == mode_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> list[EmergencyMode]:
        stmt = select(EmergencyMode).where(
            EmergencyMode.school_id == school_id
        ).order_by(EmergencyMode.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
