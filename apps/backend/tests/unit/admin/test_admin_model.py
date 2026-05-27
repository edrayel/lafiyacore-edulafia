"""Tests for Admin models and schemas - written BEFORE implementation (TDD)."""


import pytest


class TestSyncStatusModel:
    """Test cases for SyncStatus model."""

    def test_sync_status_model_exists(self):
        """Test that SyncStatus model class exists."""
        from edulafia.modules.admin.models import SyncStatus
        assert SyncStatus is not None

    def test_sync_status_has_required_fields(self):
        """Test that SyncStatus has all required fields."""
        from edulafia.modules.admin.models import SyncStatus
        columns = SyncStatus.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'device_id', 'sync_status',
            'pending_operations', 'retry_count', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"SyncStatus missing field: {field}"

    def test_sync_status_has_table_name(self):
        """Test that SyncStatus has correct table name."""
        from edulafia.modules.admin.models import SyncStatus
        assert SyncStatus.__tablename__ == 'sync_status'


class TestSentinelThresholdModel:
    """Test cases for SentinelThreshold model."""

    def test_sentinel_threshold_model_exists(self):
        """Test that SentinelThreshold model class exists."""
        from edulafia.modules.admin.models import SentinelThreshold
        assert SentinelThreshold is not None

    def test_sentinel_threshold_has_required_fields(self):
        """Test that SentinelThreshold has all required fields."""
        from edulafia.modules.admin.models import SentinelThreshold
        columns = SentinelThreshold.__table__.columns.keys()

        required_fields = [
            'id', 'symptom_category', 'time_window_hours', 'cluster_threshold',
            'school_threshold_percent', 'is_active', 'effective_from',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"SentinelThreshold missing field: {field}"

    def test_sentinel_threshold_has_table_name(self):
        """Test that SentinelThreshold has correct table name."""
        from edulafia.modules.admin.models import SentinelThreshold
        assert SentinelThreshold.__tablename__ == 'sentinel_thresholds'


class TestSystemUpdateModel:
    """Test cases for SystemUpdate model."""

    def test_system_update_model_exists(self):
        """Test that SystemUpdate model class exists."""
        from edulafia.modules.admin.models import SystemUpdate
        assert SystemUpdate is not None

    def test_system_update_has_required_fields(self):
        """Test that SystemUpdate has all required fields."""
        from edulafia.modules.admin.models import SystemUpdate
        columns = SystemUpdate.__table__.columns.keys()

        required_fields = [
            'id', 'version', 'release_type', 'title', 'release_notes',
            'deployment_type', 'status', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"SystemUpdate missing field: {field}"

    def test_system_update_has_table_name(self):
        """Test that SystemUpdate has correct table name."""
        from edulafia.modules.admin.models import SystemUpdate
        assert SystemUpdate.__tablename__ == 'system_updates'


class TestTrainingResourceModel:
    """Test cases for TrainingResource model."""

    def test_training_resource_model_exists(self):
        """Test that TrainingResource model class exists."""
        from edulafia.modules.admin.models import TrainingResource
        assert TrainingResource is not None

    def test_training_resource_has_required_fields(self):
        """Test that TrainingResource has all required fields."""
        from edulafia.modules.admin.models import TrainingResource
        columns = TrainingResource.__table__.columns.keys()

        required_fields = [
            'id', 'title', 'resource_type', 'category', 'language',
            'content_url', 'is_active', 'version', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"TrainingResource missing field: {field}"

    def test_training_resource_has_table_name(self):
        """Test that TrainingResource has correct table name."""
        from edulafia.modules.admin.models import TrainingResource
        assert TrainingResource.__tablename__ == 'training_resources'


class TestAdminSchemas:
    """Test cases for Admin schemas."""

    def test_school_provision_request_exists(self):
        """Test that SchoolProvisionRequest schema exists."""
        from edulafia.modules.admin.schemas import SchoolProvisionRequest
        assert SchoolProvisionRequest is not None

    def test_school_provision_request_validates_tier(self):
        """Test that SchoolProvisionRequest validates subscription tier."""
        from pydantic import ValidationError

        from edulafia.modules.admin.schemas import SchoolProvisionRequest

        with pytest.raises(ValidationError):
            SchoolProvisionRequest(
                school_name="Test School",
                school_type="private",
                state="Lagos",
                phone="08012345678",
                email="test@school.com",
                principal_name="John Doe",
                principal_email="john@school.com",
                subscription_tier="invalid",
            )

    def test_school_provision_request_validates_school_type(self):
        """Test that SchoolProvisionRequest validates school type."""
        from pydantic import ValidationError

        from edulafia.modules.admin.schemas import SchoolProvisionRequest

        with pytest.raises(ValidationError):
            SchoolProvisionRequest(
                school_name="Test School",
                school_type="invalid",
                state="Lagos",
                phone="08012345678",
                email="test@school.com",
                principal_name="John Doe",
                principal_email="john@school.com",
            )

    def test_provisioning_response_exists(self):
        """Test that ProvisioningResponse schema exists."""
        from edulafia.modules.admin.schemas import ProvisioningResponse
        assert ProvisioningResponse is not None

    def test_sentinel_threshold_create_exists(self):
        """Test that SentinelThresholdCreate schema exists."""
        from edulafia.modules.admin.schemas import SentinelThresholdCreate
        assert SentinelThresholdCreate is not None

    def test_system_update_create_validates_release_type(self):
        """Test that SystemUpdateCreate validates release type."""
        from pydantic import ValidationError

        from edulafia.modules.admin.schemas import SystemUpdateCreate

        with pytest.raises(ValidationError):
            SystemUpdateCreate(
                version="1.0.0",
                release_type="invalid",
                title="Test Update",
                release_notes="Test notes",
            )

    def test_training_resource_create_exists(self):
        """Test that TrainingResourceCreate schema exists."""
        from edulafia.modules.admin.schemas import TrainingResourceCreate
        assert TrainingResourceCreate is not None

    def test_analytics_overview_response_exists(self):
        """Test that AnalyticsOverviewResponse schema exists."""
        from edulafia.modules.admin.schemas import AnalyticsOverviewResponse
        assert AnalyticsOverviewResponse is not None
