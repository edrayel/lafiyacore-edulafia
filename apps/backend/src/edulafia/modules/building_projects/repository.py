from __future__ import annotations
"""Building projects repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.building_projects.models import Project


class ProjectRepository:
    """Repository for building project database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Project:
        """Create a new building project."""
        project = Project(**data)
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def get_by_id(self, project_id: UUID) -> Project | None:
        """Get a building project by ID."""
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, project_id: UUID, school_id: UUID) -> Project | None:
        """Get a building project by ID scoped to school."""
        stmt = select(Project).where(
            Project.id == project_id,
            Project.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[Project]:
        """List all building projects for a school."""
        stmt = select(Project).where(
            Project.school_id == school_id
        ).order_by(Project.start_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_status(self, school_id: UUID, status: str) -> Sequence[Project]:
        """List building projects by status for a school."""
        stmt = select(Project).where(
            Project.school_id == school_id,
            Project.status == status,
        ).order_by(Project.start_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, project: Project, data: dict) -> Project:
        """Update a building project."""
        for key, value in data.items():
            if value is not None:
                setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        """Delete a building project."""
        await self.db.delete(project)
        await self.db.flush()
