"""Bus tracking Pydantic schemas."""

from datetime import date as DateType
from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BusRouteBase(BaseModel):
    """Base schema for bus route."""

    school_id: UUID = Field(..., description="ID of the school")
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)
    driver_name: str = Field(..., min_length=1, max_length=255)
    driver_phone: str = Field(..., min_length=1, max_length=20)
    capacity: int = Field(default=0, ge=0)


class BusRouteCreate(BusRouteBase):
    """Schema for creating a bus route."""


class BusRouteUpdate(BaseModel):
    """Schema for updating a bus route."""

    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=500)
    driver_name: str | None = Field(None, max_length=255)
    driver_phone: str | None = Field(None, max_length=20)
    capacity: int | None = Field(None, ge=0)


class BusRouteResponse(BaseModel):
    """Schema for bus route response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    name: str
    description: str | None = None
    driver_name: str
    driver_phone: str
    capacity: int
    created_at: datetime
    updated_at: datetime


class BusStopBase(BaseModel):
    """Base schema for bus stop."""

    route_id: UUID = Field(..., description="ID of the route")
    stop_name: str = Field(..., min_length=1, max_length=255)
    location: str = Field(..., max_length=500)
    estimated_time: time | None = Field(None)


class BusStopCreate(BusStopBase):
    """Schema for creating a bus stop."""


class BusStopResponse(BaseModel):
    """Schema for bus stop response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    route_id: UUID
    stop_name: str
    location: str
    estimated_time: time | None = None
    created_at: datetime
    updated_at: datetime


class BusAttendanceBase(BaseModel):
    """Base schema for bus attendance."""

    student_id: UUID = Field(..., description="ID of the student")
    route_id: UUID = Field(..., description="ID of the route")
    date: DateType = Field(...)
    boarded: bool = Field(default=False)
    alighted: bool = Field(default=False)
    board_time: time | None = Field(None)
    alight_time: time | None = Field(None)


class BusAttendanceCreate(BusAttendanceBase):
    """Schema for creating a bus attendance record."""


class BusAttendanceUpdate(BaseModel):
    """Schema for updating a bus attendance record."""

    model_config = ConfigDict(from_attributes=True)

    boarded: bool | None = None
    alighted: bool | None = None
    board_time: time | None = None
    alight_time: time | None = None


class BusAttendanceResponse(BaseModel):
    """Schema for bus attendance response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    route_id: UUID
    date: DateType
    boarded: bool
    alighted: bool
    board_time: time | None = None
    alight_time: time | None = None
    created_at: datetime
    updated_at: datetime
