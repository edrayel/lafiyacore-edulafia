"""Alumni API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.alumni.repository import AlumniRepository
from edulafia.modules.alumni.schemas import (
    AlumniProfileCreate,
    AlumniProfileResponse,
    AlumniProfileUpdate,
)
from edulafia.modules.alumni.service import AlumniService

router = APIRouter(prefix="/alumni", tags=["Alumni"])


def get_alumni_service(db: AsyncSession = Depends(get_db)) -> AlumniService:
    """Dependency to get AlumniService."""
    repository = AlumniRepository(db)
    return AlumniService(repository)


@router.post(
    "",
    response_model=AlumniProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an alumni profile",
)
async def create_alumni_profile(
    data: AlumniProfileCreate,
    current_user: CurrentUser,
    service: AlumniService = Depends(get_alumni_service),
) -> AlumniProfileResponse:
    """Create a new alumni profile."""
    try:
        return await service.create(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{profile_id}",
    response_model=AlumniProfileResponse,
    summary="Get an alumni profile by ID",
)
async def get_alumni_profile(
    profile_id: UUID,
    current_user: CurrentUser,
    service: AlumniService = Depends(get_alumni_service),
) -> AlumniProfileResponse:
    """Get an alumni profile by ID."""
    profile = await service.get_by_id(
        profile_id=profile_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumni profile not found",
        )
    return profile


@router.get(
    "",
    response_model=list[AlumniProfileResponse],
    summary="List alumni profiles",
)
async def list_alumni_profiles(
    current_user: CurrentUser,
    service: AlumniService = Depends(get_alumni_service),
) -> list[AlumniProfileResponse]:
    """List all alumni profiles for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{profile_id}",
    response_model=AlumniProfileResponse,
    summary="Update an alumni profile",
)
async def update_alumni_profile(
    profile_id: UUID,
    data: AlumniProfileUpdate,
    current_user: CurrentUser,
    service: AlumniService = Depends(get_alumni_service),
) -> AlumniProfileResponse:
    """Update an alumni profile."""
    try:
        return await service.update(
            profile_id=profile_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{profile_id}",
    summary="Delete an alumni profile",
)
async def delete_alumni_profile(
    profile_id: UUID,
    current_user: CurrentUser,
    service: AlumniService = Depends(get_alumni_service),
) -> dict:
    """Delete an alumni profile."""
    try:
        await service.delete(
            profile_id=profile_id,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
        return {"message": "Alumni profile deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
