"""Finance Pydantic schemas."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field


class FeeScheduleBase(BaseModel):
    """Base schema for fee schedules."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    is_active: bool = True


class FeeScheduleCreate(FeeScheduleBase):
    """Schema for creating a fee schedule."""

    academic_year_id: UUID
    items: list["FeeScheduleItemCreate"] = Field(default=[])


class FeeScheduleItemCreate(BaseModel):
    """Schema for creating fee schedule items."""

    class_level: str = Field(..., min_length=1, max_length=20)
    fee_category: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., ge=0, le=9999999999.99)
    is_mandatory: bool = True


class FeeScheduleItemResponse(BaseModel):
    """Schema for fee schedule item response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fee_schedule_id: UUID
    class_level: str
    fee_category: str
    amount: Decimal
    is_mandatory: bool
    created_at: datetime
    updated_at: datetime


class FeeScheduleResponse(FeeScheduleBase):
    """Schema for fee schedule response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    academic_year_id: UUID
    locked_at: datetime | None = None
    locked_by: UUID | None = None
    created_at: datetime
    updated_at: datetime


class FeeScheduleCopy(BaseModel):
    """Schema for copying a fee schedule."""

    source_schedule_id: UUID
    target_academic_year_id: UUID
    adjust_percentage: Decimal | None = Field(
        None,
        ge=-100,
        le=100,
        description="Percentage adjustment (-100 to 100)",
    )


class PaymentRecord(BaseModel):
    """Schema for recording a payment."""

    student_id: UUID
    amount: Decimal = Field(..., ge=0.01, le=500000)
    fee_category: str | None = Field(
        None,
        description="Fee category - auto-determined if not specified",
    )
    payment_method: str = Field(
        ...,
        description="cash, bank_transfer, paystack, flutterwave, remita, cheque",
    )
    payment_reference: str | None = None
    description: str | None = None
    term_id: UUID | None = None

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, v: str) -> str:
        """Validate payment method."""
        valid_methods = ["cash", "bank_transfer", "paystack", "flutterwave", "remita", "cheque"]
        if v.lower() not in valid_methods:
            raise ValueError(f"Payment method must be one of: {', '.join(valid_methods)}")
        return v.lower()

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate payment amount."""
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        if v > 500000:
            raise ValueError("Amount exceeds maximum transaction limit of ₦500,000")
        return v


class PaymentReversal(BaseModel):
    """Schema for reversing a payment."""

    reason: str = Field(..., min_length=1, max_length=500)
    gateway_confirmation: str | None = Field(
        None,
        description="Required for online payment reversals",
    )


class FeeLedgerResponse(BaseModel):
    """Schema for fee ledger entry response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    school_id: UUID
    transaction_date: datetime
    transaction_type: str
    fee_category: str
    amount: Decimal
    payment_method: str | None = None
    payment_reference: str | None = None
    receipt_number: str | None = None
    description: str | None = None
    term_id: UUID | None = None
    academic_year_id: UUID | None = None
    recorded_by: UUID
    gateway_reference: str | None = None
    gateway_response: dict | None = None
    
    @computed_field
    @property
    def status(self) -> str:
        if self.gateway_response and isinstance(self.gateway_response, dict):
            return self.gateway_response.get("status", "completed")
        return "completed"

    created_at: datetime
    updated_at: datetime


class StudentBalanceResponse(BaseModel):
    """Schema for student balance response."""

    student_id: UUID
    student_name: str
    class_name: str | None = None
    total_charges: Decimal
    total_payments: Decimal
    total_waivers: Decimal
    balance: Decimal
    term_id: UUID | None = None
    academic_year_id: UUID | None = None


class FinancialDashboardResponse(BaseModel):
    """Schema for financial dashboard response."""

    total_charges: Decimal
    total_payments: Decimal
    total_waivers: Decimal
    outstanding_balance: Decimal
    collection_rate: float
    class_breakdown: list[dict] = []
    category_breakdown: list[dict] = []


class ScholarshipCreate(BaseModel):
    """Schema for creating a scholarship."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    amount: Decimal | None = Field(None, ge=0)
    percentage: Decimal | None = Field(None, ge=0, le=100)
    criteria: dict | None = None
    start_date: date | None = None
    end_date: date | None = None
    donor_name: str | None = None
    donor_contact: str | None = None


class ScholarshipAward(BaseModel):
    """Schema for awarding a scholarship."""

    student_id: UUID
    academic_year_id: UUID
    amount_awarded: Decimal = Field(..., ge=0)
    notes: str | None = None


class ScholarshipResponse(BaseModel):
    """Schema for scholarship response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    amount: Decimal | None = None
    percentage: Decimal | None = None
    is_active: bool
    donor_name: str | None = None
    created_at: datetime
    updated_at: datetime


class OnlinePaymentInitiate(BaseModel):
    """Schema for initiating online payment."""

    student_id: UUID
    amount: Decimal = Field(..., ge=0.01, le=500000)
    fee_category: str | None = None
    gateway: str = Field(
        ...,
        description="paystack, flutterwave, or remita",
    )
    callback_url: str = Field(
        ...,
        description="URL to redirect after payment",
    )

    @field_validator("gateway")
    @classmethod
    def validate_gateway(cls, v: str) -> str:
        """Validate payment gateway."""
        valid_gateways = ["paystack", "flutterwave", "remita"]
        if v.lower() not in valid_gateways:
            raise ValueError(f"Gateway must be one of: {', '.join(valid_gateways)}")
        return v.lower()


class OnlinePaymentResponse(BaseModel):
    """Schema for online payment initiation response."""

    payment_url: str
    reference: str
    gateway: str
    amount: Decimal
    status: str = "pending"


class WebhookPayload(BaseModel):
    """Schema for webhook payload."""

    event: str
    data: dict
