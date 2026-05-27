"""Admission service for business logic operations."""

from uuid import UUID

from edulafia.modules.admissions.repository import ApplicationRepository
from edulafia.modules.admissions.schemas import (
    ApplicationCreate,
    ApplicationFilters,
    ApplicationListResponse,
    ApplicationResponse,
    ApplicationUpdate,
)


class ApplicationService:
    """Service for application business logic."""

    def __init__(self, repository: ApplicationRepository):
        self.repository = repository

    async def create(
        self,
        data: ApplicationCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> ApplicationResponse:
        """Create a new application."""
        application_data = data.model_dump()
        application_data["school_id"] = school_id
        application_data["created_by"] = user_id

        application = await self.repository.create(application_data)
        return ApplicationResponse.model_validate(application)

    async def get_by_id(
        self,
        application_id: UUID,
        school_id: UUID,
    ) -> ApplicationResponse | None:
        """Get an application by ID."""
        application = await self.repository.get_by_id(application_id, school_id)
        if application:
            return ApplicationResponse.model_validate(application)
        return None

    async def list_applications(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
        filters: ApplicationFilters | None = None,
    ) -> ApplicationListResponse:
        """List applications with pagination and filters."""
        applications, total = await self.repository.list(
            school_id=school_id,
            page=page,
            per_page=per_page,
            filters=filters,
        )

        pages = (total + per_page - 1) // per_page

        return ApplicationListResponse(
            items=[ApplicationResponse.model_validate(a) for a in applications],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

    async def update(
        self,
        application_id: UUID,
        data: ApplicationUpdate,
        school_id: UUID,
    ) -> ApplicationResponse:
        """Update an application."""
        application = await self.repository.get_by_id(application_id, school_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_application = await self.repository.update(application, update_data)
        return ApplicationResponse.model_validate(updated_application)

    async def delete(self, application_id: UUID, school_id: UUID) -> None:
        """Soft delete an application."""
        application = await self.repository.get_by_id_and_school(application_id, school_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")
        await self.repository.delete(application)

    async def approve(
        self,
        application_id: UUID,
        school_id: UUID,
    ) -> ApplicationResponse:
        """Approve an application."""
        application = await self.repository.get_by_id(application_id, school_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.status = "approved"
        updated_application = await self.repository.update(application, {})
        return ApplicationResponse.model_validate(updated_application)

    async def reject(
        self,
        application_id: UUID,
        school_id: UUID,
    ) -> ApplicationResponse:
        """Reject an application."""
        application = await self.repository.get_by_id(application_id, school_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.status = "rejected"
        updated_application = await self.repository.update(application, {})
        return ApplicationResponse.model_validate(updated_application)

    async def enroll(
        self,
        application_id: UUID,
        school_id: UUID,
    ) -> ApplicationResponse:
        """Mark an application as enrolled."""
        application = await self.repository.get_by_id(application_id, school_id)
        if not application:
            raise ValueError(f"Application {application_id} not found")

        application.status = "enrolled"
        updated_application = await self.repository.update(application, {})
        return ApplicationResponse.model_validate(updated_application)
