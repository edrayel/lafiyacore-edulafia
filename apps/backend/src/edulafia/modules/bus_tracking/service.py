"""Bus tracking service for business logic operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from edulafia.modules.bus_tracking.repository import (
    BusAttendanceRepository,
    BusRouteRepository,
    BusStopRepository,
)
from edulafia.modules.bus_tracking.schemas import (
    BusAttendanceCreate,
    BusAttendanceResponse,
    BusAttendanceUpdate,
    BusRouteCreate,
    BusRouteResponse,
    BusRouteUpdate,
    BusStopCreate,
    BusStopResponse,
)


class BusRouteService:
    """Service for bus route business logic."""

    def __init__(self, repository: BusRouteRepository):
        self.repository = repository

    async def create(self, data: BusRouteCreate, user_id: UUID) -> BusRouteResponse:
        """Create a new bus route."""
        route_data = data.model_dump()
        route = await self.repository.create(route_data)
        return BusRouteResponse.model_validate(route)

    async def get_by_id(self, route_id: UUID, school_id: UUID) -> BusRouteResponse | None:
        """Get a bus route by ID."""
        route = await self.repository.get_by_id_and_school(route_id, school_id)
        if route:
            return BusRouteResponse.model_validate(route)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[BusRouteResponse]:
        """List all bus routes for a school."""
        routes = await self.repository.list_by_school(school_id)
        return [BusRouteResponse.model_validate(r) for r in routes]

    async def update(self, route_id: UUID, data: BusRouteUpdate, school_id: UUID, user_id: UUID) -> BusRouteResponse:
        """Update a bus route."""
        route = await self.repository.get_by_id_and_school(route_id, school_id)
        if not route:
            raise ValueError(f"Bus route {route_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_route = await self.repository.update(route, update_data)
        return BusRouteResponse.model_validate(updated_route)



    async def delete(self, route_id: UUID, school_id: UUID) -> None:
        """Delete a record."""
        record = await self.repository.get_by_id_and_school(route_id, school_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
class BusStopService:
    """Service for bus stop business logic."""

    def __init__(self, repository: BusStopRepository):
        self.repository = repository

    async def create(self, data: BusStopCreate, user_id: UUID) -> BusStopResponse:
        """Create a new bus stop."""
        stop_data = data.model_dump()
        stop = await self.repository.create(stop_data)
        return BusStopResponse.model_validate(stop)

    async def list_by_route(self, route_id: UUID) -> Sequence[BusStopResponse]:
        """List all stops for a route."""
        stops = await self.repository.list_by_route(route_id)
        return [BusStopResponse.model_validate(s) for s in stops]

    async def update(self, stop_id: UUID, data: BusStopCreate, user_id: UUID) -> BusStopResponse:
        """Update a bus stop."""
        stop = await self.repository.get_by_id(stop_id)
        if not stop:
            raise ValueError(f"Bus stop {stop_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_stop = await self.repository.update(stop, update_data)
        return BusStopResponse.model_validate(updated_stop)


class BusAttendanceService:
    """Service for bus attendance business logic."""

    def __init__(self, repository: BusAttendanceRepository):
        self.repository = repository

    async def create(self, data: BusAttendanceCreate, user_id: UUID) -> BusAttendanceResponse:
        """Create a new bus attendance record."""
        attendance_data = data.model_dump()
        attendance = await self.repository.create(attendance_data)
        return BusAttendanceResponse.model_validate(attendance)

    async def get_by_student_and_date(self, student_id: UUID, attendance_date: date) -> BusAttendanceResponse | None:
        """Get attendance by student and date."""
        attendance = await self.repository.get_by_student_and_date(student_id, attendance_date)
        if attendance:
            return BusAttendanceResponse.model_validate(attendance)
        return None

    async def list_by_route_and_date(self, route_id: UUID, attendance_date: date) -> Sequence[BusAttendanceResponse]:
        """List attendance for a route on a date."""
        attendance_records = await self.repository.list_by_route_and_date(route_id, attendance_date)
        return [BusAttendanceResponse.model_validate(a) for a in attendance_records]

    async def update(self, attendance_id: UUID, data: BusAttendanceUpdate, user_id: UUID) -> BusAttendanceResponse:
        """Update a bus attendance record."""
        attendance = await self.repository.get_by_id(attendance_id)
        if not attendance:
            raise ValueError(f"Bus attendance {attendance_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_attendance = await self.repository.update(attendance, update_data)
        return BusAttendanceResponse.model_validate(updated_attendance)
