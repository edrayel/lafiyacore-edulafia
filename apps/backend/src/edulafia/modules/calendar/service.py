"""Service layer for calendar business logic."""

from datetime import datetime
from uuid import UUID

from edulafia.modules.calendar.repository import EventRepository
from edulafia.modules.calendar.schemas import EventCreate, EventUpdate, EventResponse


class EventNotFoundError(Exception):
    """Exception raised when an event is not found."""
    pass


class EventService:
    """Service for managing events."""

    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def create(self, data: EventCreate, school_id: UUID, user_id: UUID) -> EventResponse:
        """Create a new event."""
        create_data = data.model_dump()
        create_data.update({
            "school_id": school_id,
            "created_by": user_id,
        })
        
        event = await self.repository.create(create_data)
        return EventResponse.model_validate(event)

    async def get_by_id(self, event_id: UUID, school_id: UUID) -> EventResponse | None:
        """Get an event by ID."""
        event = await self.repository.get_by_id(event_id, school_id)
        if not event:
            return None
        return EventResponse.model_validate(event)

    async def list_events(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 50,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict:
        """List events with pagination, optionally filtered by date range."""
        events, total = await self.repository.list(
            school_id=school_id,
            page=page,
            per_page=per_page,
            start_date=start_date,
            end_date=end_date,
        )

        return {
            "items": [EventResponse.model_validate(e) for e in events],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def update(
        self,
        event_id: UUID,
        data: EventUpdate,
        school_id: UUID,
        user_id: UUID,
    ) -> EventResponse:
        """Update an event."""
        event = await self.repository.get_by_id(event_id, school_id)
        if not event:
            raise EventNotFoundError(f"Event {event_id} not found")

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return EventResponse.model_validate(event)

        update_data["updated_by"] = user_id
        
        updated_event = await self.repository.update(event, update_data)
        return EventResponse.model_validate(updated_event)

    async def archive(self, event_id: UUID, school_id: UUID) -> EventResponse:
        """Archive (soft delete) an event."""
        event = await self.repository.get_by_id(event_id, school_id)
        if not event:
            raise EventNotFoundError(f"Event {event_id} not found")

        archived_event = await self.repository.soft_delete(event)
        return EventResponse.model_validate(archived_event)
