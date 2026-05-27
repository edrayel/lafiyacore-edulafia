from __future__ import annotations
"""Cafeteria repository for data access operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.cafeteria.models import MealPlan, MealRecord


class MealPlanRepository:
    """Repository for meal plan database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> MealPlan:
        """Create a new meal plan."""
        plan = MealPlan(**data)
        self.db.add(plan)
        await self.db.flush()
        await self.db.refresh(plan)
        return plan

    async def get_by_id(self, plan_id: UUID) -> MealPlan | None:
        """Get a meal plan by ID."""
        stmt = select(MealPlan).where(MealPlan.id == plan_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, plan_id: UUID, school_id: UUID) -> MealPlan | None:
        """Get a meal plan by ID scoped to school."""
        stmt = select(MealPlan).where(
            MealPlan.id == plan_id,
            MealPlan.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[MealPlan]:
        """List all meal plans for a school."""
        stmt = select(MealPlan).where(
            MealPlan.school_id == school_id
        ).order_by(MealPlan.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, plan: MealPlan, data: dict) -> MealPlan:
        """Update a meal plan."""
        for key, value in data.items():
            if value is not None:
                setattr(plan, key, value)
        await self.db.flush()
        await self.db.refresh(plan)
        return plan

    async def delete(self, plan: MealPlan) -> None:
        """Delete a meal plan."""
        await self.db.delete(plan)
        await self.db.flush()


class MealRecordRepository:
    """Repository for meal record database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> MealRecord:
        """Create a new meal record."""
        record = MealRecord(**data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_by_id(self, record_id: UUID) -> MealRecord | None:
        """Get a meal record by ID."""
        stmt = select(MealRecord).where(MealRecord.id == record_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_and_date(self, student_id: UUID, meal_date: date) -> MealRecord | None:
        """Get a meal record by student and date."""
        stmt = select(MealRecord).where(
            MealRecord.student_id == student_id,
            MealRecord.date == meal_date,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_student(self, student_id: UUID) -> Sequence[MealRecord]:
        """List all meal records for a student."""
        stmt = select(MealRecord).where(
            MealRecord.student_id == student_id
        ).order_by(MealRecord.date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, record: MealRecord, data: dict) -> MealRecord:
        """Update a meal record."""
        for key, value in data.items():
            if value is not None:
                setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record
