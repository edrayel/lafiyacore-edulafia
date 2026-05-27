"""Leave management Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LeaveRequestBase(BaseModel):
    """Base schema for leave request."""

    staff_id: UUID = Field(..., description="ID of the staff")
    leave_type: str = Field(...)
    start_date: date = Field(...)
    end_date: date = Field(...)
    reason: str = Field(..., min_length=1)


class LeaveRequestCreate(LeaveRequestBase):
    """Schema for creating a leave request."""


class LeaveRequestUpdate(BaseModel):
    """Schema for updating a leave request."""

    model_config = ConfigDict(from_attributes=True)

    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = Field(None, min_length=1)


class LeaveRequestResponse(BaseModel):
    """Schema for leave request response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    staff_id: UUID
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str
    approved_by: UUID | None = None
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class LeaveApprovalRequest(BaseModel):
    """Schema for approving or rejecting a leave request."""

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(...)
    reason: str | None = None
