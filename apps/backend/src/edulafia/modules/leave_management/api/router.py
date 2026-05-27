"""Leave management API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.leave_management.repository import LeaveRequestRepository
from edulafia.modules.leave_management.schemas import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestUpdate,
)
from edulafia.modules.leave_management.service import LeaveRequestService

router = APIRouter(prefix="/leave", tags=["Leave Management"])


def get_leave_service(db: AsyncSession = Depends(get_db)) -> LeaveRequestService:
    """Dependency to get LeaveRequestService."""
    repository = LeaveRequestRepository(db)
    return LeaveRequestService(repository)


@router.post(
    "",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a leave request",
)
async def create_leave_request(
    data: LeaveRequestCreate,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> LeaveRequestResponse:
    """Create a new leave request."""
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
    "/{request_id}",
    response_model=LeaveRequestResponse,
    summary="Get a leave request by ID",
)
async def get_leave_request(
    request_id: UUID,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> LeaveRequestResponse:
    """Get a leave request by ID."""
    request = await service.get_by_id(request_id=request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )
    return request


@router.get(
    "/staff/{staff_id}",
    response_model=list[LeaveRequestResponse],
    summary="List leave requests for a staff member",
)
async def list_staff_leave_requests(
    staff_id: UUID,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> list[LeaveRequestResponse]:
    """List all leave requests for a staff member."""
    return await service.list_by_staff(staff_id=staff_id)


@router.patch(
    "/{request_id}",
    response_model=LeaveRequestResponse,
    summary="Update a leave request",
)
async def update_leave_request(
    request_id: UUID,
    data: LeaveRequestUpdate,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> LeaveRequestResponse:
    """Update a leave request."""
    try:
        return await service.update(
            request_id=request_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{request_id}/approve",
    response_model=LeaveRequestResponse,
    summary="Approve a leave request",
)
async def approve_leave_request(
    request_id: UUID,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> LeaveRequestResponse:
    """Approve a leave request."""
    try:
        return await service.approve(
            request_id=request_id,
            approver_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{request_id}/reject",
    response_model=LeaveRequestResponse,
    summary="Reject a leave request",
)
async def reject_leave_request(
    request_id: UUID,
    current_user: CurrentUser,
    service: LeaveRequestService = Depends(get_leave_service),
) -> LeaveRequestResponse:
    """Reject a leave request."""
    try:
        return await service.reject(
            request_id=request_id,
            approver_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
