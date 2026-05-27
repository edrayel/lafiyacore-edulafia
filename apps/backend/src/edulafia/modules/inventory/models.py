"""Inventory SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class Asset(Base):
    """Asset model for tracking school inventory."""

    __tablename__ = "assets"

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
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    unit_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    condition: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="new",
    )
    assigned_to: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    purchase_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    depreciation_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
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
        return f"<Asset(id={self.id}, name={self.name}, category={self.category})>"
