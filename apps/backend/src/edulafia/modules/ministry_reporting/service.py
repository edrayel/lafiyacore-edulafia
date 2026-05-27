"""Ministry reporting service for business logic operations."""

from collections.abc import Sequence
from datetime import timezone, UTC, datetime
from uuid import UUID

from edulafia.modules.ministry_reporting.repository import MinistryReportRepository
from edulafia.modules.ministry_reporting.schemas import (
    MinistryReportCreate,
    MinistryReportResponse,
    MinistryReportUpdate,
)


class MinistryReportService:
    """Service for ministry report business logic."""

    def __init__(self, repository: MinistryReportRepository):
        self.repository = repository

    async def create(self, data: MinistryReportCreate, user_id: UUID) -> MinistryReportResponse:
        """Create a new ministry report."""
        report_data = data.model_dump()
        report = await self.repository.create(report_data)
        return MinistryReportResponse.model_validate(report)

    async def get_by_id(self, report_id: UUID) -> MinistryReportResponse | None:
        """Get a ministry report by ID."""
        report = await self.repository.get_by_id(report_id)
        if report:
            return MinistryReportResponse.model_validate(report)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[MinistryReportResponse]:
        """List all ministry reports for a school."""
        reports = await self.repository.list_by_school(school_id)
        return [MinistryReportResponse.model_validate(r) for r in reports]

    async def list_by_type(self, school_id: UUID, report_type: str) -> Sequence[MinistryReportResponse]:
        """List ministry reports by type."""
        reports = await self.repository.list_by_type(school_id, report_type)
        return [MinistryReportResponse.model_validate(r) for r in reports]

    async def update(self, report_id: UUID, data: MinistryReportUpdate, user_id: UUID) -> MinistryReportResponse:
        """Update a ministry report."""
        report = await self.repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Ministry report {report_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_report = await self.repository.update(report, update_data)
        return MinistryReportResponse.model_validate(updated_report)

    async def submit(self, report_id: UUID) -> MinistryReportResponse:
        """Submit a ministry report."""
        report = await self.repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Ministry report {report_id} not found")
        if report.submitted:
            raise ValueError("Report already submitted")

        update_data = {
            "submitted": True,
            "submitted_at": datetime.now(UTC),
        }
        updated_report = await self.repository.update(report, update_data)
        return MinistryReportResponse.model_validate(updated_report)
