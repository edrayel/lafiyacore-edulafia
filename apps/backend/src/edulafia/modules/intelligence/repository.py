from __future__ import annotations
"""Intelligence repository for data access operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.intelligence.models import (
    GeneratedReport,
    KPIDefinition,
    LGAAggregate,
    ReportTemplate,
    ResearchDataRequest,
    SchoolKPISnapshot,
    StateAggregate,
)


class KPIDefinitionRepository:
    """Repository for KPI definition database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_code(self, code: str) -> KPIDefinition | None:
        """Get KPI definition by code."""
        stmt = select(KPIDefinition).where(
            KPIDefinition.code == code,
            KPIDefinition.is_active == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_active(self) -> list[KPIDefinition]:
        """List all active KPI definitions."""
        stmt = select(KPIDefinition).where(
            KPIDefinition.is_active == True,
        ).order_by(KPIDefinition.code)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class SchoolKPISnapshotRepository:
    """Repository for school KPI snapshot database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_date(self, school_id: UUID, target_date: date) -> Sequence[SchoolKPISnapshot]:
        """Get KPI snapshots for a school on a specific date."""
        stmt = select(SchoolKPISnapshot).where(
            SchoolKPISnapshot.school_id == school_id,
            SchoolKPISnapshot.snapshot_date == target_date,
        ).order_by(SchoolKPISnapshot.kpi_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_latest(self, school_id: UUID) -> Sequence[SchoolKPISnapshot]:
        """Get the latest KPI snapshots for a school."""
        stmt = select(SchoolKPISnapshot).where(
            SchoolKPISnapshot.school_id == school_id,
        ).order_by(SchoolKPISnapshot.snapshot_date.desc()).limit(10)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, data: dict) -> SchoolKPISnapshot:
        """Create a new KPI snapshot."""
        snapshot = SchoolKPISnapshot(**data)
        self.db.add(snapshot)
        await self.db.flush()
        await self.db.refresh(snapshot)
        return snapshot

    async def get_by_id(self, snapshot_id: UUID) -> SchoolKPISnapshot | None:
        """Get KPI snapshot by ID."""
        stmt = select(SchoolKPISnapshot).where(
            SchoolKPISnapshot.id == snapshot_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_student_count(self, school_id: UUID) -> int:
        """Get active student count for a school."""
        from edulafia.modules.students.models import Student
        stmt = select(func.count()).select_from(Student).where(
            Student.school_id == school_id,
            Student.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_teacher_count(self, school_id: UUID) -> int:
        """Get active teacher count for a school."""
        from edulafia.modules.staff.models import Staff
        stmt = select(func.count()).select_from(Staff).where(
            Staff.school_id == school_id,
            Staff.role == "teacher",
            Staff.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_class_count(self, school_id: UUID) -> int:
        """Get active class count for a school."""
        from edulafia.modules.academics.models import Class
        stmt = select(func.count()).select_from(Class).where(
            Class.school_id == school_id,
            Class.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_active_alert_count(self, school_id: UUID) -> int:
        """Get active sentinel signal count for a school."""
        from edulafia.modules.health.models import SentinelSignal
        stmt = select(func.count()).select_from(SentinelSignal).where(
            SentinelSignal.school_ids.contains([str(school_id)]),
            SentinelSignal.status == "active",
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0


class LGAAggregateRepository:
    """Repository for LGA aggregate database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> LGAAggregate:
        """Create a new LGA aggregate."""
        aggregate = LGAAggregate(**data)
        self.db.add(aggregate)
        await self.db.flush()
        await self.db.refresh(aggregate)
        return aggregate

    async def get_by_lga_date(
        self,
        lga: str,
        state: str,
        aggregate_date: date,
    ) -> LGAAggregate | None:
        """Get LGA aggregate by LGA, state, and date."""
        stmt = select(LGAAggregate).where(
            LGAAggregate.lga == lga,
            LGAAggregate.state == state,
            LGAAggregate.aggregate_date == aggregate_date,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_state(
        self,
        state: str,
        aggregate_date: date,
    ) -> list[LGAAggregate]:
        """List all LGA aggregates for a state on a date."""
        stmt = select(LGAAggregate).where(
            LGAAggregate.state == state,
            LGAAggregate.aggregate_date == aggregate_date,
        ).order_by(LGAAggregate.lga)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class StateAggregateRepository:
    """Repository for state aggregate database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> StateAggregate:
        """Create a new state aggregate."""
        aggregate = StateAggregate(**data)
        self.db.add(aggregate)
        await self.db.flush()
        await self.db.refresh(aggregate)
        return aggregate

    async def get_by_state_date(
        self,
        state: str,
        aggregate_date: date,
    ) -> StateAggregate | None:
        """Get state aggregate by state and date."""
        stmt = select(StateAggregate).where(
            StateAggregate.state == state,
            StateAggregate.aggregate_date == aggregate_date,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class ResearchDataRequestRepository:
    """Repository for research data request database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ResearchDataRequest:
        """Create a new research data request."""
        request = ResearchDataRequest(**data)
        self.db.add(request)
        await self.db.flush()
        await self.db.refresh(request)
        return request

    async def get_by_id(self, request_id: UUID) -> ResearchDataRequest | None:
        """Get research request by ID."""
        stmt = select(ResearchDataRequest).where(
            ResearchDataRequest.id == request_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_researcher(
        self,
        researcher_id: UUID,
    ) -> list[ResearchDataRequest]:
        """List research requests by researcher."""
        stmt = select(ResearchDataRequest).where(
            ResearchDataRequest.researcher_id == researcher_id,
        ).order_by(ResearchDataRequest.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def increment_download(self, request_id: UUID) -> None:
        """Increment download count."""
        stmt = select(ResearchDataRequest).where(
            ResearchDataRequest.id == request_id,
        )
        result = await self.db.execute(stmt)
        request = result.scalar_one()

        request.download_count += 1
        await self.db.flush()


class ReportTemplateRepository:
    """Repository for report template database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ReportTemplate:
        """Create a new report template."""
        template = ReportTemplate(**data)
        self.db.add(template)
        await self.db.flush()
        await self.db.refresh(template)
        return template

    async def list(
        self,
        school_id: UUID | None = None,
        report_type: str | None = None,
    ) -> list[ReportTemplate]:
        """List report templates with filters."""
        stmt = select(ReportTemplate)

        if school_id:
            stmt = stmt.where(
                (ReportTemplate.school_id == school_id) |
                (ReportTemplate.is_system == True)
            )
        if report_type:
            stmt = stmt.where(ReportTemplate.report_type == report_type)

        stmt = stmt.order_by(ReportTemplate.name)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class GeneratedReportRepository:
    """Repository for generated report database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> GeneratedReport:
        """Create a new generated report."""
        report = GeneratedReport(**data)
        self.db.add(report)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def get_by_id(self, report_id: UUID) -> GeneratedReport | None:
        """Get generated report by ID."""
        stmt = select(GeneratedReport).where(
            GeneratedReport.id == report_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, report: GeneratedReport, data: dict) -> GeneratedReport:
        """Update a generated report."""
        for key, value in data.items():
            if value is not None:
                setattr(report, key, value)
        await self.db.flush()
        await self.db.refresh(report)
        return report

    async def list_by_user(
        self,
        user_id: UUID,
        report_type: str | None = None,
    ) -> list[GeneratedReport]:
        """List reports by user."""
        stmt = select(GeneratedReport).where(
            GeneratedReport.generated_by == user_id,
        )

        if report_type:
            stmt = stmt.where(GeneratedReport.report_type == report_type)

        stmt = stmt.order_by(GeneratedReport.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
