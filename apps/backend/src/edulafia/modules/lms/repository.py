from __future__ import annotations
"""LMS Repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.lms.models import Assignment, Submission


class LMSRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Assignments
    async def create_assignment(self, data: dict) -> Assignment:
        assignment = Assignment(**data)
        self.db.add(assignment)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def get_assignment_by_id(self, assignment_id: UUID, school_id: UUID) -> Assignment | None:
        stmt = select(Assignment).where(
            Assignment.id == assignment_id,
            Assignment.school_id == school_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_assignments(
        self,
        school_id: UUID,
        class_id: UUID | None = None,
        subject_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[Assignment], int]:
        stmt = select(Assignment).where(Assignment.school_id == school_id)
        if class_id:
            stmt = stmt.where(Assignment.class_id == class_id)
        if subject_id:
            stmt = stmt.where(Assignment.subject_id == subject_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Assignment.created_at.desc())

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def update_assignment(self, assignment: Assignment, data: dict) -> Assignment:
        for key, value in data.items():
            if value is not None:
                setattr(assignment, key, value)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def delete_assignment(self, assignment: Assignment) -> None:
        await self.db.delete(assignment)
        await self.db.flush()

    # Submissions
    async def create_submission(self, data: dict) -> Submission:
        submission = Submission(**data)
        self.db.add(submission)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def get_submission_by_id(self, submission_id: UUID, school_id: UUID) -> Submission | None:
        stmt = select(Submission).where(
            Submission.id == submission_id,
            Submission.school_id == school_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_submissions(self, assignment_id: UUID, school_id: UUID) -> Sequence[Submission]:
        stmt = select(Submission).where(
            Submission.assignment_id == assignment_id,
            Submission.school_id == school_id
        ).order_by(Submission.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_submission(self, submission: Submission, data: dict) -> Submission:
        for key, value in data.items():
            if value is not None:
                setattr(submission, key, value)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def delete_submission(self, submission: Submission) -> None:
        await self.db.delete(submission)
        await self.db.flush()