from __future__ import annotations
"""Inventory repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.inventory.models import Asset


class AssetRepository:
    """Repository for asset database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Asset:
        """Create a new asset."""
        asset = Asset(**data)
        self.db.add(asset)
        await self.db.flush()
        await self.db.refresh(asset)
        return asset

    async def get_by_id(self, asset_id: UUID) -> Asset | None:
        """Get an asset by ID."""
        stmt = select(Asset).where(Asset.id == asset_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, asset_id: UUID, school_id: UUID) -> Asset | None:
        """Get an asset by ID scoped to school."""
        stmt = select(Asset).where(
            Asset.id == asset_id,
            Asset.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[Asset]:
        """List all assets for a school."""
        stmt = select(Asset).where(
            Asset.school_id == school_id
        ).order_by(Asset.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_category(self, school_id: UUID, category: str) -> Sequence[Asset]:
        """List assets by category for a school."""
        stmt = select(Asset).where(
            Asset.school_id == school_id,
            Asset.category == category,
        ).order_by(Asset.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, asset: Asset, data: dict) -> Asset:
        """Update an asset."""
        for key, value in data.items():
            if value is not None:
                setattr(asset, key, value)
        await self.db.flush()
        await self.db.refresh(asset)
        return asset

    async def delete(self, asset: Asset) -> None:
        """Delete an asset."""
        await self.db.delete(asset)
        await self.db.flush()
