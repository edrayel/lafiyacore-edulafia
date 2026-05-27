from __future__ import annotations
"""Guardian repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.guardians.models import Guardian
from edulafia.modules.guardians.student_guardian import StudentGuardian


class GuardianRepository:
    """Repository for guardian database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Guardian:
        """Create a new guardian."""
        guardian = Guardian(**data)
        self.db.add(guardian)
        await self.db.flush()
        await self.db.refresh(guardian)
        return guardian

    async def get_by_id(self, guardian_id: UUID, school_id: UUID) -> Guardian | None:
        """Get a guardian by ID, scoped to school."""
        stmt = select(Guardian).where(
            Guardian.id == guardian_id,
            Guardian.school_id == school_id,
            Guardian.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_nin(self, nin: str) -> bool:
        """Check if a guardian with the given NIN exists."""
        stmt = (
            select(func.count())
            .select_from(Guardian)
            .where(
                Guardian.nin == nin,
                Guardian.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count > 0

    async def list(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[Guardian], int]:
        """List guardians with pagination."""
        stmt = select(Guardian).where(
            Guardian.school_id == school_id,
            Guardian.deleted_at.is_(None),
        )

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Guardian.created_at.desc())

        result = await self.db.execute(stmt)
        guardians = result.scalars().all()

        return guardians, total

    async def update(self, guardian: Guardian, data: dict) -> Guardian:
        """Update a guardian."""
        for key, value in data.items():
            if value is not None:
                setattr(guardian, key, value)
        await self.db.flush()
        await self.db.refresh(guardian)
        return guardian

    async def soft_delete(self, guardian: Guardian) -> Guardian:
        """Soft delete a guardian."""
        guardian.deleted_at = func.now()
        await self.db.flush()
        await self.db.refresh(guardian)
        return guardian

    async def link_to_student(
        self,
        student_id: UUID,
        guardian_id: UUID,
        is_primary: bool = False,
        is_emergency_contact: bool = False,
        can_pickup: bool = True,
    ) -> StudentGuardian:
        """Link a guardian to a student."""
        link = StudentGuardian(
            student_id=student_id,
            guardian_id=guardian_id,
            is_primary=is_primary,
            is_emergency_contact=is_emergency_contact,
            can_pickup=can_pickup,
        )
        self.db.add(link)
        await self.db.flush()
        await self.db.refresh(link)
        return link

    async def get_student_guardians(
        self,
        student_id: UUID,
    ) -> Sequence[Guardian]:
        """Get all guardians for a student."""
        stmt = (
            select(Guardian)
            .join(StudentGuardian, Guardian.id == StudentGuardian.guardian_id)
            .where(
                StudentGuardian.student_id == student_id,
                Guardian.deleted_at.is_(None),
            )
            .order_by(StudentGuardian.is_primary.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_guardian_count_for_student(self, student_id: UUID) -> int:
        """Get the count of guardians linked to a student."""
        stmt = (
            select(func.count())
            .select_from(StudentGuardian)
            .where(StudentGuardian.student_id == student_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def unlink_from_student(
        self,
        student_id: UUID,
        guardian_id: UUID,
    ) -> bool:
        """Unlink a guardian from a student."""
        stmt = select(StudentGuardian).where(
            StudentGuardian.student_id == student_id,
            StudentGuardian.guardian_id == guardian_id,
        )
        result = await self.db.execute(stmt)
        link = result.scalar_one_or_none()
        if link:
            await self.db.delete(link)
            await self.db.flush()
            return True
        return False

    async def has_primary_guardian(self, student_id: UUID) -> bool:
        """Check if a student has a primary guardian."""
        stmt = (
            select(func.count())
            .select_from(StudentGuardian)
            .where(
                StudentGuardian.student_id == student_id,
                StudentGuardian.is_primary == True,
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count > 0

    async def clear_primary_for_student(self, student_id: UUID) -> int:
        """Remove primary flag from all guardians for a student.

        Returns the number of links updated.
        """
        from sqlalchemy import update

        stmt = (
            update(StudentGuardian)
            .where(
                StudentGuardian.student_id == student_id,
                StudentGuardian.is_primary == True,
            )
            .values(is_primary=False)
        )
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount
