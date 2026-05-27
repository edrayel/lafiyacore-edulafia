"""Payroll Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PayrollRunBase(BaseModel):
    """Base schema for payroll run."""

    school_id: UUID = Field(..., description="ID of the school")
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)
    total_gross: float = Field(default=0.0, ge=0)
    total_deductions: float = Field(default=0.0, ge=0)
    total_net: float = Field(default=0.0, ge=0)
    status: str = Field(default="draft")
    run_date: datetime = Field(...)


class PayrollRunCreate(PayrollRunBase):
    """Schema for creating a payroll run."""


class PayrollRunUpdate(BaseModel):
    """Schema for updating a payroll run."""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = None
    total_gross: float | None = Field(None, ge=0)
    total_deductions: float | None = Field(None, ge=0)
    total_net: float | None = Field(None, ge=0)


class PayrollRunResponse(BaseModel):
    """Schema for payroll run response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    month: int
    year: int
    total_gross: float
    total_deductions: float
    total_net: float
    status: str
    run_date: datetime
    created_at: datetime
    updated_at: datetime


class PayrollEntryBase(BaseModel):
    """Base schema for payroll entry."""

    payroll_run_id: UUID = Field(..., description="ID of the payroll run")
    staff_id: UUID = Field(..., description="ID of the staff")
    gross_pay: float = Field(default=0.0, ge=0)
    tax: float = Field(default=0.0, ge=0)
    pension: float = Field(default=0.0, ge=0)
    nhf: float = Field(default=0.0, ge=0)
    other_deductions: float = Field(default=0.0, ge=0)
    net_pay: float = Field(default=0.0, ge=0)


class PayrollEntryCreate(PayrollEntryBase):
    """Schema for creating a payroll entry."""


class PayrollEntryUpdate(BaseModel):
    """Schema for updating a payroll entry."""

    model_config = ConfigDict(from_attributes=True)

    gross_pay: float | None = Field(None, ge=0)
    tax: float | None = Field(None, ge=0)
    pension: float | None = Field(None, ge=0)
    nhf: float | None = Field(None, ge=0)
    other_deductions: float | None = Field(None, ge=0)
    net_pay: float | None = Field(None, ge=0)


class PayrollEntryResponse(BaseModel):
    """Schema for payroll entry response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    payroll_run_id: UUID
    staff_id: UUID
    gross_pay: float
    tax: float
    pension: float
    nhf: float
    other_deductions: float
    net_pay: float
    created_at: datetime
    updated_at: datetime
