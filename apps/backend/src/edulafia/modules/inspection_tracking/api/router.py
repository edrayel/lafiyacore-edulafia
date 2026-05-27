"""Inspection tracking API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.inspection_tracking.repository import SchoolInspectionRepository
from edulafia.modules.inspection_tracking.schemas import (
    SchoolInspectionCreate,
    SchoolInspectionResponse,
    SchoolInspectionUpdate,
)
from edulafia.modules.inspection_tracking.service import SchoolInspectionService

router = APIRouter(prefix="/inspections", tags=["Inspections"])


def get_inspection_service(db: AsyncSession = Depends(get_db)) -> SchoolInspectionService:
    """Dependency to get SchoolInspectionService."""
    repository = SchoolInspectionRepository(db)
    return SchoolInspectionService(repository)


@router.post(
    "",
    response_model=SchoolInspectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a school inspection",
)
async def create_inspection(
    data: SchoolInspectionCreate,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> SchoolInspectionResponse:
    """Create a new school inspection."""
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
    "/{inspection_id}",
    response_model=SchoolInspectionResponse,
    summary="Get a school inspection by ID",
)
async def get_inspection(
    inspection_id: UUID,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> SchoolInspectionResponse:
    """Get a school inspection by ID."""
    inspection = await service.get_by_id(inspection_id=inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School inspection not found",
        )
    return inspection


@router.get(
    "/school/{school_id}",
    response_model=list[SchoolInspectionResponse],
    summary="List inspections for a school",
)
async def list_school_inspections(
    school_id: UUID,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> list[SchoolInspectionResponse]:
    """List all inspections for a school."""
    return await service.list_by_school(school_id=school_id)


@router.get(
    "/status/{status}",
    response_model=list[SchoolInspectionResponse],
    summary="List inspections by status",
)
async def list_inspections_by_status(
    status: str,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> list[SchoolInspectionResponse]:
    """List inspections by status."""
    return await service.list_by_status(status=status)


@router.patch(
    "/{inspection_id}",
    response_model=SchoolInspectionResponse,
    summary="Update a school inspection",
)
async def update_inspection(
    inspection_id: UUID,
    data: SchoolInspectionUpdate,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> SchoolInspectionResponse:
    """Update a school inspection."""
    try:
        return await service.update(
            inspection_id=inspection_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{inspection_id}/resolve",
    response_model=SchoolInspectionResponse,
    summary="Resolve a school inspection",
)
async def resolve_inspection(
    inspection_id: UUID,
    current_user: CurrentUser,
    service: SchoolInspectionService = Depends(get_inspection_service),
) -> SchoolInspectionResponse:
    """Resolve a school inspection."""
    try:
        return await service.resolve(inspection_id=inspection_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
