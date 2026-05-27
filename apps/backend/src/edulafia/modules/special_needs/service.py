"""Special needs / IEP service."""
from uuid import UUID

from edulafia.modules.special_needs.repository import IEPRepository
from edulafia.modules.special_needs.schemas import IEPCreate, IEPResponse, IEPUpdate


class IEPService:
    def __init__(self, repository: IEPRepository):
        self.repository = repository

    async def create(self, data: IEPCreate, school_id: UUID, user_id: UUID) -> IEPResponse:
        iep = await self.repository.create({**data.model_dump(), "school_id": school_id, "status": "draft", "created_by": user_id})
        return IEPResponse.model_validate(iep)

    async def update(self, student_id: UUID, data: IEPUpdate, user_id: UUID) -> IEPResponse | None:
        iep = await self.repository.get_by_student(student_id)
        if iep:
            iep = await self.repository.update(iep, {**data.model_dump(exclude_none=True), "reviewed_by": user_id})
            return IEPResponse.model_validate(iep)
        return None

    async def get_by_student(self, student_id: UUID) -> IEPResponse | None:
        iep = await self.repository.get_by_student(student_id)
        return IEPResponse.model_validate(iep) if iep else None

    async def list_by_school(self, school_id: UUID) -> list[IEPResponse]:
        ieps = await self.repository.list_by_school(school_id)
        return [IEPResponse.model_validate(i) for i in ieps]
