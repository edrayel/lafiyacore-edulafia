"""Inventory Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssetBase(BaseModel):
    """Base schema for asset."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None)
    quantity: int = Field(default=1, ge=0)
    unit_value: float = Field(default=0.0, ge=0)
    location: str | None = Field(None, max_length=255)
    condition: str = Field(default="new")
    assigned_to: str | None = Field(None, max_length=255)
    purchase_date: date | None = Field(None)
    depreciation_rate: float = Field(default=0.0, ge=0, le=100)


class AssetCreate(AssetBase):
    """Schema for creating an asset."""


class AssetUpdate(BaseModel):
    """Schema for updating an asset."""

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=255)
    category: str | None = Field(None, max_length=100)
    description: str | None = None
    quantity: int | None = Field(None, ge=0)
    unit_value: float | None = Field(None, ge=0)
    location: str | None = Field(None, max_length=255)
    condition: str | None = None
    assigned_to: str | None = Field(None, max_length=255)
    purchase_date: date | None = None
    depreciation_rate: float | None = Field(None, ge=0, le=100)


class AssetResponse(BaseModel):
    """Schema for asset response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    category: str
    description: str | None = None
    quantity: int
    unit_value: float
    location: str | None = None
    condition: str
    assigned_to: str | None = None
    purchase_date: date | None = None
    depreciation_rate: float
    created_at: datetime
    updated_at: datetime
