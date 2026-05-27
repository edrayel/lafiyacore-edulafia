"""Emergency service for business logic."""

from uuid import UUID

from edulafia.modules.emergency.repository import EmergencyModeRepository
from edulafia.modules.emergency.schemas import EmergencyModeCreate, EmergencyModeResponse


class EmergencyModeService:
    def __init__(self, repository: EmergencyModeRepository):
        self.repository = repository

    async def activate(self, data: EmergencyModeCreate, school_id: UUID, user_id: UUID) -> EmergencyModeResponse:
        existing = await self.repository.get_active(school_id)
        if existing:
            existing.status = "resolved"
            self.repository.db.add(existing)

        mode = await self.repository.create({
            **data.model_dump(),
            "school_id": school_id,
            "status": "active",
            "created_by": user_id,
        })
        return EmergencyModeResponse.model_validate(mode)

    async def deactivate(self, mode_id: UUID) -> EmergencyModeResponse | None:
        mode = await self.repository.deactivate(mode_id)
        if mode:
            return EmergencyModeResponse.model_validate(mode)
        return None

    async def get_active(self, school_id: UUID) -> EmergencyModeResponse | None:
        mode = await self.repository.get_active(school_id)
        if mode:
            return EmergencyModeResponse.model_validate(mode)
        return None

    async def list_by_school(self, school_id: UUID) -> list[EmergencyModeResponse]:
        modes = await self.repository.list_by_school(school_id)
        return [EmergencyModeResponse.model_validate(m) for m in modes]
