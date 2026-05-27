"""Staff Timetable API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.staff.exceptions import (
    DraftTimetableExistsError,
    TimetableAlreadyPublishedError,
    TimetableClashError,
    TimetableNotFoundError,
)
from edulafia.modules.staff.repository import (
    TimetableEntryRepository,
    TimetableRepository,
)
from edulafia.modules.staff.schemas import (
    ClashInfo,
    TimetableCreate,
    TimetableEntryCreate,
    TimetableEntryEnriched,
    TimetableEntryResponse,
    TimetableResponse,
)
from edulafia.modules.staff.timetable import TimetableService

router = APIRouter(prefix="/staff/timetables", tags=["Staff Timetables"])


def get_timetable_service(db: AsyncSession = Depends(get_db)) -> TimetableService:
    """Dependency to get TimetableService."""
    timetable_repo = TimetableRepository(db)
    entry_repo = TimetableEntryRepository(db)
    return TimetableService(timetable_repo, entry_repo)


@router.post(
    "",
    response_model=TimetableResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create timetable",
)
async def create_timetable(
    data: TimetableCreate,
    current_user: CurrentUser,
    service: TimetableService = Depends(get_timetable_service),
) -> TimetableResponse:
    """Create a new timetable."""
    try:
        return await service.create_timetable(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DraftTimetableExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/{timetable_id}",
    response_model=TimetableResponse,
    summary="Get timetable",
)
async def get_timetable(
    timetable_id: UUID,
    current_user: CurrentUser,
    service: TimetableService = Depends(get_timetable_service),
) -> TimetableResponse:
    """Get timetable by ID."""
    try:
        return await service.get_timetable(timetable_id)
    except TimetableNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")


@router.get(
    "/{timetable_id}/entries",
    summary="Get timetable entries",
)
async def get_timetable_entries(
    timetable_id: UUID,
    current_user: CurrentUser,
    include_names: bool = Query(False),
    service: TimetableService = Depends(get_timetable_service),
) -> list[TimetableEntryResponse | dict]:
    """Get all entries for a timetable.
    When include_names=true, resolves staff and subject IDs to display names."""
    try:
        if include_names:
            return await service.get_entries_with_names(timetable_id)
        return await service.get_entries(timetable_id)
    except TimetableNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")


@router.post(
    "/{timetable_id}/entries",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Add timetable entry",
)
async def add_timetable_entry(
    timetable_id: UUID,
    data: TimetableEntryCreate,
    current_user: CurrentUser,
    service: TimetableService = Depends(get_timetable_service),
) -> dict:
    """Add entry to timetable with clash detection."""
    try:
        entry, clashes = await service.add_entry(timetable_id, data)
        return {
            "entry": TimetableEntryResponse.model_validate(entry).model_dump(),
            "clashes": [ClashInfo.model_validate(c).model_dump() for c in clashes],
            "has_clashes": len(clashes) > 0,
        }
    except TimetableNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")
    except TimetableAlreadyPublishedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(
    "/{timetable_id}/validate",
    response_model=list[ClashInfo],
    summary="Validate timetable",
)
async def validate_timetable(
    timetable_id: UUID,
    current_user: CurrentUser,
    service: TimetableService = Depends(get_timetable_service),
) -> list[ClashInfo]:
    """Validate timetable for clashes."""
    try:
        return await service.validate_timetable(timetable_id)
    except TimetableNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")


@router.post(
    "/{timetable_id}/publish",
    response_model=TimetableResponse,
    summary="Publish timetable",
)
async def publish_timetable(
    timetable_id: UUID,
    current_user: CurrentUser,
    service: TimetableService = Depends(get_timetable_service),
) -> TimetableResponse:
    """Publish a timetable after validation."""
    try:
        return await service.publish_timetable(
            timetable_id=timetable_id,
            user_id=UUID(current_user["sub"]),
        )
    except TimetableNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")
    except TimetableClashError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/teacher/{staff_id}",
    response_model=list[TimetableEntryResponse],
    summary="Get teacher timetable",
)
async def get_teacher_timetable(
    staff_id: UUID,
    current_user: CurrentUser,
    class_id: UUID | None = Query(None),
    academic_year_id: UUID | None = Query(None),
    term_id: UUID | None = Query(None),
    service: TimetableService = Depends(get_timetable_service),
) -> list[TimetableEntryResponse]:
    """Get timetable entries for a specific teacher."""
    return await service.get_teacher_timetable(
        staff_id=staff_id,
        class_id=class_id,
        academic_year_id=academic_year_id,
        term_id=term_id,
    )
