"""Clubs service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.clubs.repository import ClubMembershipRepository, ClubRepository
from edulafia.modules.clubs.schemas import (
    ClubCreate,
    ClubMembershipCreate,
    ClubMembershipResponse,
    ClubMembershipUpdateRequest,
    ClubResponse,
    ClubUpdateRequest,
)


class ClubService:
    """Service for club business logic."""

    def __init__(self, repository: ClubRepository):
        self.repository = repository

    async def create(self, data: ClubCreate, user_id: UUID) -> ClubResponse:
        """Create a new club."""
        club_data = data.model_dump()
        club = await self.repository.create(club_data)
        return ClubResponse.model_validate(club)

    async def get_by_id(self, club_id: UUID, school_id: UUID) -> ClubResponse | None:
        """Get a club by ID."""
        club = await self.repository.get_by_id_and_school(club_id, school_id)
        if club:
            return ClubResponse.model_validate(club)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[ClubResponse]:
        """List all clubs for a school."""
        clubs = await self.repository.list_by_school(school_id)
        return [ClubResponse.model_validate(c) for c in clubs]

    async def update(self, club_id: UUID, data: ClubUpdateRequest, school_id: UUID, user_id: UUID) -> ClubResponse:
        """Update a club."""
        club = await self.repository.get_by_id_and_school(club_id, school_id)
        if not club:
            raise ValueError(f"Club {club_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_club = await self.repository.update(club, update_data)
        return ClubResponse.model_validate(updated_club)


class ClubMembershipService:
    """Service for club membership business logic."""

    def __init__(self, repository: ClubMembershipRepository, club_repository: ClubRepository):
        self.repository = repository
        self.club_repository = club_repository

    async def create(self, data: ClubMembershipCreate, user_id: UUID) -> ClubMembershipResponse:
        """Create a new club membership."""
        existing = await self.repository.get_by_club_and_student(data.club_id, data.student_id)
        if existing:
            raise ValueError("Student is already a member of this club")

        membership_data = data.model_dump()
        membership = await self.repository.create(membership_data)
        return ClubMembershipResponse.model_validate(membership)

    async def get_by_id(self, membership_id: UUID) -> ClubMembershipResponse | None:
        """Get a membership by ID."""
        membership = await self.repository.get_by_id(membership_id)
        if membership:
            return ClubMembershipResponse.model_validate(membership)
        return None

    async def list_by_club(self, club_id: UUID) -> Sequence[ClubMembershipResponse]:
        """List all memberships for a club."""
        memberships = await self.repository.list_by_club(club_id)
        return [ClubMembershipResponse.model_validate(m) for m in memberships]

    async def list_by_student(self, student_id: UUID) -> Sequence[ClubMembershipResponse]:
        """List all memberships for a student."""
        memberships = await self.repository.list_by_student(student_id)
        return [ClubMembershipResponse.model_validate(m) for m in memberships]

    async def update(self, membership_id: UUID, data: ClubMembershipUpdateRequest, user_id: UUID) -> ClubMembershipResponse:
        """Update a club membership."""
        membership = await self.repository.get_by_id(membership_id)
        if not membership:
            raise ValueError(f"Club membership {membership_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_membership = await self.repository.update(membership, update_data)
        return ClubMembershipResponse.model_validate(updated_membership)

    async def remove(self, membership_id: UUID) -> None:
        """Remove a club membership."""
        membership = await self.repository.get_by_id(membership_id)
        if not membership:
            raise ValueError(f"Club membership {membership_id} not found")

        await self.repository.delete(membership)
