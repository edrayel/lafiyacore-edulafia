"""Fundraising Pydantic schemas."""

from datetime import date as DateType
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    """Base schema for campaign."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None)
    target_amount: float = Field(default=0.0, ge=0)
    start_date: DateType = Field(...)
    end_date: DateType = Field(...)
    status: str = Field(default="active")


class CampaignCreate(CampaignBase):
    """Schema for creating a campaign."""

    pass


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign."""

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=255)
    description: str | None = None
    target_amount: float | None = Field(None, ge=0)
    start_date: DateType | None = None
    end_date: DateType | None = None
    status: str | None = None


class CampaignResponse(BaseModel):
    """Schema for campaign response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    target_amount: float
    start_date: DateType
    end_date: DateType
    status: str
    created_at: datetime
    updated_at: datetime


class DonationBase(BaseModel):
    """Base schema for donation."""

    campaign_id: UUID = Field(..., description="ID of the campaign")
    donor_name: str = Field(..., min_length=1, max_length=255)
    donor_phone: str | None = Field(None, max_length=20)
    amount: float = Field(default=0.0, ge=0)
    date: DateType = Field(...)
    notes: str | None = Field(None)


class CampaignUpdateRequest(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    target_amount: float | None = Field(None, gt=0)
    end_date: DateType | None = None
    status: str | None = Field(None, max_length=50)


class DonationCreate(BaseModel):
    campaign_id: UUID
    donor_name: str = Field(..., max_length=150)
    amount: float = Field(..., gt=0)
    is_anonymous: bool = False
    payment_reference: str | None = None


class DonationResponse(DonationCreate):
    id: UUID
    school_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DonationUpdateRequest(BaseModel):
    amount: float | None = Field(None, gt=0)
    payment_reference: str | None = None
