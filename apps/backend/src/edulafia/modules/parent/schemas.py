"""Parent Pydantic schemas."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OTPRequest(BaseModel):
    """Schema for OTP request."""

    phone: str = Field(..., min_length=13, max_length=14)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate Nigerian phone format."""
        if not v.startswith("+234"):
            raise ValueError("Phone must start with +234")
        digits = v[4:]
        if not digits.isdigit() or len(digits) != 10:
            raise ValueError("Phone must be +234 followed by 10 digits")
        return v


class OTPVerify(BaseModel):
    """Schema for OTP verification."""

    phone: str = Field(..., min_length=13, max_length=14)
    otp_code: str = Field(..., min_length=6, max_length=6)


class AuthResponse(BaseModel):
    """Schema for authentication response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    guardian_id: UUID
    guardian_name: str
    children: list[dict]


class TokenRefresh(BaseModel):
    """Schema for token refresh."""

    refresh_token: str


class ChildSummary(BaseModel):
    """Schema for child summary in portal."""

    model_config = ConfigDict(from_attributes=True)

    student_id: UUID
    first_name: str
    last_name: str
    admission_number: str
    class_name: str | None = None
    status: str


class ChildProfileResponse(BaseModel):
    """Schema for child profile response."""

    model_config = ConfigDict(from_attributes=True)

    student_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    admission_number: str
    date_of_birth: date
    gender: str
    class_name: str | None = None
    status: str
    photo_url: str | None = None
    nationality: str
    created_at: datetime


class AcademicResultResponse(BaseModel):
    """Schema for academic result response."""

    model_config = ConfigDict(from_attributes=True)

    subject_name: str
    subject_code: str
    ca_score: Decimal | None = None
    exam_score: Decimal | None = None
    total_score: Decimal | None = None
    grade: str | None = None
    class_rank: int | None = None


class AttendanceSummaryResponse(BaseModel):
    """Schema for attendance summary response."""

    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    excused_days: int
    attendance_rate: float


class FinanceStatusResponse(BaseModel):
    """Schema for finance status response."""

    student_id: UUID
    total_charges: Decimal
    total_payments: Decimal
    total_waivers: Decimal
    balance: Decimal
    last_payment_date: date | None = None


class PaymentInitiate(BaseModel):
    """Schema for payment initiation."""

    student_id: UUID
    amount: Decimal = Field(..., ge=0.01, le=500000)
    fee_category: str | None = None


class PaymentInitiateResponse(BaseModel):
    """Schema for payment initiation response."""

    payment_url: str
    reference: str
    gateway: str
    amount: Decimal
    status: str


class ParentNotificationResponse(BaseModel):
    """Schema for parent notification response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    notification_type: str
    title: str
    message: str
    channel: str
    priority: str
    status: str
    notification_metadata: dict | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    created_at: datetime


class NotificationPreferenceResponse(BaseModel):
    """Schema for notification preference response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    notification_type: str
    channel: str
    is_enabled: bool


class NotificationPreferenceUpdate(BaseModel):
    """Schema for updating notification preference."""

    notification_type: str
    channel: str
    is_enabled: bool


class AbsenceExcusalCreate(BaseModel):
    """Schema for creating absence excusal."""

    student_id: UUID
    absence_date: date
    reason: str = Field(..., min_length=1, max_length=100)
    details: str | None = None


class AbsenceExcusalResponse(BaseModel):
    """Schema for absence excusal response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    guardian_id: UUID
    absence_date: datetime
    reason: str
    details: str | None = None
    status: str
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    review_notes: str | None = None
    created_at: datetime
    updated_at: datetime


class CorrectionRequestCreate(BaseModel):
    """Schema for creating correction request."""

    student_id: UUID
    field_name: str = Field(..., min_length=1, max_length=100)
    requested_value: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)


class CorrectionRequestResponse(BaseModel):
    """Schema for correction request response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    guardian_id: UUID
    student_id: UUID
    field_name: str
    current_value: str | None = None
    requested_value: str
    reason: str
    status: str
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class FeedbackCreate(BaseModel):
    """Schema for creating feedback."""

    feedback_type: str = Field(..., description="complaint, suggestion, praise, question")
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    is_anonymous: bool = False

    @field_validator("feedback_type")
    @classmethod
    def validate_feedback_type(cls, v: str) -> str:
        """Validate feedback type."""
        valid_types = ["complaint", "suggestion", "praise", "question"]
        if v.lower() not in valid_types:
            raise ValueError(f"Feedback type must be one of: {', '.join(valid_types)}")
        return v.lower()


class FeedbackResponse(BaseModel):
    """Schema for feedback response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    guardian_id: UUID
    school_id: UUID
    feedback_type: str
    subject: str
    message: str
    is_anonymous: bool
    status: str
    response: str | None = None
    responded_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class SchoolAnnouncement(BaseModel):
    """Schema for school announcement."""

    id: UUID
    title: str
    content: str
    priority: str
    published_at: datetime
    school_name: str
