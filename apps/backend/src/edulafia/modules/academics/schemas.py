"""Academics Pydantic schemas for request/response validation."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SubjectBase(BaseModel):
    """Base schema with common subject fields."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Subject name",
    )
    code: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Subject code (unique within school)",
    )
    description: str | None = Field(
        None,
        max_length=500,
    )
    is_core: bool = Field(
        default=True,
        description="Whether this is a core or elective subject",
    )
    waec_code: str | None = Field(
        None,
        max_length=20,
        description="WAEC subject code",
    )
    neco_code: str | None = Field(
        None,
        max_length=20,
        description="NECO subject code",
    )


class SubjectCreate(SubjectBase):
    """Schema for creating a new subject."""

    pass


class SubjectUpdate(BaseModel):
    """Schema for updating a subject."""

    name: str | None = Field(None, min_length=1, max_length=100)
    code: str | None = Field(None, min_length=1, max_length=20)
    description: str | None = Field(None, max_length=500)
    is_core: bool | None = None
    waec_code: str | None = Field(None, max_length=20)
    neco_code: str | None = Field(None, max_length=20)


class SubjectResponse(BaseModel):
    """Schema for subject response data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    code: str
    description: str | None = None
    is_core: bool
    waec_code: str | None = None
    neco_code: str | None = None
    created_at: datetime
    updated_at: datetime


class CAScoreEntry(BaseModel):
    """Schema for entering CA scores."""

    student_id: UUID
    subject_id: UUID
    class_id: UUID
    term_id: UUID
    academic_year_id: UUID
    ca_scores: dict = Field(
        default={},
        description="CA component scores {component_name: score}",
    )

    @field_validator("ca_scores")
    @classmethod
    def validate_ca_scores(cls, v: dict) -> dict:
        """Ensure each CA component score is within 0-100."""
        for component, score in v.items():
            if not isinstance(score, (int, float, Decimal)):
                raise ValueError(f"CA score for '{component}' must be a number")
            score_val = float(score)
            if score_val < 0 or score_val > 100:
                raise ValueError(f"CA score for '{component}' must be between 0 and 100")
        return v
    exam_score: Decimal | None = Field(
        None,
        ge=0,
        le=100,
        description="Exam score",
    )
    flag: str | None = Field(None, max_length=10)


class CAScoreBulkEntry(BaseModel):
    """Schema for bulk CA score entry."""

    subject_id: UUID
    class_id: UUID
    term_id: UUID
    scores: list[CAScoreEntry]


class AcademicResultCreate(BaseModel):
    """Schema for creating an academic result."""

    student_id: UUID
    subject_id: UUID
    class_id: UUID
    term_id: UUID
    ca_scores: dict = Field(default={})
    ca_total: Decimal = Field(ge=0, le=30)
    exam_score: Decimal = Field(ge=0, le=70)
    total_score: Decimal = Field(ge=0, le=100)
    flag: str | None = Field(None, max_length=10)


class AcademicResultUpdate(BaseModel):
    """Schema for updating an academic result."""

    ca_scores: dict | None = None
    ca_total: Decimal | None = Field(None, ge=0, le=30)
    exam_score: Decimal | None = Field(None, ge=0, le=70)
    total_score: Decimal | None = Field(None, ge=0, le=100)
    flag: str | None = Field(None, max_length=10)


class AcademicResultResponse(BaseModel):
    """Schema for academic result response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    subject_id: UUID
    class_id: UUID
    term_id: UUID
    school_id: UUID
    ca_scores: dict | None = None
    ca_total: Decimal
    exam_score: Decimal
    total_score: Decimal
    grade: str | None = None
    class_rank: int | None = None
    flag: str | None = None
    teacher_id: UUID | None = None
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class GradingScaleCreate(BaseModel):
    """Schema for creating a grading scale."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    is_default: bool = False


class GradingScaleResponse(BaseModel):
    """Schema for grading scale response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    is_default: bool
    created_at: datetime
    updated_at: datetime


class GradingScaleDetailCreate(BaseModel):
    """Schema for grading scale detail."""

    grade: str = Field(..., max_length=5)
    min_score: Decimal = Field(ge=0, le=100)
    max_score: Decimal = Field(ge=0, le=100)
    remark: str | None = Field(None, max_length=50)
    position: int = Field(ge=1)


class GradingScaleDetailResponse(BaseModel):
    """Schema for grading scale detail response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    grading_scale_id: UUID
    grade: str
    min_score: Decimal
    max_score: Decimal
    remark: str | None = None
    position: int


class ReportCardCreate(BaseModel):
    """Schema for creating a report card."""

    student_id: UUID
    term_id: UUID


class ReportCardResponse(BaseModel):
    """Schema for report card response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    term_id: UUID
    academic_year_id: UUID
    class_id: UUID
    school_id: UUID
    overall_average: Decimal
    class_rank: int | None = None
    total_students: int | None = None
    attendance_summary: dict | None = None
    nurse_remark: str | None = None
    principal_remark: str | None = None
    generated_at: datetime | None = None
    pdf_url: str | None = None
    created_at: datetime
    updated_at: datetime


class ReportCardBulkGenerate(BaseModel):
    """Schema for bulk report card generation."""

    class_id: UUID
    term_id: UUID
    student_ids: list[UUID] | None = None  # If None, generate for all students


class ComputeGradesRequest(BaseModel):
    """Schema for grade computation request."""

    class_id: UUID
    term_id: UUID


class ReportCardDeliveryRequest(BaseModel):
    term_id: str
    academic_year_id: UUID
    delivery_method: str = Field(..., description="e.g., whatsapp, sms, email")
    student_ids: list[UUID] | None = None
