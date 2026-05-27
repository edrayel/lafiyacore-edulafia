"""Ministry reporting API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.ministry_reporting.repository import MinistryReportRepository
from edulafia.modules.ministry_reporting.schemas import (
    MinistryReportCreate,
    MinistryReportResponse,
    MinistryReportUpdate,
)
from edulafia.modules.ministry_reporting.service import MinistryReportService

router = APIRouter(prefix="/ministry-reports", tags=["Ministry Reporting"])


def get_ministry_report_service(db: AsyncSession = Depends(get_db)) -> MinistryReportService:
    """Dependency to get MinistryReportService."""
    repository = MinistryReportRepository(db)
    return MinistryReportService(repository)


@router.post(
    "",
    response_model=MinistryReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a ministry report",
)
async def create_ministry_report(
    data: MinistryReportCreate,
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> MinistryReportResponse:
    """Create a new ministry report."""
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
    "/{report_id}",
    response_model=MinistryReportResponse,
    summary="Get a ministry report by ID",
)
async def get_ministry_report(
    report_id: UUID,
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> MinistryReportResponse:
    """Get a ministry report by ID."""
    report = await service.get_by_id(report_id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry report not found",
        )
    return report


@router.get(
    "",
    response_model=list[MinistryReportResponse],
    summary="List ministry reports",
)
async def list_ministry_reports(
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> list[MinistryReportResponse]:
    """List all ministry reports for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.get(
    "/type/{report_type}",
    response_model=list[MinistryReportResponse],
    summary="List ministry reports by type",
)
async def list_ministry_reports_by_type(
    report_type: str,
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> list[MinistryReportResponse]:
    """List ministry reports by type."""
    return await service.list_by_type(
        school_id=UUID(current_user["school_id"]),
        report_type=report_type,
    )


@router.patch(
    "/{report_id}",
    response_model=MinistryReportResponse,
    summary="Update a ministry report",
)
async def update_ministry_report(
    report_id: UUID,
    data: MinistryReportUpdate,
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> MinistryReportResponse:
    """Update a ministry report."""
    try:
        return await service.update(
            report_id=report_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{report_id}/submit",
    response_model=MinistryReportResponse,
    summary="Submit a ministry report",
)
async def submit_ministry_report(
    report_id: UUID,
    current_user: CurrentUser,
    service: MinistryReportService = Depends(get_ministry_report_service),
) -> MinistryReportResponse:
    """Submit a ministry report."""
    try:
        return await service.submit(report_id=report_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
