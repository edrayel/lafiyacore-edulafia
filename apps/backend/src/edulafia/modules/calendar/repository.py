from __future__ import annotations
"""Repository for calendar data access operations."""

from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.calendar.models import Event


class EventRepository:
    """Repository for event database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Event:
        """Create a new event."""
        event = Event(**data)
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def get_by_id(self, event_id: UUID, school_id: UUID) -> Event | None:
        """Get an event by ID, scoped to school."""
        stmt = select(Event).where(
            Event.id == event_id,
            Event.school_id == school_id,
            Event.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 50,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> tuple[Sequence[Event], int]:
        """List events with pagination, optionally filtered by date range."""
        stmt = select(Event).where(
            Event.school_id == school_id,
            Event.deleted_at.is_(None),
        )

        if start_date:
            stmt = stmt.where(Event.start_date >= start_date)
        if end_date:
            stmt = stmt.where(Event.start_date <= end_date)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.order_by(Event.start_date.asc())
        stmt = stmt.offset(offset).limit(per_page)

        result = await self.db.execute(stmt)
        events = result.scalars().all()

        return events, total

    async def update(self, event: Event, data: dict) -> Event:
        """Update an event."""
        for key, value in data.items():
            if value is not None:
                setattr(event, key, value)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def soft_delete(self, event: Event) -> Event:
        """Soft delete an event."""
        event.deleted_at = func.now()
        await self.db.flush()
        await self.db.refresh(event)
        return event
