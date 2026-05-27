"""Hostel service."""

from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import HostelResponse

from .repository import HostelRepository
from .schemas import (
    BedAllocationCreate,
    BedAllocationUpdate,
    HostelCreate,
    HostelUpdate,
    RoomCreate,
    RoomUpdate,
)


class HostelService:
    """Service for hostel operations."""

    def __init__(self, session: AsyncSession):
        self.repository = HostelRepository(session)

    # Hostel
    async def create_hostel(self, data: HostelCreate, school_id: UUID) -> dict:
        dump = data.model_dump()
        dump["school_id"] = school_id
        hostel = await self.repository.create_hostel(dump)
        return hostel

    async def get_hostel(self, hostel_id: UUID, school_id: UUID) -> dict:
        hostel = await self.repository.get_hostel(hostel_id, school_id)
        if not hostel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
        return hostel

    async def get_hostels(
        self, school_id: UUID, page: int = 1, per_page: int = 20,
    ) -> dict:
        hostels, total = await self.repository.get_hostels(
            school_id, page=page, per_page=per_page,
        )
        return {
            "items": [HostelResponse.model_validate(h) for h in hostels],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def update_hostel(self, hostel_id: UUID, data: HostelUpdate, school_id: UUID) -> dict:
        hostel = await self.repository.get_hostel(hostel_id, school_id)
        if not hostel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
        
        update_data = data.model_dump(exclude_unset=True)
        return await self.repository.update_hostel(hostel, update_data)

    async def delete_hostel(self, hostel_id: UUID, school_id: UUID) -> None:
        hostel = await self.repository.get_hostel(hostel_id, school_id)
        if not hostel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
        await self.repository.delete_hostel(hostel)

    # Room
    async def create_room(self, data: RoomCreate, school_id: UUID) -> dict:
        # Check if hostel exists and belongs to school
        hostel = await self.repository.get_hostel(data.hostel_id, school_id)
        if not hostel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
        
        return await self.repository.create_room(data.model_dump())

    async def get_room(self, room_id: UUID, school_id: UUID) -> dict:
        room = await self.repository.get_room(room_id, school_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room

    async def get_rooms(self, hostel_id: UUID, school_id: UUID) -> List[dict]:
        # Validate hostel belongs to school
        await self.get_hostel(hostel_id, school_id)
        return await self.repository.get_rooms(hostel_id, school_id)

    async def update_room(self, room_id: UUID, data: RoomUpdate, school_id: UUID) -> dict:
        room = await self.repository.get_room(room_id, school_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
        update_data = data.model_dump(exclude_unset=True)
        return await self.repository.update_room(room, update_data)

    async def delete_room(self, room_id: UUID, school_id: UUID) -> None:
        room = await self.repository.get_room(room_id, school_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        await self.repository.delete_room(room)

    # Bed Allocation
    async def create_allocation(self, data: BedAllocationCreate, school_id: UUID) -> dict:
        # Check room exists and belongs to school, with for_update to prevent race condition
        room = await self.repository.get_room_for_update(data.room_id, school_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
            
        # Verify capacity limit
        current_allocations = await self.repository.get_allocations_by_room(data.room_id, school_id)
        if len(current_allocations) >= room.capacity:
            await self.repository.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is full")
            
        return await self.repository.create_allocation(data.model_dump())

    async def get_allocation(self, allocation_id: UUID, school_id: UUID) -> dict:
        allocation = await self.repository.get_allocation(allocation_id, school_id)
        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
        return allocation

    async def get_allocations_by_room(self, room_id: UUID, school_id: UUID) -> List[dict]:
        return await self.repository.get_allocations_by_room(room_id, school_id)

    async def get_allocations_by_student(self, student_id: UUID, school_id: UUID) -> List[dict]:
        return await self.repository.get_allocations_by_student(student_id, school_id)

    async def update_allocation(self, allocation_id: UUID, data: BedAllocationUpdate, school_id: UUID) -> dict:
        allocation = await self.repository.get_allocation(allocation_id, school_id)
        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
            
        update_data = data.model_dump(exclude_unset=True)
        return await self.repository.update_allocation(allocation, update_data)

    async def delete_allocation(self, allocation_id: UUID, school_id: UUID) -> None:
        allocation = await self.repository.get_allocation(allocation_id, school_id)
        if not allocation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
        await self.repository.delete_allocation(allocation)
