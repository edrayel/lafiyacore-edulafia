"""Tests for SchoolProvisioningService - written BEFORE implementation (TDD)."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Needs proper DB setup")


@pytest.fixture
def mock_sync_repo():
    """Create a mock sync repository."""
    return AsyncMock()


@pytest.fixture
def mock_training_repo():
    """Create a mock training repository."""
    return AsyncMock()


@pytest.fixture
def mock_analytics_repo():
    """Create a mock analytics repository."""
    return AsyncMock()


@pytest.fixture
def provisioning_service(db_session):
    """Create SchoolProvisioningService with mocked repositories."""
    from edulafia.modules.admin.provisioning import SchoolProvisioningService
    return SchoolProvisioningService(db_session)


class TestSchoolProvisioningService:
    """Test cases for SchoolProvisioningService."""

    def test_provisioning_service_exists(self):
        """Test that SchoolProvisioningService class exists."""
        from edulafia.modules.admin.provisioning import SchoolProvisioningService
        assert SchoolProvisioningService is not None

    async def test_provision_school_success(self, provisioning_service):
        """Test successful school provisioning."""
        from edulafia.modules.admin.schemas import SchoolProvisionRequest

        data = SchoolProvisionRequest(
            school_name="Test Academy",
            school_type="private",
            state="Lagos",
            phone="08012345678",
            email="admin@testacademy.com",
            principal_name="John Doe",
            principal_email="john@testacademy.com",
            subscription_tier="standard",
        )

        with patch("edulafia.modules.admin.provisioning.AsyncSessionLocal") as mock_session:
            mock_ctx = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_ctx
            mock_ctx.add = MagicMock()
            mock_ctx.commit = AsyncMock()

            result = await provisioning_service.provision_school(data, uuid4())

        assert result.school_name == "Test Academy"
        assert result.provisioning_status == "in_progress"
        assert result.school_code is not None
        assert result.school_id != UUID(int=0)
        assert result.admin_user_id != UUID(int=0)

    def test_generate_school_code(self, provisioning_service):
        """Test school code generation."""
        code = provisioning_service._generate_school_code("Lagos", 1)

        assert code.startswith("LAG")
        assert len(code) == 11  # LAG-XXX-001 format (3+1+3+1+3=11)

    def test_generate_school_code_increments_sequence(self, provisioning_service):
        """Test school code increments sequence."""
        code1 = provisioning_service._generate_school_code("Lagos", 1)
        code2 = provisioning_service._generate_school_code("Lagos", 2)

        assert code1.endswith("001")
        assert code2.endswith("002")

    def test_generate_temp_password(self, provisioning_service):
        """Test temporary password generation."""
        password = provisioning_service._generate_temp_password()

        assert len(password) == 12
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)

    def test_create_onboarding_checklist(self, provisioning_service):
        """Test onboarding checklist creation."""
        checklist = provisioning_service._create_onboarding_checklist()

        assert len(checklist) == 8
        assert "profile_complete" in checklist
        assert "admin_first_login" in checklist
        assert "go_live" in checklist

    def test_calculate_progress_empty(self, provisioning_service):
        """Test progress calculation with empty checklist."""
        checklist = provisioning_service._create_onboarding_checklist()
        progress = provisioning_service._calculate_progress(checklist)

        assert progress == 0

    def test_calculate_progress_partial(self, provisioning_service):
        """Test progress calculation with partial completion."""
        checklist = provisioning_service._create_onboarding_checklist()
        checklist["profile_complete"]["completed"] = True
        checklist["admin_first_login"]["completed"] = True

        progress = provisioning_service._calculate_progress(checklist)

        assert progress == 25  # 2 out of 8 steps

    def test_calculate_progress_complete(self, provisioning_service):
        """Test progress calculation with full completion."""
        checklist = provisioning_service._create_onboarding_checklist()
        for step in checklist.values():
            step["completed"] = True

        progress = provisioning_service._calculate_progress(checklist)

        assert progress == 100

    async def test_get_onboarding_status(self, provisioning_service):
        """Test getting onboarding status."""
        result = await provisioning_service.get_onboarding_status(uuid4())

        assert result.provisioning_status == "in_progress"
        assert result.checklist is not None
        assert result.progress_percent == 0

    async def test_activate_school_success(self, provisioning_service):
        """Test successful school activation."""
        from edulafia.modules.admin.schemas import SchoolActivateRequest

        data = SchoolActivateRequest(confirm=True)
        result = await provisioning_service.activate_school(uuid4(), data, uuid4())

        assert result["status"] == "activated"

    async def test_activate_school_requires_confirmation(self, provisioning_service):
        """Test that activation requires confirmation."""
        from edulafia.modules.admin.schemas import SchoolActivateRequest

        data = SchoolActivateRequest(confirm=False)

        with pytest.raises(ValueError):
            await provisioning_service.activate_school(uuid4(), data, uuid4())


class TestAdminService:
    """Test cases for AdminService."""

    @pytest.fixture
    def admin_service(self):
        """Create AdminService with mocked repositories."""
        from edulafia.modules.admin.service import AdminService

        sync_status_repo = AsyncMock()
        sync_history_repo = AsyncMock()
        threshold_repo = AsyncMock()
        update_repo = AsyncMock()
        training_repo = AsyncMock()
        analytics_repo = AsyncMock()

        return AdminService(
            sync_status_repo,
            sync_history_repo,
            threshold_repo,
            update_repo,
            training_repo,
            analytics_repo,
        )

    def test_admin_service_exists(self):
        """Test that AdminService class exists."""
        from edulafia.modules.admin.service import AdminService
        assert AdminService is not None

    async def test_get_sync_dashboard(self, admin_service):
        """Test getting sync dashboard."""
        admin_service.sync_status_repo.count_by_status.return_value = {
            "synced": 100,
            "pending": 5,
            "failed": 2,
        }
        admin_service.sync_status_repo.get_schools_with_issues.return_value = []

        result = await admin_service.get_sync_dashboard()

        assert result.total_schools == 107
        assert result.synced_schools == 100
        assert result.failed_schools == 2

    async def test_list_thresholds(self, admin_service):
        """Test listing sentinel thresholds."""
        admin_service.threshold_repo.list.return_value = []

        result = await admin_service.list_thresholds(state="Lagos")

        assert len(result) == 0

    async def test_list_updates(self, admin_service):
        """Test listing system updates."""
        admin_service.update_repo.list.return_value = []

        result = await admin_service.list_updates(status="pending")

        assert len(result) == 0

    async def test_list_training_resources(self, admin_service):
        """Test listing training resources."""
        admin_service.training_repo.list.return_value = []

        result = await admin_service.list_training_resources(category="onboarding")

        assert len(result) == 0

    async def test_get_analytics_overview(self, admin_service):
        """Test getting analytics overview."""
        admin_service.analytics_repo.aggregate_platform_metrics.return_value = {"total": 500}
        admin_service.sync_status_repo.count_by_status.return_value = {"synced": 10, "pending": 2}

        result = await admin_service.get_analytics_overview()

        assert result.total_schools == 12
        assert result.active_schools == 10
        assert result.total_students == 500
