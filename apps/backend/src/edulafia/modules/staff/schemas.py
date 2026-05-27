"""Staff Pydantic schemas."""

from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StaffCreate(BaseModel):
    """Schema for creating a staff member."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: str | None = Field(None, max_length=100)
    email: str | None = Field(None, max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    whatsapp_phone: str | None = Field(None, max_length=20)
    date_of_birth: date | None = None
    gender: str = Field(..., description="male or female")
    address: str | None = None
    role: str = Field(..., description="teacher, nurse, bursar, admin, etc.")
    department: str | None = None
    qualifications: dict | None = None
    documents: dict | None = None
    subjects: list[UUID] | None = None
    employment_type: str = Field(default="permanent")
    employment_date: date | None = None
    salary: Decimal | None = Field(None, ge=0)
    bank_details: dict | None = None
    next_of_kin: dict | None = None
    emergency_contact: dict | None = None

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender."""
        if v.lower() not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role."""
        valid_roles = [
            "teacher", "nurse", "bursar", "admin", "accountant",
            "librarian", "lab_attendant", "security", "cleaner", "other"
        ]
        if v.lower() not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
        return v.lower()

    @field_validator("employment_type")
    @classmethod
    def validate_employment_type(cls, v: str) -> str:
        """Validate employment type."""
        valid_types = ["permanent", "contract", "nysc", "intern"]
        if v.lower() not in valid_types:
            raise ValueError(f"Employment type must be one of: {', '.join(valid_types)}")
        return v.lower()


class StaffUpdate(BaseModel):
    """Schema for updating a staff member."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    middle_name: str | None = Field(None, max_length=100)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, min_length=10, max_length=20)
    whatsapp_phone: str | None = Field(None, max_length=20)
    date_of_birth: date | None = None
    address: str | None = None
    department: str | None = None
    qualifications: dict | None = None
    documents: dict | None = None
    subjects: list[UUID] | None = None
    employment_type: str | None = None
    salary: Decimal | None = Field(None, ge=0)
    bank_details: dict | None = None
    next_of_kin: dict | None = None
    emergency_contact: dict | None = None
    status: str | None = None


class StaffResponse(BaseModel):
    """Schema for staff response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    user_id: UUID | None = None
    staff_id: str
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str | None = None
    phone: str
    whatsapp_phone: str | None = None
    date_of_birth: date | None = None
    gender: str
    address: str | None = None
    photo_url: str | None = None
    role: str
    department: str | None = None
    qualifications: dict | None = None
    documents: dict | None = None
    subjects: list[UUID] | None = None
    employment_type: str
    employment_date: date | None = None
    exit_date: date | None = None
    status: str
    version: int
    created_at: datetime
    updated_at: datetime


class StaffDeactivate(BaseModel):
    """Schema for deactivating staff."""

    reason: str = Field(..., min_length=1, max_length=100)
    exit_date: date | None = None


class StaffAssignmentCreate(BaseModel):
    """Schema for creating staff assignment."""

    staff_id: UUID
    class_id: UUID
    subject_id: UUID | None = None
    academic_year_id: UUID
    term_id: UUID | None = None
    assignment_type: str = Field(default="regular")
    is_form_teacher: bool = False
    start_date: date | None = None
    end_date: date | None = None
    notes: str | None = None

    @field_validator("assignment_type")
    @classmethod
    def validate_assignment_type(cls, v: str) -> str:
        """Validate assignment type."""
        valid_types = ["regular", "substitute", "temporary"]
        if v.lower() not in valid_types:
            raise ValueError(f"Assignment type must be one of: {', '.join(valid_types)}")
        return v.lower()


class StaffAssignmentResponse(BaseModel):
    """Schema for staff assignment response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    staff_id: UUID
    class_id: UUID
    subject_id: UUID | None = None
    academic_year_id: UUID
    term_id: UUID | None = None
    assignment_type: str
    is_form_teacher: bool
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class TimetableCreate(BaseModel):
    """Schema for creating timetable."""

    class_id: UUID
    academic_year_id: UUID
    term_id: UUID
    effective_from: date


class TimetableEntryCreate(BaseModel):
    """Schema for creating timetable entry."""

    day_of_week: int = Field(..., ge=1, le=7)
    period_number: int = Field(..., ge=1)
    start_time: time
    end_time: time
    subject_id: UUID
    staff_id: UUID
    room_number: str | None = None
    notes: str | None = None
    is_break: bool = False

    @field_validator("day_of_week")
    @classmethod
    def validate_day_of_week(cls, v: int) -> int:
        """Validate day of week."""
        if v < 1 or v > 7:
            raise ValueError("Day of week must be between 1 (Monday) and 7 (Sunday)")
        return v


class TimetableEntryResponse(BaseModel):
    """Schema for timetable entry response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    timetable_id: UUID
    day_of_week: int
    period_number: int
    start_time: time
    end_time: time
    subject_id: UUID
    staff_id: UUID
    room_number: str | None = None
    notes: str | None = None
    is_break: bool
    created_at: datetime
    updated_at: datetime


class TimetableEntryEnriched(TimetableEntryResponse):
    """Schema for timetable entry response with resolved names."""

    staff_name: str | None = None
    subject_name: str | None = None
    class_name: str | None = None


class TimetableResponse(BaseModel):
    """Schema for timetable response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    class_id: UUID
    academic_year_id: UUID
    term_id: UUID
    effective_from: date
    effective_to: date | None = None
    is_published: bool
    published_at: datetime | None = None
    version_number: int
    is_draft: bool
    created_at: datetime
    updated_at: datetime


class TeacherCheckIn(BaseModel):
    """Schema for teacher check-in."""

    check_in_method: str = Field(default="manual")
    qr_code: str | None = None

    @field_validator("check_in_method")
    @classmethod
    def validate_check_in_method(cls, v: str) -> str:
        """Validate check-in method."""
        valid_methods = ["manual", "qr_code", "geofencing"]
        if v.lower() not in valid_methods:
            raise ValueError(f"Check-in method must be one of: {', '.join(valid_methods)}")
        return v.lower()


class TeacherAttendanceResponse(BaseModel):
    """Schema for teacher attendance response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    staff_id: UUID
    school_id: UUID
    date: date
    check_in_time: datetime | None = None
    check_out_time: datetime | None = None
    status: str
    check_in_method: str | None = None
    late_minutes: int | None = None
    early_departure_minutes: int | None = None
    reason_code: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class StaffCommunicationCreate(BaseModel):
    """Schema for creating staff communication."""

    communication_type: str = Field(..., description="announcement, broadcast, message, meeting")
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    target_audience: dict | None = None
    channels: list[str] = Field(default=["in_app"])
    requires_acknowledgement: bool = False
    priority: str = Field(default="normal")
    scheduled_for: datetime | None = None

    @field_validator("communication_type")
    @classmethod
    def validate_communication_type(cls, v: str) -> str:
        """Validate communication type."""
        valid_types = ["announcement", "broadcast", "message", "meeting"]
        if v.lower() not in valid_types:
            raise ValueError(f"Communication type must be one of: {', '.join(valid_types)}")
        return v.lower()

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority."""
        valid_priorities = ["low", "normal", "high", "urgent"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return v.lower()


class StaffCommunicationResponse(BaseModel):
    """Schema for staff communication response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    sender_id: UUID
    communication_type: str
    title: str
    content: str
    target_audience: dict | None = None
    channels: list[str]
    requires_acknowledgement: bool
    priority: str
    scheduled_for: datetime | None = None
    sent_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ClashInfo(BaseModel):
    """Schema for timetable clash information."""

    clash_type: str  # "teacher_clash", "class_clash", "break_period"
    day_of_week: int
    period_number: int
    existing_entry_id: UUID | None = None
    message: str
