"""Emergency Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EmergencyModeCreate(BaseModel):
    type: str
    title: str
    description: str | None = None
    start_date: date
    end_date: date | None = None
    protocols: dict | None = None


class EmergencyModeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    type: str
    title: str
    description: str | None
    start_date: date
    end_date: date | None
    status: str
    protocols: dict | None
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime
