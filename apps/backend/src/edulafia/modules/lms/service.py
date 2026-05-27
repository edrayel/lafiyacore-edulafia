"""LMS Service."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.lms.models import Assignment, Submission
from edulafia.modules.lms.repository import LMSRepository
from edulafia.modules.lms.schemas import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentUpdateRequest,
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdateRequest,
)


class LMSService:
    def __init__(self, repository: LMSRepository):
        self.repository = repository

    # Assignments
    async def create_assignment(self, data: AssignmentCreate, school_id: UUID) -> Assignment:
        dump = data.model_dump()
        dump["school_id"] = school_id
        return await self.repository.create_assignment(dump)

    async def get_assignment(self, assignment_id: UUID, school_id: UUID) -> Assignment | None:
        return await self.repository.get_assignment_by_id(assignment_id, school_id)

    async def list_assignments(
        self,
        school_id: UUID,
        class_id: UUID | None = None,
        subject_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        assignments, total = await self.repository.list_assignments(
            school_id=school_id, class_id=class_id, subject_id=subject_id,
            page=page, per_page=per_page,
        )

        return {
            "items": [AssignmentResponse.model_validate(a) for a in assignments],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def update_assignment(self, assignment_id: UUID, data: AssignmentUpdateRequest, school_id: UUID) -> Assignment | None:
        assignment = await self.get_assignment(assignment_id, school_id)
        if not assignment:
            return None
        return await self.repository.update_assignment(assignment, data.model_dump(exclude_unset=True))

    async def delete_assignment(self, assignment_id: UUID, school_id: UUID) -> bool:
        assignment = await self.get_assignment(assignment_id, school_id)
        if not assignment:
            return False
        await self.repository.delete_assignment(assignment)
        return True

    # Submissions
    async def create_submission(self, data: SubmissionCreate, school_id: UUID) -> Submission:
        dump = data.model_dump()
        dump["school_id"] = school_id
        return await self.repository.create_submission(dump)

    async def get_submission(self, submission_id: UUID, school_id: UUID) -> Submission | None:
        return await self.repository.get_submission_by_id(submission_id, school_id)

    async def list_submissions(self, assignment_id: UUID, school_id: UUID) -> Sequence[Submission]:
        return await self.repository.list_submissions(assignment_id, school_id)

    async def update_submission(self, submission_id: UUID, data: SubmissionUpdateRequest, school_id: UUID) -> Submission | None:
        submission = await self.get_submission(submission_id, school_id)
        if not submission:
            return None
        return await self.repository.update_submission(submission, data.model_dump(exclude_unset=True))

    async def delete_submission(self, submission_id: UUID, school_id: UUID) -> bool:
        submission = await self.get_submission(submission_id, school_id)
        if not submission:
            return False
        await self.repository.delete_submission(submission)
        return True