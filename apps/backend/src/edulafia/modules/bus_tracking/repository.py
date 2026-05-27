from __future__ import annotations
"""Bus tracking repository for data access operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.bus_tracking.models import BusAttendance, BusRoute, BusStop


class BusRouteRepository:
    """Repository for bus route database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> BusRoute:
        """Create a new bus route."""
        route = BusRoute(**data)
        self.db.add(route)
        await self.db.flush()
        await self.db.refresh(route)
        return route

    async def get_by_id(self, route_id: UUID) -> BusRoute | None:
        """Get a bus route by ID."""
        stmt = select(BusRoute).where(BusRoute.id == route_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, route_id: UUID, school_id: UUID) -> BusRoute | None:
        """Get a bus route by ID scoped to school."""
        stmt = select(BusRoute).where(
            BusRoute.id == route_id,
            BusRoute.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[BusRoute]:
        """List all bus routes for a school."""
        stmt = select(BusRoute).where(
            BusRoute.school_id == school_id
        ).order_by(BusRoute.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, route: BusRoute, data: dict) -> BusRoute:
        """Update a bus route."""
        for key, value in data.items():
            if value is not None:
                setattr(route, key, value)
        await self.db.flush()
        await self.db.refresh(route)
        return route

    async def delete(self, route: BusRoute) -> None:
        """Delete a bus route."""
        await self.db.delete(route)
        await self.db.flush()


class BusStopRepository:
    """Repository for bus stop database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> BusStop:
        """Create a new bus stop."""
        stop = BusStop(**data)
        self.db.add(stop)
        await self.db.flush()
        await self.db.refresh(stop)
        return stop

    async def get_by_id(self, stop_id: UUID) -> BusStop | None:
        """Get a bus stop by ID."""
        stmt = select(BusStop).where(BusStop.id == stop_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_route(self, route_id: UUID) -> Sequence[BusStop]:
        """List all stops for a route."""
        stmt = select(BusStop).where(
            BusStop.route_id == route_id
        ).order_by(BusStop.estimated_time)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, stop: BusStop, data: dict) -> BusStop:
        """Update a bus stop."""
        for key, value in data.items():
            if value is not None:
                setattr(stop, key, value)
        await self.db.flush()
        await self.db.refresh(stop)
        return stop

    async def delete(self, stop: BusStop) -> None:
        """Delete a bus stop."""
        await self.db.delete(stop)
        await self.db.flush()


class BusAttendanceRepository:
    """Repository for bus attendance database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> BusAttendance:
        """Create a new bus attendance record."""
        attendance = BusAttendance(**data)
        self.db.add(attendance)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def get_by_id(self, attendance_id: UUID) -> BusAttendance | None:
        """Get a bus attendance record by ID."""
        stmt = select(BusAttendance).where(BusAttendance.id == attendance_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_and_date(self, student_id: UUID, attendance_date: date) -> BusAttendance | None:
        """Get attendance by student and date."""
        stmt = select(BusAttendance).where(
            BusAttendance.student_id == student_id,
            BusAttendance.date == attendance_date,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_route_and_date(self, route_id: UUID, attendance_date: date) -> Sequence[BusAttendance]:
        """List attendance for a route on a date."""
        stmt = select(BusAttendance).where(
            BusAttendance.route_id == route_id,
            BusAttendance.date == attendance_date,
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, attendance: BusAttendance, data: dict) -> BusAttendance:
        """Update a bus attendance record."""
        for key, value in data.items():
            if value is not None:
                setattr(attendance, key, value)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance
