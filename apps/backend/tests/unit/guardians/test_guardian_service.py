"""Tests for GuardianService - TDD implementation."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


def make_guardian_mock(
    id=None,
    school_id=None,
    first_name="Ngozi",
    last_name="Okonkwo",
    phone_number="+2348012345678",
    relationship_type="mother",
    nin=None,
    whatsapp_number=None,
    portal_access=False,
    deleted_at=None,
):
    """Create a properly configured Guardian mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = school_id or uuid4()
    mock.first_name = first_name
    mock.last_name = last_name
    mock.middle_name = None
    mock.phone_number = phone_number
    mock.relationship_type = relationship_type
    mock.email = None
    mock.whatsapp_number = whatsapp_number
    mock.occupation = None
    mock.address = None
    mock.nin = nin
    mock.portal_access = portal_access
    mock.user_id = None
    mock.deleted_at = deleted_at
    mock.created_at = datetime(2026, 1, 15, tzinfo=UTC)
    mock.updated_at = datetime(2026, 1, 15, tzinfo=UTC)
    return mock


@pytest.fixture
def mock_repository():
    """Create a mock guardian repository."""
    repo = AsyncMock()
    repo.exists_by_nin.return_value = False
    repo.get_guardian_count_for_student.return_value = 0
    return repo


@pytest.fixture
def service(mock_repository):
    """Create GuardianService with mocked repository."""
    from edulafia.modules.guardians.service import GuardianService
    return GuardianService(repository=mock_repository)


class TestGuardianServiceCreate:
    """Test cases for GuardianService.create()"""

    async def test_create_guardian_success(self, service, mock_repository):
        """Test successful guardian creation."""
        from edulafia.modules.guardians.schemas import GuardianCreate

        mock_repository.create.return_value = make_guardian_mock(
            first_name="Ngozi",
            last_name="Okonkwo",
        )

        data = GuardianCreate(
            first_name="Ngozi",
            last_name="Okonkwo",
            phone_number="+2348012345678",
            relationship_type="mother",
        )

        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.first_name == "Ngozi"
        assert result.last_name == "Okonkwo"

    async def test_create_guardian_duplicate_nin_fails(self, service, mock_repository):
        """Test that duplicate NIN raises error."""
        from edulafia.modules.guardians.schemas import GuardianCreate

        mock_repository.exists_by_nin.return_value = True

        data = GuardianCreate(
            first_name="Ngozi",
            last_name="Okonkwo",
            phone_number="+2348012345678",
            relationship_type="mother",
            nin="12345678901",
        )

        with pytest.raises(ValueError, match="NIN already exists"):
            await service.create(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_create_guardian_with_whatsapp_enables_portal(self, service, mock_repository):
        """Test that providing WhatsApp number enables portal access."""
        from edulafia.modules.guardians.schemas import GuardianCreate

        mock = make_guardian_mock(whatsapp_number="+2348012345678", portal_access=True)
        mock_repository.create.return_value = mock

        data = GuardianCreate(
            first_name="Ngozi",
            last_name="Okonkwo",
            phone_number="+2348012345678",
            relationship_type="mother",
            whatsapp_number="+2348012345678",
        )

        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.portal_access is True


class TestGuardianServiceGetById:
    """Test cases for GuardianService.get_by_id()"""

    async def test_get_guardian_by_id(self, service, mock_repository):
        """Test retrieving guardian by ID."""
        guardian_id = uuid4()
        mock_repository.get_by_id.return_value = make_guardian_mock(
            id=guardian_id,
            first_name="Test",
        )

        result = await service.get_by_id(guardian_id=guardian_id, school_id=uuid4())

        assert result is not None
        assert result.id == guardian_id

    async def test_get_guardian_not_found(self, service, mock_repository):
        """Test retrieving non-existent guardian returns None."""
        mock_repository.get_by_id.return_value = None

        result = await service.get_by_id(guardian_id=uuid4(), school_id=uuid4())

        assert result is None


class TestGuardianServiceList:
    """Test cases for GuardianService.list_guardians()"""

    async def test_list_guardians_with_pagination(self, service, mock_repository):
        """Test listing guardians with pagination."""
        mock_repository.list.return_value = (
            [make_guardian_mock(), make_guardian_mock()],
            50,
        )

        result = await service.list_guardians(
            school_id=uuid4(),
            page=1,
            per_page=20,
        )

        assert len(result["items"]) == 2
        assert result["total"] == 50
        assert result["page"] == 1
        assert result["pages"] == 3  # ceil(50/20)

    async def test_list_guardians_empty(self, service, mock_repository):
        """Test listing guardians when none exist."""
        mock_repository.list.return_value = ([], 0)

        result = await service.list_guardians(school_id=uuid4())

        assert len(result["items"]) == 0
        assert result["total"] == 0


class TestGuardianServiceUpdate:
    """Test cases for GuardianService.update()"""

    async def test_update_guardian_success(self, service, mock_repository):
        """Test successful guardian update."""
        from edulafia.modules.guardians.schemas import GuardianUpdate

        guardian_id = uuid4()
        mock_repository.get_by_id.return_value = make_guardian_mock(id=guardian_id)
        mock_repository.update.return_value = make_guardian_mock(
            id=guardian_id,
            first_name="UpdatedName",
        )

        update = GuardianUpdate(first_name="UpdatedName")
        result = await service.update(
            guardian_id=guardian_id,
            data=update,
            school_id=uuid4(),
        )

        assert result.first_name == "UpdatedName"

    async def test_update_guardian_not_found(self, service, mock_repository):
        """Test updating non-existent guardian raises error."""
        from edulafia.modules.guardians.schemas import GuardianUpdate

        mock_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Guardian not found"):
            await service.update(
                guardian_id=uuid4(),
                data=GuardianUpdate(first_name="NewName"),
                school_id=uuid4(),
            )


class TestGuardianServiceArchive:
    """Test cases for GuardianService.archive()"""

    async def test_archive_guardian_success(self, service, mock_repository):
        """Test successful guardian archival."""
        guardian_id = uuid4()
        mock_repository.get_by_id.return_value = make_guardian_mock(id=guardian_id)
        mock_repository.soft_delete.return_value = make_guardian_mock(
            id=guardian_id,
            deleted_at=datetime.now(UTC),
        )

        result = await service.archive(guardian_id=guardian_id, school_id=uuid4())

        assert result is not None

    async def test_archive_guardian_not_found(self, service, mock_repository):
        """Test archiving non-existent guardian raises error."""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Guardian not found"):
            await service.archive(guardian_id=uuid4(), school_id=uuid4())


class TestGuardianServiceLinkToStudent:
    """Test cases for GuardianService.link_to_student()"""

    async def test_link_guardian_to_student_success(self, service, mock_repository):
        """Test successful guardian-student link."""
        student_id = uuid4()
        guardian_id = uuid4()

        link_mock = MagicMock()
        link_mock.student_id = student_id
        link_mock.guardian_id = guardian_id
        link_mock.is_primary = True
        link_mock.is_emergency_contact = False
        link_mock.can_pickup = True

        mock_repository.link_to_student.return_value = link_mock

        result = await service.link_to_student(
            student_id=student_id,
            guardian_id=guardian_id,
            is_primary=True,
        )

        assert result["student_id"] == student_id
        assert result["guardian_id"] == guardian_id
        assert result["is_primary"] is True

    async def test_link_guardian_max_limit_fails(self, service, mock_repository):
        """Test that exceeding max guardians limit raises error."""
        mock_repository.get_guardian_count_for_student.return_value = 2

        with pytest.raises(ValueError, match="maximum"):
            await service.link_to_student(
                student_id=uuid4(),
                guardian_id=uuid4(),
            )


class TestGuardianServiceUnlinkFromStudent:
    """Test cases for GuardianService.unlink_from_student()"""

    async def test_unlink_guardian_success(self, service, mock_repository):
        """Test successful guardian-student unlink."""
        mock_repository.get_guardian_count_for_student.return_value = 2
        mock_repository.unlink_from_student.return_value = True

        result = await service.unlink_from_student(
            student_id=uuid4(),
            guardian_id=uuid4(),
        )

        assert result is True

    async def test_unlink_last_guardian_fails(self, service, mock_repository):
        """Test that removing the last guardian raises error."""
        mock_repository.get_guardian_count_for_student.return_value = 1

        with pytest.raises(ValueError, match="Cannot remove the last guardian"):
            await service.unlink_from_student(
                student_id=uuid4(),
                guardian_id=uuid4(),
            )


class TestGuardianServiceGetStudentGuardians:
    """Test cases for GuardianService.get_student_guardians()"""

    async def test_get_student_guardians(self, service, mock_repository):
        """Test getting all guardians for a student."""
        mock_repository.get_student_guardians.return_value = [
            make_guardian_mock(first_name="Mother"),
            make_guardian_mock(first_name="Father"),
        ]

        result = await service.get_student_guardians(student_id=uuid4())

        assert len(result) == 2
