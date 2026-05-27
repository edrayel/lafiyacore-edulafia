"""Admissions API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.admissions.repository import ApplicationRepository
from edulafia.modules.admissions.schemas import (
    ApplicationCreate,
    ApplicationFilters,
    ApplicationListResponse,
    ApplicationResponse,
    ApplicationUpdate,
)
from edulafia.modules.admissions.service import ApplicationService

router = APIRouter(prefix="/admissions", tags=["Admissions"])


def get_application_service(db: AsyncSession = Depends(get_db)) -> ApplicationService:
    """Dependency to get ApplicationService."""
    repository = ApplicationRepository(db)
    return ApplicationService(repository)


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new application",
)
async def create_application(
    data: ApplicationCreate,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Create a new application record."""
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
    "",
    response_model=ApplicationListResponse,
    summary="List applications",
)
async def list_applications(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias="status"),
    class_applied_for: str | None = Query(None),
    admission_year: int | None = Query(None),
    gender: str | None = Query(None),
    search: str | None = Query(None),
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationListResponse:
    """List applications with optional filters and pagination."""
    filters = ApplicationFilters(
        status=status_filter,
        class_applied_for=class_applied_for,
        admission_year=admission_year,
        gender=gender,
        search=search,
    )
    return await service.list_applications(
        school_id=UUID(current_user["school_id"]),
        page=page,
        per_page=per_page,
        filters=filters,
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Get an application by ID",
)
async def get_application(
    application_id: UUID,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Get an application's details by ID."""
    application = await service.get_by_id(
        application_id=application_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application


@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Update an application",
)
async def update_application(
    application_id: UUID,
    data: ApplicationUpdate,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Update an application's information."""
    try:
        return await service.update(
            application_id=application_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{application_id}",
    summary="Delete an application",
)
async def delete_application(
    application_id: UUID,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> dict:
    """Soft delete an application."""
    try:
        await service.delete(
            application_id=application_id,
            school_id=UUID(current_user["school_id"]),
        )
        return {"message": "Application deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{application_id}/approve",
    response_model=ApplicationResponse,
    summary="Approve an application",
)
async def approve_application(
    application_id: UUID,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Approve an application."""
    try:
        return await service.approve(
            application_id=application_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{application_id}/reject",
    response_model=ApplicationResponse,
    summary="Reject an application",
)
async def reject_application(
    application_id: UUID,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Reject an application."""
    try:
        return await service.reject(
            application_id=application_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{application_id}/enroll",
    response_model=ApplicationResponse,
    summary="Enroll an application",
)
async def enroll_application(
    application_id: UUID,
    current_user: CurrentUser,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationResponse:
    """Mark an application as enrolled."""
    try:
        return await service.enroll(
            application_id=application_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
