"""Calendar Pydantic schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    """Base schema with common event fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Event title")
    description: str | None = Field(None, description="Event description")
    start_date: datetime = Field(..., description="Start date and time of the event")
    end_date: datetime = Field(..., description="End date and time of the event")
    event_type: str = Field(..., min_length=1, max_length=50, description="Type of event (e.g. holiday, exam, term_dates)")


class EventCreate(EventBase):
    """Schema for creating a new event."""
    pass


class EventUpdate(BaseModel):
    """Schema for updating an event."""

    title: str | None = Field(None, max_length=200)
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    event_type: str | None = Field(None, max_length=50)
    is_public: bool | None = None


class EventResponse(BaseModel):
    """Schema for event response data."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    title: str
    description: str | None = None
    start_date: datetime
    end_date: datetime
    event_type: str
    created_at: datetime
    updated_at: datetime
