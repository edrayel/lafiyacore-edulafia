"""Accreditation service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.accreditation.repository import AccreditationChecklistRepository
from edulafia.modules.accreditation.schemas import (
    AccreditationChecklistCreate,
    AccreditationChecklistResponse,
    AccreditationChecklistUpdate,
)


class AccreditationChecklistService:
    """Service for accreditation checklist business logic."""

    def __init__(self, repository: AccreditationChecklistRepository):
        self.repository = repository

    async def create(self, data: AccreditationChecklistCreate, user_id: UUID) -> AccreditationChecklistResponse:
        """Create a new accreditation checklist."""
        checklist_data = data.model_dump()
        checklist = await self.repository.create(checklist_data)
        return AccreditationChecklistResponse.model_validate(checklist)

    async def get_by_id(self, checklist_id: UUID) -> AccreditationChecklistResponse | None:
        """Get an accreditation checklist by ID."""
        checklist = await self.repository.get_by_id(checklist_id)
        if checklist:
            return AccreditationChecklistResponse.model_validate(checklist)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[AccreditationChecklistResponse]:
        """List all checklists for a school."""
        checklists = await self.repository.list_by_school(school_id)
        return [AccreditationChecklistResponse.model_validate(c) for c in checklists]

    async def list_by_school_and_category(self, school_id: UUID, category: str) -> Sequence[AccreditationChecklistResponse]:
        """List checklists for a school by category."""
        checklists = await self.repository.list_by_school_and_category(school_id, category)
        return [AccreditationChecklistResponse.model_validate(c) for c in checklists]

    async def update(self, checklist_id: UUID, data: AccreditationChecklistUpdate, user_id: UUID) -> AccreditationChecklistResponse:
        """Update an accreditation checklist."""
        checklist = await self.repository.get_by_id(checklist_id)
        if not checklist:
            raise ValueError(f"Accreditation checklist {checklist_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_checklist = await self.repository.update(checklist, update_data)
        return AccreditationChecklistResponse.model_validate(updated_checklist)
