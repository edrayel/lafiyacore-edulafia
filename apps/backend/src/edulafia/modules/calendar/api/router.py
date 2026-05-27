"""Calendar API endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.calendar.repository import EventRepository
from edulafia.modules.calendar.schemas import EventCreate, EventResponse, EventUpdate
from edulafia.modules.calendar.service import EventNotFoundError, EventService

router = APIRouter(prefix="/calendar/events", tags=["Calendar"])


def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    """Dependency to get EventService."""
    repository = EventRepository(db)
    return EventService(repository)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
)
async def create_event(
    data: EventCreate,
    current_user: CurrentUser,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    """Create a new event."""
    return await service.create(
        data=data,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
    )


@router.get(
    "",
    response_model=dict,
    summary="List events",
)
async def list_events(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    service: EventService = Depends(get_event_service),
) -> dict:
    """List events with pagination, optionally filtered by date range."""
    return await service.list_events(
        school_id=UUID(current_user["school_id"]),
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get an event by ID",
)
async def get_event(
    event_id: UUID,
    current_user: CurrentUser,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    """Get an event's details by ID."""
    event = await service.get_by_id(
        event_id=event_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update an event",
)
async def update_event(
    event_id: UUID,
    data: EventUpdate,
    current_user: CurrentUser,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    """Update an event's information."""
    try:
        return await service.update(
            event_id=event_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except EventNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )


@router.delete(
    "/{event_id}",
    response_model=EventResponse,
    summary="Archive an event",
)
async def archive_event(
    event_id: UUID,
    current_user: CurrentUser,
    service: EventService = Depends(get_event_service),
) -> EventResponse:
    """Archive an event (soft delete)."""
    try:
        return await service.archive(
            event_id=event_id,
            school_id=UUID(current_user["school_id"]),
        )
    except EventNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
