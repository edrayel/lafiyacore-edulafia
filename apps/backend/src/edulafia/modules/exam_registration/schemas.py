"""Exam registration Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExamRegistrationBase(BaseModel):
    """Base schema for exam registration."""

    school_id: UUID = Field(..., description="ID of the school")
    exam_type: str = Field(...)
    year: int = Field(..., ge=2000)
    student_id: UUID = Field(..., description="ID of the student")
    candidate_number: str | None = Field(None, max_length=50)
    subjects: list = Field(default_factory=list)
    status: str = Field(default="registered")
    registration_date: date = Field(...)


class ExamRegistrationCreate(ExamRegistrationBase):
    """Schema for creating an exam registration."""

    pass


class ExamRegistrationUpdate(BaseModel):
    """Schema for updating an exam registration."""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(None, max_length=50)
    subjects: list[str] | None = None
    exam_number: str | None = Field(None, max_length=50)
    is_paid: bool | None = None


class ExamRegistrationResponse(BaseModel):
    """Schema for exam registration response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    exam_type: str
    year: int
    student_id: UUID
    candidate_number: str | None = None
    subjects: list
    status: str
    registration_date: date
    created_at: datetime
    updated_at: datetime
