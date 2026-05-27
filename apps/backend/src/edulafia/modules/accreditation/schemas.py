"""Accreditation Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AccreditationChecklistBase(BaseModel):
    """Base schema for accreditation checklist."""

    school_id: UUID = Field(..., description="ID of the school")
    category: str = Field(...)
    requirement: str = Field(..., min_length=1, max_length=500)
    status: str = Field(default="not_met")
    evidence_path: str | None = Field(None, max_length=500)
    notes: str | None = Field(None)
    inspected_by: str = Field(..., min_length=1, max_length=255)
    inspected_at: datetime = Field(...)


class AccreditationChecklistCreate(AccreditationChecklistBase):
    """Schema for creating an accreditation checklist."""


class AccreditationChecklistUpdate(BaseModel):
    """Schema for updating an accreditation checklist."""

    model_config = ConfigDict(from_attributes=True)

    category: str | None = None
    requirement: str | None = Field(None, max_length=500)
    status: str | None = None
    evidence_path: str | None = Field(None, max_length=500)
    notes: str | None = None
    inspected_by: str | None = Field(None, max_length=255)


class AccreditationChecklistResponse(BaseModel):
    """Schema for accreditation checklist response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    category: str
    requirement: str
    status: str
    evidence_path: str | None = None
    notes: str | None = None
    inspected_by: str
    inspected_at: datetime
    created_at: datetime
    updated_at: datetime
