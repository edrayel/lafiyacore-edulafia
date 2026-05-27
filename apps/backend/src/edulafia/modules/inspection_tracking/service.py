"""Inspection tracking service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.inspection_tracking.repository import SchoolInspectionRepository
from edulafia.modules.inspection_tracking.schemas import (
    SchoolInspectionCreate,
    SchoolInspectionResponse,
    SchoolInspectionUpdate,
)


class SchoolInspectionService:
    """Service for school inspection business logic."""

    def __init__(self, repository: SchoolInspectionRepository):
        self.repository = repository

    async def create(self, data: SchoolInspectionCreate, user_id: UUID) -> SchoolInspectionResponse:
        """Create a new school inspection."""
        inspection_data = data.model_dump()
        inspection = await self.repository.create(inspection_data)
        return SchoolInspectionResponse.model_validate(inspection)

    async def get_by_id(self, inspection_id: UUID) -> SchoolInspectionResponse | None:
        """Get a school inspection by ID."""
        inspection = await self.repository.get_by_id(inspection_id)
        if inspection:
            return SchoolInspectionResponse.model_validate(inspection)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[SchoolInspectionResponse]:
        """List all inspections for a school."""
        inspections = await self.repository.list_by_school(school_id)
        return [SchoolInspectionResponse.model_validate(i) for i in inspections]

    async def list_by_status(self, status: str) -> Sequence[SchoolInspectionResponse]:
        """List inspections by status."""
        inspections = await self.repository.list_by_status(status)
        return [SchoolInspectionResponse.model_validate(i) for i in inspections]

    async def update(self, inspection_id: UUID, data: SchoolInspectionUpdate, user_id: UUID) -> SchoolInspectionResponse:
        """Update a school inspection."""
        inspection = await self.repository.get_by_id(inspection_id)
        if not inspection:
            raise ValueError(f"School inspection {inspection_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_inspection = await self.repository.update(inspection, update_data)
        return SchoolInspectionResponse.model_validate(updated_inspection)

    async def resolve(self, inspection_id: UUID) -> SchoolInspectionResponse:
        """Resolve a school inspection."""
        inspection = await self.repository.get_by_id(inspection_id)
        if not inspection:
            raise ValueError(f"School inspection {inspection_id} not found")

        update_data = {"status": "resolved"}
        updated_inspection = await self.repository.update(inspection, update_data)
        return SchoolInspectionResponse.model_validate(updated_inspection)
