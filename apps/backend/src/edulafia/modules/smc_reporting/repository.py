from __future__ import annotations
"""SMC reporting repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.smc_reporting.models import SMCReport


class SMCReportRepository:
    """Repository for SMC report database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SMCReport:
        """Create a new SMC report."""
        report = SMCReport(**data)
        self.db.add(report)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def get_by_id(self, report_id: UUID) -> SMCReport | None:
        """Get an SMC report by ID."""
        stmt = select(SMCReport).where(SMCReport.id == report_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[SMCReport]:
        """List all SMC reports for a school."""
        stmt = select(SMCReport).where(
            SMCReport.school_id == school_id
        ).order_by(SMCReport.report_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, report: SMCReport, data: dict) -> SMCReport:
        """Update an SMC report."""
        for key, value in data.items():
            if value is not None:
                setattr(report, key, value)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def delete(self, report: SMCReport) -> None:
        """Delete an SMC report."""
        await self.db.delete(report)
        await self.db.flush()
