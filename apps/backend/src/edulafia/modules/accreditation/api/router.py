"""Accreditation API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.accreditation.repository import AccreditationChecklistRepository
from edulafia.modules.accreditation.schemas import (
    AccreditationChecklistCreate,
    AccreditationChecklistResponse,
    AccreditationChecklistUpdate,
)
from edulafia.modules.accreditation.service import AccreditationChecklistService

router = APIRouter(prefix="/accreditation", tags=["Accreditation"])


def get_accreditation_service(db: AsyncSession = Depends(get_db)) -> AccreditationChecklistService:
    """Dependency to get AccreditationChecklistService."""
    repository = AccreditationChecklistRepository(db)
    return AccreditationChecklistService(repository)


@router.post(
    "",
    response_model=AccreditationChecklistResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an accreditation checklist",
)
async def create_accreditation_checklist(
    data: AccreditationChecklistCreate,
    current_user: CurrentUser,
    service: AccreditationChecklistService = Depends(get_accreditation_service),
) -> AccreditationChecklistResponse:
    """Create a new accreditation checklist."""
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
    "/{checklist_id}",
    response_model=AccreditationChecklistResponse,
    summary="Get an accreditation checklist by ID",
)
async def get_accreditation_checklist(
    checklist_id: UUID,
    current_user: CurrentUser,
    service: AccreditationChecklistService = Depends(get_accreditation_service),
) -> AccreditationChecklistResponse:
    """Get an accreditation checklist by ID."""
    checklist = await service.get_by_id(checklist_id=checklist_id)
    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accreditation checklist not found",
        )
    return checklist


@router.get(
    "/school/{school_id}",
    response_model=list[AccreditationChecklistResponse],
    summary="List accreditation checklists for a school",
)
async def list_school_accreditation(
    school_id: UUID,
    current_user: CurrentUser,
    service: AccreditationChecklistService = Depends(get_accreditation_service),
) -> list[AccreditationChecklistResponse]:
    """List all accreditation checklists for a school."""
    return await service.list_by_school(school_id=school_id)


@router.get(
    "/school/{school_id}/category/{category}",
    response_model=list[AccreditationChecklistResponse],
    summary="List accreditation checklists by category",
)
async def list_accreditation_by_category(
    school_id: UUID,
    category: str,
    current_user: CurrentUser,
    service: AccreditationChecklistService = Depends(get_accreditation_service),
) -> list[AccreditationChecklistResponse]:
    """List accreditation checklists for a school by category."""
    return await service.list_by_school_and_category(school_id=school_id, category=category)


@router.patch(
    "/{checklist_id}",
    response_model=AccreditationChecklistResponse,
    summary="Update an accreditation checklist",
)
async def update_accreditation_checklist(
    checklist_id: UUID,
    data: AccreditationChecklistUpdate,
    current_user: CurrentUser,
    service: AccreditationChecklistService = Depends(get_accreditation_service),
) -> AccreditationChecklistResponse:
    """Update an accreditation checklist."""
    try:
        return await service.update(
            checklist_id=checklist_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
