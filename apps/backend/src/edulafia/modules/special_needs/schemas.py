"""Special needs / IEP schemas."""
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IEPCreate(BaseModel):
    student_id: UUID
    disability_type: str
    diagnosis_date: date | None = None
    diagnosed_by: str | None = None
    goals: dict | None = None
    accommodations: dict | None = None
    support_staff: dict | None = None
    review_date: date | None = None

class IEPUpdate(BaseModel):
    goals: dict | None = None
    accommodations: dict | None = None
    support_staff: dict | None = None
    status: str | None = None
    review_date: date | None = None

class IEPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    student_id: UUID
    school_id: UUID
    disability_type: str
    diagnosis_date: date | None
    diagnosed_by: str | None
    goals: dict | None
    accommodations: dict | None
    support_staff: dict | None
    status: str
    review_date: date | None
    reviewed_by: UUID | None
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime
