from __future__ import annotations
"""Payroll repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.payroll.models import PayrollEntry, PayrollRun


class PayrollRunRepository:
    """Repository for payroll run database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> PayrollRun:
        """Create a new payroll run."""
        run = PayrollRun(**data)
        self.db.add(run)
        await self.db.flush()
        await self.db.refresh(run)
        return run

    async def get_by_id(self, run_id: UUID) -> PayrollRun | None:
        """Get a payroll run by ID."""
        stmt = select(PayrollRun).where(PayrollRun.id == run_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, run_id: UUID, school_id: UUID) -> PayrollRun | None:
        """Get a payroll run by ID scoped to school."""
        stmt = select(PayrollRun).where(
            PayrollRun.id == run_id,
            PayrollRun.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_school_month_year(self, school_id: UUID, month: int, year: int) -> PayrollRun | None:
        """Get a payroll run by school, month, and year."""
        stmt = select(PayrollRun).where(
            PayrollRun.school_id == school_id,
            PayrollRun.month == month,
            PayrollRun.year == year,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[PayrollRun]:
        """List all payroll runs for a school."""
        stmt = select(PayrollRun).where(
            PayrollRun.school_id == school_id
        ).order_by(PayrollRun.year.desc(), PayrollRun.month.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, run: PayrollRun, data: dict) -> PayrollRun:
        """Update a payroll run."""
        for key, value in data.items():
            if value is not None:
                setattr(run, key, value)
        await self.db.flush()
        await self.db.refresh(run)
        return run

    async def delete(self, run: PayrollRun) -> None:
        """Delete a payroll run."""
        await self.db.delete(run)
        await self.db.flush()


class PayrollEntryRepository:
    """Repository for payroll entry database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> PayrollEntry:
        """Create a new payroll entry."""
        entry = PayrollEntry(**data)
        self.db.add(entry)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def get_by_id_and_school(self, entry_id: UUID, school_id: UUID) -> PayrollEntry | None:
        """Get a payroll entry by ID and school_id."""
        stmt = select(PayrollEntry).join(PayrollRun).where(
            PayrollEntry.id == entry_id,
            PayrollRun.school_id == school_id,
            PayrollEntry.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, entry_id: UUID) -> PayrollEntry | None:
        """Get a payroll entry by ID."""
        stmt = select(PayrollEntry).where(PayrollEntry.id == entry_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_payroll_run(self, payroll_run_id: UUID) -> Sequence[PayrollEntry]:
        """List all entries for a payroll run."""
        stmt = select(PayrollEntry).where(
            PayrollEntry.payroll_run_id == payroll_run_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, entry: PayrollEntry, data: dict) -> PayrollEntry:
        """Update a payroll entry."""
        for key, value in data.items():
            if value is not None:
                setattr(entry, key, value)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def delete(self, entry: PayrollEntry) -> None:
        """Delete a payroll entry."""
        await self.db.delete(entry)
        await self.db.flush()
