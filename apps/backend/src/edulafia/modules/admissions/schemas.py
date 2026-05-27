"""Admission Pydantic schemas for request/response validation."""

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApplicationBase(BaseModel):
    """Base schema with common application fields."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Applicant's first name",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Applicant's last name",
    )
    middle_name: str | None = Field(
        None,
        max_length=100,
        description="Applicant's middle name",
    )
    date_of_birth: date = Field(
        ...,
        description="Applicant's date of birth",
    )
    gender: str = Field(
        ...,
        description="Applicant's gender",
    )
    nationality: str = Field(
        "Nigerian",
        max_length=100,
    )
    state_of_origin: str | None = Field(
        None,
        max_length=100,
    )
    lga_of_origin: str | None = Field(
        None,
        max_length=100,
    )
    previous_school: str | None = Field(
        None,
        max_length=255,
    )
    class_applied_for: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Class the applicant is applying for",
    )
    admission_year: int = Field(
        ...,
        description="Academic year of admission",
    )
    parent_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Parent/Guardian name",
    )
    parent_phone: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Parent/Guardian phone number",
    )
    parent_email: str | None = Field(
        None,
        max_length=255,
        description="Parent/Guardian email",
    )

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        """Validate that date of birth is not in the future."""
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender is male or female."""
        if v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower()


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""


class ApplicationUpdate(BaseModel):
    """Schema for updating an existing application."""

    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    middle_name: str | None = Field(None, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = None
    nationality: str | None = Field(None, max_length=100)
    state_of_origin: str | None = Field(None, max_length=100)
    lga_of_origin: str | None = Field(None, max_length=100)
    previous_school: str | None = Field(None, max_length=255)
    class_applied_for: str | None = Field(None, min_length=1, max_length=50)
    admission_year: int | None = None
    parent_name: str | None = Field(None, min_length=1, max_length=200)
    parent_phone: str | None = Field(None, min_length=1, max_length=20)
    parent_email: str | None = Field(None, max_length=255)
    exam_score: float | None = None
    interview_score: float | None = None
    interview_notes: str | None = None

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str | None) -> str | None:
        """Validate gender is male or female."""
        if v is not None and v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower() if v else v


class ApplicationResponse(BaseModel):
    """Schema for application response data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    date_of_birth: date
    gender: str
    nationality: str
    state_of_origin: str | None = None
    lga_of_origin: str | None = None
    previous_school: str | None = None
    class_applied_for: str
    admission_year: int
    parent_name: str
    parent_phone: str
    parent_email: str | None = None
    status: str
    exam_score: float | None = None
    interview_score: float | None = None
    interview_notes: str | None = None
    created_at: date
    updated_at: date

    @property
    def full_name(self) -> str:
        """Get applicant's full name."""
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)


class ApplicationListResponse(BaseModel):
    """Schema for paginated application list response."""

    items: list[ApplicationResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ApplicationFilters(BaseModel):
    """Schema for application list filters."""

    status: str | None = None
    class_applied_for: str | None = None
    admission_year: int | None = None
    gender: str | None = None
    search: str | None = None  # Full name search
