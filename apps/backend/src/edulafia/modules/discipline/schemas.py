"""Discipline Pydantic schemas."""

from datetime import date as DateType
from datetime import datetime
from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DisciplineRecordBase(BaseModel):
    """Base schema for discipline record."""

    student_id: UUID = Field(..., description="ID of the student")
    date: DateType = Field(...)
    offense_type: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    action_taken: str = Field(...)
    reported_by: str = Field(..., min_length=1, max_length=255)
    parent_notified: bool = Field(default=False)
    follow_up_date: DateType | None = Field(None)
    status: str = Field(default="open")


class DisciplineRecordCreate(DisciplineRecordBase):
    """Schema for creating a discipline record."""

    pass


class DisciplineRecordUpdate(BaseModel):
    """Schema for updating a discipline record."""

    model_config = ConfigDict(from_attributes=True)

    offense_type: str | None = Field(None, max_length=100)
    description: str | None = Field(None, min_length=1)
    action_taken: str | None = None
    reported_by: str | None = Field(None, max_length=255)
    parent_notified: bool | None = None
    follow_up_date: DateType | None = None
    status: str | None = None


class DisciplineRecordResponse(BaseModel):
    """Schema for discipline record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    date: DateType
    offense_type: str
    description: str
    action_taken: str
    reported_by: str
    parent_notified: bool
    follow_up_date: DateType | None = None
    status: str
    created_at: datetime
    updated_at: datetime


class RecordUpdateRequest(BaseModel):
    incident_type: str | None = Field(None, max_length=100)
    description: str | None = None
    action_taken: str | None = None
    severity: str | None = Field(None, max_length=20)
    incident_date: date | None = None
