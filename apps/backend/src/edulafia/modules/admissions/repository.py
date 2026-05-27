from __future__ import annotations
"""Admission repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.admissions.models import Application
from edulafia.modules.admissions.schemas import ApplicationFilters


class ApplicationRepository:
    """Repository for application database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Application:
        """Create a new application."""
        application = Application(**data)
        self.db.add(application)
        await self.db.flush()
        await self.db.refresh(application)
        return application

    async def get_by_id(self, application_id: UUID, school_id: UUID) -> Application | None:
        """Get an application by ID, scoped to school."""
        stmt = select(Application).where(
            Application.id == application_id,
            Application.school_id == school_id,
            Application.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
        filters: ApplicationFilters | None = None,
    ) -> tuple[Sequence[Application], int]:
        """List applications with pagination and filters."""
        stmt = select(Application).where(
            Application.school_id == school_id,
            Application.deleted_at.is_(None),
        )

        if filters:
            if filters.status:
                stmt = stmt.where(Application.status == filters.status)
            if filters.class_applied_for:
                stmt = stmt.where(Application.class_applied_for == filters.class_applied_for)
            if filters.admission_year:
                stmt = stmt.where(Application.admission_year == filters.admission_year)
            if filters.gender:
                stmt = stmt.where(Application.gender == filters.gender.lower())
            if filters.search:
                search_term = f"%{filters.search}%"
                stmt = stmt.where(
                    (Application.first_name.ilike(search_term))
                    | (Application.last_name.ilike(search_term))
                )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Application.created_at.desc())

        result = await self.db.execute(stmt)
        applications = result.scalars().all()

        return applications, total

    async def update(self, application: Application, data: dict) -> Application:
        """Update an application."""
        for key, value in data.items():
            if value is not None:
                setattr(application, key, value)
        await self.db.flush()
        await self.db.refresh(application)
        return application

    async def soft_delete(self, application: Application) -> Application:
        """Soft delete an application."""
        application.deleted_at = datetime.now(UTC)
        await self.db.flush()
        await self.db.refresh(application)
        return application
