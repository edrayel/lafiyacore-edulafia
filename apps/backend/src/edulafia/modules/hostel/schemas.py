"""Hostel schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HostelBase(BaseModel):
    name: str
    capacity: int
    gender: str


class HostelCreate(HostelBase):
    school_id: UUID


class HostelUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = None
    gender: str | None = None


class HostelResponse(HostelBase):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoomBase(BaseModel):
    room_number: str
    capacity: int


class RoomCreate(RoomBase):
    hostel_id: UUID


class RoomUpdate(BaseModel):
    room_number: str | None = None
    capacity: int | None = None


class RoomResponse(RoomBase):
    id: UUID
    hostel_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BedAllocationBase(BaseModel):
    room_id: UUID
    student_id: UUID
    academic_year_id: UUID


class BedAllocationCreate(BedAllocationBase):
    pass


class BedAllocationUpdate(BaseModel):
    room_id: UUID | None = None
    student_id: UUID | None = None
    academic_year_id: UUID | None = None


class BedAllocationResponse(BedAllocationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AllocationUpdateRequest(BaseModel):
    room_number: str | None = Field(None, max_length=50)
    bed_number: str | None = Field(None, max_length=50)
    status: str | None = Field(None, max_length=20)
    notes: str | None = None
