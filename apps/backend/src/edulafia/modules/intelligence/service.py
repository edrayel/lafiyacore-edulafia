"""Dashboard service for analytics and KPI management."""

from datetime import timezone, date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from edulafia.modules.intelligence.exceptions import (
    ReportNotFoundError,
)
from edulafia.modules.intelligence.repository import (
    GeneratedReportRepository,
    KPIDefinitionRepository,
    LGAAggregateRepository,
    ReportTemplateRepository,
    SchoolKPISnapshotRepository,
    StateAggregateRepository,
)
from edulafia.modules.intelligence.schemas import (
    DashboardFilters,
    KPIResponse,
    LGADashboardResponse,
    QuickStatsResponse,
    ReportGenerateRequest,
    ReportResponse,
    ReportTemplateResponse,
    SchoolDashboardResponse,
    SentinelDashboardResponse,
    StateDashboardResponse,
)

# Default KPI definitions
DEFAULT_KPIS = [
    {
        "code": "ATTENDANCE_RATE",
        "name": "Attendance Rate",
        "unit": "percent",
        "source_module": "attendance",
        "critical_threshold": 85.0,
        "warning_threshold": 95.0,
        "higher_is_better": True,
    },
    {
        "code": "SICK_BAY_VISITS",
        "name": "Sick Bay Visits",
        "unit": "count",
        "source_module": "health",
        "warning_threshold": 10.0,
        "higher_is_better": False,
    },
    {
        "code": "FEE_COLLECTIONS",
        "name": "Fee Collections",
        "unit": "currency",
        "source_module": "finance",
        "higher_is_better": True,
    },
    {
        "code": "OUTSTANDING_BALANCE",
        "name": "Outstanding Balance",
        "unit": "currency",
        "source_module": "finance",
        "warning_threshold": 1000000.0,
        "higher_is_better": False,
    },
    {
        "code": "OPEN_ALERTS",
        "name": "Open Health Alerts",
        "unit": "count",
        "source_module": "sentinel",
        "critical_threshold": 1.0,
        "higher_is_better": False,
    },
]


class DashboardService:
    """Service for dashboard operations."""

    def __init__(
        self,
        kpi_repo: KPIDefinitionRepository,
        snapshot_repo: SchoolKPISnapshotRepository,
        lga_repo: LGAAggregateRepository,
        state_repo: StateAggregateRepository,
        report_repo: GeneratedReportRepository,
        template_repo: ReportTemplateRepository,
    ):
        self.kpi_repo = kpi_repo
        self.snapshot_repo = snapshot_repo
        self.lga_repo = lga_repo
        self.state_repo = state_repo
        self.report_repo = report_repo
        self.template_repo = template_repo

    def _get_kpi_status(
        self,
        value: Decimal,
        kpi_config: dict,
    ) -> str:
        """Get KPI status based on thresholds."""
        critical = kpi_config.get("critical_threshold")
        warning = kpi_config.get("warning_threshold")
        higher_is_better = kpi_config.get("higher_is_better", True)

        if higher_is_better:
            if critical and value < critical:
                return "critical"
            if warning and value < warning:
                return "warning"
            return "normal"
        else:
            if critical and value >= critical:
                return "critical"
            if warning and value >= warning:
                return "warning"
            return "normal"

    def _get_trend(
        self,
        current: Decimal,
        previous: Decimal | None,
    ) -> str:
        """Calculate trend direction."""
        if previous is None:
            return "stable"
        if current > previous:
            return "up"
        if current < previous:
            return "down"
        return "stable"

    async def get_school_dashboard(
        self,
        school_id: UUID,
        filters: DashboardFilters | None = None,
    ) -> SchoolDashboardResponse:
        """Get school dashboard data."""
        target_date = filters.date if filters and filters.date else date.today()

        # Get KPI snapshots
        snapshots = await self.snapshot_repo.get_by_date(school_id, target_date)

        # Build KPI responses with proper lookup
        kpis = []
        for snapshot in snapshots:
            # Look up KPI definition by ID
            kpi_def = await self.kpi_repo.get_by_id(snapshot.kpi_id)
            if kpi_def:
                kpi_config = {
                    "code": kpi_def.code,
                    "name": kpi_def.name,
                    "unit": kpi_def.unit,
                    "critical_threshold": float(kpi_def.critical_threshold) if kpi_def.critical_threshold else None,
                    "warning_threshold": float(kpi_def.warning_threshold) if kpi_def.warning_threshold else None,
                    "higher_is_better": kpi_def.higher_is_better,
                }
            else:
                kpi_config = {"name": "Unknown", "unit": "", "higher_is_better": True}

            kpis.append(KPIResponse(
                code=kpi_config.get("code", str(snapshot.kpi_id)),
                name=kpi_config.get("name", "Unknown"),
                value=Decimal(str(snapshot.value)),
                unit=kpi_config.get("unit", ""),
                trend=snapshot.trend,
                status=snapshot.status,
                previous_value=Decimal(str(snapshot.previous_value)) if snapshot.previous_value else None,
            ))

        # Quick stats - compute from database
        quick_stats = await self._compute_quick_stats(school_id, target_date)

        # Calculate cache expiry (5 minutes)
        now = datetime.now(timezone.utc)
        cache_expires = now + timedelta(minutes=5)

        return SchoolDashboardResponse(
            kpis=kpis,
            alerts=[],
            trends=[],
            quick_stats=quick_stats,
            date=target_date,
            last_updated=now,
            cache_expires_at=cache_expires,
        )

    async def _compute_quick_stats(self, school_id: UUID, target_date: date) -> QuickStatsResponse:
        """Compute quick stats from database."""
        total_students = await self.snapshot_repo.get_student_count(school_id)
        total_teachers = await self.snapshot_repo.get_teacher_count(school_id)
        total_classes = await self.snapshot_repo.get_class_count(school_id)
        active_alerts = await self.snapshot_repo.get_active_alert_count(school_id)

        return QuickStatsResponse(
            total_students=total_students,
            total_teachers=total_teachers,
            total_classes=total_classes,
            active_alerts=active_alerts,
        )

    async def get_lga_dashboard(
        self,
        lga: str,
        state: str,
        target_date: date | None = None,
    ) -> LGADashboardResponse:
        """Get LGA dashboard data."""
        target_date = target_date or date.today()

        # Get LGA aggregate
        aggregate = await self.lga_repo.get_by_lga_date(lga, state, target_date)

        if not aggregate:
            # Return empty dashboard
            return LGADashboardResponse(
                lga=lga,
                state=state,
                date=target_date,
                total_schools=0,
                total_students=0,
                last_updated=datetime.now(timezone.utc),
            )

        return LGADashboardResponse(
            lga=aggregate.lga,
            state=aggregate.state,
            date=aggregate.aggregate_date,
            total_schools=aggregate.total_schools,
            total_students=aggregate.total_students,
            avg_attendance_rate=Decimal(str(aggregate.avg_attendance_rate)) if aggregate.avg_attendance_rate else None,
            total_sick_bay_visits=aggregate.total_sick_bay_visits,
            total_collections=Decimal(str(aggregate.total_collections)),
            open_alerts=aggregate.open_alerts_count,
            last_updated=datetime.now(timezone.utc),
        )

    async def get_state_dashboard(
        self,
        state: str,
        target_date: date | None = None,
    ) -> StateDashboardResponse:
        """Get state dashboard data."""
        target_date = target_date or date.today()

        aggregate = await self.state_repo.get_by_state_date(state, target_date)
        if aggregate:
            return StateDashboardResponse(
                state=aggregate.state,
                date=aggregate.aggregate_date,
                total_lgas=aggregate.total_lgas,
                total_schools=aggregate.total_schools,
                total_students=aggregate.total_students,
                avg_attendance_rate=Decimal(str(aggregate.avg_attendance_rate)) if aggregate.avg_attendance_rate else None,
                total_sick_bay_visits=aggregate.total_sick_bay_visits,
                total_collections=Decimal(str(aggregate.total_collections)),
                open_alerts=aggregate.open_alerts_count,
                last_updated=datetime.now(timezone.utc),
            )

        return StateDashboardResponse(
            state=state,
            date=target_date,
            total_lgas=0,
            total_schools=0,
            total_students=0,
            last_updated=datetime.now(timezone.utc),
        )

    async def get_sentinel_dashboard(
        self,
        school_id: UUID | None = None,
        lga: str | None = None,
        state: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> SentinelDashboardResponse:
        """Get sentinel dashboard data."""
        from sqlalchemy import select, func, and_

        from edulafia.database import AsyncSessionLocal
        from edulafia.modules.health.models import SentinelSignal

        end_date = end_date or date.today()
        start_date = start_date or (end_date - timedelta(days=30))

        # Build query filters safely using SQLAlchemy expressions
        filters = [SentinelSignal.date_generated >= start_date]

        if school_id:
            filters.append(SentinelSignal.school_id == school_id)
        if lga:
            filters.append(SentinelSignal.lga == lga)
        if state:
            filters.append(SentinelSignal.state == state)

        async with AsyncSessionLocal() as session:
            # Count active alerts
            active_q = select(func.count()).select_from(SentinelSignal).where(
                SentinelSignal.status == "active",
                *filters,
            )
            r = await session.execute(active_q)
            active_alerts = r.scalar() or 0

            # Count recent signals (same filters, date already included)
            recent_q = select(func.count()).select_from(SentinelSignal).where(*filters)
            r = await session.execute(recent_q)
            recent_signals = r.scalar() or 0

            # Count by tier
            tier_q = select(
                SentinelSignal.alert_tier, func.count()
            ).where(
                *filters
            ).group_by(SentinelSignal.alert_tier)
            r = await session.execute(tier_q)
            signals_by_tier = {row[0]: row[1] for row in r.fetchall()}

            # Count by status
            status_q = select(
                SentinelSignal.status, func.count()
            ).where(
                *filters
            ).group_by(SentinelSignal.status)
            r = await session.execute(status_q)
            signals_by_status = {row[0]: row[1] for row in r.fetchall()}

        # Ensure all tiers/statuses present
        for tier in ["school", "lga", "state"]:
            signals_by_tier.setdefault(tier, 0)
        for status in ["active", "acknowledged", "resolved"]:
            signals_by_status.setdefault(status, 0)

        return SentinelDashboardResponse(
            date=end_date,
            date_range_start=start_date,
            date_range_end=end_date,
            active_alerts=active_alerts,
            recent_signals=recent_signals,
            signals_by_tier=signals_by_tier,
            signals_by_status=signals_by_status,
            last_updated=datetime.now(timezone.utc),
        )

    async def generate_report(
        self,
        data: ReportGenerateRequest,
        user_id: UUID,
        school_id: UUID,
    ) -> ReportResponse:
        """Generate a report asynchronously."""
        import asyncio
        from edulafia.core.arq_queue import enqueue_generate_report

        # Create report record
        report_data = {
            "report_type": data.report_type,
            "parameters": {**data.parameters, "format": data.format},
            "status": "pending",
            "progress_percent": 0,
            "generated_by": user_id,
        }

        report = await self.report_repo.create(report_data)

        # Enqueue durable job using ARQ
        await enqueue_generate_report(report.id, data.model_dump(), school_id)

        return ReportResponse.model_validate(report)

    async def _generate_report_async(
        self,
        report_id: UUID,
        data: ReportGenerateRequest,
        school_id: UUID,
    ) -> None:
        """Generate report asynchronously."""
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Update to generating
            report = await self.report_repo.get_by_id(report_id)
            if report:
                await self.report_repo.update(report, {
                    "status": "generating",
                    "progress_percent": 10,
                })

            # Simulate report generation steps
            await self.report_repo.update(report, {"progress_percent": 30})
            await self.report_repo.update(report, {"progress_percent": 60})

            # Generate an actual simple CSV file
            import os
            import csv
            from sqlalchemy import select, text
            from edulafia.database import AsyncSessionLocal
            
            reports_dir = "/tmp/edulafia_reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            file_name = f"{report_id}.{data.format}"
            real_file_path = os.path.join(reports_dir, file_name)
            
            async with AsyncSessionLocal() as session:
                if data.report_type == "attendance_summary":
                    stmt = text("SELECT date, status, count(*) FROM attendance_records WHERE school_id = :school_id GROUP BY date, status ORDER BY date DESC LIMIT 100")
                    result = await session.execute(stmt, {"school_id": str(school_id)})
                    rows = [["Date", "Status", "Count"]] + [[str(row[0]), row[1], row[2]] for row in result]
                elif data.report_type == "academic_performance":
                    stmt = text("SELECT term_id, grade, count(*) FROM score_entries JOIN academic_results ON score_entries.result_id = academic_results.id JOIN students ON academic_results.student_id = students.id WHERE students.school_id = :school_id GROUP BY term_id, grade ORDER BY term_id DESC LIMIT 100")
                    result = await session.execute(stmt, {"school_id": str(school_id)})
                    rows = [["Term", "Grade", "Count"]] + [[row[0], row[1], row[2]] for row in result]
                else:
                    rows = [["Report ID", "Report Type", "Format"], [str(report_id), data.report_type, data.format]]

            # Write the aggregated report data to file
            with open(real_file_path, "w", newline="") as f:
                if data.format == "csv":
                    writer = csv.writer(f)
                    writer.writerows(rows)
                else:
                    # Basic text file for pdf/xlsx mock
                    f.write(f"Generated {data.report_type} Report\nID: {report_id}\n\n")
                    for r in rows:
                        f.write(", ".join(str(c) for c in r) + "\n")
            
            # For downloading via an API, we could serve from a static route or an endpoint.
            # Assuming the frontend uses this file_path directly or an endpoint reads it:
            download_path = f"/api/v1/intelligence/download/{file_name}"

            # Mark as completed
            await self.report_repo.update(report, {
                "status": "completed",
                "progress_percent": 100,
                "file_path": download_path,
                "file_format": data.format,
                "completed_at": datetime.now(timezone.utc),
                "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
            })
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            report = await self.report_repo.get_by_id(report_id)
            if report:
                await self.report_repo.update(report, {
                    "status": "failed",
                    "progress_percent": 0,
                    "error_message": str(e),
                })

    async def get_report(self, report_id: UUID, user_id: UUID) -> ReportResponse:
        """Get report by ID."""
        report = await self.report_repo.get_by_id(report_id)
        if not report:
            raise ReportNotFoundError(str(report_id))

        return ReportResponse.model_validate(report)

    async def list_report_templates(
        self,
        school_id: UUID | None = None,
        report_type: str | None = None,
    ) -> list[ReportTemplateResponse]:
        """List report templates."""
        templates = await self.template_repo.list(
            school_id=school_id,
            report_type=report_type,
        )
        return [ReportTemplateResponse.model_validate(t) for t in templates]
