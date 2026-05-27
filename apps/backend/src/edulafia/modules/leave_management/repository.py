from __future__ import annotations
"""Leave management repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.leave_management.models import LeaveRequest


class LeaveRequestRepository:
    """Repository for leave request database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> LeaveRequest:
        """Create a new leave request."""
        request = LeaveRequest(**data)
        self.db.add(request)
        await self.db.flush()
        await self.db.refresh(request)
        return request

    async def get_by_id(self, request_id: UUID) -> LeaveRequest | None:
        """Get a leave request by ID."""
        stmt = select(LeaveRequest).where(LeaveRequest.id == request_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_staff(self, staff_id: UUID) -> Sequence[LeaveRequest]:
        """List all leave requests for a staff member."""
        stmt = select(LeaveRequest).where(
            LeaveRequest.staff_id == staff_id
        ).order_by(LeaveRequest.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_pending_by_staff(self, staff_id: UUID) -> Sequence[LeaveRequest]:
        """List pending leave requests for a staff member."""
        stmt = select(LeaveRequest).where(
            LeaveRequest.staff_id == staff_id,
            LeaveRequest.status == "pending",
        ).order_by(LeaveRequest.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, request: LeaveRequest, data: dict) -> LeaveRequest:
        """Update a leave request."""
        for key, value in data.items():
            if value is not None:
                setattr(request, key, value)
        await self.db.flush()
        await self.db.refresh(request)
        return request

    async def delete(self, request: LeaveRequest) -> None:
        """Delete a leave request."""
        await self.db.delete(request)
        await self.db.flush()
