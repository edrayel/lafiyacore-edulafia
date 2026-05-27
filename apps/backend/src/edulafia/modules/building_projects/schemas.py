"""Building projects Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    """Base schema for building project."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    type: str = Field(...)
    budget: float = Field(default=0.0, ge=0)
    start_date: date = Field(...)
    end_date: date | None = Field(None)
    contractor: str | None = Field(None, max_length=255)
    status: str = Field(default="planned")
    progress_percent: int = Field(default=0, ge=0, le=100)


class ProjectCreate(ProjectBase):
    """Schema for creating a building project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a building project."""

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=1000)
    type: str | None = None
    budget: float | None = Field(None, ge=0)
    start_date: date | None = None
    end_date: date | None = None
    contractor: str | None = Field(None, max_length=255)
    status: str | None = None
    progress_percent: int | None = Field(None, ge=0, le=100)


class ProjectResponse(BaseModel):
    """Schema for building project response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    type: str
    budget: float
    start_date: date
    end_date: date | None = None
    contractor: str | None = None
    status: str
    progress_percent: int
    created_at: datetime
    updated_at: datetime


class ProjectUpdateRequest(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    target_amount: float | None = Field(None, gt=0)
    status: str | None = Field(None, description="e.g., planning, ongoing, completed")
    end_date: date | None = None
