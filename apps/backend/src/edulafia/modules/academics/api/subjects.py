"""Subject API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.academics.exceptions import (
    DuplicateSubjectCodeError,
    SubjectNotFoundError,
)
from edulafia.modules.academics.repository import SubjectRepository
from edulafia.modules.academics.schemas import (
    SubjectCreate,
    SubjectResponse,
    SubjectUpdate,
)
from edulafia.modules.academics.service import SubjectService

router = APIRouter(prefix="/subjects", tags=["Subjects"])


def get_subject_service(db: AsyncSession = Depends(get_db)) -> SubjectService:
    """Dependency to get SubjectService."""
    repository = SubjectRepository(db)
    return SubjectService(repository)


@router.post(
    "",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new subject",
)
async def create_subject(
    data: SubjectCreate,
    current_user: CurrentUser,
    service: SubjectService = Depends(get_subject_service),
) -> SubjectResponse:
    """Create a new subject."""
    try:
        return await service.create(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateSubjectCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=dict,
    summary="List subjects",
)
async def list_subjects(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    is_core: bool | None = Query(None),
    service: SubjectService = Depends(get_subject_service),
) -> dict:
    """List subjects with pagination and optional filter."""
    return await service.list_subjects(
        school_id=UUID(current_user["school_id"]),
        page=page,
        per_page=per_page,
        is_core=is_core,
    )


@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
    summary="Get a subject by ID",
)
async def get_subject(
    subject_id: UUID,
    current_user: CurrentUser,
    service: SubjectService = Depends(get_subject_service),
) -> SubjectResponse:
    """Get a subject's details by ID."""
    subject = await service.get_by_id(
        subject_id=subject_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    return subject


@router.patch(
    "/{subject_id}",
    response_model=SubjectResponse,
    summary="Update a subject",
)
async def update_subject(
    subject_id: UUID,
    data: SubjectUpdate,
    current_user: CurrentUser,
    service: SubjectService = Depends(get_subject_service),
) -> SubjectResponse:
    """Update a subject's information."""
    try:
        return await service.update(
            subject_id=subject_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except SubjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )


@router.delete(
    "/{subject_id}",
    response_model=SubjectResponse,
    summary="Archive a subject",
)
async def archive_subject(
    subject_id: UUID,
    current_user: CurrentUser,
    service: SubjectService = Depends(get_subject_service),
) -> SubjectResponse:
    """Archive a subject (soft delete)."""
    try:
        return await service.archive(
            subject_id=subject_id,
            school_id=UUID(current_user["school_id"]),
        )
    except SubjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
