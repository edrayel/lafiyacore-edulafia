"""Health SQLAlchemy models."""

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
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.core.encryption import EncryptedJSON, EncryptedString
from edulafia.database import Base


class StudentHealthProfile(Base):
    """Student health profile model for storing health information."""

    __tablename__ = "student_health_profiles"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_student_health_profile"),
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
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Basic health info
    blood_group: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )
    genotype: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )

    # Health conditions
    chronic_conditions: Mapped[list | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
    )
    allergies: Mapped[list | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
    )
    current_medications: Mapped[list | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
    )
    disability_status: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )

    # Emergency info
    emergency_notes: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )
    family_health_history: Mapped[dict | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
    )

    # Screening data
    vision_left: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )
    vision_right: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )
    hearing_left: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    hearing_right: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Consent
    parental_consent_given: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    consent_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Version tracking
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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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

    def __repr__(self) -> str:
        return f"<StudentHealthProfile(student_id={self.student_id})>"


class SickBayVisit(Base):
    """Sick bay visit model for recording student health visits."""

    __tablename__ = "sick_bay_visits"

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
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Visit details
    visit_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    visit_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    presenting_complaint_codes: Mapped[list] = mapped_column(
        EncryptedJSON,
        nullable=False,
    )
    presenting_complaint_notes: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )

    # Vital signs
    temperature: Mapped[float | None] = mapped_column(
        Numeric(4, 1),
        nullable=True,
    )
    blood_pressure_systolic: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    blood_pressure_diastolic: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    pulse_rate: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Treatment
    treatment_given: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )
    outcome: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="returned_to_class, sent_home, referred, hospitalized",
    )
    referred_to: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Parent notification
    parent_notified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    parent_notified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Sentinel flags
    is_sentinel_relevant: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Recording
    recorded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
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
        return f"<SickBayVisit(student_id={self.student_id}, date={self.visit_date})>"


class HealthScreening(Base):
    """Health screening model for annual health checks."""

    __tablename__ = "health_screenings"

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
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    term_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("terms.id"),
        nullable=True,
    )

    # Screening details
    screening_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    screening_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="annual, pre_sports, special",
    )

    # Anthropometric measurements
    height: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )
    weight: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )
    bmi: Mapped[float | None] = mapped_column(
        Numeric(4, 1),
        nullable=True,
    )
    muac: Mapped[float | None] = mapped_column(
        Numeric(4, 1),
        nullable=True,
    )

    # Vision
    vision_left: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )
    vision_right: Mapped[float | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )

    # Hearing
    hearing_left: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    hearing_right: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Other
    blood_pressure_systolic: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    blood_pressure_diastolic: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    dental_notes: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )
    sickle_cell_test_result: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )

    # Mental Health
    phq_a_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    sdq_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Flags
    flags: Mapped[list | None] = mapped_column(
        EncryptedJSON,
        nullable=True,
    )
    follow_up_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    follow_up_notes: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )

    # Recording
    conducted_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Version tracking
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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<HealthScreening(student_id={self.student_id}, type={self.screening_type})>"


class Referral(Base):
    """Referral model for tracking health referrals."""

    __tablename__ = "referrals"

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
    sick_bay_visit_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sick_bay_visits.id"),
        nullable=True,
    )
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Referral details
    referral_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    destination_facility: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(
        EncryptedString,
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="normal",
        comment="urgent, normal, follow_up",
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="pending, sent, acknowledged, attended, completed",
    )

    # Follow-up
    follow_up_due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    outcome_notes: Mapped[str | None] = mapped_column(
        EncryptedString,
        nullable=True,
    )
    outcome_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Tracking
    reminder_sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    reminder_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Recording
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
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
        return f"<Referral(student_id={self.student_id}, facility={self.destination_facility})>"


class VaccinationRecord(Base):
    """Vaccination record model for tracking student vaccinations."""

    __tablename__ = "vaccination_records"

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
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Vaccination details
    vaccine_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    vaccine_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    dose_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    administration_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    lot_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    administering_facility: Mapped[str | None] = mapped_column(
        String(255),
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

    def __repr__(self) -> str:
        return f"<VaccinationRecord(student_id={self.student_id}, vaccine={self.vaccine_name})>"


class SentinelSignal(Base):
    """Sentinel signal model for disease surveillance."""

    __tablename__ = "sentinel_signals"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Location
    school_ids: Mapped[list] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        nullable=False,
    )
    lga: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Signal details
    date_generated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    symptom_profile: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    students_affected: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    threshold_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="class_cluster, school_cluster, lga_cluster",
    )
    alert_tier: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="school, lga, state",
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        comment="active, acknowledged, resolved, false_positive",
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    acknowledged_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    resolved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    response_notes: Mapped[str | None] = mapped_column(
        Text,
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
        return f"<SentinelSignal(id={self.id}, tier={self.alert_tier}, status={self.status})>"


class SentinelConfiguration(Base):
    """Sentinel configuration model for threshold settings."""

    __tablename__ = "sentinel_configurations"

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
    )
    lga: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    school_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id"),
        nullable=True,
    )

    # Configuration
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
    baseline_illness_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )
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
        return f"<SentinelConfiguration(category={self.symptom_category})>"
