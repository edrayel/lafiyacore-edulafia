from __future__ import annotations
"""Ministry reporting repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.ministry_reporting.models import MinistryReport


class MinistryReportRepository:
    """Repository for ministry report database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> MinistryReport:
        """Create a new ministry report."""
        report = MinistryReport(**data)
        self.db.add(report)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def get_by_id(self, report_id: UUID) -> MinistryReport | None:
        """Get a ministry report by ID."""
        stmt = select(MinistryReport).where(MinistryReport.id == report_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[MinistryReport]:
        """List all ministry reports for a school."""
        stmt = select(MinistryReport).where(
            MinistryReport.school_id == school_id
        ).order_by(MinistryReport.period_start.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_type(self, school_id: UUID, report_type: str) -> Sequence[MinistryReport]:
        """List ministry reports by type for a school."""
        stmt = select(MinistryReport).where(
            MinistryReport.school_id == school_id,
            MinistryReport.report_type == report_type,
        ).order_by(MinistryReport.period_start.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, report: MinistryReport, data: dict) -> MinistryReport:
        """Update a ministry report."""
        for key, value in data.items():
            if value is not None:
                setattr(report, key, value)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def delete(self, report: MinistryReport) -> None:
        """Delete a ministry report."""
        await self.db.delete(report)
        await self.db.flush()
