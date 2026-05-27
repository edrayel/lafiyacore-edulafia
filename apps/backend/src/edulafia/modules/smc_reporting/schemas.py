"""SMC reporting Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SMCReportBase(BaseModel):
    """Base schema for SMC report."""

    school_id: UUID = Field(..., description="ID of the school")
    report_date: datetime = Field(...)
    attendance_data: dict = Field(default_factory=dict)
    financial_data: dict = Field(default_factory=dict)
    challenges: str | None = Field(None)
    action_items: list = Field(default_factory=list)
    meeting_minutes: str | None = Field(None)


class SMCReportCreate(SMCReportBase):
    """Schema for creating an SMC report."""


class SMCReportUpdate(BaseModel):
    """Schema for updating an SMC report."""

    model_config = ConfigDict(from_attributes=True)

    report_date: datetime | None = None
    attendance_data: dict | None = None
    financial_data: dict | None = None
    challenges: str | None = None
    action_items: list | None = None
    meeting_minutes: str | None = None


class SMCReportResponse(BaseModel):
    """Schema for SMC report response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    report_date: datetime
    attendance_data: dict
    financial_data: dict
    challenges: str | None = None
    action_items: list
    meeting_minutes: str | None = None
    created_at: datetime
    updated_at: datetime
