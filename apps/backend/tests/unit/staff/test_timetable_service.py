"""Tests for TimetableService - written BEFORE implementation (TDD)."""

from datetime import date, time
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_timetable_repo():
    """Create a mock timetable repository."""
    return AsyncMock()


@pytest.fixture
def mock_entry_repo():
    """Create a mock timetable entry repository."""
    repo = AsyncMock()
    repo.get_teacher_entries_on_day.return_value = []
    repo.get_class_entries_on_period.return_value = None
    return repo


@pytest.fixture
def timetable_service(mock_timetable_repo, mock_entry_repo):
    """Create TimetableService with mocked repositories."""
    from edulafia.modules.staff.timetable import TimetableService
    return TimetableService(mock_timetable_repo, mock_entry_repo)


def make_timetable_mock(
    id=None,
    class_id=None,
    is_published=False,
    is_draft=True,
) -> MagicMock:
    """Create a properly configured Timetable mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = uuid4()
    mock.class_id = class_id or uuid4()
    mock.academic_year_id = uuid4()
    mock.term_id = uuid4()
    mock.effective_from = date.today()
    mock.effective_to = None
    mock.is_published = is_published
    mock.published_at = None
    mock.published_by = None
    mock.version_number = 1
    mock.is_draft = is_draft
    mock.created_at = date.today()
    mock.updated_at = date.today()
    return mock


def make_entry_mock(
    id=None,
    timetable_id=None,
    day_of_week=1,
    period_number=1,
    staff_id=None,
    is_break=False,
) -> MagicMock:
    """Create a properly configured TimetableEntry mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.timetable_id = timetable_id or uuid4()
    mock.day_of_week = day_of_week
    mock.period_number = period_number
    mock.start_time = time(8, 0)
    mock.end_time = time(9, 0)
    mock.subject_id = uuid4()
    mock.staff_id = staff_id or uuid4()
    mock.room_number = None
    mock.notes = None
    mock.is_break = is_break
    mock.created_at = date.today()
    mock.updated_at = date.today()
    return mock


class TestTimetableService:
    """Test cases for TimetableService."""

    def test_timetable_service_exists(self):
        """Test that TimetableService class exists."""
        from edulafia.modules.staff.timetable import TimetableService
        assert TimetableService is not None

    async def test_create_timetable_success(self, timetable_service, mock_timetable_repo):
        """Test successful timetable creation."""
        from edulafia.modules.staff.schemas import TimetableCreate

        mock_timetable_repo.get_draft.return_value = None
        mock_timetable_repo.create.return_value = make_timetable_mock()

        data = TimetableCreate(
            class_id=uuid4(),
            academic_year_id=uuid4(),
            term_id=uuid4(),
            effective_from=date.today(),
        )

        result = await timetable_service.create_timetable(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result is not None
        assert result.is_draft == True

    async def test_create_timetable_draft_exists_fails(self, timetable_service, mock_timetable_repo):
        """Test that creating timetable when draft exists fails."""
        from edulafia.modules.staff.exceptions import DraftTimetableExistsError
        from edulafia.modules.staff.schemas import TimetableCreate

        mock_timetable_repo.get_draft.return_value = make_timetable_mock()

        data = TimetableCreate(
            class_id=uuid4(),
            academic_year_id=uuid4(),
            term_id=uuid4(),
            effective_from=date.today(),
        )

        with pytest.raises(DraftTimetableExistsError):
            await timetable_service.create_timetable(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_add_entry_success(self, timetable_service, mock_timetable_repo, mock_entry_repo):
        """Test successful entry addition."""
        from edulafia.modules.staff.schemas import TimetableEntryCreate

        timetable_id = uuid4()
        mock_timetable_repo.get_by_id.return_value = make_timetable_mock(id=timetable_id)
        mock_entry_repo.create.return_value = make_entry_mock(timetable_id=timetable_id)

        data = TimetableEntryCreate(
            day_of_week=1,
            period_number=1,
            start_time=time(8, 0),
            end_time=time(9, 0),
            subject_id=uuid4(),
            staff_id=uuid4(),
        )

        result, clashes = await timetable_service.add_entry(
            timetable_id=timetable_id,
            data=data,
        )

        assert result is not None
        assert len(clashes) == 0

    async def test_detect_teacher_clash(self, timetable_service, mock_entry_repo):
        """Test teacher clash detection."""
        from edulafia.modules.staff.schemas import TimetableEntryCreate

        # Teacher already has entry on day 1, period 1
        existing_entry = make_entry_mock(
            day_of_week=1,
            period_number=1,
            staff_id=uuid4(),
        )
        mock_entry_repo.get_teacher_entries_on_day.return_value = [existing_entry]

        data = TimetableEntryCreate(
            day_of_week=1,
            period_number=1,
            start_time=time(8, 0),
            end_time=time(9, 0),
            subject_id=uuid4(),
            staff_id=existing_entry.staff_id,  # Same teacher
        )

        clashes = await timetable_service.detect_clashes(
            timetable_id=uuid4(),
            data=data,
        )

        assert len(clashes) > 0
        assert clashes[0].clash_type == "teacher_clash"

    async def test_no_clash_for_different_period(self, timetable_service, mock_entry_repo):
        """Test no clash for different period."""
        from edulafia.modules.staff.schemas import TimetableEntryCreate

        # Teacher has entry on day 1, period 1
        existing_entry = make_entry_mock(
            day_of_week=1,
            period_number=1,
            staff_id=uuid4(),
        )
        mock_entry_repo.get_teacher_entries_on_day.return_value = [existing_entry]

        data = TimetableEntryCreate(
            day_of_week=1,
            period_number=2,  # Different period
            start_time=time(9, 0),
            end_time=time(10, 0),
            subject_id=uuid4(),
            staff_id=existing_entry.staff_id,
        )

        clashes = await timetable_service.detect_clashes(
            timetable_id=uuid4(),
            data=data,
        )

        assert len(clashes) == 0

    async def test_validate_timetable_success(self, timetable_service, mock_entry_repo):
        """Test timetable validation success."""
        timetable_id = uuid4()
        mock_entry_repo.list_by_timetable.return_value = [
            make_entry_mock(day_of_week=1, period_number=1),
            make_entry_mock(day_of_week=1, period_number=2),
            make_entry_mock(day_of_week=2, period_number=1),
        ]

        clashes = await timetable_service.validate_timetable(timetable_id)

        assert len(clashes) == 0

    async def test_validate_timetable_finds_clashes(self, timetable_service, mock_entry_repo):
        """Test timetable validation finds clashes."""
        timetable_id = uuid4()
        staff_id = uuid4()

        # Two entries for same period = clash
        mock_entry_repo.list_by_timetable.return_value = [
            make_entry_mock(day_of_week=1, period_number=1, staff_id=staff_id),
            make_entry_mock(day_of_week=1, period_number=1, staff_id=staff_id),  # Clash
        ]

        clashes = await timetable_service.validate_timetable(timetable_id)

        assert len(clashes) > 0

    async def test_publish_timetable_success(self, timetable_service, mock_timetable_repo, mock_entry_repo):
        """Test successful timetable publication."""
        timetable_id = uuid4()
        mock_timetable_repo.get_by_id.return_value = make_timetable_mock(id=timetable_id)
        mock_timetable_repo.publish.return_value = make_timetable_mock(
            id=timetable_id,
            is_published=True,
            is_draft=False,
        )
        mock_entry_repo.list_by_timetable.return_value = [
            make_entry_mock(timetable_id=timetable_id),
        ]

        result = await timetable_service.publish_timetable(
            timetable_id=timetable_id,
            user_id=uuid4(),
        )

        assert result.is_published == True
        assert result.is_draft == False

    async def test_publish_timetable_with_clashes_fails(self, timetable_service, mock_timetable_repo, mock_entry_repo):
        """Test publishing timetable with clashes fails."""
        from edulafia.modules.staff.exceptions import TimetableClashError

        timetable_id = uuid4()
        staff_id = uuid4()

        mock_timetable_repo.get_by_id.return_value = make_timetable_mock(id=timetable_id)

        # Entries with clashes
        mock_entry_repo.list_by_timetable.return_value = [
            make_entry_mock(timetable_id=timetable_id, day_of_week=1, period_number=1, staff_id=staff_id),
            make_entry_mock(timetable_id=timetable_id, day_of_week=1, period_number=1, staff_id=staff_id),
        ]

        with pytest.raises(TimetableClashError):
            await timetable_service.publish_timetable(
                timetable_id=timetable_id,
                user_id=uuid4(),
            )
