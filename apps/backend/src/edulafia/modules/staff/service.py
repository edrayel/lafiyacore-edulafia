"""Staff service for business logic operations."""

from uuid import UUID

from edulafia.modules.staff.exceptions import (
    AssignmentNotFoundError,
    DuplicateAssignmentError,
    DuplicateStaffIdError,
    FormTeacherAlreadyAssignedError,
    MaxLoadExceededError,
    StaffNotFoundError,
)
from edulafia.modules.staff.repository import (
    StaffAssignmentRepository,
    StaffRepository,
)
from edulafia.modules.staff.schemas import (
    StaffAssignmentCreate,
    StaffAssignmentResponse,
    StaffCreate,
    StaffDeactivate,
    StaffResponse,
    StaffUpdate,
)

# Maximum teaching load per teacher (configurable)
MAX_TEACHING_LOAD = 30


class StaffService:
    """Service for staff management."""

    def __init__(self, repository: StaffRepository):
        self.repository = repository

    async def create_staff(
        self,
        data: StaffCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> StaffResponse:
        """Create a new staff member."""
        # Generate staff ID
        role_prefix = "TCH" if data.role == "teacher" else "STF"
        staff_id = await self.repository.get_next_staff_id(school_id, role_prefix)

        # Check for duplicate (shouldn't happen with generated ID, but safe check)
        if await self.repository.exists_by_staff_id(staff_id, school_id):
            raise DuplicateStaffIdError(staff_id)

        # Create staff
        staff_data = data.model_dump(exclude_none=True)
        staff_data["school_id"] = school_id
        staff_data["staff_id"] = staff_id
        staff_data["created_by"] = user_id
        staff_data["updated_by"] = user_id

        staff = await self.repository.create(staff_data)
        return StaffResponse.model_validate(staff)

    async def get_staff(
        self,
        staff_id: UUID,
        school_id: UUID,
    ) -> StaffResponse:
        """Get staff by ID."""
        staff = await self.repository.get_by_id(staff_id, school_id)
        if not staff:
            raise StaffNotFoundError(str(staff_id))
        return StaffResponse.model_validate(staff)

    async def list_staff(
        self,
        school_id: UUID,
        role: str | None = None,
        department: str | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List staff with filters."""
        staff_list, total = await self.repository.list(
            school_id=school_id,
            role=role,
            department=department,
            status=status,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [StaffResponse.model_validate(s) for s in staff_list],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def update_staff(
        self,
        staff_id: UUID,
        data: StaffUpdate,
        school_id: UUID,
        user_id: UUID,
        is_self: bool = False,
    ) -> StaffResponse:
        """Update staff information."""
        staff = await self.repository.get_by_id(staff_id, school_id)
        if not staff:
            raise StaffNotFoundError(str(staff_id))

        # If self-update, restrict fields
        if is_self:
            allowed_fields = [
                "email", "phone", "whatsapp_phone", "address",
                "next_of_kin", "emergency_contact"
            ]
            update_data = {
                k: v for k, v in data.model_dump(exclude_none=True).items()
                if k in allowed_fields
            }
        else:
            update_data = data.model_dump(exclude_none=True)

        update_data["updated_by"] = user_id

        updated_staff = await self.repository.update(staff, update_data)
        return StaffResponse.model_validate(updated_staff)

    async def deactivate_staff(
        self,
        staff_id: UUID,
        data: StaffDeactivate,
        school_id: UUID,
    ) -> StaffResponse:
        """Deactivate a staff member."""
        staff = await self.repository.get_by_id(staff_id, school_id)
        if not staff:
            raise StaffNotFoundError(str(staff_id))

        deactivated_staff = await self.repository.deactivate(
            staff, data.reason, data.exit_date
        )
        return StaffResponse.model_validate(deactivated_staff)


class AssignmentService:
    """Service for staff assignment management."""

    def __init__(
        self,
        assignment_repo: StaffAssignmentRepository,
        staff_repo: StaffRepository,
    ):
        self.assignment_repo = assignment_repo
        self.staff_repo = staff_repo

    async def create_assignment(
        self,
        data: StaffAssignmentCreate,
        user_id: UUID,
    ) -> StaffAssignmentResponse:
        """Create a staff assignment."""
        # Check for duplicate
        if await self.assignment_repo.exists_duplicate(
            data.staff_id,
            data.class_id,
            data.subject_id,
            data.academic_year_id,
        ):
            raise DuplicateAssignmentError(
                str(data.staff_id), str(data.class_id), str(data.subject_id)
            )

        # Check form teacher constraint
        if data.is_form_teacher:
            if await self.assignment_repo.has_form_teacher(
                data.class_id, data.academic_year_id
            ):
                raise FormTeacherAlreadyAssignedError(str(data.class_id))

        # Check teaching load
        if data.subject_id:
            current_load = await self.assignment_repo.get_teacher_load(
                data.staff_id, data.academic_year_id
            )
            if current_load >= MAX_TEACHING_LOAD:
                raise MaxLoadExceededError(
                    str(data.staff_id), current_load, MAX_TEACHING_LOAD
                )

        # Create assignment
        assignment_data = data.model_dump()
        assignment = await self.assignment_repo.create(assignment_data)
        return StaffAssignmentResponse.model_validate(assignment)

    async def list_assignments(
        self,
        school_id: UUID,
        staff_id: UUID | None = None,
        class_id: UUID | None = None,
        academic_year_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List staff assignments with pagination."""
        assignments, total = await self.assignment_repo.list_assignments(
            school_id=school_id,
            staff_id=staff_id,
            class_id=class_id,
            academic_year_id=academic_year_id,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [StaffAssignmentResponse.model_validate(a) for a in assignments],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def delete_assignment(self, assignment_id: UUID, school_id: UUID) -> bool:
        """Delete an assignment."""
        assignment = await self.assignment_repo.get_by_id(assignment_id)
        if not assignment or assignment.school_id != school_id:
            raise AssignmentNotFoundError(f"Assignment {assignment_id} not found")
        return await self.assignment_repo.delete(assignment_id)

    async def bulk_create_assignments(
        self,
        assignments: list[StaffAssignmentCreate],
        user_id: UUID,
    ) -> dict:
        """Bulk create assignments with validation."""
        created = []
        errors = []

        for i, assignment_data in enumerate(assignments):
            try:
                result = await self.create_assignment(assignment_data, user_id)
                created.append(result)
            except Exception as e:
                errors.append({
                    "index": i,
                    "data": assignment_data.model_dump(),
                    "error": str(e),
                })

        return {
            "created_count": len(created),
            "error_count": len(errors),
            "created": created,
            "errors": errors,
        }
