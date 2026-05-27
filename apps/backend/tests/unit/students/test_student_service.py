"""Tests for StudentService - TDD implementation."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest


@pytest.fixture
def mock_repository():
    """Create a mock student repository."""
    repo = AsyncMock()
    # Set default return values for common methods
    repo.exists_by_admission.return_value = False
    repo.exists_by_nin.return_value = False
    return repo


@pytest.fixture
def service(mock_repository):
    """Create StudentService with mocked repository."""
    from edulafia.modules.students.service import StudentService
    return StudentService(repository=mock_repository)


def make_student_mock(
    id: UUID = None,
    first_name: str = "Test",
    last_name: str = "Student",
    admission_number: str = "EDU/2026/001",
    status: str = "active",
    deleted_at=None,
) -> MagicMock:
    """Create a properly configured Student mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = uuid4()
    mock.first_name = first_name
    mock.last_name = last_name
    mock.middle_name = None
    mock.admission_number = admission_number
    mock.date_of_birth = date(2012, 5, 15)
    mock.gender = "female"
    mock.status = status
    mock.admission_date = date(2026, 1, 15)
    mock.class_id = uuid4()
    mock.nationality = "Nigerian"
    mock.state_of_origin = None
    mock.lga = None
    mock.address = None
    mock.photo_url = None
    mock.blood_group = None
    mock.genotype = None
    mock.nin = None
    mock.previous_school = None
    mock.graduation_date = None
    mock.deleted_at = deleted_at
    mock.created_at = date(2026, 1, 15)
    mock.updated_at = date(2026, 1, 15)
    return mock


class TestStudentService:
    """Test cases for StudentService business logic."""

    def test_student_service_exists(self):
        """Test that StudentService class exists."""
        from edulafia.modules.students.service import StudentService
        assert StudentService is not None

    async def test_create_student_success(self, service, mock_repository):
        """Test successful student creation."""
        from edulafia.modules.students.schemas import StudentCreate

        mock_repository.create.return_value = make_student_mock(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
        )

        data = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4(),
            admission_date=date(2026, 1, 15),
        )

        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.first_name == "Chioma"
        assert result.last_name == "Okonkwo"

    async def test_create_student_duplicate_admission_number_fails(
        self, service, mock_repository
    ):
        """Test that duplicate admission number raises error."""
        from edulafia.modules.students.exceptions import DuplicateAdmissionNumberError
        from edulafia.modules.students.schemas import StudentCreate

        mock_repository.exists_by_admission.return_value = True

        data = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4(),
            admission_date=date(2026, 1, 15),
        )

        with pytest.raises(DuplicateAdmissionNumberError):
            await service.create(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_get_student_by_id(self, service, mock_repository):
        """Test retrieving student by ID."""
        student_id = uuid4()
        mock_repository.get_by_id.return_value = make_student_mock(
            id=student_id,
            first_name="Test",
            last_name="Student",
        )

        result = await service.get_by_id(student_id=student_id, school_id=uuid4())

        assert result is not None
        assert result.id == student_id

    async def test_get_student_not_found(self, service, mock_repository):
        """Test retrieving non-existent student returns None."""
        mock_repository.get_by_id.return_value = None

        result = await service.get_by_id(
            student_id=uuid4(),
            school_id=uuid4(),
        )

        assert result is None

    async def test_list_students_with_pagination(self, service, mock_repository):
        """Test listing students with pagination."""
        mock_repository.list.return_value = (
            [make_student_mock(), make_student_mock()],
            100,
        )

        result = await service.list_students(
            school_id=uuid4(),
            page=1,
            per_page=20,
        )

        assert len(result.items) == 2
        assert result.total == 100
        assert result.page == 1

    async def test_list_students_with_class_filter(self, service, mock_repository):
        """Test listing students filtered by class."""
        class_id = uuid4()
        mock_repository.list.return_value = (
            [make_student_mock()],
            25,
        )

        filters = MagicMock()
        filters.class_id = class_id

        result = await service.list_students(
            school_id=uuid4(),
            page=1,
            per_page=20,
            filters=filters,
        )

        assert len(result.items) == 1

    async def test_update_student_success(self, service, mock_repository):
        """Test successful student update."""
        from edulafia.modules.students.schemas import StudentUpdate

        student_id = uuid4()
        mock_repository.get_by_id.return_value = make_student_mock(
            id=student_id,
            first_name="OldName",
        )
        mock_repository.update.return_value = make_student_mock(
            id=student_id,
            first_name="NewName",
        )

        update = StudentUpdate(first_name="NewName")
        result = await service.update(
            student_id=student_id,
            data=update,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.first_name == "NewName"

    async def test_archive_student_success(self, service, mock_repository):
        """Test successful student archival (soft delete)."""
        student_id = uuid4()
        mock_repository.get_by_id.return_value = make_student_mock(
            id=student_id,
            status="active",
        )
        mock_repository.soft_delete.return_value = make_student_mock(
            id=student_id,
            status="inactive",
        )

        result = await service.archive(
            student_id=student_id,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.status == "inactive"

    async def test_generate_unique_admission_number(self, service, mock_repository):
        """Test unique admission number generation."""
        mock_repository.get_next_admission_number.return_value = 42

        result = await service.generate_admission_number(
            school_id=uuid4(),
            school_code="EDU",
        )

        assert result.startswith("EDU")
        assert "0042" in result or "042" in result or "42" in result
