"""Discipline SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class DisciplineRecord(Base):
    """Discipline record model for tracking student behavior incidents."""

    __tablename__ = "discipline_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    offense_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    action_taken: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    reported_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    parent_notified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    follow_up_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="open",
        index=True,
    )

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
        return f"<DisciplineRecord(id={self.id}, student_id={self.student_id}, offense={self.offense_type}, status={self.status})>"
