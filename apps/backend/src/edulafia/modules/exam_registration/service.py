"""Exam registration service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.exam_registration.repository import ExamRegistrationRepository
from edulafia.modules.exam_registration.schemas import (
    ExamRegistrationCreate,
    ExamRegistrationResponse,
    ExamRegistrationUpdate,
)


class ExamRegistrationService:
    """Service for exam registration business logic."""

    def __init__(self, repository: ExamRegistrationRepository):
        self.repository = repository

    async def create(self, data: ExamRegistrationCreate, user_id: UUID) -> ExamRegistrationResponse:
        """Create a new exam registration."""
        existing = await self.repository.get_by_student_and_exam(
            data.student_id, data.exam_type, data.year
        )
        if existing:
            raise ValueError(f"Student already registered for {data.exam_type} {data.year}")

        registration_data = data.model_dump()
        registration = await self.repository.create(registration_data)
        return ExamRegistrationResponse.model_validate(registration)

    async def get_by_id(self, registration_id: UUID) -> ExamRegistrationResponse | None:
        """Get an exam registration by ID."""
        registration = await self.repository.get_by_id(registration_id)
        if registration:
            return ExamRegistrationResponse.model_validate(registration)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[ExamRegistrationResponse]:
        """List all exam registrations for a school."""
        registrations = await self.repository.list_by_school(school_id)
        return [ExamRegistrationResponse.model_validate(r) for r in registrations]

    async def list_by_student(self, student_id: UUID) -> Sequence[ExamRegistrationResponse]:
        """List all exam registrations for a student."""
        registrations = await self.repository.list_by_student(student_id)
        return [ExamRegistrationResponse.model_validate(r) for r in registrations]

    async def update(self, registration_id: UUID, data: ExamRegistrationUpdate, user_id: UUID) -> ExamRegistrationResponse:
        """Update an exam registration."""
        registration = await self.repository.get_by_id(registration_id)
        if not registration:
            raise ValueError(f"Exam registration {registration_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_registration = await self.repository.update(registration, update_data)
        return ExamRegistrationResponse.model_validate(updated_registration)

    async def mark_completed(self, registration_id: UUID) -> ExamRegistrationResponse:
        """Mark an exam registration as completed."""
        registration = await self.repository.get_by_id(registration_id)
        if not registration:
            raise ValueError(f"Exam registration {registration_id} not found")

        update_data = {"status": "completed"}
        updated_registration = await self.repository.update(registration, update_data)
        return ExamRegistrationResponse.model_validate(updated_registration)
