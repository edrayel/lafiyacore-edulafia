"""Alumni SQLAlchemy models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class AlumniProfile(Base):
    """Alumni profile model for tracking past students."""

    __tablename__ = "alumni_profiles"

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
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )
    graduation_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    current_occupation: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    university: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    contact_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
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
        return f"<AlumniProfile(id={self.id}, student_id={self.student_id}, year={self.graduation_year})>"
