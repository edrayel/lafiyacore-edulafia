from __future__ import annotations
"""Hostel repository."""

from collections.abc import Sequence
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BedAllocation, Hostel, Room


class HostelRepository:
    """Repository for hostel operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Hostel methods
    async def create_hostel(self, data: dict) -> Hostel:
        hostel = Hostel(**data)
        self.session.add(hostel)
        await self.session.commit()
        await self.session.refresh(hostel)
        return hostel

    async def get_hostel(self, hostel_id: UUID, school_id: UUID) -> Optional[Hostel]:
        result = await self.session.execute(select(Hostel).filter(Hostel.id == hostel_id, Hostel.school_id == school_id))
        return result.scalars().first()

    async def get_hostels(
        self, school_id: UUID, page: int = 1, per_page: int = 20
    ) -> tuple[Sequence[Hostel], int]:
        stmt = select(Hostel).filter(Hostel.school_id == school_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)

        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def update_hostel(self, hostel: Hostel, data: dict) -> Hostel:
        for key, value in data.items():
            setattr(hostel, key, value)
        await self.session.commit()
        await self.session.refresh(hostel)
        return hostel

    async def delete_hostel(self, hostel: Hostel) -> None:
        await self.session.delete(hostel)
        await self.session.commit()

    # Room methods
    async def create_room(self, data: dict) -> Room:
        room = Room(**data)
        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def get_room(self, room_id: UUID, school_id: UUID) -> Optional[Room]:
        result = await self.session.execute(
            select(Room).join(Hostel).filter(Room.id == room_id, Hostel.school_id == school_id)
        )
        return result.scalars().first()

    async def get_room_for_update(self, room_id: UUID, school_id: UUID) -> Optional[Room]:
        result = await self.session.execute(
            select(Room).join(Hostel).filter(Room.id == room_id, Hostel.school_id == school_id).with_for_update()
        )
        return result.scalars().first()

    async def get_rooms(self, hostel_id: UUID, school_id: UUID) -> List[Room]:
        result = await self.session.execute(
            select(Room).join(Hostel).filter(Room.hostel_id == hostel_id, Hostel.school_id == school_id)
        )
        return list(result.scalars().all())

    async def update_room(self, room: Room, data: dict) -> Room:
        for key, value in data.items():
            setattr(room, key, value)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def delete_room(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()

    # Bed Allocation methods
    async def create_allocation(self, data: dict) -> BedAllocation:
        allocation = BedAllocation(**data)
        self.session.add(allocation)
        await self.session.commit()
        await self.session.refresh(allocation)
        return allocation

    async def get_allocation(self, allocation_id: UUID, school_id: UUID) -> Optional[BedAllocation]:
        result = await self.session.execute(
            select(BedAllocation).join(Room).join(Hostel).filter(BedAllocation.id == allocation_id, Hostel.school_id == school_id)
        )
        return result.scalars().first()

    async def get_allocations_by_room(self, room_id: UUID, school_id: UUID) -> List[BedAllocation]:
        result = await self.session.execute(
            select(BedAllocation).join(Room).join(Hostel).filter(BedAllocation.room_id == room_id, Hostel.school_id == school_id)
        )
        return list(result.scalars().all())

    async def get_allocations_by_student(self, student_id: UUID, school_id: UUID) -> List[BedAllocation]:
        result = await self.session.execute(
            select(BedAllocation).join(Room).join(Hostel).filter(BedAllocation.student_id == student_id, Hostel.school_id == school_id)
        )
        return list(result.scalars().all())

    async def update_allocation(self, allocation: BedAllocation, data: dict) -> BedAllocation:
        for key, value in data.items():
            setattr(allocation, key, value)
        await self.session.commit()
        await self.session.refresh(allocation)
        return allocation

    async def delete_allocation(self, allocation: BedAllocation) -> None:
        await self.session.delete(allocation)
        await self.session.commit()
