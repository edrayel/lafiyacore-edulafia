"""Discipline API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.discipline.repository import DisciplineRecordRepository
from edulafia.modules.discipline.schemas import (
    DisciplineRecordCreate,
    DisciplineRecordResponse,
    DisciplineRecordUpdate,
)
from edulafia.modules.discipline.service import DisciplineRecordService

router = APIRouter(prefix="/discipline", tags=["Discipline"])


def get_discipline_service(db: AsyncSession = Depends(get_db)) -> DisciplineRecordService:
    """Dependency to get DisciplineRecordService."""
    repository = DisciplineRecordRepository(db)
    return DisciplineRecordService(repository)


@router.post(
    "",
    response_model=DisciplineRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a discipline record",
)
async def create_discipline_record(
    data: DisciplineRecordCreate,
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> DisciplineRecordResponse:
    """Create a new discipline record."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{record_id}",
    response_model=DisciplineRecordResponse,
    summary="Get a discipline record by ID",
)
async def get_discipline_record(
    record_id: UUID,
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> DisciplineRecordResponse:
    """Get a discipline record by ID."""
    record = await service.get_by_id(record_id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discipline record not found",
        )
    return record


@router.get(
    "/student/{student_id}",
    response_model=list[DisciplineRecordResponse],
    summary="List discipline records for a student",
)
async def list_student_discipline_records(
    student_id: UUID,
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> list[DisciplineRecordResponse]:
    """List all discipline records for a student."""
    return await service.list_by_student(student_id=student_id)


@router.get(
    "/open",
    response_model=list[DisciplineRecordResponse],
    summary="List open discipline records",
)
async def list_open_discipline_records(
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> list[DisciplineRecordResponse]:
    """List all open discipline records."""
    return await service.list_open()


@router.patch(
    "/{record_id}",
    response_model=DisciplineRecordResponse,
    summary="Update a discipline record",
)
async def update_discipline_record(
    record_id: UUID,
    data: DisciplineRecordUpdate,
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> DisciplineRecordResponse:
    """Update a discipline record."""
    try:
        return await service.update(
            record_id=record_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{record_id}/resolve",
    response_model=DisciplineRecordResponse,
    summary="Resolve a discipline record",
)
async def resolve_discipline_record(
    record_id: UUID,
    current_user: CurrentUser,
    service: DisciplineRecordService = Depends(get_discipline_service),
) -> DisciplineRecordResponse:
    """Resolve a discipline record."""
    try:
        return await service.resolve(record_id=record_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
