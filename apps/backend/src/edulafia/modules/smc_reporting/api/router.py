"""SMC reporting API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.smc_reporting.repository import SMCReportRepository
from edulafia.modules.smc_reporting.schemas import (
    SMCReportCreate,
    SMCReportResponse,
    SMCReportUpdate,
)
from edulafia.modules.smc_reporting.service import SMCReportService

router = APIRouter(prefix="/smc-reports", tags=["SMC Reporting"])


def get_smc_report_service(db: AsyncSession = Depends(get_db)) -> SMCReportService:
    """Dependency to get SMCReportService."""
    repository = SMCReportRepository(db)
    return SMCReportService(repository)


@router.post(
    "",
    response_model=SMCReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an SMC report",
)
async def create_smc_report(
    data: SMCReportCreate,
    current_user: CurrentUser,
    service: SMCReportService = Depends(get_smc_report_service),
) -> SMCReportResponse:
    """Create a new SMC report."""
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
    response_model=SMCReportResponse,
    summary="Get an SMC report by ID",
)
async def get_smc_report(
    report_id: UUID,
    current_user: CurrentUser,
    service: SMCReportService = Depends(get_smc_report_service),
) -> SMCReportResponse:
    """Get an SMC report by ID."""
    report = await service.get_by_id(report_id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SMC report not found",
        )
    return report


@router.get(
    "",
    response_model=list[SMCReportResponse],
    summary="List SMC reports",
)
async def list_smc_reports(
    current_user: CurrentUser,
    service: SMCReportService = Depends(get_smc_report_service),
) -> list[SMCReportResponse]:
    """List all SMC reports for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{report_id}",
    response_model=SMCReportResponse,
    summary="Update an SMC report",
)
async def update_smc_report(
    report_id: UUID,
    data: SMCReportUpdate,
    current_user: CurrentUser,
    service: SMCReportService = Depends(get_smc_report_service),
) -> SMCReportResponse:
    """Update an SMC report."""
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


@router.delete(
    "/{report_id}",
    summary="Delete an SMC report",
)
async def delete_smc_report(
    report_id: UUID,
    current_user: CurrentUser,
    service: SMCReportService = Depends(get_smc_report_service),
) -> dict:
    """Delete an SMC report."""
    report = await service.get_by_id(report_id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SMC report not found",
        )
    await service.delete(report_id)
    return {"message": "SMC report deleted"}
