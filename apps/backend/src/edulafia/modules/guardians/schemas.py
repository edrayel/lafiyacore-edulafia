"""Guardian Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GuardianBase(BaseModel):
    """Base schema with common guardian fields."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    middle_name: str | None = Field(
        None,
        max_length=100,
    )
    phone_number: str = Field(
        ...,
        min_length=13,
        max_length=14,
        description="Phone number in +234XXXXXXXXXX format",
    )
    relationship_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Relationship to student (e.g., father, mother, guardian)",
    )
    email: str | None = Field(
        None,
        max_length=255,
    )
    whatsapp_number: str | None = Field(
        None,
        min_length=13,
        max_length=14,
    )
    occupation: str | None = Field(
        None,
        max_length=100,
    )
    address: str | None = Field(
        None,
        max_length=500,
    )
    nin: str | None = Field(
        None,
        min_length=11,
        max_length=11,
    )

    @field_validator("phone_number", "whatsapp_number")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Validate phone number format."""
        if v is not None:
            if not v.startswith("+234"):
                raise ValueError("Phone number must start with +234")
            digits = v[4:]
            if not digits.isdigit() or len(digits) != 10:
                raise ValueError("Phone number must be +234 followed by 10 digits")
        return v

    @field_validator("nin")
    @classmethod
    def validate_nin(cls, v: str | None) -> str | None:
        """Validate NIN is 11 digits."""
        if v is not None:
            if not v.isdigit() or len(v) != 11:
                raise ValueError("NIN must be exactly 11 digits")
        return v


class GuardianCreate(GuardianBase):
    """Schema for creating a new guardian."""

    is_primary: bool = Field(
        default=False,
        description="Whether this is the primary contact",
    )
    is_emergency_contact: bool = Field(
        default=False,
        description="Whether this is an emergency contact",
    )


class GuardianUpdate(BaseModel):
    """Schema for updating a guardian."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    middle_name: str | None = Field(None, max_length=100)
    relationship_type: str | None = Field(None, min_length=1, max_length=50)
    phone_number: str | None = Field(None, min_length=13, max_length=14, description="Phone number in +234XXXXXXXXXX format")
    email: str | None = Field(None, max_length=255)
    whatsapp_number: str | None = Field(None, min_length=13, max_length=14)
    occupation: str | None = Field(None, max_length=100)
    address: str | None = Field(None, max_length=500)
    nin: str | None = Field(None, min_length=11, max_length=11)

    @field_validator("phone_number", "whatsapp_number")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Validate phone number format."""
        if v is not None:
            if not v.startswith("+234"):
                raise ValueError("Phone number must start with +234")
            digits = v[4:]
            if not digits.isdigit() or len(digits) != 10:
                raise ValueError("Phone number must be +234 followed by 10 digits")
        return v

    @field_validator("nin")
    @classmethod
    def validate_nin(cls, v: str | None) -> str | None:
        """Validate NIN is 11 digits."""
        if v is not None:
            if not v.isdigit() or len(v) != 11:
                raise ValueError("NIN must be exactly 11 digits")
        return v


class GuardianResponse(BaseModel):
    """Schema for guardian response data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone_number: str
    relationship_type: str
    email: str | None = None
    whatsapp_number: str | None = None
    occupation: str | None = None
    address: str | None = None
    nin: str | None = None
    portal_access: bool
    created_at: datetime
    updated_at: datetime

    @property
    def full_name(self) -> str:
        """Get guardian's full name."""
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)


class StudentGuardianLink(BaseModel):
    """Schema for linking a guardian to a student."""

    student_id: UUID
    guardian_id: UUID
    is_primary: bool = False
    is_emergency_contact: bool = False
    can_pickup: bool = True
