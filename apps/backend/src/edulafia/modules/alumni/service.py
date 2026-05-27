"""Alumni service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.alumni.repository import AlumniRepository
from edulafia.modules.alumni.schemas import (
    AlumniProfileCreate,
    AlumniProfileResponse,
    AlumniProfileUpdate,
)


class AlumniService:
    """Service for alumni business logic."""

    def __init__(self, repository: AlumniRepository):
        self.repository = repository

    async def create(self, data: AlumniProfileCreate, school_id: UUID, user_id: UUID) -> AlumniProfileResponse:
        """Create a new alumni profile."""
        existing = await self.repository.get_by_student_and_school(data.student_id, school_id)
        if existing:
            raise ValueError(f"Alumni profile already exists for student {data.student_id}")

        profile_data = data.model_dump()
        profile_data["school_id"] = school_id
        profile = await self.repository.create(profile_data)
        return AlumniProfileResponse.model_validate(profile)

    async def get_by_id(self, profile_id: UUID, school_id: UUID) -> AlumniProfileResponse | None:
        """Get an alumni profile by ID."""
        profile = await self.repository.get_by_id_and_school(profile_id, school_id)
        if profile:
            return AlumniProfileResponse.model_validate(profile)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[AlumniProfileResponse]:
        """List all alumni profiles for a school."""
        profiles = await self.repository.list_by_school(school_id)
        return [AlumniProfileResponse.model_validate(p) for p in profiles]

    async def update(self, profile_id: UUID, data: AlumniProfileUpdate, school_id: UUID, user_id: UUID) -> AlumniProfileResponse:
        """Update an alumni profile."""
        profile = await self.repository.get_by_id_and_school(profile_id, school_id)
        if not profile:
            raise ValueError(f"Alumni profile {profile_id} not found")

        update_data = data.model_dump(exclude_unset=True)
        updated_profile = await self.repository.update(profile, update_data)
        return AlumniProfileResponse.model_validate(updated_profile)

    async def delete(self, profile_id: UUID, school_id: UUID, user_id: UUID) -> None:
        """Delete an alumni profile."""
        profile = await self.repository.get_by_id_and_school(profile_id, school_id)
        if not profile:
            raise ValueError(f"Alumni profile {profile_id} not found")

        await self.repository.delete(profile)
