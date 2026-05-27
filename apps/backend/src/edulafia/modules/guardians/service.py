"""Guardian service for business logic operations."""

from uuid import UUID

from edulafia.modules.guardians.repository import GuardianRepository
from edulafia.modules.guardians.schemas import (
    GuardianCreate,
    GuardianResponse,
    GuardianUpdate,
)


class GuardianService:
    """Service for guardian business logic."""

    MAX_GUARDIANS_PER_STUDENT = 2

    def __init__(self, repository: GuardianRepository):
        self.repository = repository

    async def create(
        self,
        data: GuardianCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> GuardianResponse:
        """Create a new guardian."""
        # Check for duplicate NIN if provided
        if data.nin and await self.repository.exists_by_nin(data.nin):
            raise ValueError(f"NIN already exists: {data.nin}")

        # Prepare data
        guardian_data = data.model_dump(exclude={"is_primary", "is_emergency_contact"})
        guardian_data["school_id"] = school_id

        # Auto-provision portal access if WhatsApp number provided
        if data.whatsapp_number:
            guardian_data["portal_access"] = True

        # Create guardian
        guardian = await self.repository.create(guardian_data)
        return GuardianResponse.model_validate(guardian)

    async def get_by_id(
        self,
        guardian_id: UUID,
        school_id: UUID,
    ) -> GuardianResponse | None:
        """Get a guardian by ID."""
        guardian = await self.repository.get_by_id(guardian_id, school_id)
        if guardian:
            return GuardianResponse.model_validate(guardian)
        return None

    async def list_guardians(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List guardians with pagination."""
        guardians, total = await self.repository.list(
            school_id=school_id,
            page=page,
            per_page=per_page,
        )

        pages = (total + per_page - 1) // per_page

        return {
            "items": [GuardianResponse.model_validate(g) for g in guardians],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }

    async def update(
        self,
        guardian_id: UUID,
        data: GuardianUpdate,
        school_id: UUID,
    ) -> GuardianResponse:
        """Update a guardian."""
        guardian = await self.repository.get_by_id(guardian_id, school_id)
        if not guardian:
            raise ValueError("Guardian not found")

        # Prepare update data
        update_data = data.model_dump(exclude_none=True)

        updated_guardian = await self.repository.update(guardian, update_data)
        return GuardianResponse.model_validate(updated_guardian)

    async def archive(
        self,
        guardian_id: UUID,
        school_id: UUID,
    ) -> GuardianResponse:
        """Archive (soft delete) a guardian."""
        guardian = await self.repository.get_by_id(guardian_id, school_id)
        if not guardian:
            raise ValueError("Guardian not found")

        archived_guardian = await self.repository.soft_delete(guardian)
        return GuardianResponse.model_validate(archived_guardian)

    async def link_to_student(
        self,
        student_id: UUID,
        guardian_id: UUID,
        is_primary: bool = False,
        is_emergency_contact: bool = False,
        can_pickup: bool = True,
    ) -> dict:
        """Link a guardian to a student."""
        # Check max guardians limit
        count = await self.repository.get_guardian_count_for_student(student_id)
        if count >= self.MAX_GUARDIANS_PER_STUDENT:
            raise ValueError(
                f"Student already has maximum {self.MAX_GUARDIANS_PER_STUDENT} guardians"
            )

        # Check if setting as primary
        if is_primary:
            # Remove primary flag from any existing primary guardian
            await self.repository.clear_primary_for_student(student_id)

        link = await self.repository.link_to_student(
            student_id=student_id,
            guardian_id=guardian_id,
            is_primary=is_primary,
            is_emergency_contact=is_emergency_contact,
            can_pickup=can_pickup,
        )

        return {
            "student_id": link.student_id,
            "guardian_id": link.guardian_id,
            "is_primary": link.is_primary,
            "is_emergency_contact": link.is_emergency_contact,
            "can_pickup": link.can_pickup,
        }

    async def get_student_guardians(
        self,
        student_id: UUID,
    ) -> list[GuardianResponse]:
        """Get all guardians for a student."""
        guardians = await self.repository.get_student_guardians(student_id)
        return [GuardianResponse.model_validate(g) for g in guardians]

    async def unlink_from_student(
        self,
        student_id: UUID,
        guardian_id: UUID,
    ) -> bool:
        """Unlink a guardian from a student."""
        # Check if this is the last guardian
        count = await self.repository.get_guardian_count_for_student(student_id)
        if count <= 1:
            raise ValueError("Cannot remove the last guardian from a student")

        return await self.repository.unlink_from_student(student_id, guardian_id)

    async def get_guardian_students(self, guardian_id: UUID, school_id: UUID):
        """Get all students linked to a guardian."""
        from edulafia.modules.students.schemas import StudentResponse
        from edulafia.modules.students.models import Student
        from edulafia.modules.guardians.models import StudentGuardian
        from sqlalchemy import select
        
        stmt = (
            select(Student)
            .join(StudentGuardian, Student.id == StudentGuardian.student_id)
            .where(
                StudentGuardian.guardian_id == guardian_id,
                Student.school_id == school_id
            )
        )
        result = await self.repository.session.execute(stmt)
        students = result.scalars().all()
        return [StudentResponse.model_validate(s) for s in students]
