"""Cafeteria Pydantic schemas."""

from datetime import date as DateType
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MealPlanBase(BaseModel):
    """Base schema for meal plan."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)
    price: float = Field(default=0.0, ge=0)
    is_active: bool = Field(default=True)


class MealPlanCreate(MealPlanBase):
    """Schema for creating a meal plan."""

    pass


class MealPlanUpdate(BaseModel):
    """Schema for updating a meal plan."""

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, ge=0)
    is_active: bool | None = None


class MealPlanResponse(BaseModel):
    """Schema for meal plan response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


class MealRecordBase(BaseModel):
    """Base schema for meal record."""

    student_id: UUID = Field(..., description="ID of the student")
    meal_plan_id: UUID = Field(..., description="ID of the meal plan")
    date: DateType = Field(...)
    served: bool = Field(default=False)


class MealPlanUpdateRequest(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    price_per_term: float | None = Field(None, gt=0)
    is_active: bool | None = None


class MealRecordCreate(BaseModel):
    student_id: UUID
    meal_plan_id: UUID
    date: DateType
    meal_type: str = Field(..., description="e.g., breakfast, lunch")


class MealRecordResponse(MealRecordCreate):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MealRecordUpdateRequest(BaseModel):
    meal_type: str | None = Field(None, description="e.g., breakfast, lunch")
    date: DateType | None = None
