"""WAEC bulk API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.waec_bulk.repository import WAECBulkRegistrationRepository
from edulafia.modules.waec_bulk.schemas import (
    WAECBulkRegistrationCreate,
    WAECBulkRegistrationResponse,
    WAECBulkRegistrationUpdate,
)
from edulafia.modules.waec_bulk.service import WAECBulkRegistrationService

router = APIRouter(prefix="/waec-bulk", tags=["WAEC Bulk"])


def get_waec_bulk_service(db: AsyncSession = Depends(get_db)) -> WAECBulkRegistrationService:
    """Dependency to get WAECBulkRegistrationService."""
    repository = WAECBulkRegistrationRepository(db)
    return WAECBulkRegistrationService(repository)


@router.post(
    "",
    response_model=WAECBulkRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a WAEC bulk registration",
)
async def create_waec_bulk_registration(
    data: WAECBulkRegistrationCreate,
    current_user: CurrentUser,
    service: WAECBulkRegistrationService = Depends(get_waec_bulk_service),
) -> WAECBulkRegistrationResponse:
    """Create a new WAEC bulk registration."""
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
    response_model=WAECBulkRegistrationResponse,
    summary="Get a WAEC bulk registration by ID",
)
async def get_waec_bulk_registration(
    registration_id: UUID,
    current_user: CurrentUser,
    service: WAECBulkRegistrationService = Depends(get_waec_bulk_service),
) -> WAECBulkRegistrationResponse:
    """Get a WAEC bulk registration by ID."""
    registration = await service.get_by_id(
        registration_id=registration_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WAEC bulk registration not found",
        )
    return registration


@router.get(
    "",
    response_model=list[WAECBulkRegistrationResponse],
    summary="List WAEC bulk registrations",
)
async def list_waec_bulk_registrations(
    current_user: CurrentUser,
    exam_year: int = Query(None),
    service: WAECBulkRegistrationService = Depends(get_waec_bulk_service),
) -> list[WAECBulkRegistrationResponse]:
    """List all WAEC bulk registrations for the school."""
    if exam_year:
        return await service.list_by_school_and_year(
            school_id=UUID(current_user["school_id"]),
            exam_year=exam_year,
        )
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{registration_id}",
    response_model=WAECBulkRegistrationResponse,
    summary="Update a WAEC bulk registration",
)
async def update_waec_bulk_registration(
    registration_id: UUID,
    data: WAECBulkRegistrationUpdate,
    current_user: CurrentUser,
    service: WAECBulkRegistrationService = Depends(get_waec_bulk_service),
) -> WAECBulkRegistrationResponse:
    """Update a WAEC bulk registration."""
    try:
        return await service.update(
            registration_id=registration_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{registration_id}/submit",
    response_model=WAECBulkRegistrationResponse,
    summary="Submit a WAEC bulk registration",
)
async def submit_waec_bulk_registration(
    registration_id: UUID,
    current_user: CurrentUser,
    service: WAECBulkRegistrationService = Depends(get_waec_bulk_service),
) -> WAECBulkRegistrationResponse:
    """Submit a WAEC bulk registration."""
    try:
        return await service.submit(
            registration_id=registration_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
