"""Clubs API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.clubs.repository import ClubMembershipRepository, ClubRepository
from edulafia.modules.clubs.schemas import (
    ClubCreate,
    ClubMembershipCreate,
    ClubMembershipResponse,
    ClubMembershipUpdateRequest,
    ClubResponse,
    ClubUpdateRequest,
)
from edulafia.modules.clubs.service import ClubMembershipService, ClubService

router = APIRouter(prefix="/clubs", tags=["Clubs"])


def get_club_service(db: AsyncSession = Depends(get_db)) -> ClubService:
    """Dependency to get ClubService."""
    repository = ClubRepository(db)
    return ClubService(repository)


def get_membership_service(db: AsyncSession = Depends(get_db)) -> ClubMembershipService:
    """Dependency to get ClubMembershipService."""
    club_repo = ClubRepository(db)
    membership_repo = ClubMembershipRepository(db)
    return ClubMembershipService(membership_repo, club_repo)


@router.post(
    "",
    response_model=ClubResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a club",
)
async def create_club(
    data: ClubCreate,
    current_user: CurrentUser,
    service: ClubService = Depends(get_club_service),
) -> ClubResponse:
    """Create a new club."""
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
    "/{club_id}",
    response_model=ClubResponse,
    summary="Get a club by ID",
)
async def get_club(
    club_id: UUID,
    current_user: CurrentUser,
    service: ClubService = Depends(get_club_service),
) -> ClubResponse:
    """Get a club by ID."""
    club = await service.get_by_id(
        club_id=club_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found",
        )
    return club


@router.get(
    "",
    response_model=list[ClubResponse],
    summary="List clubs",
)
async def list_clubs(
    current_user: CurrentUser,
    service: ClubService = Depends(get_club_service),
) -> list[ClubResponse]:
    """List all clubs for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{club_id}",
    response_model=ClubResponse,
    summary="Update a club",
)
async def update_club(
    club_id: UUID,
    data: ClubUpdateRequest,
    current_user: CurrentUser,
    service: ClubService = Depends(get_club_service),
) -> ClubResponse:
    """Update a club."""
    try:
        return await service.update(
            club_id=club_id,
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
    "/{club_id}",
    summary="Delete a club",
)
async def delete_club(
    club_id: UUID,
    current_user: CurrentUser,
    service: ClubService = Depends(get_club_service),
) -> dict:
    """Delete a club."""
    try:
        await service.update(
            club_id=club_id,
            data=ClubUpdateRequest(is_active=False),
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
        return {"message": "Club deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{club_id}/join",
    response_model=ClubMembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join a club",
)
async def join_club(
    club_id: UUID,
    student_id: UUID,
    current_user: CurrentUser,
    service: ClubMembershipService = Depends(get_membership_service),
) -> ClubMembershipResponse:
    """Add a student to a club."""
    try:
        data = ClubMembershipCreate(club_id=club_id, student_id=student_id)
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{club_id}/leave",
    summary="Leave a club",
)
async def leave_club(
    club_id: UUID,
    student_id: UUID,
    current_user: CurrentUser,
    service: ClubMembershipService = Depends(get_membership_service),
) -> dict:
    """Remove a student from a club."""
    membership = await service.repository.get_by_club_and_student(club_id, student_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )
    try:
        await service.remove(membership_id=membership.id)
        return {"message": "Left club successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
