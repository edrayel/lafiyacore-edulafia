"""Building projects service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.building_projects.repository import ProjectRepository
from edulafia.modules.building_projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)


class ProjectService:
    """Service for building project business logic."""

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create(self, data: ProjectCreate, user_id: UUID) -> ProjectResponse:
        """Create a new building project."""
        project_data = data.model_dump()
        project = await self.repository.create(project_data)
        return ProjectResponse.model_validate(project)

    async def get_by_id(self, project_id: UUID, school_id: UUID) -> ProjectResponse | None:
        """Get a building project by ID."""
        project = await self.repository.get_by_id_and_school(project_id, school_id)
        if project:
            return ProjectResponse.model_validate(project)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[ProjectResponse]:
        """List all building projects for a school."""
        projects = await self.repository.list_by_school(school_id)
        return [ProjectResponse.model_validate(p) for p in projects]

    async def list_by_status(self, school_id: UUID, status: str) -> Sequence[ProjectResponse]:
        """List building projects by status."""
        projects = await self.repository.list_by_status(school_id, status)
        return [ProjectResponse.model_validate(p) for p in projects]

    async def update(self, project_id: UUID, data: ProjectUpdate, school_id: UUID, user_id: UUID) -> ProjectResponse:
        """Update a building project."""
        project = await self.repository.get_by_id_and_school(project_id, school_id)
        if not project:
            raise ValueError(f"Building project {project_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_project = await self.repository.update(project, update_data)
        return ProjectResponse.model_validate(updated_project)

    async def update_progress(self, project_id: UUID, progress_percent: int, school_id: UUID) -> ProjectResponse:
        """Update the progress of a building project."""
        project = await self.repository.get_by_id_and_school(project_id, school_id)
        if not project:
            raise ValueError(f"Building project {project_id} not found")

        update_data = {"progress_percent": progress_percent}
        if progress_percent >= 100:
            update_data["status"] = "completed"

        updated_project = await self.repository.update(project, update_data)
        return ProjectResponse.model_validate(updated_project)
