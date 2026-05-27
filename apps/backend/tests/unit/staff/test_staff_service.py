"""Tests for StaffService and AssignmentService - written BEFORE implementation (TDD)."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_staff_repo():
    """Create a mock staff repository."""
    repo = AsyncMock()
    repo.get_next_staff_id.return_value = "TCH-00001"
    repo.exists_by_staff_id.return_value = False
    return repo


@pytest.fixture
def mock_assignment_repo():
    """Create a mock assignment repository."""
    repo = AsyncMock()
    repo.exists_duplicate.return_value = False
    repo.has_form_teacher.return_value = False
    repo.get_teacher_load.return_value = 5
    return repo


@pytest.fixture
def staff_service(mock_staff_repo):
    """Create StaffService with mocked repository."""
    from edulafia.modules.staff.service import StaffService
    return StaffService(mock_staff_repo)


@pytest.fixture
def assignment_service(mock_assignment_repo, mock_staff_repo):
    """Create AssignmentService with mocked repositories."""
    from edulafia.modules.staff.service import AssignmentService
    return AssignmentService(mock_assignment_repo, mock_staff_repo)


def make_staff_mock(
    id=None,
    first_name="John",
    last_name="Doe",
    staff_id="TCH-00001",
    role="teacher",
    status="active",
) -> MagicMock:
    """Create a properly configured Staff mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = uuid4()
    mock.user_id = uuid4()
    mock.staff_id = staff_id
    mock.first_name = first_name
    mock.last_name = last_name
    mock.middle_name = None
    mock.email = None
    mock.phone = "08012345678"
    mock.whatsapp_phone = None
    mock.date_of_birth = None
    mock.gender = "male"
    mock.address = None
    mock.photo_url = None
    mock.role = role
    mock.department = None
    mock.qualifications = None
    mock.documents = None
    mock.subjects = None
    mock.employment_type = "permanent"
    mock.employment_date = None
    mock.exit_date = None
    mock.status = status
    mock.version = 1
    mock.created_at = date.today()
    mock.updated_at = date.today()
    return mock


def make_assignment_mock(
    id=None,
    staff_id=None,
    class_id=None,
    subject_id=None,
    is_form_teacher=False,
    school_id=None,
) -> MagicMock:
    """Create a properly configured StaffAssignment mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.staff_id = staff_id or uuid4()
    mock.class_id = class_id or uuid4()
    mock.subject_id = subject_id or uuid4()
    mock.school_id = school_id or uuid4()
    mock.academic_year_id = uuid4()
    mock.term_id = None
    mock.assignment_type = "regular"
    mock.is_form_teacher = is_form_teacher
    mock.start_date = None
    mock.end_date = None
    mock.is_active = True
    mock.notes = None
    mock.created_at = date.today()
    mock.updated_at = date.today()
    return mock


class TestStaffService:
    """Test cases for StaffService."""

    def test_staff_service_exists(self):
        """Test that StaffService class exists."""
        from edulafia.modules.staff.service import StaffService
        assert StaffService is not None

    async def test_create_staff_success(self, staff_service, mock_staff_repo):
        """Test successful staff creation."""
        from edulafia.modules.staff.schemas import StaffCreate

        mock_staff_repo.create.return_value = make_staff_mock(
            first_name="John",
            last_name="Doe",
            staff_id="TCH-00001",
        )

        data = StaffCreate(
            first_name="John",
            last_name="Doe",
            phone="08012345678",
            gender="male",
            role="teacher",
        )

        result = await staff_service.create_staff(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.staff_id == "TCH-00001"

    async def test_create_staff_generates_staff_id(self, staff_service, mock_staff_repo):
        """Test that staff ID is generated."""
        from edulafia.modules.staff.schemas import StaffCreate

        mock_staff_repo.get_next_staff_id.return_value = "TCH-00042"
        mock_staff_repo.create.return_value = make_staff_mock(staff_id="TCH-00042")

        data = StaffCreate(
            first_name="Jane",
            last_name="Smith",
            phone="08012345678",
            gender="female",
            role="teacher",
        )

        result = await staff_service.create_staff(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.staff_id == "TCH-00042"

    async def test_get_staff_by_id(self, staff_service, mock_staff_repo):
        """Test getting staff by ID."""
        staff_id = uuid4()
        mock_staff_repo.get_by_id.return_value = make_staff_mock(id=staff_id)

        result = await staff_service.get_staff(
            staff_id=staff_id,
            school_id=uuid4(),
        )

        assert result.id == staff_id

    async def test_get_staff_not_found(self, staff_service, mock_staff_repo):
        """Test getting non-existent staff."""
        from edulafia.modules.staff.exceptions import StaffNotFoundError

        mock_staff_repo.get_by_id.return_value = None

        with pytest.raises(StaffNotFoundError):
            await staff_service.get_staff(
                staff_id=uuid4(),
                school_id=uuid4(),
            )

    async def test_list_staff_with_filters(self, staff_service, mock_staff_repo):
        """Test listing staff with filters."""
        mock_staff_repo.list.return_value = (
            [make_staff_mock(), make_staff_mock()],
            50,
        )

        result = await staff_service.list_staff(
            school_id=uuid4(),
            role="teacher",
            page=1,
            per_page=20,
        )

        assert len(result["items"]) == 2
        assert result["total"] == 50

    async def test_update_staff_success(self, staff_service, mock_staff_repo):
        """Test successful staff update."""
        from edulafia.modules.staff.schemas import StaffUpdate

        staff_id = uuid4()
        mock_staff_repo.get_by_id.return_value = make_staff_mock(id=staff_id)
        mock_staff_repo.update.return_value = make_staff_mock(
            id=staff_id,
            first_name="Updated",
        )

        update = StaffUpdate(first_name="Updated")
        result = await staff_service.update_staff(
            staff_id=staff_id,
            data=update,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.first_name == "Updated"

    async def test_deactivate_staff_success(self, staff_service, mock_staff_repo):
        """Test successful staff deactivation."""
        from edulafia.modules.staff.schemas import StaffDeactivate

        staff_id = uuid4()
        mock_staff_repo.get_by_id.return_value = make_staff_mock(id=staff_id)
        mock_staff_repo.deactivate.return_value = make_staff_mock(
            id=staff_id,
            status="inactive",
        )

        data = StaffDeactivate(reason="Resignation")
        result = await staff_service.deactivate_staff(
            staff_id=staff_id,
            data=data,
            school_id=uuid4(),
        )

        assert result.status == "inactive"


class TestAssignmentService:
    """Test cases for AssignmentService."""

    def test_assignment_service_exists(self):
        """Test that AssignmentService class exists."""
        from edulafia.modules.staff.service import AssignmentService
        assert AssignmentService is not None

    async def test_create_assignment_success(self, assignment_service, mock_assignment_repo):
        """Test successful assignment creation."""
        from edulafia.modules.staff.schemas import StaffAssignmentCreate

        mock_assignment_repo.create.return_value = make_assignment_mock()

        data = StaffAssignmentCreate(
            staff_id=uuid4(),
            class_id=uuid4(),
            subject_id=uuid4(),
            academic_year_id=uuid4(),
        )

        result = await assignment_service.create_assignment(
            data=data,
            user_id=uuid4(),
        )

        assert result is not None
        assert result.assignment_type == "regular"

    async def test_create_form_teacher_assignment(self, assignment_service, mock_assignment_repo):
        """Test creating form teacher assignment."""
        from edulafia.modules.staff.schemas import StaffAssignmentCreate

        mock_assignment_repo.create.return_value = make_assignment_mock(is_form_teacher=True)

        data = StaffAssignmentCreate(
            staff_id=uuid4(),
            class_id=uuid4(),
            academic_year_id=uuid4(),
            is_form_teacher=True,
        )

        result = await assignment_service.create_assignment(
            data=data,
            user_id=uuid4(),
        )

        assert result.is_form_teacher == True

    async def test_create_duplicate_assignment_fails(self, assignment_service, mock_assignment_repo):
        """Test that duplicate assignment fails."""
        from edulafia.modules.staff.exceptions import DuplicateAssignmentError
        from edulafia.modules.staff.schemas import StaffAssignmentCreate

        mock_assignment_repo.exists_duplicate.return_value = True

        data = StaffAssignmentCreate(
            staff_id=uuid4(),
            class_id=uuid4(),
            subject_id=uuid4(),
            academic_year_id=uuid4(),
        )

        with pytest.raises(DuplicateAssignmentError):
            await assignment_service.create_assignment(
                data=data,
                user_id=uuid4(),
            )

    async def test_form_teacher_already_assigned_fails(self, assignment_service, mock_assignment_repo):
        """Test that duplicate form teacher assignment fails."""
        from edulafia.modules.staff.exceptions import FormTeacherAlreadyAssignedError
        from edulafia.modules.staff.schemas import StaffAssignmentCreate

        mock_assignment_repo.has_form_teacher.return_value = True

        data = StaffAssignmentCreate(
            staff_id=uuid4(),
            class_id=uuid4(),
            academic_year_id=uuid4(),
            is_form_teacher=True,
        )

        with pytest.raises(FormTeacherAlreadyAssignedError):
            await assignment_service.create_assignment(
                data=data,
                user_id=uuid4(),
            )

    async def test_max_load_exceeded_fails(self, assignment_service, mock_assignment_repo):
        """Test that exceeding max load fails."""
        from edulafia.modules.staff.exceptions import MaxLoadExceededError
        from edulafia.modules.staff.schemas import StaffAssignmentCreate

        mock_assignment_repo.get_teacher_load.return_value = 30  # At max

        data = StaffAssignmentCreate(
            staff_id=uuid4(),
            class_id=uuid4(),
            subject_id=uuid4(),
            academic_year_id=uuid4(),
        )

        with pytest.raises(MaxLoadExceededError):
            await assignment_service.create_assignment(
                data=data,
                user_id=uuid4(),
            )

    async def test_delete_assignment_success(self, assignment_service, mock_assignment_repo):
        """Test successful assignment deletion."""
        assignment_id = uuid4()
        school_id = uuid4()
        mock_assignment_repo.get_by_id.return_value = make_assignment_mock(id=assignment_id, school_id=school_id)
        mock_assignment_repo.delete.return_value = True

        result = await assignment_service.delete_assignment(assignment_id, school_id)
        assert result is True
        mock_assignment_repo.delete.assert_called_once_with(assignment_id)

    async def test_delete_assignment_not_found(self, assignment_service, mock_assignment_repo):
        """Test assignment deletion when not found."""
        from edulafia.modules.staff.exceptions import AssignmentNotFoundError
        
        assignment_id = uuid4()
        school_id = uuid4()
        mock_assignment_repo.get_by_id.return_value = None

        with pytest.raises(AssignmentNotFoundError):
            await assignment_service.delete_assignment(assignment_id, school_id)
