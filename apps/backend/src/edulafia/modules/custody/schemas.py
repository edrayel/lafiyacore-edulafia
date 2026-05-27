"""Custody Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CustodyOrderBase(BaseModel):
    """Base schema for custody order."""

    student_id: UUID = Field(..., description="ID of the student")
    custodial_guardian_id: UUID = Field(..., description="ID of custodial guardian")
    non_custodial_guardian_id: UUID | None = Field(None, description="ID of non-custodial guardian")
    court_order_number: str = Field(..., min_length=1, max_length=100)
    court_name: str = Field(..., min_length=1, max_length=255)
    order_date: date = Field(...)
    restrictions: dict = Field(default_factory=dict)
    expiry_date: date | None = Field(None)
    status: str = Field(default="active")
    notes: str | None = Field(None)


class CustodyOrderCreate(CustodyOrderBase):
    """Schema for creating a custody order."""


class CustodyOrderUpdate(BaseModel):
    """Schema for updating a custody order."""

    model_config = ConfigDict(from_attributes=True)

    custodial_guardian_id: UUID | None = None
    non_custodial_guardian_id: UUID | None = None
    court_order_number: str | None = Field(None, max_length=100)
    court_name: str | None = Field(None, max_length=255)
    order_date: date | None = None
    restrictions: dict | None = None
    expiry_date: date | None = None
    status: str | None = None
    notes: str | None = None


class CustodyOrderResponse(BaseModel):
    """Schema for custody order response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    custodial_guardian_id: UUID
    non_custodial_guardian_id: UUID | None = None
    court_order_number: str
    court_name: str
    order_date: date
    restrictions: dict
    expiry_date: date | None = None
    status: str
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
