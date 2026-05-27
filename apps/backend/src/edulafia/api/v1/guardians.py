"""Guardian API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.guardians.repository import GuardianRepository
from edulafia.modules.guardians.schemas import (
    GuardianCreate,
    GuardianResponse,
    GuardianUpdate,
)
from edulafia.modules.guardians.service import GuardianService

router = APIRouter(prefix="/guardians", tags=["Guardians"])


def get_guardian_service(db: AsyncSession = Depends(get_db)) -> GuardianService:
    """Dependency to get GuardianService."""
    repository = GuardianRepository(db)
    return GuardianService(repository)


@router.post(
    "",
    response_model=GuardianResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new guardian",
)
async def create_guardian(
    data: GuardianCreate,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> GuardianResponse:
    """Create a new guardian record."""
    try:
        return await service.create(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=dict,
    summary="List guardians",
)
async def list_guardians(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    service: GuardianService = Depends(get_guardian_service),
) -> dict:
    """List guardians with pagination."""
    return await service.list_guardians(
        school_id=UUID(current_user["school_id"]),
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{guardian_id}",
    response_model=GuardianResponse,
    summary="Get a guardian by ID",
)
async def get_guardian(
    guardian_id: UUID,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> GuardianResponse:
    """Get a guardian's details by ID."""
    guardian = await service.get_by_id(
        guardian_id=guardian_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guardian not found",
        )
    return guardian


@router.patch(
    "/{guardian_id}",
    response_model=GuardianResponse,
    summary="Update a guardian",
)
async def update_guardian(
    guardian_id: UUID,
    data: GuardianUpdate,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> GuardianResponse:
    """Update a guardian's information."""
    try:
        return await service.update(
            guardian_id=guardian_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{guardian_id}",
    response_model=GuardianResponse,
    summary="Archive a guardian",
)
async def archive_guardian(
    guardian_id: UUID,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> GuardianResponse:
    """Archive a guardian (soft delete)."""
    try:
        return await service.archive(
            guardian_id=guardian_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guardian not found",
        )


# Student-Guardian relationship endpoints

@router.post(
    "/{guardian_id}/students/{student_id}",
    summary="Link guardian to student",
)
async def link_guardian_to_student(
    guardian_id: UUID,
    student_id: UUID,
    current_user: CurrentUser,
    is_primary: bool = Query(False),
    is_emergency_contact: bool = Query(False),
    can_pickup: bool = Query(True),
    service: GuardianService = Depends(get_guardian_service),
) -> dict:
    """Link a guardian to a student."""
    try:
        return await service.link_to_student(
            student_id=student_id,
            guardian_id=guardian_id,
            is_primary=is_primary,
            is_emergency_contact=is_emergency_contact,
            can_pickup=can_pickup,
        )
    except ValueError as e:
        if "maximum" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "/students/{student_id}",
    response_model=list[GuardianResponse],
    summary="Get guardians for a student",
)
async def get_student_guardians(
    student_id: UUID,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> list[GuardianResponse]:
    """Get all guardians linked to a student."""
    return await service.get_student_guardians(student_id=student_id)


@router.delete(
    "/{guardian_id}/students/{student_id}",
    summary="Unlink guardian from student",
)
async def unlink_guardian_from_student(
    guardian_id: UUID,
    student_id: UUID,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> dict:
    """Unlink a guardian from a student."""
    try:
        success = await service.unlink_from_student(
            student_id=student_id,
            guardian_id=guardian_id,
        )
        return {"success": success}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
