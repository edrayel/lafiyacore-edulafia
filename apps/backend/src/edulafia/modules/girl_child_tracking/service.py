"""Girl child tracking service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.girl_child_tracking.repository import GirlChildRecordRepository
from edulafia.modules.girl_child_tracking.schemas import (
    GirlChildRecordCreate,
    GirlChildRecordResponse,
    GirlChildRecordUpdate,
)


class GirlChildRecordService:
    """Service for girl child record business logic."""

    def __init__(self, repository: GirlChildRecordRepository):
        self.repository = repository

    async def create(self, data: GirlChildRecordCreate, user_id: UUID) -> GirlChildRecordResponse:
        """Create a new girl child record."""
        existing = await self.repository.get_by_student_id(data.student_id)
        if existing:
            raise ValueError(f"Girl child record already exists for student {data.student_id}")

        record_data = data.model_dump()
        record = await self.repository.create(record_data)
        return GirlChildRecordResponse.model_validate(record)

    async def get_by_id(self, record_id: UUID) -> GirlChildRecordResponse | None:
        """Get a girl child record by ID."""
        record = await self.repository.get_by_id(record_id)
        if record:
            return GirlChildRecordResponse.model_validate(record)
        return None

    async def get_by_student_id(self, student_id: UUID) -> GirlChildRecordResponse | None:
        """Get a girl child record by student ID."""
        record = await self.repository.get_by_student_id(student_id)
        if record:
            return GirlChildRecordResponse.model_validate(record)
        return None

    async def list_by_dropout_risk(self, risk_level: str) -> Sequence[GirlChildRecordResponse]:
        """List girl child records by dropout risk level."""
        records = await self.repository.list_by_dropout_risk(risk_level)
        return [GirlChildRecordResponse.model_validate(r) for r in records]

    async def update(self, record_id: UUID, data: GirlChildRecordUpdate, user_id: UUID) -> GirlChildRecordResponse:
        """Update a girl child record."""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Girl child record {record_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_record = await self.repository.update(record, update_data)
        return GirlChildRecordResponse.model_validate(updated_record)
