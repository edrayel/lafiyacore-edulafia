"""Cafeteria service for business logic operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from edulafia.modules.cafeteria.repository import MealPlanRepository, MealRecordRepository
from edulafia.modules.cafeteria.schemas import (
    MealPlanCreate,
    MealPlanResponse,
    MealPlanUpdate,
    MealRecordCreate,
    MealRecordResponse,
)


class MealPlanService:
    """Service for meal plan business logic."""

    def __init__(self, repository: MealPlanRepository):
        self.repository = repository

    async def create(self, data: MealPlanCreate, user_id: UUID) -> MealPlanResponse:
        """Create a new meal plan."""
        plan_data = data.model_dump()
        plan = await self.repository.create(plan_data)
        return MealPlanResponse.model_validate(plan)

    async def get_by_id(self, plan_id: UUID, school_id: UUID) -> MealPlanResponse | None:
        """Get a meal plan by ID."""
        plan = await self.repository.get_by_id_and_school(plan_id, school_id)
        if plan:
            return MealPlanResponse.model_validate(plan)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[MealPlanResponse]:
        """List all meal plans for a school."""
        plans = await self.repository.list_by_school(school_id)
        return [MealPlanResponse.model_validate(p) for p in plans]

    async def update(self, plan_id: UUID, data: MealPlanUpdate, school_id: UUID, user_id: UUID) -> MealPlanResponse:
        """Update a meal plan."""
        plan = await self.repository.get_by_id_and_school(plan_id, school_id)
        if not plan:
            raise ValueError(f"Meal plan {plan_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_plan = await self.repository.update(plan, update_data)
        return MealPlanResponse.model_validate(updated_plan)



    async def delete(self, plan_id: UUID, school_id: UUID) -> None:
        """Delete a record."""
        record = await self.repository.get_by_id_and_school(plan_id, school_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
class MealRecordService:
    """Service for meal record business logic."""

    def __init__(self, repository: MealRecordRepository, plan_repository: MealPlanRepository):
        self.repository = repository
        self.plan_repository = plan_repository

    async def create(self, data: MealRecordCreate, user_id: UUID) -> MealRecordResponse:
        """Create a new meal record."""
        plan = await self.plan_repository.get_by_id(data.meal_plan_id)
        if not plan:
            raise ValueError(f"Meal plan {data.meal_plan_id} not found")

        record_data = data.model_dump()
        record = await self.repository.create(record_data)
        return MealRecordResponse.model_validate(record)

    async def get_by_student_and_date(self, student_id: UUID, meal_date: date) -> MealRecordResponse | None:
        """Get a meal record by student and date."""
        record = await self.repository.get_by_student_and_date(student_id, meal_date)
        if record:
            return MealRecordResponse.model_validate(record)
        return None

    async def list_by_student(self, student_id: UUID) -> Sequence[MealRecordResponse]:
        """List all meal records for a student."""
        records = await self.repository.list_by_student(student_id)
        return [MealRecordResponse.model_validate(r) for r in records]

    async def mark_served(self, record_id: UUID) -> MealRecordResponse:
        """Mark a meal as served."""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Meal record {record_id} not found")

        update_data = {"served": True}
        updated_record = await self.repository.update(record, update_data)
        return MealRecordResponse.model_validate(updated_record)
