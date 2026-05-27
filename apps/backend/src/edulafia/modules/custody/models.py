"""Custody SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class CustodyOrder(Base):
    """Custody order model for tracking legal custody arrangements."""

    __tablename__ = "custody_orders"

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
    custodial_guardian_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("student_guardians.id"),
        nullable=False,
        index=True,
    )
    non_custodial_guardian_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("student_guardians.id"),
        nullable=True,
    )

    court_order_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    court_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    restrictions: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        index=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
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
        return f"<CustodyOrder(id={self.id}, student_id={self.student_id}, status={self.status})>"
