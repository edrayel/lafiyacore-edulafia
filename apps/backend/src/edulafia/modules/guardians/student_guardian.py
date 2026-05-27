"""Student-Guardian relationship model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edulafia.database import Base

if TYPE_CHECKING:
    from edulafia.modules.guardians.models import Guardian
    from edulafia.modules.students.models import Student


class StudentGuardian(Base):
    """Association model linking students to guardians."""

    __tablename__ = "student_guardians"

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

    # Relationship details
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    is_emergency_contact: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    can_pickup: Mapped[bool] = mapped_column(
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

    # Relationships
    student: Mapped[Student] = relationship(
        "Student",
        back_populates="guardians",
    )
    guardian: Mapped[Guardian] = relationship(
        "Guardian",
        back_populates="students",
    )

    def __repr__(self) -> str:
        return f"<StudentGuardian(student_id={self.student_id}, guardian_id={self.guardian_id})>"
