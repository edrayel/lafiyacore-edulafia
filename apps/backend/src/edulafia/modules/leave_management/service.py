"""Leave management service for business logic operations."""

from collections.abc import Sequence
from datetime import timezone, UTC, datetime
from uuid import UUID

from edulafia.modules.leave_management.repository import LeaveRequestRepository
from edulafia.modules.leave_management.schemas import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestUpdate,
)


class LeaveRequestService:
    """Service for leave request business logic."""

    def __init__(self, repository: LeaveRequestRepository):
        self.repository = repository

    async def create(self, data: LeaveRequestCreate, user_id: UUID) -> LeaveRequestResponse:
        """Create a new leave request."""
        request_data = data.model_dump()
        request = await self.repository.create(request_data)
        return LeaveRequestResponse.model_validate(request)

    async def get_by_id(self, request_id: UUID) -> LeaveRequestResponse | None:
        """Get a leave request by ID."""
        request = await self.repository.get_by_id(request_id)
        if request:
            return LeaveRequestResponse.model_validate(request)
        return None

    async def list_by_staff(self, staff_id: UUID) -> Sequence[LeaveRequestResponse]:
        """List all leave requests for a staff member."""
        requests = await self.repository.list_by_staff(staff_id)
        return [LeaveRequestResponse.model_validate(r) for r in requests]

    async def update(self, request_id: UUID, data: LeaveRequestUpdate, user_id: UUID) -> LeaveRequestResponse:
        """Update a leave request."""
        request = await self.repository.get_by_id(request_id)
        if not request:
            raise ValueError(f"Leave request {request_id} not found")
        if request.status != "pending":
            raise ValueError("Only pending leave requests can be updated")

        update_data = data.model_dump(exclude_none=True)
        updated_request = await self.repository.update(request, update_data)
        return LeaveRequestResponse.model_validate(updated_request)

    async def approve(self, request_id: UUID, approver_id: UUID) -> LeaveRequestResponse:
        """Approve a leave request."""
        request = await self.repository.get_by_id(request_id)
        if not request:
            raise ValueError(f"Leave request {request_id} not found")
        if request.status != "pending":
            raise ValueError("Only pending leave requests can be approved")

        update_data = {
            "status": "approved",
            "approved_by": approver_id,
            "approved_at": datetime.now(UTC),
        }
        updated_request = await self.repository.update(request, update_data)
        return LeaveRequestResponse.model_validate(updated_request)

    async def reject(self, request_id: UUID, approver_id: UUID) -> LeaveRequestResponse:
        """Reject a leave request."""
        request = await self.repository.get_by_id(request_id)
        if not request:
            raise ValueError(f"Leave request {request_id} not found")
        if request.status != "pending":
            raise ValueError("Only pending leave requests can be rejected")

        update_data = {
            "status": "rejected",
            "approved_by": approver_id,
            "approved_at": datetime.now(UTC),
        }
        updated_request = await self.repository.update(request, update_data)
        return LeaveRequestResponse.model_validate(updated_request)
