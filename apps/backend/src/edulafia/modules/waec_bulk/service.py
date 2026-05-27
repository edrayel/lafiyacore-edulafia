"""WAEC bulk service for business logic operations."""

from collections.abc import Sequence
from datetime import timezone, UTC, datetime
from uuid import UUID

from edulafia.modules.waec_bulk.repository import WAECBulkRegistrationRepository
from edulafia.modules.waec_bulk.schemas import (
    WAECBulkRegistrationCreate,
    WAECBulkRegistrationResponse,
    WAECBulkRegistrationUpdate,
)


class WAECBulkRegistrationService:
    """Service for WAEC bulk registration business logic."""

    def __init__(self, repository: WAECBulkRegistrationRepository):
        self.repository = repository

    async def create(self, data: WAECBulkRegistrationCreate, user_id: UUID) -> WAECBulkRegistrationResponse:
        """Create a new WAEC bulk registration."""
        registration_data = data.model_dump()
        registration = await self.repository.create(registration_data)
        return WAECBulkRegistrationResponse.model_validate(registration)

    async def get_by_id(self, registration_id: UUID, school_id: UUID) -> WAECBulkRegistrationResponse | None:
        """Get a WAEC bulk registration by ID."""
        registration = await self.repository.get_by_id_and_school(registration_id, school_id)
        if registration:
            return WAECBulkRegistrationResponse.model_validate(registration)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[WAECBulkRegistrationResponse]:
        """List all WAEC bulk registrations for a school."""
        registrations = await self.repository.list_by_school(school_id)
        return [WAECBulkRegistrationResponse.model_validate(r) for r in registrations]

    async def list_by_school_and_year(self, school_id: UUID, exam_year: int) -> Sequence[WAECBulkRegistrationResponse]:
        """List WAEC bulk registrations for a school by year."""
        registrations = await self.repository.list_by_school_and_year(school_id, exam_year)
        return [WAECBulkRegistrationResponse.model_validate(r) for r in registrations]

    async def update(self, registration_id: UUID, data: WAECBulkRegistrationUpdate, school_id: UUID, user_id: UUID) -> WAECBulkRegistrationResponse:
        """Update a WAEC bulk registration."""
        registration = await self.repository.get_by_id_and_school(registration_id, school_id)
        if not registration:
            raise ValueError(f"WAEC bulk registration {registration_id} not found")
        if registration.status == "submitted":
            raise ValueError("Submitted registrations cannot be updated")

        update_data = data.model_dump(exclude_none=True)
        updated_registration = await self.repository.update(registration, update_data)
        return WAECBulkRegistrationResponse.model_validate(updated_registration)

    async def submit(self, registration_id: UUID, school_id: UUID) -> WAECBulkRegistrationResponse:
        """Submit a WAEC bulk registration."""
        registration = await self.repository.get_by_id_and_school(registration_id, school_id)
        if not registration:
            raise ValueError(f"WAEC bulk registration {registration_id} not found")
        if registration.status == "submitted":
            raise ValueError("Registration already submitted")

        update_data = {
            "status": "submitted",
            "submitted_at": datetime.now(UTC),
        }
        updated_registration = await self.repository.update(registration, update_data)
        return WAECBulkRegistrationResponse.model_validate(updated_registration)
