from __future__ import annotations
"""Repository for data access operations."""

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.academics.models import AcademicResult, Subject


class SubjectRepository:
    """Repository for subject database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Subject:
        """Create a new subject."""
        subject = Subject(**data)
        self.db.add(subject)
        await self.db.flush()
        await self.db.refresh(subject)
        return subject

    async def get_by_id(self, subject_id: UUID, school_id: UUID) -> Subject | None:
        """Get a subject by ID, scoped to school."""
        stmt = select(Subject).where(
            Subject.id == subject_id,
            Subject.school_id == school_id,
            Subject.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str, school_id: UUID) -> Subject | None:
        """Get a subject by code within a school."""
        stmt = select(Subject).where(
            Subject.code == code,
            Subject.school_id == school_id,
            Subject.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_code(self, code: str, school_id: UUID) -> bool:
        """Check if a subject with the given code exists."""
        stmt = (
            select(func.count())
            .select_from(Subject)
            .where(
                Subject.code == code,
                Subject.school_id == school_id,
                Subject.deleted_at.is_(None),
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
        is_core: bool | None = None,
    ) -> tuple[Sequence[Subject], int]:
        """List subjects with pagination and optional filter."""
        stmt = select(Subject).where(
            Subject.school_id == school_id,
            Subject.deleted_at.is_(None),
        )

        if is_core is not None:
            stmt = stmt.where(Subject.is_core == is_core)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Subject.name.asc())

        result = await self.db.execute(stmt)
        subjects = result.scalars().all()

        return subjects, total

    async def update(self, subject: Subject, data: dict) -> Subject:
        """Update a subject."""
        for key, value in data.items():
            if value is not None:
                setattr(subject, key, value)
        await self.db.flush()
        await self.db.refresh(subject)
        return subject

    async def soft_delete(self, subject: Subject) -> Subject:
        """Soft delete a subject."""
        subject.deleted_at = func.now()
        await self.db.flush()
        await self.db.refresh(subject)
        return subject


class AcademicResultRepository:
    """Repository for academic result database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AcademicResult:
        """Create a new academic result."""
        result = AcademicResult(**data)
        self.db.add(result)
        await self.db.flush()
        await self.db.refresh(result)
        return result

    async def create_many(self, data_list: list[dict]) -> list[AcademicResult]:
        """Create multiple academic results. This does an UPSERT."""
        if not data_list:
            return []
            
        from sqlalchemy.dialects.postgresql import insert
        
        stmt = insert(AcademicResult).values(data_list)
        
        # On conflict, update the scores
        update_dict = {
            "ca_scores": stmt.excluded.ca_scores,
            "ca_total": stmt.excluded.ca_total,
            "exam_score": stmt.excluded.exam_score,
            "total_score": stmt.excluded.total_score,
            "grade": stmt.excluded.grade,
            "flag": stmt.excluded.flag,
            "updated_by": stmt.excluded.updated_by,
            "updated_at": func.now(),
        }
        
        stmt = stmt.on_conflict_do_update(
            constraint="uq_academic_result_student_subject_term",
            set_=update_dict
        ).returning(AcademicResult)
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        return list(result.scalars().all())

    async def update(self, result: AcademicResult, data: dict) -> AcademicResult:
        """Update an academic result."""
        for key, value in data.items():
            if value is not None:
                setattr(result, key, value)
        await self.db.flush()
        await self.db.refresh(result)
        return result

    async def update_ranks(self, rank_updates: list[dict]) -> int:
        """Bulk update class ranks."""
        from sqlalchemy import update
        total = 0
        for entry in rank_updates:
            stmt = update(AcademicResult).where(AcademicResult.id == entry["id"]).values(class_rank=entry["class_rank"])
            res = await self.db.execute(stmt)
            total += res.rowcount
        await self.db.flush()
        return total

    async def get_by_student_subject_term(
        self,
        student_id: UUID,
        subject_id: UUID,
        term_id: UUID,
    ) -> AcademicResult | None:
        """Get an academic result by student, subject, and term."""
        stmt = select(AcademicResult).where(
            AcademicResult.student_id == student_id,
            AcademicResult.subject_id == subject_id,
            AcademicResult.term_id == term_id,
            AcademicResult.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_class_term_subject(
        self,
        class_id: UUID,
        term_id: UUID,
        subject_id: UUID,
        school_id: UUID | None = None,
        page: int | None = None,
        per_page: int = 20,
    ) -> tuple[Sequence[AcademicResult], int] | Sequence[AcademicResult]:
        """List academic results for a class, term, and subject."""
        stmt = select(AcademicResult).where(
            AcademicResult.class_id == class_id,
            AcademicResult.term_id == term_id,
            AcademicResult.subject_id == subject_id,
            AcademicResult.deleted_at.is_(None),
        )
        if school_id:
            stmt = stmt.where(AcademicResult.school_id == school_id)

        if page is None:
            result = await self.db.execute(stmt)
            return result.scalars().all()

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def list_by_student_term(
        self,
        student_id: UUID,
        term_id: UUID,
    ) -> Sequence[AcademicResult]:
        """List all academic results for a student and term."""
        stmt = select(
            AcademicResult,
            Subject.code.label("subject_code"),
            Subject.name.label("subject_name"),
        ).join(
            Subject, AcademicResult.subject_id == Subject.id
        ).where(
            AcademicResult.student_id == student_id,
            AcademicResult.term_id == term_id,
            AcademicResult.deleted_at.is_(None),
            Subject.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.all()
