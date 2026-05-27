"""Data retention Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RetentionPolicyBase(BaseModel):
    """Base schema for retention policy."""

    school_id: UUID = Field(..., description="ID of the school")
    data_type: str = Field(..., min_length=1, max_length=100)
    retention_years: int = Field(..., ge=1)
    archive_after_years: int = Field(..., ge=0)
    auto_delete: bool = Field(default=False)


class RetentionPolicyCreate(RetentionPolicyBase):
    """Schema for creating a retention policy."""


class RetentionPolicyUpdate(BaseModel):
    """Schema for updating a retention policy."""

    model_config = ConfigDict(from_attributes=True)

    data_type: str | None = Field(None, max_length=100)
    retention_years: int | None = Field(None, ge=1)
    archive_after_years: int | None = Field(None, ge=0)
    auto_delete: bool | None = None


class RetentionPolicyResponse(BaseModel):
    """Schema for retention policy response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    data_type: str
    retention_years: int
    archive_after_years: int
    auto_delete: bool
    created_at: datetime
    updated_at: datetime


class DataArchiveBase(BaseModel):
    """Base schema for data archive."""

    school_id: UUID = Field(..., description="ID of the school")
    data_type: str = Field(..., min_length=1, max_length=100)
    storage_path: str = Field(..., max_length=500)
    record_count: int = Field(default=0, ge=0)
    status: str = Field(default="archived")


class DataArchiveCreate(DataArchiveBase):
    """Schema for creating a data archive."""


class DataArchiveResponse(BaseModel):
    """Schema for data archive response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    data_type: str
    archived_at: datetime
    delete_after_date: datetime
    storage_path: str
    record_count: int
    status: str
    created_at: datetime
    updated_at: datetime


class DataSubjectRequestCreate(BaseModel):
    """Schema for creating a data subject request."""
    
    request_type: str = Field(..., description="access, correction, erasure, portability")
    details: str | None = Field(None, description="Details of the request")


class DataSubjectRequestResponse(BaseModel):
    """Schema for data subject request response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    requester_id: UUID
    request_type: str
    status: str
    details: str | None = None
    resolved_at: datetime | None = None
    resolution_notes: str | None = None
    created_at: datetime
    updated_at: datetime


class ConsentRecordCreate(BaseModel):
    """Schema for creating a consent record."""
    
    student_id: UUID
    guardian_id: UUID
    consent_type: str = Field(..., description="medical_processing, general_data, photo_release")
    status: str = Field(default="granted", description="granted, revoked")


class ConsentRecordResponse(BaseModel):
    """Schema for consent record response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    student_id: UUID
    guardian_id: UUID
    consent_type: str
    status: str
    granted_at: datetime
    revoked_at: datetime | None = None
    ip_address: str | None = None
    created_at: datetime
    updated_at: datetime
