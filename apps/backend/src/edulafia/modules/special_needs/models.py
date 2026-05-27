"""Special needs / IEP SQLAlchemy models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class IndividualEducationPlan(Base):
    __tablename__ = "individual_education_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    disability_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="visual, hearing, mobility, cognitive, autism, other")
    diagnosis_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    diagnosed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    goals: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Array of goal objects")
    accommodations: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    support_staff: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft", index=True)
    review_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<IEP(id={self.id}, student_id={self.student_id}, status={self.status})>"
