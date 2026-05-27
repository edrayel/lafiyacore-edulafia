"""Payroll API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.payroll.repository import PayrollRunRepository
from edulafia.modules.payroll.schemas import (
    PayrollRunCreate,
    PayrollRunResponse,
    PayrollRunUpdate,
)
from edulafia.modules.payroll.service import PayrollRunService

router = APIRouter(prefix="/payroll", tags=["Payroll"])


def get_payroll_service(db: AsyncSession = Depends(get_db)) -> PayrollRunService:
    """Dependency to get PayrollRunService."""
    repository = PayrollRunRepository(db)
    return PayrollRunService(repository)


@router.post(
    "",
    response_model=PayrollRunResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a payroll run",
)
async def create_payroll_run(
    data: PayrollRunCreate,
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> PayrollRunResponse:
    """Create a new payroll run."""
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
    "/{run_id}",
    response_model=PayrollRunResponse,
    summary="Get a payroll run by ID",
)
async def get_payroll_run(
    run_id: UUID,
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> PayrollRunResponse:
    """Get a payroll run by ID."""
    run = await service.get_by_id(
        run_id=run_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll run not found",
        )
    return run


@router.get(
    "",
    response_model=list[PayrollRunResponse],
    summary="List payroll runs",
)
async def list_payroll_runs(
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> list[PayrollRunResponse]:
    """List all payroll runs for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{run_id}",
    response_model=PayrollRunResponse,
    summary="Update a payroll run",
)
async def update_payroll_run(
    run_id: UUID,
    data: PayrollRunUpdate,
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> PayrollRunResponse:
    """Update a payroll run."""
    try:
        return await service.update(
            run_id=run_id,
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
    "/{run_id}/approve",
    response_model=PayrollRunResponse,
    summary="Approve a payroll run",
)
async def approve_payroll_run(
    run_id: UUID,
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> PayrollRunResponse:
    """Approve a payroll run."""
    try:
        return await service.approve(
            run_id=run_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{run_id}/mark-paid",
    response_model=PayrollRunResponse,
    summary="Mark payroll run as paid",
)
async def mark_payroll_paid(
    run_id: UUID,
    current_user: CurrentUser,
    service: PayrollRunService = Depends(get_payroll_service),
) -> PayrollRunResponse:
    """Mark a payroll run as paid."""
    try:
        return await service.mark_paid(
            run_id=run_id,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
