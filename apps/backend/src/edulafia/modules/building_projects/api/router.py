"""Building projects API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.building_projects.repository import ProjectRepository
from edulafia.modules.building_projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from edulafia.modules.building_projects.service import ProjectService

router = APIRouter(prefix="/projects", tags=["Building Projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    """Dependency to get ProjectService."""
    repository = ProjectRepository(db)
    return ProjectService(repository)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a building project",
)
async def create_project(
    data: ProjectCreate,
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Create a new building project."""
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
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a building project by ID",
)
async def get_project(
    project_id: UUID,
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Get a building project by ID."""
    project = await service.get_by_id(
        project_id=project_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building project not found",
        )
    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="List building projects",
)
async def list_projects(
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    """List all building projects for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.get(
    "/status/{status}",
    response_model=list[ProjectResponse],
    summary="List building projects by status",
)
async def list_projects_by_status(
    status: str,
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    """List building projects by status."""
    return await service.list_by_status(
        school_id=UUID(current_user["school_id"]),
        status=status,
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a building project",
)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Update a building project."""
    try:
        return await service.update(
            project_id=project_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/{project_id}/progress",
    response_model=ProjectResponse,
    summary="Update project progress",
)
async def update_project_progress(
    project_id: UUID,
    progress_percent: int,
    current_user: CurrentUser,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """Update the progress of a building project."""
    try:
        return await service.update_progress(
            project_id=project_id,
            progress_percent=progress_percent,
            school_id=UUID(current_user["school_id"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
