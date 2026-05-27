"""Ministry reporting Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MinistryReportBase(BaseModel):
    """Base schema for ministry report."""

    school_id: UUID = Field(..., description="ID of the school")
    report_type: str = Field(...)
    period_start: datetime = Field(...)
    period_end: datetime = Field(...)
    data: dict = Field(default_factory=dict)
    submitted: bool = Field(default=False)
    submitted_at: datetime | None = Field(None)
    generated_by: str = Field(..., min_length=1, max_length=255)


class MinistryReportCreate(MinistryReportBase):
    """Schema for creating a ministry report."""


class MinistryReportUpdate(BaseModel):
    """Schema for updating a ministry report."""

    model_config = ConfigDict(from_attributes=True)

    data: dict | None = None
    submitted: bool | None = None
    submitted_at: datetime | None = None


class MinistryReportResponse(BaseModel):
    """Schema for ministry report response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    report_type: str
    period_start: datetime
    period_end: datetime
    data: dict
    submitted: bool
    submitted_at: datetime | None = None
    generated_by: str
    created_at: datetime
    updated_at: datetime
