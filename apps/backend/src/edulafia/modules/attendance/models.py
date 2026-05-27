"""Attendance SQLAlchemy models."""

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


class AttendanceRecord(Base):
    """Attendance record model for tracking student attendance."""

    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint(
            "student_id", "date", "deleted_at",
            name="uq_attendance_student_date"
        ),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id"),
        nullable=False,
        index=True,
    )
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Attendance fields
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    period: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="present, absent, late, excused",
    )
    reason_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="sick, family, unknown, excused, suspended",
    )
    symptom_codes: Mapped[list | None] = mapped_column(
        ARRAY(String),
        nullable=True,
        comment="Array of symptom codes for sick absences",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Recording info
    recorded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Edit tracking
    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    edited_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    edit_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Offline sync
    device_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    sync_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="synced",
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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<AttendanceRecord(id={self.id}, student_id={self.student_id}, date={self.date}, status={self.status})>"


class AttendancePattern(Base):
    """Attendance pattern model for tracking attendance patterns."""

    __tablename__ = "attendance_patterns"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id"),
        nullable=False,
    )
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Pattern fields
    pattern_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="chronic_absence, same_day_absence, illness_cluster",
    )
    pattern_details: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="low, medium, high, critical",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        comment="active, acknowledged, resolved, false_positive",
    )

    # Resolution
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    resolved_by: Mapped[uuid.UUID | None] = mapped_column(
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
        return f"<AttendancePattern(id={self.id}, type={self.pattern_type}, severity={self.severity})>"


class AttendanceNotification(Base):
    """Attendance notification model for tracking guardian notifications."""

    __tablename__ = "attendance_notifications"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    guardian_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guardians.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Notification fields
    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="daily_absence, consecutive_absence, weekly_summary",
    )
    channel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="whatsapp, sms, both",
    )
    message_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending, sent, delivered, failed",
    )

    # Delivery tracking
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    retry_count: Mapped[int] = mapped_column(
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<AttendanceNotification(id={self.id}, type={self.notification_type}, status={self.status})>"


class AttendanceConfiguration(Base):
    """Attendance configuration model for school attendance settings."""

    __tablename__ = "attendance_configurations"

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
        unique=True,
    )

    # Configuration fields
    marking_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="dropdown",
        comment="dropdown, swipe, qr_code",
    )
    require_reason_for_absence: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    require_symptoms_for_sick: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    edit_window_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=24,
    )
    notification_delay_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=30,
    )
    consecutive_absence_alert_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )
    chronic_absence_threshold_percent: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=20.0,
    )
    notification_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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
        return f"<AttendanceConfiguration(school_id={self.school_id})>"
