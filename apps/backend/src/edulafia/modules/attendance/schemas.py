"""Attendance Pydantic schemas."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AttendanceRecordBase(BaseModel):
    """Base schema for attendance records."""

    student_id: UUID
    class_id: UUID
    date: date
    period: int | None = None
    status: str = Field(..., description="present, absent, late, excused")
    reason_code: str | None = Field(
        None,
        description="sick, family, unknown, excused, suspended",
    )
    symptom_codes: list[str] | None = Field(
        None,
        description="Array of symptom codes when reason is sick",
    )
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate attendance status."""
        valid_statuses = ["present", "absent", "late", "excused"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v.lower()

    @field_validator("reason_code")
    @classmethod
    def validate_reason_code(cls, v: str | None) -> str | None:
        """Validate reason code."""
        if v is not None:
            valid_reasons = ["sick", "family", "unknown", "excused", "suspended"]
            if v.lower() not in valid_reasons:
                raise ValueError(f"Reason code must be one of: {', '.join(valid_reasons)}")
            return v.lower()
        return v

    @field_validator("date")
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        """Validate that attendance date is not in the future."""
        if v > date.today():
            raise ValueError("Cannot mark attendance for future dates")
        return v


class AttendanceMarkRequest(AttendanceRecordBase):
    """Schema for marking attendance."""


class AttendanceBulkMarkRequest(BaseModel):
    """Schema for bulk attendance marking."""

    class_id: UUID
    date: date
    default_status: str = "present"
    exceptions: list[AttendanceRecordBase] = Field(
        default=[],
        description="Students with non-default status",
    )

    @field_validator("date")
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        """Validate that attendance date is not in the future."""
        if v > date.today():
            raise ValueError("Cannot mark attendance for future dates")
        return v


class AttendanceUpdateRequest(BaseModel):
    """Schema for updating attendance record."""

    status: str | None = None
    reason_code: str | None = None
    symptom_codes: list[str] | None = None
    notes: str | None = None
    edit_reason: str = Field(..., description="Required reason for edit")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Validate attendance status."""
        if v is not None:
            valid_statuses = ["present", "absent", "late", "excused"]
            if v.lower() not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            return v.lower()
        return v


class AttendanceRecordResponse(BaseModel):
    """Schema for attendance record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    class_id: UUID
    school_id: UUID
    date: date
    period: int | None = None
    status: str
    reason_code: str | None = None
    symptom_codes: list[str] | None = None
    notes: str | None = None
    recorded_by: UUID
    edited_at: datetime | None = None
    edited_by: UUID | None = None
    edit_reason: str | None = None
    device_id: str | None = None
    sync_status: str
    created_at: datetime
    updated_at: datetime


class AttendanceSummaryResponse(BaseModel):
    """Schema for attendance summary."""

    total_students: int
    present: int
    absent: int
    late: int
    excused: int
    attendance_rate: float


class AttendanceFilters(BaseModel):
    """Schema for attendance query filters."""

    student_id: Optional[UUID] = None
    class_id: Optional[UUID] = None
    date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    reason_code: Optional[str] = None
