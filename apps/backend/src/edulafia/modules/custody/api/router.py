"""Custody API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.custody.repository import CustodyOrderRepository
from edulafia.modules.custody.schemas import (
    CustodyOrderCreate,
    CustodyOrderResponse,
    CustodyOrderUpdate,
)
from edulafia.modules.custody.service import CustodyOrderService

router = APIRouter(prefix="/custody", tags=["Custody"])


def get_custody_service(db: AsyncSession = Depends(get_db)) -> CustodyOrderService:
    """Dependency to get CustodyOrderService."""
    repository = CustodyOrderRepository(db)
    return CustodyOrderService(repository)


@router.post(
    "",
    response_model=CustodyOrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a custody order",
)
async def create_custody_order(
    data: CustodyOrderCreate,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> CustodyOrderResponse:
    """Create a new custody order."""
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
    "/{order_id}",
    response_model=CustodyOrderResponse,
    summary="Get a custody order by ID",
)
async def get_custody_order(
    order_id: UUID,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> CustodyOrderResponse:
    """Get a custody order by ID."""
    order = await service.get_by_id(order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Custody order not found",
        )
    return order


@router.get(
    "/student/{student_id}",
    response_model=list[CustodyOrderResponse],
    summary="Get custody orders for a student",
)
async def get_student_custody_orders(
    student_id: UUID,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> list[CustodyOrderResponse]:
    """Get all custody orders for a student."""
    return await service.get_by_student_id(student_id=student_id)


@router.patch(
    "/{order_id}",
    response_model=CustodyOrderResponse,
    summary="Update a custody order",
)
async def update_custody_order(
    order_id: UUID,
    data: CustodyOrderUpdate,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> CustodyOrderResponse:
    """Update a custody order."""
    try:
        return await service.update(
            order_id=order_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/{order_id}/revoke",
    response_model=CustodyOrderResponse,
    summary="Revoke a custody order",
)
async def revoke_custody_order(
    order_id: UUID,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> CustodyOrderResponse:
    """Revoke a custody order."""
    try:
        return await service.revoke(
            order_id=order_id,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{order_id}",
    summary="Delete a custody order",
)
async def delete_custody_order(
    order_id: UUID,
    current_user: CurrentUser,
    service: CustodyOrderService = Depends(get_custody_service),
) -> dict:
    """Delete a custody order."""
    order = await service.get_by_id(order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Custody order not found",
        )
    await service.delete(order_id)
    return {"message": "Custody order deleted"}
