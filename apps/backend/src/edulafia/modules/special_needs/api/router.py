"""Special needs / IEP API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.special_needs.repository import IEPRepository
from edulafia.modules.special_needs.schemas import (
    IEPCreate,
    IEPResponse,
    IEPUpdate,
)
from edulafia.modules.special_needs.service import IEPService

router = APIRouter(prefix="/special-needs", tags=["Special Needs"])


def get_iep_service(db: AsyncSession = Depends(get_db)) -> IEPService:
    """Dependency to get IEPService."""
    repository = IEPRepository(db)
    return IEPService(repository)


@router.post(
    "",
    response_model=IEPResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new IEP",
)
async def create_iep(
    data: IEPCreate,
    current_user: CurrentUser,
    service: IEPService = Depends(get_iep_service),
) -> IEPResponse:
    """Create a new Individual Education Plan."""
    try:
        return await service.create(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/student/{student_id}",
    response_model=IEPResponse,
    summary="Get IEP by student",
)
async def get_iep_by_student(
    student_id: UUID,
    current_user: CurrentUser,
    service: IEPService = Depends(get_iep_service),
) -> IEPResponse:
    """Get the IEP for a specific student."""
    iep = await service.get_by_student(student_id=student_id)
    if not iep:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IEP not found for student",
        )
    return iep


@router.get(
    "",
    response_model=list[IEPResponse],
    summary="List IEPs",
)
async def list_ieps(
    current_user: CurrentUser,
    service: IEPService = Depends(get_iep_service),
) -> list[IEPResponse]:
    """List all IEPs for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/student/{student_id}",
    response_model=IEPResponse,
    summary="Update an IEP",
)
async def update_iep(
    student_id: UUID,
    data: IEPUpdate,
    current_user: CurrentUser,
    service: IEPService = Depends(get_iep_service),
) -> IEPResponse:
    """Update an IEP for a student."""
    result = await service.update(
        student_id=student_id,
        data=data,
        user_id=UUID(current_user["sub"]),
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IEP not found for student",
        )
    return result
