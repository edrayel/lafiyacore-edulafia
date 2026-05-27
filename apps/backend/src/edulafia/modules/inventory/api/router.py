"""Inventory API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.inventory.repository import AssetRepository
from edulafia.modules.inventory.schemas import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)
from edulafia.modules.inventory.service import AssetService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


def get_asset_service(db: AsyncSession = Depends(get_db)) -> AssetService:
    """Dependency to get AssetService."""
    repository = AssetRepository(db)
    return AssetService(repository)


@router.post(
    "",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new asset",
)
async def create_asset(
    data: AssetCreate,
    current_user: CurrentUser,
    service: AssetService = Depends(get_asset_service),
) -> AssetResponse:
    """Create a new asset record."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
    summary="Get an asset by ID",
)
async def get_asset(
    asset_id: UUID,
    current_user: CurrentUser,
    service: AssetService = Depends(get_asset_service),
) -> AssetResponse:
    """Get an asset by ID."""
    asset = await service.get_by_id(
        asset_id=asset_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return asset


@router.get(
    "",
    response_model=list[AssetResponse],
    summary="List assets",
)
async def list_assets(
    current_user: CurrentUser,
    category: str | None = Query(None),
    service: AssetService = Depends(get_asset_service),
) -> list[AssetResponse]:
    """List all assets for the school, optionally filtered by category."""
    if category:
        return await service.list_by_category(
            school_id=UUID(current_user["school_id"]),
            category=category,
        )
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{asset_id}",
    response_model=AssetResponse,
    summary="Update an asset",
)
async def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    current_user: CurrentUser,
    service: AssetService = Depends(get_asset_service),
) -> AssetResponse:
    """Update an asset."""
    try:
        return await service.update(
            asset_id=asset_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{asset_id}",
    summary="Delete an asset",
)
async def delete_asset(
    asset_id: UUID,
    current_user: CurrentUser,
    service: AssetService = Depends(get_asset_service),
) -> dict:
    """Delete an asset."""
    try:
        await service.delete(
            asset_id=asset_id,
            school_id=UUID(current_user["school_id"]),
        )
        return {"message": "Asset deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
