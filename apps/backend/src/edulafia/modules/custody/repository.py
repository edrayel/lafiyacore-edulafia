from __future__ import annotations
"""Custody repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.custody.models import CustodyOrder


class CustodyOrderRepository:
    """Repository for custody order database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> CustodyOrder:
        """Create a new custody order."""
        order = CustodyOrder(**data)
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def get_by_id(self, order_id: UUID) -> CustodyOrder | None:
        """Get a custody order by ID."""
        stmt = select(CustodyOrder).where(CustodyOrder.id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_id(self, student_id: UUID) -> Sequence[CustodyOrder]:
        """Get all custody orders for a student."""
        stmt = select(CustodyOrder).where(
            CustodyOrder.student_id == student_id
        ).order_by(CustodyOrder.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_active_by_student_id(self, student_id: UUID) -> CustodyOrder | None:
        """Get the active custody order for a student."""
        stmt = select(CustodyOrder).where(
            CustodyOrder.student_id == student_id,
            CustodyOrder.status == "active",
        ).order_by(CustodyOrder.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, order: CustodyOrder, data: dict) -> CustodyOrder:
        """Update a custody order."""
        for key, value in data.items():
            if value is not None:
                setattr(order, key, value)
        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def delete(self, order: CustodyOrder) -> None:
        """Delete a custody order."""
        await self.db.delete(order)
        await self.db.flush()
