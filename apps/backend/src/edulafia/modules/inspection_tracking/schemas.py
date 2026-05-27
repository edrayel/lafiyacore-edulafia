"""Inspection tracking Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchoolInspectionBase(BaseModel):
    """Base schema for school inspection."""

    school_id: UUID = Field(..., description="ID of the school")
    inspector_name: str = Field(..., min_length=1, max_length=255)
    ministry: str = Field(..., min_length=1, max_length=255)
    inspection_date: date = Field(...)
    findings: list = Field(default_factory=list)
    recommendations: list = Field(default_factory=list)
    compliance_status: str = Field(default="compliant")
    follow_up_date: date | None = Field(None)
    status: str = Field(default="open")


class SchoolInspectionCreate(SchoolInspectionBase):
    """Schema for creating a school inspection."""


class SchoolInspectionUpdate(BaseModel):
    """Schema for updating a school inspection."""

    model_config = ConfigDict(from_attributes=True)

    findings: list | None = None
    recommendations: list | None = None
    compliance_status: str | None = None
    follow_up_date: date | None = None
    status: str | None = None


class SchoolInspectionResponse(BaseModel):
    """Schema for school inspection response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    inspector_name: str
    ministry: str
    inspection_date: date
    findings: list
    recommendations: list
    compliance_status: str
    follow_up_date: date | None = None
    status: str
    created_at: datetime
    updated_at: datetime
