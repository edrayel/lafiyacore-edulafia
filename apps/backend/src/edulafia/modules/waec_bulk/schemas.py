"""WAEC bulk Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WAECBulkRegistrationBase(BaseModel):
    """Base schema for WAEC bulk registration."""

    school_id: UUID = Field(..., description="ID of the school")
    exam_year: int = Field(..., ge=2000)
    class_id: UUID = Field(..., description="ID of the class")
    students: list = Field(default_factory=list)
    total_registered: int = Field(default=0, ge=0)
    total_paid: int = Field(default=0, ge=0)
    status: str = Field(default="draft")


class WAECBulkRegistrationCreate(WAECBulkRegistrationBase):
    """Schema for creating a WAEC bulk registration."""


class WAECBulkRegistrationUpdate(BaseModel):
    """Schema for updating a WAEC bulk registration."""

    model_config = ConfigDict(from_attributes=True)

    students: list | None = None
    total_registered: int | None = Field(None, ge=0)
    total_paid: int | None = Field(None, ge=0)
    status: str | None = None


class WAECBulkRegistrationResponse(BaseModel):
    """Schema for WAEC bulk registration response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    exam_year: int
    class_id: UUID
    students: list
    total_registered: int
    total_paid: int
    status: str
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
