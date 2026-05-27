from typing import Any
from edulafia.config import settings
from arq.connections import RedisSettings

# We must import the functions that the worker will execute.
# Since we might not want to initialize the entire app context here, we can define the actual worker functions.
# However, `generate_report` requires database access. Let's create small wrappers.


async def send_sentinel_email(ctx: dict[str, Any], to_email: str, subject: str, body: str) -> None:
    """Worker task to send sentinel email."""
    from edulafia.core.email import send_email_async

    await send_email_async(to_email=to_email, subject=subject, body=body)


async def generate_report(
    ctx: dict[str, Any], report_id: str, report_request: dict[str, Any], school_id: str
) -> None:
    """Worker task to generate report asynchronously."""
    import logging
    from uuid import UUID
    from edulafia.database import AsyncSessionLocal
    from edulafia.modules.intelligence.repository import GeneratedReportRepository
    from edulafia.modules.intelligence.service import DashboardService
    from edulafia.modules.intelligence.schemas import ReportGenerateRequest

    logger = logging.getLogger(__name__)

    report_id_uuid = UUID(report_id)
    school_id_uuid = UUID(school_id)
    data = ReportGenerateRequest.model_validate(report_request)

    async with AsyncSessionLocal() as session:
        report_repo = GeneratedReportRepository(session)
        # Note: DashboardService requires other repos, but we might only need `_generate_report_async`
        # which only relies on `self.report_repo`.

        # We can instantiate a minimal DashboardService just for this
        from edulafia.modules.intelligence.repository import (
            KPIDefinitionRepository,
            SchoolKPISnapshotRepository,
            LGAAggregateRepository,
            StateAggregateRepository,
            ReportTemplateRepository,
        )

        service = DashboardService(
            kpi_repo=KPIDefinitionRepository(session),
            snapshot_repo=SchoolKPISnapshotRepository(session),
            lga_repo=LGAAggregateRepository(session),
            state_repo=StateAggregateRepository(session),
            report_repo=report_repo,
            template_repo=ReportTemplateRepository(session),
        )

        try:
            await service._generate_report_async(report_id_uuid, data, school_id_uuid)
        except Exception as e:
            logger.error("Report generation failed", extra={"report_id": report_id, "error": str(e)})
            raise


async def startup(ctx: dict[str, Any]) -> None:
    """Initialize things before worker starts."""
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("ARQ Worker starting up...")


async def shutdown(ctx: dict[str, Any]) -> None:
    """Cleanup after worker shuts down."""
    import logging

    logger = logging.getLogger(__name__)
    logger.info("ARQ Worker shutting down...")


class WorkerSettings:
    """ARQ Worker configuration."""

    functions = [
        send_sentinel_email,
        generate_report,
    ]

    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
