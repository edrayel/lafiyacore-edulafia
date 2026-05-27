"""Bus tracking API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.bus_tracking.repository import BusRouteRepository
from edulafia.modules.bus_tracking.schemas import (
    BusRouteCreate,
    BusRouteResponse,
    BusRouteUpdate,
)
from edulafia.modules.bus_tracking.service import BusRouteService

router = APIRouter(prefix="/bus-tracking", tags=["Bus Tracking"])


def get_bus_route_service(db: AsyncSession = Depends(get_db)) -> BusRouteService:
    """Dependency to get BusRouteService."""
    repository = BusRouteRepository(db)
    return BusRouteService(repository)


@router.post(
    "",
    response_model=BusRouteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a bus route",
)
async def create_bus_route(
    data: BusRouteCreate,
    current_user: CurrentUser,
    service: BusRouteService = Depends(get_bus_route_service),
) -> BusRouteResponse:
    """Create a new bus route."""
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
    "/{route_id}",
    response_model=BusRouteResponse,
    summary="Get a bus route by ID",
)
async def get_bus_route(
    route_id: UUID,
    current_user: CurrentUser,
    service: BusRouteService = Depends(get_bus_route_service),
) -> BusRouteResponse:
    """Get a bus route by ID."""
    route = await service.get_by_id(
        route_id=route_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus route not found",
        )
    return route


@router.get(
    "",
    response_model=list[BusRouteResponse],
    summary="List bus routes",
)
async def list_bus_routes(
    current_user: CurrentUser,
    service: BusRouteService = Depends(get_bus_route_service),
) -> list[BusRouteResponse]:
    """List all bus routes for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{route_id}",
    response_model=BusRouteResponse,
    summary="Update a bus route",
)
async def update_bus_route(
    route_id: UUID,
    data: BusRouteUpdate,
    current_user: CurrentUser,
    service: BusRouteService = Depends(get_bus_route_service),
) -> BusRouteResponse:
    """Update a bus route."""
    try:
        return await service.update(
            route_id=route_id,
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
    "/{route_id}",
    summary="Delete a bus route",
)
async def delete_bus_route(
    route_id: UUID,
    current_user: CurrentUser,
    service: BusRouteService = Depends(get_bus_route_service),
) -> dict:
    """Delete a bus route."""
    route = await service.get_by_id(
        route_id=route_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus route not found",
        )
    await service.delete(route_id, UUID(current_user['school_id']))
    return {"message": "Bus route deleted"}
