"""Health Pydantic schemas."""

from datetime import timezone, date, datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SickBayVisitCreate(BaseModel):
    """Schema for creating a sick bay visit."""

    student_id: UUID
    visit_date: date = Field(default_factory=date.today)
    visit_time: time = Field(default_factory=lambda: datetime.now(timezone.utc).time())
    presenting_complaint_codes: list[str] = Field(..., min_length=1)
    presenting_complaint_notes: str | None = None
    temperature: Decimal | None = Field(None, ge=35, le=42)
    blood_pressure_systolic: int | None = Field(None, ge=60, le=200)
    blood_pressure_diastolic: int | None = Field(None, ge=40, le=130)
    pulse_rate: int | None = Field(None, ge=40, le=200)
    treatment_given: str | None = None
    outcome: str = Field(..., description="returned_to_class, sent_home, referred, hospitalized")
    referred_to: str | None = None

    @field_validator("outcome")
    @classmethod
    def validate_outcome(cls, v: str) -> str:
        """Validate outcome value."""
        valid_outcomes = ["returned_to_class", "sent_home", "referred", "hospitalized"]
        if v.lower() not in valid_outcomes:
            raise ValueError(f"Outcome must be one of: {', '.join(valid_outcomes)}")
        return v.lower()


class SickBayVisitResponse(BaseModel):
    """Schema for sick bay visit response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    school_id: UUID
    visit_date: date
    visit_time: time
    presenting_complaint_codes: list[str]
    presenting_complaint_notes: str | None = None
    temperature: Decimal | None = None
    blood_pressure_systolic: int | None = None
    blood_pressure_diastolic: int | None = None
    pulse_rate: int | None = None
    treatment_given: str | None = None
    outcome: str
    referred_to: str | None = None
    parent_notified: bool
    is_sentinel_relevant: bool
    recorded_by: UUID
    created_at: datetime
    updated_at: datetime


class HealthScreeningCreate(BaseModel):
    """Schema for creating a health screening."""

    student_id: UUID
    screening_date: date = Field(default_factory=date.today)
    screening_type: str = Field(..., description="annual, pre_sports, special, mental_health")
    height: Decimal | None = Field(None, ge=50, le=250)
    weight: Decimal | None = Field(None, ge=10, le=200)
    muac: Decimal | None = Field(None, ge=5, le=40)
    vision_left: Decimal | None = Field(None, ge=0, le=2)
    vision_right: Decimal | None = Field(None, ge=0, le=2)
    hearing_left: str | None = None
    hearing_right: str | None = None
    blood_pressure_systolic: int | None = Field(None, ge=60, le=200)
    blood_pressure_diastolic: int | None = Field(None, ge=40, le=130)
    dental_notes: str | None = None
    sickle_cell_test_result: str | None = None
    phq_a_score: int | None = Field(None, ge=0, le=27, description="PHQ-A total score")
    sdq_score: int | None = Field(None, ge=0, le=40, description="SDQ total difficulties score")
    flags: list[str] | None = []
    follow_up_notes: str | None = None

    @field_validator("screening_type")
    @classmethod
    def validate_screening_type(cls, v: str) -> str:
        """Validate screening type."""
        valid_types = ["annual", "pre_sports", "special", "mental_health"]
        if v.lower() not in valid_types:
            raise ValueError(f"Screening type must be one of: {', '.join(valid_types)}")
        return v.lower()


class HealthScreeningResponse(BaseModel):
    """Schema for health screening response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    school_id: UUID
    screening_date: date
    screening_type: str
    height: Decimal | None = None
    weight: Decimal | None = None
    bmi: Decimal | None = None
    vision_left: Decimal | None = None
    vision_right: Decimal | None = None
    hearing_left: str | None = None
    hearing_right: str | None = None
    phq_a_score: int | None = None
    sdq_score: int | None = None
    flags: list[str] | None = None
    follow_up_required: bool
    conducted_by: UUID
    created_at: datetime
    updated_at: datetime


class ReferralCreate(BaseModel):
    """Schema for creating a referral."""

    student_id: UUID
    sick_bay_visit_id: UUID | None = None
    destination_facility: str = Field(..., min_length=1, max_length=255)
    reason: str = Field(..., min_length=1)
    priority: str = Field(default="normal")
    follow_up_due_date: date

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority."""
        valid_priorities = ["urgent", "normal", "follow_up"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return v.lower()


class ReferralUpdate(BaseModel):
    """Schema for updating a referral."""

    status: str | None = None
    outcome_notes: str | None = None
    outcome_date: date | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Validate status."""
        if v is not None:
            valid_statuses = ["pending", "sent", "acknowledged", "attended", "completed"]
            if v.lower() not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            return v.lower()
        return v


class ReferralResponse(BaseModel):
    """Schema for referral response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    sick_bay_visit_id: UUID | None = None
    school_id: UUID
    referral_date: date
    destination_facility: str
    reason: str
    priority: str
    status: str
    follow_up_due_date: date
    outcome_notes: str | None = None
    outcome_date: date | None = None
    reminder_sent: bool
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class VaccinationRecordCreate(BaseModel):
    """Schema for creating a vaccination record."""

    student_id: UUID
    vaccine_name: str = Field(..., min_length=1, max_length=100)
    vaccine_code: str | None = None
    dose_number: int = Field(default=1, ge=1)
    administration_date: date
    lot_number: str | None = None
    administering_facility: str | None = None


class VaccinationRecordResponse(BaseModel):
    """Schema for vaccination record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    school_id: UUID
    vaccine_name: str
    vaccine_code: str | None = None
    dose_number: int
    administration_date: date
    lot_number: str | None = None
    administering_facility: str | None = None
    created_at: datetime
    updated_at: datetime


class StudentHealthProfileResponse(BaseModel):
    """Schema for student health profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    school_id: UUID
    blood_group: str | None = None
    genotype: str | None = None
    chronic_conditions: list[str] | None = None
    allergies: list[str] | None = None
    current_medications: list[str] | None = None
    disability_status: str | None = None
    emergency_notes: str | None = None
    vision_left: Decimal | None = None
    vision_right: Decimal | None = None
    hearing_left: str | None = None
    hearing_right: str | None = None
    parental_consent_given: bool
    version: int
    created_at: datetime
    updated_at: datetime


class StudentHealthProfileCreate(BaseModel):
    """Schema for creating a student health profile."""

    student_id: UUID
    school_id: UUID
    blood_group: str | None = None
    genotype: str | None = None
    chronic_conditions: list[str] | None = None
    allergies: list[str] | None = None
    current_medications: list[str] | None = None
    disability_status: str | None = None
    emergency_notes: str | None = None
    parental_consent_given: bool = False


class StudentHealthProfileUpdate(BaseModel):
    """Schema for updating a student health profile."""

    blood_group: str | None = None
    genotype: str | None = None
    chronic_conditions: list[str] | None = None
    allergies: list[str] | None = None
    current_medications: list[str] | None = None
    disability_status: str | None = None
    emergency_notes: str | None = None
    parental_consent_given: bool | None = None


class SentinelSignalResponse(BaseModel):
    """Schema for sentinel signal response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_ids: list[UUID]
    lga: str | None = None
    state: str | None = None
    date_generated: datetime
    symptom_profile: dict
    students_affected: int
    threshold_type: str
    alert_tier: str
    status: str
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None
    response_notes: str | None = None
    created_at: datetime
    updated_at: datetime


class SentinelAlertAcknowledge(BaseModel):
    """Schema for acknowledging a sentinel alert."""

    response_notes: str | None = None


class SentinelConfigCreate(BaseModel):
    """Schema for creating sentinel configuration."""

    state: str | None = None
    lga: str | None = None
    school_id: UUID | None = None
    symptom_category: str = Field(..., min_length=1)
    time_window_hours: int = Field(default=48, ge=1, le=168)
    cluster_threshold: int = Field(default=3, ge=1)
    school_threshold_percent: Decimal = Field(default=10, ge=0, le=100)
    baseline_illness_rate: Decimal | None = None


class SentinelConfigResponse(BaseModel):
    """Schema for sentinel configuration response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    state: str | None = None
    lga: str | None = None
    school_id: UUID | None = None
    symptom_category: str
    time_window_hours: int
    cluster_threshold: int
    school_threshold_percent: Decimal
    baseline_illness_rate: Decimal | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
