"""Data retention service for business logic operations."""

from collections.abc import Sequence
from datetime import timezone, UTC, datetime
from uuid import UUID

from edulafia.modules.data_retention.repository import (
    DataArchiveRepository,
    RetentionPolicyRepository,
)
from edulafia.modules.data_retention.schemas import (
    DataArchiveCreate,
    DataArchiveResponse,
    RetentionPolicyCreate,
    RetentionPolicyResponse,
    RetentionPolicyUpdate,
)


class RetentionPolicyService:
    """Service for retention policy business logic."""

    def __init__(self, repository: RetentionPolicyRepository):
        self.repository = repository

    async def create(self, data: RetentionPolicyCreate, user_id: UUID) -> RetentionPolicyResponse:
        """Create a new retention policy."""
        policy_data = data.model_dump()
        policy = await self.repository.create(policy_data)
        return RetentionPolicyResponse.model_validate(policy)

    async def get_by_id(self, policy_id: UUID) -> RetentionPolicyResponse | None:
        """Get a retention policy by ID."""
        policy = await self.repository.get_by_id(policy_id)
        if policy:
            return RetentionPolicyResponse.model_validate(policy)
        return None

    async def get_by_school_and_type(self, school_id: UUID, data_type: str) -> RetentionPolicyResponse | None:
        """Get a retention policy by school and data type."""
        policy = await self.repository.get_by_school_and_type(school_id, data_type)
        if policy:
            return RetentionPolicyResponse.model_validate(policy)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[RetentionPolicyResponse]:
        """List all retention policies for a school."""
        policies = await self.repository.list_by_school(school_id)
        return [RetentionPolicyResponse.model_validate(p) for p in policies]

    async def update(self, policy_id: UUID, data: RetentionPolicyUpdate, user_id: UUID) -> RetentionPolicyResponse:
        """Update a retention policy."""
        policy = await self.repository.get_by_id(policy_id)
        if not policy:
            raise ValueError(f"Retention policy {policy_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_policy = await self.repository.update(policy, update_data)
        return RetentionPolicyResponse.model_validate(updated_policy)



    async def delete(self, policy_id: UUID) -> None:
        """Delete a record."""
        record = await self.repository.get_by_id(policy_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
class DataArchiveService:
    """Service for data archive business logic."""

    def __init__(self, repository: DataArchiveRepository):
        self.repository = repository

    async def create(self, data: DataArchiveCreate, user_id: UUID) -> DataArchiveResponse:
        """Create a new data archive."""
        archive_data = data.model_dump()
        archive_data["archived_at"] = datetime.now(UTC)
        archive = await self.repository.create(archive_data)
        return DataArchiveResponse.model_validate(archive)

    async def get_by_id(self, archive_id: UUID) -> DataArchiveResponse | None:
        """Get a data archive by ID."""
        archive = await self.repository.get_by_id(archive_id)
        if archive:
            return DataArchiveResponse.model_validate(archive)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[DataArchiveResponse]:
        """List all data archives for a school."""
        archives = await self.repository.list_by_school(school_id)
        return [DataArchiveResponse.model_validate(a) for a in archives]

    async def mark_deleted(self, archive_id: UUID) -> DataArchiveResponse:
        """Mark an archive as deleted."""
        archive = await self.repository.get_by_id(archive_id)
        if not archive:
            raise ValueError(f"Data archive {archive_id} not found")

        update_data = {"status": "deleted"}
        updated_archive = await self.repository.update(archive, update_data)
        return DataArchiveResponse.model_validate(updated_archive)
