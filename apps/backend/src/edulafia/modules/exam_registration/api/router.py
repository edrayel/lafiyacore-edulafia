"""Exam registration API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.exam_registration.repository import ExamRegistrationRepository
from edulafia.modules.exam_registration.schemas import (
    ExamRegistrationCreate,
    ExamRegistrationResponse,
    ExamRegistrationUpdate,
)
from edulafia.modules.exam_registration.service import ExamRegistrationService

router = APIRouter(prefix="/exam-registration", tags=["Exam Registration"])


def get_exam_service(db: AsyncSession = Depends(get_db)) -> ExamRegistrationService:
    """Dependency to get ExamRegistrationService."""
    repository = ExamRegistrationRepository(db)
    return ExamRegistrationService(repository)


@router.post(
    "",
    response_model=ExamRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an exam registration",
)
async def create_exam_registration(
    data: ExamRegistrationCreate,
    current_user: CurrentUser,
    service: ExamRegistrationService = Depends(get_exam_service),
) -> ExamRegistrationResponse:
    """Create a new exam registration."""
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
    "/{registration_id}",
    response_model=ExamRegistrationResponse,
    summary="Get an exam registration by ID",
)
async def get_exam_registration(
    registration_id: UUID,
    current_user: CurrentUser,
    service: ExamRegistrationService = Depends(get_exam_service),
) -> ExamRegistrationResponse:
    """Get an exam registration by ID."""
    registration = await service.get_by_id(registration_id=registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam registration not found",
        )
    return registration


@router.get(
    "",
    response_model=list[ExamRegistrationResponse],
    summary="List exam registrations",
)
async def list_exam_registrations(
    current_user: CurrentUser,
    service: ExamRegistrationService = Depends(get_exam_service),
) -> list[ExamRegistrationResponse]:
    """List all exam registrations for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.get(
    "/student/{student_id}",
    response_model=list[ExamRegistrationResponse],
    summary="List exam registrations for a student",
)
async def list_student_exam_registrations(
    student_id: UUID,
    current_user: CurrentUser,
    service: ExamRegistrationService = Depends(get_exam_service),
) -> list[ExamRegistrationResponse]:
    """List all exam registrations for a student."""
    return await service.list_by_student(student_id=student_id)


@router.patch(
    "/{registration_id}",
    response_model=ExamRegistrationResponse,
    summary="Update an exam registration",
)
async def update_exam_registration(
    registration_id: UUID,
    data: ExamRegistrationUpdate,
    current_user: CurrentUser,
    service: ExamRegistrationService = Depends(get_exam_service),
) -> ExamRegistrationResponse:
    """Update an exam registration."""
    try:
        return await service.update(
            registration_id=registration_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
