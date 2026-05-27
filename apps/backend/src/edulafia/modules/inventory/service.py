"""Inventory service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.inventory.repository import AssetRepository
from edulafia.modules.inventory.schemas import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)


class AssetService:
    """Service for asset business logic."""

    def __init__(self, repository: AssetRepository):
        self.repository = repository

    async def create(self, data: AssetCreate, user_id: UUID) -> AssetResponse:
        """Create a new asset."""
        asset_data = data.model_dump()
        asset = await self.repository.create(asset_data)
        return AssetResponse.model_validate(asset)

    async def get_by_id(self, asset_id: UUID, school_id: UUID) -> AssetResponse | None:
        """Get an asset by ID."""
        asset = await self.repository.get_by_id_and_school(asset_id, school_id)
        if asset:
            return AssetResponse.model_validate(asset)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[AssetResponse]:
        """List all assets for a school."""
        assets = await self.repository.list_by_school(school_id)
        return [AssetResponse.model_validate(a) for a in assets]

    async def list_by_category(self, school_id: UUID, category: str) -> Sequence[AssetResponse]:
        """List assets by category."""
        assets = await self.repository.list_by_category(school_id, category)
        return [AssetResponse.model_validate(a) for a in assets]

    async def update(self, asset_id: UUID, data: AssetUpdate, school_id: UUID, user_id: UUID) -> AssetResponse:
        """Update an asset."""
        asset = await self.repository.get_by_id_and_school(asset_id, school_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_asset = await self.repository.update(asset, update_data)
        return AssetResponse.model_validate(updated_asset)

    async def delete(self, asset_id: UUID, school_id: UUID) -> None:
        """Delete an asset."""
        asset = await self.repository.get_by_id_and_school(asset_id, school_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")

        await self.repository.delete(asset)
