"""LMS Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssignmentBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    due_date: datetime
    class_id: UUID
    subject_id: UUID
    file_path: str | None = None


class CourseUpdateRequest(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    is_published: bool | None = None


class AssignmentCreate(BaseModel):
    course_id: UUID
    title: str = Field(..., max_length=200)
    description: str | None = None
    due_date: datetime | None = None
    max_score: float | None = Field(None, gt=0)


class AssignmentUpdateRequest(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    due_date: datetime | None = None
    max_score: float | None = Field(None, gt=0)


class AssignmentResponse(AssignmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime


class SubmissionBase(BaseModel):
    assignment_id: UUID
    student_id: UUID
    file_path: str | None = None
    grade: float | None = None
    feedback: str | None = None


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdateRequest(BaseModel):
    score: float | None = Field(None, ge=0)
    feedback: str | None = None
    is_graded: bool | None = None


class SubmissionResponse(SubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime