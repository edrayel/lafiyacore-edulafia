"""Intelligence & Analytics SQLAlchemy models."""

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
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class KPIDefinition(Base):
    """KPI definition model."""

    __tablename__ = "kpi_definitions"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # KPI details
    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    unit: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    source_module: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Thresholds
    critical_threshold: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    warning_threshold: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    target_threshold: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    higher_is_better: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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
        return f"<KPIDefinition(code={self.code}, name={self.name})>"


class SchoolKPISnapshot(Base):
    """School KPI snapshot model for daily KPI values."""

    __tablename__ = "school_kpi_snapshots"
    __table_args__ = (
        UniqueConstraint("school_id", "kpi_id", "snapshot_date", name="uq_school_kpi_snapshot"),
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
    kpi_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("kpi_definitions.id"),
        nullable=False,
    )

    # Snapshot data
    snapshot_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    value: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )
    previous_value: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )
    trend: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="up, down, stable",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="critical, warning, normal",
    )

    # Metadata
    calculation_metadata: Mapped[dict | None] = mapped_column(
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
        return f"<SchoolKPISnapshot(school_id={self.school_id}, kpi_id={self.kpi_id}, value={self.value})>"


class LGAAggregate(Base):
    """LGA aggregate model for LGA-level metrics."""

    __tablename__ = "lga_aggregates"
    __table_args__ = (
        UniqueConstraint("lga", "state", "aggregate_date", name="uq_lga_aggregate"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Location
    lga: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # Aggregate data
    aggregate_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    aggregate_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="daily",
    )

    # Metrics
    total_schools: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    total_students: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    avg_attendance_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )
    total_sick_bay_visits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    total_collections: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0,
    )
    open_alerts_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<LGAAggregate(lga={self.lga}, date={self.aggregate_date})>"


class StateAggregate(Base):
    """State aggregate model for state-level metrics."""

    __tablename__ = "state_aggregates"
    __table_args__ = (
        UniqueConstraint("state", "aggregate_date", name="uq_state_aggregate"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Location
    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # Aggregate data
    aggregate_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    aggregate_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="daily",
    )

    # Metrics
    total_lgas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    total_schools: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    total_students: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    avg_attendance_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )
    total_sick_bay_visits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    total_collections: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0,
    )
    open_alerts_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<StateAggregate(state={self.state}, date={self.aggregate_date})>"


class ResearchDataRequest(Base):
    """Research data request model."""

    __tablename__ = "research_data_requests"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Requester
    researcher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Request details
    request_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    research_purpose: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    data_categories: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )
    date_range_start: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    date_range_end: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    geographic_scope: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Ethics
    ethics_approval_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    ethics_approval_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    institution: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending, approved, rejected, fulfilled",
    )

    # Review
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    review_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Data delivery
    data_file_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    data_file_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    download_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    max_downloads: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
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
        return f"<ResearchDataRequest(id={self.id}, title={self.request_title}, status={self.status})>"


class ReportTemplate(Base):
    """Report template model."""

    __tablename__ = "report_templates"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key
    school_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id"),
        nullable=True,
    )

    # Template details
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    report_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    layout: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
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
        return f"<ReportTemplate(id={self.id}, name={self.name})>"


class GeneratedReport(Base):
    """Generated report model."""

    __tablename__ = "generated_reports"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("report_templates.id"),
        nullable=True,
    )
    generated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Report details
    report_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    parameters: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending, generating, completed, failed",
    )

    # File
    file_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    file_format: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )
    file_size_bytes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Progress
    progress_percent: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<GeneratedReport(id={self.id}, type={self.report_type}, status={self.status})>"
