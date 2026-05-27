"""Girl child tracking SQLAlchemy models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class GirlChildRecord(Base):
    """Girl child tracking record model."""

    __tablename__ = "girl_child_records"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_girl_child_student"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    enrollment_source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    risk_factors: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    interventions: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    attendance_trend: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    dropout_risk: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="low",
        index=True,
    )
    counselor_notes: Mapped[str | None] = mapped_column(
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
        return f"<GirlChildRecord(id={self.id}, student_id={self.student_id}, dropout_risk={self.dropout_risk})>"
