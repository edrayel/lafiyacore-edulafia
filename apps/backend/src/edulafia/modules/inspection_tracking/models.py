"""Inspection tracking SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class SchoolInspection(Base):
    """School inspection model for tracking ministry inspections."""

    __tablename__ = "school_inspections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    inspector_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    ministry: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    inspection_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    findings: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    recommendations: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    compliance_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="compliant",
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
        return f"<SchoolInspection(id={self.id}, school_id={self.school_id}, status={self.status})>"
