"""Staff SQLAlchemy models."""

import uuid
from datetime import date, datetime, time

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edulafia.core.encryption import EncryptedJSON, EncryptedString
from edulafia.database import Base


class Staff(Base):
    """Staff model for managing school staff members."""

    __tablename__ = "staff"
    __table_args__ = (
        UniqueConstraint("school_id", "staff_id", name="uq_staff_school_staff_id"),
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
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Staff identification
    staff_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Personal info
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    whatsapp_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    gender: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Employment details
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="teacher, nurse, bursar, admin, accountant, librarian, lab_attendant, security, cleaner, other",
    )
    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    qualifications: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    documents: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Dictionary of document URLs, e.g. {'cv': 'url', 'credentials': 'url'}",
    )
    subjects: Mapped[list | None] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True,
    )
    employment_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="permanent",
        comment="permanent, contract, nysc, intern",
    )
    employment_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    exit_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    exit_reason: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Financial
    salary: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    bank_details: Mapped[dict | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
        comment="Encrypted",
    )

    # Emergency contacts
    next_of_kin: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    emergency_contact: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        comment="active, inactive, on_leave, terminated, retired",
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Staff(id={self.id}, name={self.first_name} {self.last_name}, role={self.role})>"


class StaffAssignment(Base):
    """Staff class assignment model."""

    __tablename__ = "staff_class_assignments"
    __table_args__ = (
        UniqueConstraint(
            "staff_id", "class_id", "subject_id", "academic_year_id",
            name="uq_staff_class_subject_year"
        ),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subject_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        nullable=True,
    )
    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_years.id"),
        nullable=False,
    )
    term_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("terms.id"),
        nullable=True,
    )

    # Assignment details
    assignment_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="regular",
        comment="regular, substitute, temporary",
    )
    is_form_teacher: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<StaffAssignment(staff_id={self.staff_id}, class_id={self.class_id})>"


class Timetable(Base):
    """Timetable model."""

    __tablename__ = "timetables"
    __table_args__ = (
        UniqueConstraint(
            "class_id", "academic_year_id", "term_id", "version_number",
            name="uq_timetable_class_year_term_version"
        ),
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
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_years.id"),
        nullable=False,
    )
    term_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("terms.id"),
        nullable=False,
    )

    # Timetable details
    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    published_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    is_draft: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<Timetable(id={self.id}, class_id={self.class_id}, version={self.version_number})>"


class TimetableEntry(Base):
    """Timetable entry model."""

    __tablename__ = "timetable_entries"
    __table_args__ = (
        UniqueConstraint(
            "timetable_id", "day_of_week", "period_number",
            name="uq_timetable_entry_period"
        ),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key
    timetable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("timetables.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Entry details
    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="1=Monday, 7=Sunday",
    )
    period_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        nullable=False,
    )
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.id"),
        nullable=False,
        index=True,
    )
    room_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    is_break: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<TimetableEntry(day={self.day_of_week}, period={self.period_number})>"


class TeacherAttendance(Base):
    """Teacher attendance model."""

    __tablename__ = "teacher_attendance"
    __table_args__ = (
        UniqueConstraint("staff_id", "date", name="uq_teacher_attendance_staff_date"),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Attendance details
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    check_in_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    check_out_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="present, absent, late, excused, on_leave",
    )
    check_in_method: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="manual, qr_code, geofencing",
    )
    late_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    early_departure_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    reason_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Recording
    recorded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<TeacherAttendance(staff_id={self.staff_id}, date={self.date}, status={self.status})>"


class StaffCommunication(Base):
    """Staff communication model."""

    __tablename__ = "staff_communications"

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
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Communication details
    communication_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="announcement, broadcast, message, meeting",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    target_audience: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    channels: Mapped[list] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=["in_app"],
    )
    requires_acknowledgement: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="normal",
        comment="low, normal, high, urgent",
    )
    scheduled_for: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<StaffCommunication(id={self.id}, title={self.title})>"


class CommunicationRecipient(Base):
    """Communication recipient model."""

    __tablename__ = "communication_recipients"
    __table_args__ = (
        UniqueConstraint(
            "communication_id", "staff_id",
            name="uq_communication_recipient"
        ),
    )

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign keys
    communication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff_communications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="sent",
        comment="sent, delivered, read, acknowledged",
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Version
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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
        return f"<CommunicationRecipient(communication_id={self.communication_id}, staff_id={self.staff_id})>"
