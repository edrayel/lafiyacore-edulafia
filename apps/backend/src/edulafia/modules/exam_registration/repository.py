from __future__ import annotations
"""Exam registration repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.exam_registration.models import ExamRegistration


class ExamRegistrationRepository:
    """Repository for exam registration database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ExamRegistration:
        """Create a new exam registration."""
        registration = ExamRegistration(**data)
        self.db.add(registration)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def get_by_id(self, registration_id: UUID) -> ExamRegistration | None:
        """Get an exam registration by ID."""
        stmt = select(ExamRegistration).where(ExamRegistration.id == registration_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_and_exam(self, student_id: UUID, exam_type: str, year: int) -> ExamRegistration | None:
        """Get an exam registration by student, exam type, and year."""
        stmt = select(ExamRegistration).where(
            ExamRegistration.student_id == student_id,
            ExamRegistration.exam_type == exam_type,
            ExamRegistration.year == year,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[ExamRegistration]:
        """List all exam registrations for a school."""
        stmt = select(ExamRegistration).where(
            ExamRegistration.school_id == school_id
        ).order_by(ExamRegistration.registration_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_by_student(self, student_id: UUID) -> Sequence[ExamRegistration]:
        """List all exam registrations for a student."""
        stmt = select(ExamRegistration).where(
            ExamRegistration.student_id == student_id
        ).order_by(ExamRegistration.year.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, registration: ExamRegistration, data: dict) -> ExamRegistration:
        """Update an exam registration."""
        for key, value in data.items():
            if value is not None:
                setattr(registration, key, value)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def delete(self, registration: ExamRegistration) -> None:
        """Delete an exam registration."""
        await self.db.delete(registration)
        await self.db.flush()
