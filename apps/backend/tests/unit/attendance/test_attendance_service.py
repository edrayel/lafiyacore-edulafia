"""Tests for AttendanceService - written BEFORE implementation (TDD)."""

from datetime import UTC, date, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_repository():
    """Create a mock attendance repository."""
    repo = AsyncMock()
    repo.exists_for_student_date.return_value = False
    return repo


@pytest.fixture
def service(mock_repository):
    """Create AttendanceService with mocked repository."""
    from edulafia.modules.attendance.service import AttendanceService
    return AttendanceService(repository=mock_repository)


def make_attendance_mock(
    id=None,
    student_id=None,
    class_id=None,
    school_id=None,
    date_val=None,
    status="present",
    reason_code=None,
    symptom_codes=None,
    deleted_at=None,
) -> MagicMock:
    """Create a properly configured AttendanceRecord mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.student_id = student_id or uuid4()
    mock.class_id = class_id or uuid4()
    mock.school_id = school_id or uuid4()
    mock.date = date_val or date.today()
    mock.period = None
    mock.status = status
    mock.reason_code = reason_code
    mock.symptom_codes = symptom_codes
    mock.notes = None
    mock.recorded_by = uuid4()
    mock.edited_at = None
    mock.edited_by = None
    mock.edit_reason = None
    mock.device_id = None
    mock.sync_status = "synced"
    mock.created_at = date.today()
    mock.updated_at = date.today()
    mock.deleted_at = deleted_at
    return mock


class TestAttendanceService:
    """Test cases for AttendanceService."""

    def test_attendance_service_exists(self):
        """Test that AttendanceService class exists."""
        from edulafia.modules.attendance.service import AttendanceService
        assert AttendanceService is not None

    async def test_mark_attendance_success(self, service, mock_repository):
        """Test successful attendance marking."""
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        mock_repository.create.return_value = make_attendance_mock(status="present")

        data = AttendanceMarkRequest(
            student_id=uuid4(),
            class_id=uuid4(),
            date=date.today(),
            status="present",
        )

        result = await service.mark_attendance(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.status == "present"

    async def test_mark_attendance_with_symptoms(self, service, mock_repository):
        """Test marking absent attendance with symptoms."""
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        mock_repository.create.return_value = make_attendance_mock(
            status="absent",
            reason_code="sick",
            symptom_codes=["fever", "cough"],
        )

        data = AttendanceMarkRequest(
            student_id=uuid4(),
            class_id=uuid4(),
            date=date.today(),
            status="absent",
            reason_code="sick",
            symptom_codes=["fever", "cough"],
        )

        result = await service.mark_attendance(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.status == "absent"
        assert result.reason_code == "sick"
        assert result.symptom_codes == ["fever", "cough"]

    async def test_mark_attendance_duplicate_fails(self, service, mock_repository):
        """Test that duplicate attendance fails."""
        from edulafia.modules.attendance.exceptions import DuplicateAttendanceError
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        mock_repository.exists_for_student_date.return_value = True

        data = AttendanceMarkRequest(
            student_id=uuid4(),
            class_id=uuid4(),
            date=date.today(),
            status="present",
        )

        with pytest.raises(DuplicateAttendanceError):
            await service.mark_attendance(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_mark_attendance_future_date_fails(self, service, mock_repository):
        """Test that future date attendance fails at schema level."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            from edulafia.modules.attendance.schemas import AttendanceMarkRequest

            AttendanceMarkRequest(
                student_id=uuid4(),
                class_id=uuid4(),
                date=date.today() + timedelta(days=1),
                status="present",
            )

    async def test_mark_attendance_absent_requires_reason(self, service, mock_repository):
        """Test that absent status requires reason."""
        from edulafia.modules.attendance.exceptions import ReasonRequiredError
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        data = AttendanceMarkRequest(
            student_id=uuid4(),
            class_id=uuid4(),
            date=date.today(),
            status="absent",
            # No reason_code
        )

        with pytest.raises(ReasonRequiredError):
            await service.mark_attendance(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_mark_attendance_sick_requires_symptoms(self, service, mock_repository):
        """Test that sick reason requires symptoms."""
        from edulafia.modules.attendance.exceptions import SymptomRequiredError
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        data = AttendanceMarkRequest(
            student_id=uuid4(),
            class_id=uuid4(),
            date=date.today(),
            status="absent",
            reason_code="sick",
            # No symptom_codes
        )

        with pytest.raises(SymptomRequiredError):
            await service.mark_attendance(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_get_attendance_summary(self, service, mock_repository):
        """Test getting attendance summary."""
        mock_repository.get_summary.return_value = {
            "total": 100,
            "present": 85,
            "absent": 10,
            "late": 3,
            "excused": 2,
        }

        result = await service.get_summary(school_id=uuid4())

        assert result.total_students == 100
        assert result.present == 85
        assert result.absent == 10
        assert result.attendance_rate == 85.0

    async def test_get_attendance_with_filters(self, service, mock_repository):
        """Test getting attendance with filters."""
        mock_repository.list.return_value = (
            [make_attendance_mock(), make_attendance_mock()],
            50,
        )

        result = await service.get_attendance(
            school_id=uuid4(),
            page=1,
            per_page=20,
        )

        assert len(result["items"]) == 2
        assert result["total"] == 50

    async def test_update_attendance_success(self, service, mock_repository):
        """Test successful attendance update."""
        from edulafia.modules.attendance.schemas import AttendanceUpdateRequest

        record_id = uuid4()
        record = make_attendance_mock(id=record_id)
        from datetime import datetime
        record.created_at = datetime.now(UTC)

        mock_repository.get_by_id.return_value = record
        mock_repository.update.return_value = make_attendance_mock(
            id=record_id,
            status="absent",
        )

        data = AttendanceUpdateRequest(
            status="absent",
            edit_reason="Corrected error",
        )

        result = await service.update_attendance(
            record_id=record_id,
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.status == "absent"

    async def test_update_attendance_not_found(self, service, mock_repository):
        """Test update attendance not found."""
        from edulafia.modules.attendance.exceptions import AttendanceNotFoundError
        from edulafia.modules.attendance.schemas import AttendanceUpdateRequest

        mock_repository.get_by_id.return_value = None

        data = AttendanceUpdateRequest(
            status="absent",
            edit_reason="Corrected error",
        )

        with pytest.raises(AttendanceNotFoundError):
            await service.update_attendance(
                record_id=uuid4(),
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )


class TestSentinelIntegration:
    """Test cases for LafiyaSentinel integration."""

    def test_sentinel_service_exists(self):
        """Test that SentinelIntegrationService exists."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService
        assert SentinelIntegrationService is not None

    def test_is_sentinel_relevant_sick_with_symptoms(self):
        """Test that sick absence with symptoms is Sentinel relevant."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(
            status="absent",
            reason_code="sick",
            symptom_codes=["fever", "cough"],
        )

        assert SentinelIntegrationService.is_sentinel_relevant(record) == True

    def test_is_sentinel_relevant_present_not_relevant(self):
        """Test that present status is not Sentinel relevant."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(status="present")

        assert SentinelIntegrationService.is_sentinel_relevant(record) == False

    def test_is_sentinel_relevant_absent_no_reason_not_relevant(self):
        """Test that absent without reason is not Sentinel relevant."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(status="absent", reason_code=None)

        assert SentinelIntegrationService.is_sentinel_relevant(record) == False

    def test_is_sentinel_relevant_family_reason_not_relevant(self):
        """Test that family reason is not Sentinel relevant."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(
            status="absent",
            reason_code="family",
        )

        assert SentinelIntegrationService.is_sentinel_relevant(record) == False

    def test_is_sentinel_relevant_sick_no_symptoms_not_relevant(self):
        """Test that sick without symptoms is not Sentinel relevant."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(
            status="absent",
            reason_code="sick",
            symptom_codes=None,
        )

        assert SentinelIntegrationService.is_sentinel_relevant(record) == False

    def test_extract_symptom_data(self):
        """Test extracting symptom data."""
        from edulafia.modules.attendance.sentinel import SentinelIntegrationService

        record = make_attendance_mock(
            status="absent",
            reason_code="sick",
            symptom_codes=["fever", "cough", "headache"],
        )

        data = SentinelIntegrationService.extract_symptom_data(record)

        assert "student_id" in data
        assert "school_id" in data
        assert "symptom_codes" in data
        assert data["symptom_codes"] == ["fever", "cough", "headache"]
