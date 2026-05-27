"""Administration SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class School(Base):
    """School model for multi-tenant provisioning."""

    __tablename__ = "schools"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lga: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<School(id={self.id}, name={self.name}, code={self.code})>"


class SyncStatus(Base):
    """Sync status model for monitoring device sync."""

    __tablename__ = "sync_status"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Device info
    device_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    device_info: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Sync status
    last_sync_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    sync_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="unknown",
        comment="synced, pending, failed, conflict",
    )
    pending_operations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Performance metrics
    sync_duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    data_size_bytes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Error handling
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SyncStatus(school_id={self.school_id}, device={self.device_id}, status={self.sync_status})>"


class SyncHistory(Base):
    """Sync history model for audit trail."""

    __tablename__ = "sync_history"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Device info
    device_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Sync details
    sync_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    sync_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="started, completed, failed, partial",
    )

    # Metrics
    operations_sent: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    operations_received: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    conflicts_detected: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    conflicts_resolved: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    data_size_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Error details
    error_details: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SyncHistory(school_id={self.school_id}, status={self.status})>"


class SentinelThreshold(Base):
    """Sentinel threshold configuration model."""

    __tablename__ = "sentinel_thresholds"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Location
    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    lga: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Threshold config
    symptom_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    time_window_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=48,
    )
    cluster_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )
    school_threshold_percent: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=10.0,
    )
    lga_threshold_percent: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        default=5.0,
    )
    baseline_illness_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Audit
    change_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SentinelThreshold(id={self.id}, category={self.symptom_category})>"


class SystemUpdate(Base):
    """System update model."""

    __tablename__ = "system_updates"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Update details
    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    release_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="major, minor, patch, hotfix",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    release_notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Deployment
    deployment_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="global",
        comment="global, school_specific, regional",
    )
    target_schools: Mapped[list | None] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True,
    )
    target_states: Mapped[list | None] = mapped_column(
        ARRAY(String),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending, staging, deploying, deployed, rolled_back",
    )

    # Timing
    scheduled_for: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deployed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    rolled_back_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Audit
    deployed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    rollback_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SystemUpdate(version={self.version}, status={self.status})>"


class TrainingResource(Base):
    """Training resource model."""

    __tablename__ = "training_resources"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Resource details
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="video, guide, document, interactive",
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="onboarding, module_specific, advanced, troubleshooting",
    )

    # Targeting
    target_role: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    target_module: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="en",
        comment="en, ig, ha",
    )

    # Content
    content_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    file_size_bytes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="1.0",
    )

    # Audit
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<TrainingResource(id={self.id}, title={self.title})>"


class SchoolTrainingAssignment(Base):
    """School training assignment model."""

    __tablename__ = "school_training_assignments"
    __table_args__ = (
        UniqueConstraint("school_id", "resource_id", name="uq_school_training_assignment"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("training_resources.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Assignment details
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="assigned",
        comment="assigned, in_progress, completed, overdue",
    )

    # Completion
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SchoolTrainingAssignment(school_id={self.school_id}, resource_id={self.resource_id})>"


class UsageAnalytics(Base):
    """Usage analytics model."""

    __tablename__ = "usage_analytics"
    __table_args__ = (
        UniqueConstraint("school_id", "metric_date", "metric_name", name="uq_usage_analytics"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Analytics
    metric_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    metric_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    metric_value: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )
    analytics_metadata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<UsageAnalytics(school_id={self.school_id}, metric={self.metric_name}, value={self.metric_value})>"
