"""Proprietor API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser, require_role
from edulafia.modules.proprietor.repository import ProprietorRepository
from edulafia.modules.proprietor.schemas import (
    ProprietorAcademicSummary,
    ProprietorDashboardSummary,
    ProprietorEnrollmentSummary,
    ProprietorFinancialSummary,
    ProprietorOperationalSummary,
)
from edulafia.modules.proprietor.service import ProprietorService

router = APIRouter(
    prefix="/proprietor/dashboard",
    tags=["Proprietor"],
    dependencies=[require_role("owner")],
)


def get_proprietor_service(db: AsyncSession = Depends(get_db)) -> ProprietorService:
    """Dependency to get ProprietorService."""
    repository = ProprietorRepository(db)
    return ProprietorService(repository)


@router.get(
    "/summary",
    response_model=ProprietorDashboardSummary,
    summary="Get dashboard summary",
)
async def get_dashboard_summary(
    current_user: CurrentUser,
    service: ProprietorService = Depends(get_proprietor_service),
) -> ProprietorDashboardSummary:
    """Get the full dashboard summary for the school."""
    return await service.get_dashboard_summary(school_id=UUID(current_user["school_id"]))


@router.get(
    "/financial",
    response_model=ProprietorFinancialSummary,
    summary="Get financial summary",
)
async def get_financial_summary(
    current_user: CurrentUser,
    service: ProprietorService = Depends(get_proprietor_service),
) -> ProprietorFinancialSummary:
    """Get financial summary for the school."""
    return await service.get_financial_summary(school_id=UUID(current_user["school_id"]))


@router.get(
    "/enrollment",
    response_model=ProprietorEnrollmentSummary,
    summary="Get enrollment summary",
)
async def get_enrollment_summary(
    current_user: CurrentUser,
    service: ProprietorService = Depends(get_proprietor_service),
) -> ProprietorEnrollmentSummary:
    """Get enrollment summary for the school."""
    return await service.get_enrollment_summary(school_id=UUID(current_user["school_id"]))


@router.get(
    "/academic",
    response_model=ProprietorAcademicSummary,
    summary="Get academic summary",
)
async def get_academic_summary(
    current_user: CurrentUser,
    service: ProprietorService = Depends(get_proprietor_service),
) -> ProprietorAcademicSummary:
    """Get academic summary for the school."""
    return await service.get_academic_summary(school_id=UUID(current_user["school_id"]))


@router.get(
    "/operational",
    response_model=ProprietorOperationalSummary,
    summary="Get operational summary",
)
async def get_operational_summary(
    current_user: CurrentUser,
    service: ProprietorService = Depends(get_proprietor_service),
) -> ProprietorOperationalSummary:
    """Get operational summary for the school."""
    return await service.get_operational_summary(school_id=UUID(current_user["school_id"]))
