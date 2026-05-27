import os
import re

svc_file = 'apps/backend/src/edulafia/modules/guardians/service.py'
router_file = 'apps/backend/src/edulafia/modules/guardians/api/guardians.py'

# Update Service
with open(svc_file, 'r') as f:
    svc_content = f.read()

if 'async def get_guardian_students(' not in svc_content:
    new_method = """
    async def get_guardian_students(self, guardian_id: UUID, school_id: UUID):
        \"\"\"Get all students linked to a guardian.\"\"\"
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
"""
    svc_content += new_method
    with open(svc_file, 'w') as f:
        f.write(svc_content)
    print("Patched guardian service")

# Update Router
with open(router_file, 'r') as f:
    router_content = f.read()

if 'async def get_guardian_students(' not in router_content:
    new_route = """
from edulafia.modules.students.schemas import StudentResponse

@router.get(
    "/{guardian_id}/students",
    response_model=list[StudentResponse],
    summary="Get all students linked to a guardian",
)
async def get_guardian_students(
    guardian_id: UUID,
    current_user: CurrentUser,
    service: GuardianService = Depends(get_guardian_service),
) -> list[StudentResponse]:
    \"\"\"Get all students linked to a guardian.\"\"\"
    return await service.get_guardian_students(
        guardian_id=guardian_id,
        school_id=UUID(current_user["school_id"]),
    )
"""
    router_content += new_route
    with open(router_file, 'w') as f:
        f.write(router_content)
    print("Patched guardian router")
