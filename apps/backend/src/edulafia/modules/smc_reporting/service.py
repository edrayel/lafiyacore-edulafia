"""SMC reporting service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.smc_reporting.repository import SMCReportRepository
from edulafia.modules.smc_reporting.schemas import (
    SMCReportCreate,
    SMCReportResponse,
    SMCReportUpdate,
)


class SMCReportService:
    """Service for SMC report business logic."""

    def __init__(self, repository: SMCReportRepository):
        self.repository = repository

    async def create(self, data: SMCReportCreate, user_id: UUID) -> SMCReportResponse:
        """Create a new SMC report."""
        report_data = data.model_dump()
        report = await self.repository.create(report_data)
        return SMCReportResponse.model_validate(report)

    async def get_by_id(self, report_id: UUID) -> SMCReportResponse | None:
        """Get an SMC report by ID."""
        report = await self.repository.get_by_id(report_id)
        if report:
            return SMCReportResponse.model_validate(report)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[SMCReportResponse]:
        """List all SMC reports for a school."""
        reports = await self.repository.list_by_school(school_id)
        return [SMCReportResponse.model_validate(r) for r in reports]

    async def update(self, report_id: UUID, data: SMCReportUpdate, user_id: UUID) -> SMCReportResponse:
        """Update an SMC report."""
        report = await self.repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"SMC report {report_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_report = await self.repository.update(report, update_data)
        return SMCReportResponse.model_validate(updated_report)
    async def delete(self, report_id: UUID) -> None:
        """Delete a record."""
        record = await self.repository.get_by_id(report_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)

