"""Timetable service for timetable management with clash detection."""

from uuid import UUID

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
    TimetableEntryResponse,
    TimetableResponse,
)


class TimetableService:
    """Service for timetable management with clash detection."""

    def __init__(
        self,
        timetable_repo: TimetableRepository,
        entry_repo: TimetableEntryRepository,
    ):
        self.timetable_repo = timetable_repo
        self.entry_repo = entry_repo

    async def create_timetable(
        self,
        data: TimetableCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> TimetableResponse:
        """Create a new timetable."""
        # Check if draft already exists
        existing_draft = await self.timetable_repo.get_draft(
            data.class_id, data.academic_year_id, data.term_id
        )
        if existing_draft:
            raise DraftTimetableExistsError(
                str(data.class_id), str(data.term_id)
            )

        timetable_data = {
            "school_id": school_id,
            "class_id": data.class_id,
            "academic_year_id": data.academic_year_id,
            "term_id": data.term_id,
            "effective_from": data.effective_from,
        }

        timetable = await self.timetable_repo.create(timetable_data)
        return TimetableResponse.model_validate(timetable)

    async def get_timetable(self, timetable_id: UUID) -> TimetableResponse:
        """Get timetable by ID."""
        timetable = await self.timetable_repo.get_by_id(timetable_id)
        if not timetable:
            raise TimetableNotFoundError(str(timetable_id))
        return TimetableResponse.model_validate(timetable)

    async def add_entry(
        self,
        timetable_id: UUID,
        data: TimetableEntryCreate,
    ) -> tuple[TimetableEntryResponse, list[ClashInfo]]:
        """Add entry to timetable with clash detection."""
        # Get timetable
        timetable = await self.timetable_repo.get_by_id(timetable_id)
        if not timetable:
            raise TimetableNotFoundError(str(timetable_id))

        # Check if published
        if timetable.is_published:
            raise TimetableAlreadyPublishedError(str(timetable_id))

        # Detect clashes
        clashes = await self.detect_clashes(timetable_id, data)

        # Create entry (even with clashes, for draft purposes)
        entry_data = {
            "timetable_id": timetable_id,
            "day_of_week": data.day_of_week,
            "period_number": data.period_number,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "subject_id": data.subject_id,
            "staff_id": data.staff_id,
            "room_number": data.room_number,
            "notes": data.notes,
            "is_break": data.is_break,
        }

        entry = await self.entry_repo.create(entry_data)

        return TimetableEntryResponse.model_validate(entry), clashes

    async def detect_clashes(
        self,
        timetable_id: UUID,
        data: TimetableEntryCreate,
    ) -> list[ClashInfo]:
        """Detect clashes for a timetable entry."""
        clashes = []

        # Get existing entries for this day
        existing_entries = await self.entry_repo.get_teacher_entries_on_day(
            timetable_id, data.staff_id, data.day_of_week
        )

        # Check teacher clash (same teacher, overlapping time)
        for entry in existing_entries:
            if entry.period_number == data.period_number:
                clashes.append(ClashInfo(
                    clash_type="teacher_clash",
                    day_of_week=data.day_of_week,
                    period_number=data.period_number,
                    existing_entry_id=entry.id,
                    message=f"Teacher already assigned to period {data.period_number} on day {data.day_of_week}",
                ))

        # Check if period is a break period
        existing_period = await self.entry_repo.get_class_entries_on_period(
            timetable_id, data.day_of_week, data.period_number
        )
        if existing_period and existing_period.is_break:
            clashes.append(ClashInfo(
                clash_type="break_period",
                day_of_week=data.day_of_week,
                period_number=data.period_number,
                existing_entry_id=existing_period.id,
                message=f"Period {data.period_number} is a break period",
            ))

        return clashes

    async def validate_timetable(self, timetable_id: UUID) -> list[ClashInfo]:
        """Validate entire timetable for clashes."""
        entries = await self.entry_repo.list_by_timetable(timetable_id)
        clashes = []

        # Track assignments by (day, period)
        period_assignments = {}

        for entry in entries:
            key = (entry.day_of_week, entry.period_number)

            if key in period_assignments:
                # Multiple entries for same period = clash
                clashes.append(ClashInfo(
                    clash_type="class_clash",
                    day_of_week=entry.day_of_week,
                    period_number=entry.period_number,
                    existing_entry_id=period_assignments[key].id,
                    message=f"Multiple entries for period {entry.period_number} on day {entry.day_of_week}",
                ))
            else:
                period_assignments[key] = entry

            # Check teacher clashes across periods
            teacher_periods = {}
            for e in entries:
                if e.staff_id == entry.staff_id and e.day_of_week == entry.day_of_week:
                    if e.period_number in teacher_periods:
                        clashes.append(ClashInfo(
                            clash_type="teacher_clash",
                            day_of_week=entry.day_of_week,
                            period_number=entry.period_number,
                            existing_entry_id=teacher_periods[e.period_number].id,
                            message=f"Teacher clash on day {entry.day_of_week}, period {e.period_number}",
                        ))
                    teacher_periods[e.period_number] = e

        return clashes

    async def publish_timetable(
        self,
        timetable_id: UUID,
        user_id: UUID,
    ) -> TimetableResponse:
        """Publish a timetable after validation."""
        # Validate timetable
        clashes = await self.validate_timetable(timetable_id)
        if clashes:
            raise TimetableClashError(clashes)

        # Check has entries for each day
        entries = await self.entry_repo.list_by_timetable(timetable_id)
        if not entries:
            raise TimetableClashError([ClashInfo(
                clash_type="no_entries",
                day_of_week=0,
                period_number=0,
                message="Timetable has no entries",
            )])

        # Publish
        timetable = await self.timetable_repo.publish(timetable_id, user_id)
        return TimetableResponse.model_validate(timetable)

    async def get_entries(self, timetable_id: UUID) -> list[TimetableEntryResponse]:
        """Get all entries for a timetable."""
        entries = await self.entry_repo.list_by_timetable(timetable_id)
        return [TimetableEntryResponse.model_validate(e) for e in entries]

    async def get_entries_with_names(self, timetable_id: UUID) -> list[dict]:
        """Get all entries for a timetable with resolved staff and subject names."""
        return await self.entry_repo.list_entries_with_names(timetable_id)

    async def get_teacher_timetable(
        self,
        staff_id: UUID,
        class_id: UUID | None = None,
        academic_year_id: UUID | None = None,
        term_id: UUID | None = None,
    ) -> list[TimetableEntryResponse]:
        """Get timetable entries for a specific teacher."""
        entries = await self.entry_repo.get_teacher_published_entries(
            staff_id, class_id, academic_year_id, term_id
        )
        return [TimetableEntryResponse.model_validate(e) for e in entries]
