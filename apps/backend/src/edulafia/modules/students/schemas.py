"""Student Pydantic schemas for request/response validation."""

import uuid
from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    """Base schema with common student fields."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Student's first name",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Student's last name",
    )
    middle_name: str | None = Field(
        None,
        max_length=100,
        description="Student's middle name",
    )
    date_of_birth: date = Field(
        ...,
        description="Student's date of birth",
    )
    gender: str = Field(
        ...,
        description="Student's gender (male/female)",
    )
    admission_number: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unique admission number within school",
    )
    admission_date: date = Field(
        ...,
        description="Date of admission",
    )
    class_id: UUID | None = Field(
        None,
        description="ID of the class the student is enrolled in",
    )

    # Optional fields
    nationality: str | None = Field(
        "Nigerian",
        max_length=100,
    )
    state_of_origin: str | None = Field(
        None,
        max_length=100,
    )
    lga: str | None = Field(
        None,
        max_length=100,
    )
    address: str | None = Field(
        None,
        max_length=500,
    )
    blood_group: str | None = Field(
        None,
        max_length=5,
    )
    genotype: str | None = Field(
        None,
        max_length=5,
    )
    nin: str | None = Field(
        None,
        description="National Identification Number",
    )

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        """Validate that date of birth is between 6 and 20 years ago."""
        today = date.today()
        if v > today:
            raise ValueError("Date of birth cannot be in the future")
        
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 6 or age > 20:
            raise ValueError("Student age must be between 6 and 20 years")
        return v

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender is male or female."""
        if v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower()

    @field_validator("nin")
    @classmethod
    def validate_nin(cls, v: str | None) -> str | None:
        """Validate NIN is 11 digits if provided."""
        if v is not None:
            if not v.isdigit() or len(v) != 11:
                raise ValueError("NIN must be exactly 11 digits")
        return v


class StudentCreate(StudentBase):
    """Schema for creating a new student."""

    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, v: date) -> date:
        """Validate student age is between 6 and 20."""
        today = date.today()
        age = (today - v).days / 365.25
        if age < 6 or age > 20:
            raise ValueError("Student must be between 6 and 20 years old")
        return v


class StudentUpdate(BaseModel):
    """Schema for updating an existing student."""

    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
    )
    middle_name: str | None = Field(
        None,
        max_length=100,
    )
    date_of_birth: date | None = None
    gender: str | None = None
    class_id: UUID | None = None
    nationality: str | None = Field(None, max_length=100)
    state_of_origin: str | None = Field(None, max_length=100)
    lga: str | None = Field(None, max_length=100)
    address: str | None = Field(None, max_length=500)
    blood_group: str | None = Field(None, max_length=5)
    genotype: str | None = Field(None, max_length=5)
    nin: str | None = Field(None, description="National Identification Number")
    previous_school: str | None = Field(None, max_length=255)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str | None) -> str | None:
        """Validate gender is male or female."""
        if v is not None and v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower() if v else v

    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, v):
        """Validate student age is between 6 and 20."""
        if v:
            age = (date.today() - v).days // 365
            if age < 6 or age > 20:
                raise ValueError("Student age must be between 6 and 20")
        return v

    @field_validator("nin")
    @classmethod
    def validate_nin(cls, v: str | None) -> str | None:
        """Validate NIN is 11 digits if provided."""
        if v is not None:
            if not v.isdigit() or len(v) != 11:
                raise ValueError("NIN must be exactly 11 digits")
        return v


class StudentResponse(BaseModel):
    """Schema for student response data (public profile, no NIN or health data)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    admission_number: str
    first_name: str
    last_name: str
    middle_name: str | None = None
    date_of_birth: date
    gender: str
    status: str
    admission_date: date
    class_id: UUID | None = None
    nationality: str
    state_of_origin: str | None = None
    lga: str | None = None
    address: str | None = None
    photo_url: str | None = None
    previous_school: str | None = None
    graduation_date: date | None = None
    created_at: datetime
    updated_at: datetime

    @property
    def full_name(self) -> str:
        """Get student's full name."""
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)

    @property
    def age(self) -> int:
        """Calculate student's current age."""
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )


class StudentListResponse(BaseModel):
    """Schema for paginated student list response."""

    items: list[StudentResponse]
    total: int
    page: int
    per_page: int
    pages: int


class StudentFilters(BaseModel):
    """Schema for student list filters."""

    class_id: UUID | None = None
    status: str | None = None
    gender: str | None = None
    search: str | None = None  # Full name or admission number search
    age_min: int | None = None
    age_max: int | None = None
    guardian_id: UUID | None = None


# ==========================================
# Student Document Schemas
# ==========================================

class StudentDocumentBase(BaseModel):
    """Base schema for student document properties."""
    
    document_type: str = Field(..., max_length=50, description="E.g., admission_letter, birth_certificate")
    title: str = Field(..., max_length=200)
    file_url: str = Field(..., max_length=1000)
    file_size_bytes: int | None = None
    mime_type: str | None = Field(None, max_length=100)


class StudentDocumentCreate(StudentDocumentBase):
    """Schema for creating a student document."""
    pass


class StudentDocumentResponse(StudentDocumentBase):
    """Schema for student document response."""
    
    id: UUID
    student_id: UUID
    created_at: datetime
    updated_at: datetime
    uploaded_by: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class StudentDocumentListResponse(BaseModel):
    """Response schema for a list of student documents."""
    
    items: list[StudentDocumentResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ExportDataRequest(BaseModel):
    export_type: str = Field("transfer", description="e.g., transfer, backup, full_record")
    include_medical: bool = True
    include_financial: bool = False
    include_attendance: bool = True
    include_academics: bool = True
