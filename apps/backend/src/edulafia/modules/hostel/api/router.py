"""Hostel API router."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.hostel.models import Hostel

from ..schemas import (
    BedAllocationCreate,
    BedAllocationResponse,
    BedAllocationUpdate,
    HostelCreate,
    HostelResponse,
    HostelUpdate,
    RoomCreate,
    RoomResponse,
    RoomUpdate,
)
from ..service import HostelService

router = APIRouter(prefix="/hostel", tags=["Hostel"])


def get_hostel_service(db: AsyncSession = Depends(get_db)) -> HostelService:
    return HostelService(db)


# Hostel Endpoints
@router.post("/hostels", response_model=HostelResponse, status_code=status.HTTP_201_CREATED)
async def create_hostel(
    data: HostelCreate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.create_hostel(data, UUID(current_user["school_id"]))

@router.get("/hostels/{hostel_id}", response_model=HostelResponse)
async def get_hostel(
    hostel_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_hostel(hostel_id, UUID(current_user["school_id"]))

@router.get(
    "/hostels",
    response_model=Page[HostelResponse],
    summary="List all hostels",
)
async def list_hostels(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    service: HostelService = Depends(get_hostel_service),
) -> dict:
    """List hostels for a school with pagination."""
    return await service.get_hostels(
        school_id=UUID(current_user["school_id"]),
        page=pag.page,
        per_page=pag.per_page,
    )

@router.patch("/hostels/{hostel_id}", response_model=HostelResponse)
async def update_hostel(
    hostel_id: UUID,
    data: HostelUpdate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.update_hostel(hostel_id, data, UUID(current_user["school_id"]))

@router.delete("/hostels/{hostel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hostel(
    hostel_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    await service.delete_hostel(hostel_id, UUID(current_user["school_id"]))

# Room Endpoints
@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    data: RoomCreate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.create_room(data, UUID(current_user["school_id"]))

@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_room(room_id, UUID(current_user["school_id"]))

@router.get("/hostels/{hostel_id}/rooms", response_model=List[RoomResponse])
async def get_rooms(
    hostel_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_rooms(hostel_id, UUID(current_user["school_id"]))

@router.patch("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: UUID,
    data: RoomUpdate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.update_room(room_id, data, UUID(current_user["school_id"]))

@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    await service.delete_room(room_id, UUID(current_user["school_id"]))

# Bed Allocation Endpoints
@router.post("/allocations", response_model=BedAllocationResponse, status_code=status.HTTP_201_CREATED)
async def create_allocation(
    data: BedAllocationCreate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.create_allocation(data, UUID(current_user["school_id"]))

@router.get("/allocations/{allocation_id}", response_model=BedAllocationResponse)
async def get_allocation(
    allocation_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_allocation(allocation_id, UUID(current_user["school_id"]))

@router.get("/rooms/{room_id}/allocations", response_model=List[BedAllocationResponse])
async def get_allocations_by_room(
    room_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_allocations_by_room(room_id, UUID(current_user["school_id"]))

@router.get("/students/{student_id}/allocations", response_model=List[BedAllocationResponse])
async def get_allocations_by_student(
    student_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.get_allocations_by_student(student_id, UUID(current_user["school_id"]))

@router.patch("/allocations/{allocation_id}", response_model=BedAllocationResponse)
async def update_allocation(
    allocation_id: UUID,
    data: BedAllocationUpdate,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    return await service.update_allocation(allocation_id, data, UUID(current_user["school_id"]))

@router.delete("/allocations/{allocation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allocation(
    allocation_id: UUID,
    current_user: CurrentUser,
    service: HostelService = Depends(get_hostel_service),
):
    await service.delete_allocation(allocation_id, UUID(current_user["school_id"]))
