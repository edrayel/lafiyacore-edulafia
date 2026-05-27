"""Tests for SubjectService - written BEFORE implementation (TDD)."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_repository():
    """Create a mock subject repository."""
    repo = AsyncMock()
    repo.exists_by_code.return_value = False
    return repo


@pytest.fixture
def service(mock_repository):
    """Create SubjectService with mocked repository."""
    from edulafia.modules.academics.service import SubjectService
    return SubjectService(repository=mock_repository)


def make_subject_mock(
    id=None,
    name="Mathematics",
    code="MATH",
    is_core=True,
    waec_code=None,
    neco_code=None,
    deleted_at=None,
) -> MagicMock:
    """Create a properly configured Subject mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.school_id = uuid4()
    mock.name = name
    mock.code = code
    mock.description = None
    mock.is_core = is_core
    mock.waec_code = waec_code
    mock.neco_code = neco_code
    mock.deleted_at = deleted_at
    mock.created_at = date(2026, 1, 15)
    mock.updated_at = date(2026, 1, 15)
    return mock


class TestSubjectService:
    """Test cases for SubjectService business logic."""

    def test_subject_service_exists(self):
        """Test that SubjectService class exists."""
        from edulafia.modules.academics.service import SubjectService
        assert SubjectService is not None

    async def test_create_subject_success(self, service, mock_repository):
        """Test successful subject creation."""
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.create.return_value = make_subject_mock(
            name="Mathematics",
            code="MATH",
        )

        data = SubjectCreate(name="Mathematics", code="MATH")
        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.name == "Mathematics"
        assert result.code == "MATH"

    async def test_create_subject_duplicate_code_fails(self, service, mock_repository):
        """Test that duplicate code raises error."""
        from edulafia.modules.academics.exceptions import DuplicateSubjectCodeError
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.exists_by_code.return_value = True

        data = SubjectCreate(name="Mathematics", code="MATH")

        with pytest.raises(DuplicateSubjectCodeError):
            await service.create(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_create_subject_with_waec_code(self, service, mock_repository):
        """Test creating subject with WAEC code."""
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.create.return_value = make_subject_mock(
            name="Mathematics",
            code="MATH",
            waec_code="402",
        )

        data = SubjectCreate(
            name="Mathematics",
            code="MATH",
            waec_code="402",
        )
        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.waec_code == "402"

    async def test_create_subject_with_neco_code(self, service, mock_repository):
        """Test creating subject with NECO code."""
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.create.return_value = make_subject_mock(
            name="Mathematics",
            code="MATH",
            neco_code="MAT001",
        )

        data = SubjectCreate(
            name="Mathematics",
            code="MATH",
            neco_code="MAT001",
        )
        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.neco_code == "MAT001"

    async def test_create_subject_core_subject(self, service, mock_repository):
        """Test creating core subject."""
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.create.return_value = make_subject_mock(
            name="English Language",
            code="ENG",
            is_core=True,
        )

        data = SubjectCreate(
            name="English Language",
            code="ENG",
            is_core=True,
        )
        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.is_core == True

    async def test_create_subject_elective_subject(self, service, mock_repository):
        """Test creating elective subject."""
        from edulafia.modules.academics.schemas import SubjectCreate

        mock_repository.create.return_value = make_subject_mock(
            name="French",
            code="FRE",
            is_core=False,
        )

        data = SubjectCreate(
            name="French",
            code="FRE",
            is_core=False,
        )
        result = await service.create(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.is_core == False

    async def test_get_subject_by_id(self, service, mock_repository):
        """Test retrieving subject by ID."""
        subject_id = uuid4()
        mock_repository.get_by_id.return_value = make_subject_mock(
            id=subject_id,
            name="Mathematics",
        )

        result = await service.get_by_id(
            subject_id=subject_id,
            school_id=uuid4(),
        )

        assert result is not None
        assert result.id == subject_id

    async def test_get_subject_not_found(self, service, mock_repository):
        """Test retrieving non-existent subject returns None."""
        mock_repository.get_by_id.return_value = None

        result = await service.get_by_id(
            subject_id=uuid4(),
            school_id=uuid4(),
        )

        assert result is None

    async def test_list_subjects_with_pagination(self, service, mock_repository):
        """Test listing subjects with pagination."""
        mock_repository.list.return_value = (
            [make_subject_mock(), make_subject_mock()],
            10,
        )

        result = await service.list_subjects(
            school_id=uuid4(),
            page=1,
            per_page=20,
        )

        assert len(result['items']) == 2
        assert result['total'] == 10

    async def test_update_subject_success(self, service, mock_repository):
        """Test successful subject update."""
        from edulafia.modules.academics.schemas import SubjectUpdate

        subject_id = uuid4()
        mock_repository.get_by_id.return_value = make_subject_mock(
            id=subject_id,
            name="Mathematics",
        )
        mock_repository.update.return_value = make_subject_mock(
            id=subject_id,
            name="Advanced Mathematics",
        )

        update = SubjectUpdate(name="Advanced Mathematics")
        result = await service.update(
            subject_id=subject_id,
            data=update,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.name == "Advanced Mathematics"

    async def test_archive_subject_success(self, service, mock_repository):
        """Test successful subject archival."""
        subject_id = uuid4()
        mock_repository.get_by_id.return_value = make_subject_mock(
            id=subject_id,
        )
        mock_repository.soft_delete.return_value = make_subject_mock(
            id=subject_id,
        )

        result = await service.archive(
            subject_id=subject_id,
            school_id=uuid4(),
        )

        mock_repository.soft_delete.assert_called_once()
