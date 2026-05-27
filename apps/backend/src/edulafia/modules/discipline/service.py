"""Discipline service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.discipline.repository import DisciplineRecordRepository
from edulafia.modules.discipline.schemas import (
    DisciplineRecordCreate,
    DisciplineRecordResponse,
    DisciplineRecordUpdate,
)


class DisciplineRecordService:
    """Service for discipline record business logic."""

    def __init__(self, repository: DisciplineRecordRepository):
        self.repository = repository

    async def create(self, data: DisciplineRecordCreate, user_id: UUID) -> DisciplineRecordResponse:
        """Create a new discipline record."""
        record_data = data.model_dump()
        record = await self.repository.create(record_data)
        return DisciplineRecordResponse.model_validate(record)

    async def get_by_id(self, record_id: UUID) -> DisciplineRecordResponse | None:
        """Get a discipline record by ID."""
        record = await self.repository.get_by_id(record_id)
        if record:
            return DisciplineRecordResponse.model_validate(record)
        return None

    async def list_by_student(self, student_id: UUID) -> Sequence[DisciplineRecordResponse]:
        """List all discipline records for a student."""
        records = await self.repository.list_by_student(student_id)
        return [DisciplineRecordResponse.model_validate(r) for r in records]

    async def list_open(self) -> Sequence[DisciplineRecordResponse]:
        """List all open discipline records."""
        records = await self.repository.list_open()
        return [DisciplineRecordResponse.model_validate(r) for r in records]

    async def update(self, record_id: UUID, data: DisciplineRecordUpdate, user_id: UUID) -> DisciplineRecordResponse:
        """Update a discipline record."""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Discipline record {record_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_record = await self.repository.update(record, update_data)
        return DisciplineRecordResponse.model_validate(updated_record)

    async def resolve(self, record_id: UUID) -> DisciplineRecordResponse:
        """Resolve a discipline record."""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Discipline record {record_id} not found")

        update_data = {"status": "resolved"}
        updated_record = await self.repository.update(record, update_data)
        return DisciplineRecordResponse.model_validate(updated_record)
