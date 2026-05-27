"""Clubs Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClubBase(BaseModel):
    """Base schema for club."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)
    category: str = Field(default="other")
    advisor_staff_id: UUID | None = Field(None)
    is_active: bool = Field(default=True)


class ClubCreate(ClubBase):
    """Schema for creating a club."""

    pass


class ClubUpdateRequest(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None
    teacher_id: UUID | None = None
    is_active: bool | None = None


class ClubResponse(BaseModel):
    """Schema for club response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    category: str
    advisor_staff_id: UUID | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ClubMembershipBase(BaseModel):
    """Base schema for club membership."""

    club_id: UUID = Field(..., description="ID of the club")
    student_id: UUID = Field(..., description="ID of the student")
    joined_date: date = Field(...)
    role: str = Field(default="member")


class ClubMembershipCreate(BaseModel):
    student_id: UUID
    club_id: UUID
    role: str = Field("member", max_length=50)


class ClubMembershipResponse(ClubMembershipCreate):
    id: UUID
    joined_at: datetime
    school_id: UUID

    class Config:
        from_attributes = True


class ClubMembershipUpdateRequest(BaseModel):
    role: str | None = Field(None, max_length=50)
