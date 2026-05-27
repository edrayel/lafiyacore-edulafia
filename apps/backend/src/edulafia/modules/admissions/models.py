"""Admission SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class Application(Base):
    """Application model representing an admission application."""

    __tablename__ = "applications"

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

    # Applicant personal details
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
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    gender: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    nationality: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Nigerian",
    )
    state_of_origin: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    lga_of_origin: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Academic details
    previous_school: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    class_applied_for: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    admission_year: Mapped[int] = mapped_column(
        nullable=False,
    )

    # Parent/Guardian details
    parent_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    parent_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    parent_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Status and evaluation
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )
    exam_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    interview_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    interview_notes: Mapped[str | None] = mapped_column(
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

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Audit fields
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Application(id={self.id}, name={self.first_name} {self.last_name}, status={self.status})>"
