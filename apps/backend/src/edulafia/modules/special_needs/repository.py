from __future__ import annotations
"""Special needs / IEP repository."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.special_needs.models import IndividualEducationPlan


class IEPRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_student(self, student_id: UUID) -> IndividualEducationPlan | None:
        stmt = select(IndividualEducationPlan).where(IndividualEducationPlan.student_id == student_id).order_by(IndividualEducationPlan.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_by_school(self, school_id: UUID) -> list[IndividualEducationPlan]:
        stmt = select(IndividualEducationPlan).where(IndividualEducationPlan.school_id == school_id).order_by(IndividualEducationPlan.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, data: dict) -> IndividualEducationPlan:
        iep = IndividualEducationPlan(**data)
        self.db.add(iep)
        await self.db.flush()
        await self.db.refresh(iep)
        return iep

    async def update(self, iep: IndividualEducationPlan, data: dict) -> IndividualEducationPlan:
        for k, v in data.items():
            setattr(iep, k, v)
        self.db.add(iep)
        await self.db.flush()
        await self.db.refresh(iep)
        return iep
