"""Emergency API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.emergency.repository import EmergencyModeRepository
from edulafia.modules.emergency.schemas import (
    EmergencyModeCreate,
    EmergencyModeResponse,
)
from edulafia.modules.emergency.service import EmergencyModeService

router = APIRouter(prefix="/emergency", tags=["Emergency"])


def get_emergency_service(db: AsyncSession = Depends(get_db)) -> EmergencyModeService:
    """Dependency to get EmergencyModeService."""
    repository = EmergencyModeRepository(db)
    return EmergencyModeService(repository)


@router.post(
    "/activate",
    response_model=EmergencyModeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Activate emergency mode",
)
async def activate_emergency(
    data: EmergencyModeCreate,
    current_user: CurrentUser,
    service: EmergencyModeService = Depends(get_emergency_service),
) -> EmergencyModeResponse:
    """Activate emergency mode for the school."""
    try:
        return await service.activate(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/{mode_id}/deactivate",
    response_model=EmergencyModeResponse,
    summary="Deactivate emergency mode",
)
async def deactivate_emergency(
    mode_id: UUID,
    current_user: CurrentUser,
    service: EmergencyModeService = Depends(get_emergency_service),
) -> EmergencyModeResponse:
    """Deactivate an emergency mode."""
    result = await service.deactivate(mode_id=mode_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency mode not found",
        )
    return result


@router.get(
    "/active",
    response_model=EmergencyModeResponse,
    summary="Get active emergency mode",
)
async def get_active_emergency(
    current_user: CurrentUser,
    service: EmergencyModeService = Depends(get_emergency_service),
) -> EmergencyModeResponse:
    """Get the currently active emergency mode."""
    result = await service.get_active(school_id=UUID(current_user["school_id"]))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active emergency mode",
        )
    return result


@router.get(
    "",
    response_model=list[EmergencyModeResponse],
    summary="List emergency modes",
)
async def list_emergency_modes(
    current_user: CurrentUser,
    service: EmergencyModeService = Depends(get_emergency_service),
) -> list[EmergencyModeResponse]:
    """List all emergency modes for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))
