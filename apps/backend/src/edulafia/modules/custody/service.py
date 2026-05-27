"""Custody service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.custody.repository import CustodyOrderRepository
from edulafia.modules.custody.schemas import (
    CustodyOrderCreate,
    CustodyOrderResponse,
    CustodyOrderUpdate,
)


class CustodyOrderService:
    """Service for custody order business logic."""

    def __init__(self, repository: CustodyOrderRepository):
        self.repository = repository

    async def create(
        self,
        data: CustodyOrderCreate,
        user_id: UUID,
    ) -> CustodyOrderResponse:
        """Create a new custody order."""
        order_data = data.model_dump()
        order = await self.repository.create(order_data)
        return CustodyOrderResponse.model_validate(order)

    async def get_by_id(self, order_id: UUID) -> CustodyOrderResponse | None:
        """Get a custody order by ID."""
        order = await self.repository.get_by_id(order_id)
        if order:
            return CustodyOrderResponse.model_validate(order)
        return None

    async def get_by_student_id(self, student_id: UUID) -> Sequence[CustodyOrderResponse]:
        """Get all custody orders for a student."""
        orders = await self.repository.get_by_student_id(student_id)
        return [CustodyOrderResponse.model_validate(o) for o in orders]

    async def get_active_by_student_id(self, student_id: UUID) -> CustodyOrderResponse | None:
        """Get the active custody order for a student."""
        order = await self.repository.get_active_by_student_id(student_id)
        if order:
            return CustodyOrderResponse.model_validate(order)
        return None

    async def update(
        self,
        order_id: UUID,
        data: CustodyOrderUpdate,
        user_id: UUID,
    ) -> CustodyOrderResponse:
        """Update a custody order."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Custody order {order_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_order = await self.repository.update(order, update_data)
        return CustodyOrderResponse.model_validate(updated_order)

    async def revoke(self, order_id: UUID, user_id: UUID) -> CustodyOrderResponse:
        """Revoke a custody order."""
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Custody order {order_id} not found")

        update_data = {"status": "revoked"}
        updated_order = await self.repository.update(order, update_data)
        return CustodyOrderResponse.model_validate(updated_order)
