"""Payroll SQLAlchemy models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from edulafia.database import Base


class PayrollRun(Base):
    """Payroll run model for tracking monthly payroll processing."""

    __tablename__ = "payroll_runs"

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
    month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    total_gross: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    total_deductions: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    total_net: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        index=True,
    )
    run_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
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
        return f"<PayrollRun(id={self.id}, month={self.month}, year={self.year}, status={self.status})>"


class PayrollEntry(Base):
    """Payroll entry model for individual staff payroll."""

    __tablename__ = "payroll_entries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    payroll_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("payroll_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.id"),
        nullable=False,
        index=True,
    )
    gross_pay: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    tax: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    pension: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    nhf: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    other_deductions: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    net_pay: Mapped[float] = mapped_column(
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
        return f"<PayrollEntry(id={self.id}, staff_id={self.staff_id}, net_pay={self.net_pay})>"
