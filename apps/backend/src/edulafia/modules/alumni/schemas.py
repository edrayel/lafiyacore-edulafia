"""Alumni Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AlumniProfileBase(BaseModel):
    """Base schema for alumni profile."""

    student_id: UUID = Field(..., description="ID of the student")
    graduation_year: int = Field(..., description="Year of graduation")
    current_occupation: str | None = Field(None, max_length=255)
    university: str | None = Field(None, max_length=255)
    linkedin_url: str | None = Field(None, max_length=500)
    contact_email: str | None = Field(None, max_length=255)
    contact_phone: str | None = Field(None, max_length=50)


class AlumniProfileCreate(AlumniProfileBase):
    """Schema for creating an alumni profile."""

    pass


class AlumniProfileUpdate(BaseModel):
    """Schema for updating an alumni profile."""

    model_config = ConfigDict(from_attributes=True)

    graduation_year: int | None = None
    current_occupation: str | None = Field(None, max_length=255)
    university: str | None = Field(None, max_length=255)
    linkedin_url: str | None = Field(None, max_length=500)
    contact_email: str | None = Field(None, max_length=255)
    contact_phone: str | None = Field(None, max_length=50)


class AlumniProfileResponse(BaseModel):
    """Schema for alumni profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    student_id: UUID
    graduation_year: int
    current_occupation: str | None = None
    university: str | None = None
    linkedin_url: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    created_at: datetime
    updated_at: datetime


class AlumniUpdateRequest(BaseModel):
    current_occupation: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    linkedin_url: str | None = None
    degree_earned: str | None = None
    university_attended: str | None = None
