"""Cafeteria API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.cafeteria.repository import MealPlanRepository
from edulafia.modules.cafeteria.schemas import (
    MealPlanCreate,
    MealPlanResponse,
    MealPlanUpdate,
)
from edulafia.modules.cafeteria.service import MealPlanService

router = APIRouter(prefix="/cafeteria", tags=["Cafeteria"])


def get_meal_plan_service(db: AsyncSession = Depends(get_db)) -> MealPlanService:
    """Dependency to get MealPlanService."""
    repository = MealPlanRepository(db)
    return MealPlanService(repository)


@router.post(
    "",
    response_model=MealPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a meal plan",
)
async def create_meal_plan(
    data: MealPlanCreate,
    current_user: CurrentUser,
    service: MealPlanService = Depends(get_meal_plan_service),
) -> MealPlanResponse:
    """Create a new meal plan."""
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
    "/{plan_id}",
    response_model=MealPlanResponse,
    summary="Get a meal plan by ID",
)
async def get_meal_plan(
    plan_id: UUID,
    current_user: CurrentUser,
    service: MealPlanService = Depends(get_meal_plan_service),
) -> MealPlanResponse:
    """Get a meal plan by ID."""
    plan = await service.get_by_id(
        plan_id=plan_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )
    return plan


@router.get(
    "",
    response_model=list[MealPlanResponse],
    summary="List meal plans",
)
async def list_meal_plans(
    current_user: CurrentUser,
    service: MealPlanService = Depends(get_meal_plan_service),
) -> list[MealPlanResponse]:
    """List all meal plans for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{plan_id}",
    response_model=MealPlanResponse,
    summary="Update a meal plan",
)
async def update_meal_plan(
    plan_id: UUID,
    data: MealPlanUpdate,
    current_user: CurrentUser,
    service: MealPlanService = Depends(get_meal_plan_service),
) -> MealPlanResponse:
    """Update a meal plan."""
    try:
        return await service.update(
            plan_id=plan_id,
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
    "/{plan_id}",
    summary="Delete a meal plan",
)
async def delete_meal_plan(
    plan_id: UUID,
    current_user: CurrentUser,
    service: MealPlanService = Depends(get_meal_plan_service),
) -> dict:
    """Delete a meal plan."""
    plan = await service.get_by_id(
        plan_id=plan_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )
    await service.delete(plan_id, UUID(current_user['school_id']))
    return {"message": "Meal plan deleted"}
