"""Girl child tracking Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GirlChildRecordBase(BaseModel):
    """Base schema for girl child record."""

    student_id: UUID = Field(..., description="ID of the student")
    enrollment_source: str | None = Field(None, max_length=255)
    risk_factors: list = Field(default_factory=list)
    interventions: list = Field(default_factory=list)
    attendance_trend: float | None = Field(None, ge=0, le=100)
    dropout_risk: str = Field(default="low")
    counselor_notes: str | None = Field(None)


class GirlChildRecordCreate(GirlChildRecordBase):
    """Schema for creating a girl child record."""

    pass


class GirlChildRecordUpdate(BaseModel):
    """Schema for updating a girl child record."""

    model_config = ConfigDict(from_attributes=True)

    enrollment_source: str | None = Field(None, max_length=255)
    risk_factors: list | None = None
    interventions: list | None = None
    attendance_trend: float | None = Field(None, ge=0, le=100)
    dropout_risk: str | None = None
    counselor_notes: str | None = None


class GirlChildRecordResponse(BaseModel):
    """Schema for girl child record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    enrollment_source: str | None = None
    risk_factors: list
    interventions: list
    attendance_trend: float | None = None
    dropout_risk: str
    counselor_notes: str | None = None
    created_at: datetime
    updated_at: datetime


class RecordUpdateRequest(BaseModel):
    has_menstrual_hygiene_kit: bool | None = None
    counseling_sessions_attended: int | None = Field(None, ge=0)
    risk_level: str | None = Field(None, max_length=50)
    notes: str | None = None
