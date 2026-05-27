"""Guardian SQLAlchemy model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edulafia.database import Base

if TYPE_CHECKING:
    from edulafia.modules.guardians.student_guardian import StudentGuardian


class Guardian(Base):
    """Guardian model representing a parent/guardian of students."""

    __tablename__ = "guardians"

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

    # Required fields
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Optional fields
    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    whatsapp_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    occupation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    nin: Mapped[str | None] = mapped_column(
        String(11),
        nullable=True,
        unique=True,
    )

    # Portal access
    portal_access: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
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
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    students: Mapped[list[StudentGuardian]] = relationship(
        "StudentGuardian",
        back_populates="guardian",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Guardian(id={self.id}, name={self.first_name} {self.last_name})>"
