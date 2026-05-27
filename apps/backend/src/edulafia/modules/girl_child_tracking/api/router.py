"""Girl child tracking API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.girl_child_tracking.repository import GirlChildRecordRepository
from edulafia.modules.girl_child_tracking.schemas import (
    GirlChildRecordCreate,
    GirlChildRecordResponse,
    GirlChildRecordUpdate,
)
from edulafia.modules.girl_child_tracking.service import GirlChildRecordService

router = APIRouter(prefix="/girl-child", tags=["Girl Child Tracking"])


def get_girl_child_service(db: AsyncSession = Depends(get_db)) -> GirlChildRecordService:
    """Dependency to get GirlChildRecordService."""
    repository = GirlChildRecordRepository(db)
    return GirlChildRecordService(repository)


@router.post(
    "",
    response_model=GirlChildRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a girl child record",
)
async def create_girl_child_record(
    data: GirlChildRecordCreate,
    current_user: CurrentUser,
    service: GirlChildRecordService = Depends(get_girl_child_service),
) -> GirlChildRecordResponse:
    """Create a new girl child record."""
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
    response_model=GirlChildRecordResponse,
    summary="Get a girl child record by ID",
)
async def get_girl_child_record(
    record_id: UUID,
    current_user: CurrentUser,
    service: GirlChildRecordService = Depends(get_girl_child_service),
) -> GirlChildRecordResponse:
    """Get a girl child record by ID."""
    record = await service.get_by_id(record_id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Girl child record not found",
        )
    return record


@router.get(
    "/student/{student_id}",
    response_model=GirlChildRecordResponse,
    summary="Get a girl child record by student",
)
async def get_girl_child_by_student(
    student_id: UUID,
    current_user: CurrentUser,
    service: GirlChildRecordService = Depends(get_girl_child_service),
) -> GirlChildRecordResponse:
    """Get a girl child record by student ID."""
    record = await service.get_by_student_id(student_id=student_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Girl child record not found for student",
        )
    return record


@router.get(
    "/risk/{risk_level}",
    response_model=list[GirlChildRecordResponse],
    summary="List girl child records by dropout risk",
)
async def list_by_dropout_risk(
    risk_level: str,
    current_user: CurrentUser,
    service: GirlChildRecordService = Depends(get_girl_child_service),
) -> list[GirlChildRecordResponse]:
    """List girl child records by dropout risk level."""
    return await service.list_by_dropout_risk(risk_level=risk_level)


@router.patch(
    "/{record_id}",
    response_model=GirlChildRecordResponse,
    summary="Update a girl child record",
)
async def update_girl_child_record(
    record_id: UUID,
    data: GirlChildRecordUpdate,
    current_user: CurrentUser,
    service: GirlChildRecordService = Depends(get_girl_child_service),
) -> GirlChildRecordResponse:
    """Update a girl child record."""
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
