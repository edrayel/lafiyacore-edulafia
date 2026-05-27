"""Administration Pydantic schemas."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

# School Provisioning Schemas

class SchoolProvisionRequest(BaseModel):
    """Schema for provisioning a new school."""

    school_name: str = Field(..., min_length=1, max_length=255)
    school_type: str = Field(..., description="public, private, government")
    address: str | None = None
    state: str = Field(..., min_length=1, max_length=100)
    lga: str | None = Field(None, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    email: str = Field(..., min_length=1, max_length=255)
    principal_name: str = Field(..., min_length=1, max_length=255)
    principal_phone: str | None = None
    principal_email: str = Field(..., min_length=1, max_length=255)
    subscription_tier: str = Field(default="standard")
    modules: list[str] = Field(default=[])
    start_trial: bool = False

    @field_validator("subscription_tier")
    @classmethod
    def validate_tier(cls, v: str) -> str:
        """Validate subscription tier."""
        valid_tiers = ["starter", "standard", "premium"]
        if v.lower() not in valid_tiers:
            raise ValueError(f"Tier must be one of: {', '.join(valid_tiers)}")
        return v.lower()

    @field_validator("school_type")
    @classmethod
    def validate_school_type(cls, v: str) -> str:
        """Validate school type."""
        valid_types = ["public", "private", "government"]
        if v.lower() not in valid_types:
            raise ValueError(f"School type must be one of: {', '.join(valid_types)}")
        return v.lower()


class ProvisioningResponse(BaseModel):
    """Schema for provisioning response."""

    school_id: UUID
    school_code: str
    school_name: str
    provisioning_status: str
    admin_user_id: UUID
    admin_email: str
    temp_password_sent: bool
    onboarding_url: str
    created_at: datetime


class OnboardingStatusResponse(BaseModel):
    """Schema for onboarding status response."""

    school_id: UUID
    school_code: str
    provisioning_status: str
    checklist: dict
    progress_percent: int
    training_progress: dict
    activated_at: datetime | None = None


class SchoolActivateRequest(BaseModel):
    """Schema for activating a school."""

    confirm: bool = Field(..., description="Must be true to activate")
    notes: str | None = None


# User Management Schemas

class UserCreateRequest(BaseModel):
    """Schema for creating a user."""

    email: str = Field(..., min_length=1, max_length=255)
    phone: str | None = Field(None, min_length=10, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., description="school_admin, teacher, nurse, bursar, etc.")
    send_welcome_email: bool = True

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role."""
        valid_roles = [
            "super_admin", "school_admin", "teacher", "nurse",
            "bursar", "accountant", "librarian", "parent"
        ]
        if v.lower() not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
        return v.lower()


class UserResponse(BaseModel):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    phone: str | None = None
    first_name: str
    last_name: str
    role: str
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(BaseModel):
    """Schema for updating a user."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    phone: str | None = Field(None, min_length=10, max_length=20)
    role: str | None = None  # Only super_admin can update role


class PasswordResetRequest(BaseModel):
    """Schema for password reset."""

    send_notification: bool = True


class UserDeactivateRequest(BaseModel):
    """Schema for deactivating a user."""

    reason: str = Field(..., min_length=1, max_length=500)


# Sync Monitoring Schemas

class SyncStatusResponse(BaseModel):
    """Schema for sync status response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    device_id: str
    device_info: dict | None = None
    last_sync_at: datetime | None = None
    sync_status: str
    pending_operations: int
    sync_duration_ms: int | None = None
    data_size_bytes: int | None = None
    error_message: str | None = None
    retry_count: int
    created_at: datetime
    updated_at: datetime


class SyncDashboardResponse(BaseModel):
    """Schema for sync dashboard response."""

    total_schools: int
    synced_schools: int
    pending_schools: int
    failed_schools: int
    conflict_schools: int
    total_devices: int
    total_pending_operations: int
    schools_with_issues: list[dict]
    last_updated: datetime


class SyncHistoryResponse(BaseModel):
    """Schema for sync history response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    device_id: str
    sync_start: datetime
    sync_end: datetime | None = None
    status: str
    operations_sent: int
    operations_received: int
    conflicts_detected: int
    conflicts_resolved: int
    data_size_bytes: int
    created_at: datetime


# Sentinel Configuration Schemas

class SentinelThresholdCreate(BaseModel):
    """Schema for creating sentinel threshold."""

    state: str | None = None
    lga: str | None = None
    symptom_category: str = Field(..., min_length=1)
    time_window_hours: int = Field(default=48, ge=1, le=168)
    cluster_threshold: int = Field(default=3, ge=1)
    school_threshold_percent: Decimal = Field(default=10, ge=0, le=100)
    lga_threshold_percent: Decimal | None = Field(None, ge=0, le=100)
    baseline_illness_rate: Decimal | None = None
    effective_from: date = Field(default_factory=date.today)
    change_reason: str = Field(..., min_length=1)


class SentinelThresholdResponse(BaseModel):
    """Schema for sentinel threshold response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    state: str | None = None
    lga: str | None = None
    symptom_category: str
    time_window_hours: int
    cluster_threshold: int
    school_threshold_percent: Decimal
    lga_threshold_percent: Decimal | None = None
    baseline_illness_rate: Decimal | None = None
    is_active: bool
    effective_from: date
    change_reason: str | None = None
    created_at: datetime
    updated_at: datetime


# System Update Schemas

class SystemUpdateCreate(BaseModel):
    """Schema for creating system update."""

    version: str = Field(..., min_length=1, max_length=50)
    release_type: str = Field(..., description="major, minor, patch, hotfix")
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    release_notes: str = Field(..., min_length=1)
    deployment_type: str = Field(default="global")
    target_schools: list[UUID] | None = None
    target_states: list[str] | None = None
    scheduled_for: datetime | None = None

    @field_validator("release_type")
    @classmethod
    def validate_release_type(cls, v: str) -> str:
        """Validate release type."""
        valid_types = ["major", "minor", "patch", "hotfix"]
        if v.lower() not in valid_types:
            raise ValueError(f"Release type must be one of: {', '.join(valid_types)}")
        return v.lower()


class SystemUpdateResponse(BaseModel):
    """Schema for system update response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    version: str
    release_type: str
    title: str
    description: str | None = None
    release_notes: str
    deployment_type: str
    status: str
    scheduled_for: datetime | None = None
    deployed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


# Training Resource Schemas

class TrainingResourceCreate(BaseModel):
    """Schema for creating training resource."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    resource_type: str = Field(..., description="video, guide, document, interactive")
    category: str = Field(..., description="onboarding, module_specific, advanced, troubleshooting")
    target_role: str | None = None
    target_module: str | None = None
    language: str = Field(default="en")
    content_url: str = Field(..., min_length=1, max_length=500)
    duration_minutes: int | None = Field(None, ge=0)

    @field_validator("resource_type")
    @classmethod
    def validate_resource_type(cls, v: str) -> str:
        """Validate resource type."""
        valid_types = ["video", "guide", "document", "interactive"]
        if v.lower() not in valid_types:
            raise ValueError(f"Resource type must be one of: {', '.join(valid_types)}")
        return v.lower()


class TrainingResourceResponse(BaseModel):
    """Schema for training resource response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None = None
    resource_type: str
    category: str
    target_role: str | None = None
    target_module: str | None = None
    language: str
    content_url: str
    duration_minutes: int | None = None
    is_active: bool
    version: str
    created_at: datetime
    updated_at: datetime


class TrainingAssignmentRequest(BaseModel):
    """Schema for assigning training to school."""

    school_id: UUID
    resource_ids: list[UUID] = Field(..., min_length=1)
    due_date: date | None = None


# Analytics Schemas

class AnalyticsOverviewResponse(BaseModel):
    """Schema for analytics overview response."""

    total_schools: int
    active_schools: int
    inactive_schools: int
    total_users: int
    total_students: int
    active_schools_percent: float
    module_adoption: dict
    geographic_distribution: dict
    last_updated: datetime


class SchoolAnalyticsResponse(BaseModel):
    """Schema for school analytics response."""

    school_id: UUID
    school_name: str
    module_engagement: dict
    feature_adoption: dict
    user_activity: dict
    data_completeness: dict
    last_updated: datetime


class FilterParams(BaseModel):
    """Schema for common filter parameters."""

    start_date: date | None = None
    end_date: date | None = None
    state: str | None = None
    lga: str | None = None
    status: str | None = None
    page: int = 1
    per_page: int = 50
