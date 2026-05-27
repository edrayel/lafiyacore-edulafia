from __future__ import annotations
"""Student repository for data access operations."""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from typing import Any

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.students.models import Student, StudentDocument
from edulafia.modules.students.schemas import StudentFilters


class StudentRepository:
    """Repository for student database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Student:
        """Create a new student."""
        student = Student(**data)
        self.db.add(student)
        await self.db.flush()
        await self.db.refresh(student)
        return student

    async def get_by_id(self, student_id: UUID, school_id: UUID) -> Student | None:
        """Get a student by ID, scoped to school."""
        stmt = select(Student).where(
            Student.id == student_id,
            Student.school_id == school_id,
            Student.deleted_at.is_(None),
        ).options(selectinload(Student.guardians), selectinload(Student.documents))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_admission_number(
        self, admission_number: str, school_id: UUID
    ) -> Student | None:
        """Get a student by admission number within a school."""
        stmt = select(Student).where(
            Student.admission_number == admission_number,
            Student.school_id == school_id,
            Student.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_admission(
        self, admission_number: str, school_id: UUID
    ) -> bool:
        """Check if a student with the given admission number exists."""
        stmt = (
            select(func.count())
            .select_from(Student)
            .where(
                Student.admission_number == admission_number,
                Student.school_id == school_id,
                Student.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count > 0

    async def exists_by_nin(self, nin: str) -> bool:
        """Check if a student with the given NIN exists."""
        stmt = (
            select(func.count())
            .select_from(Student)
            .where(
                Student.nin == nin,
                Student.deleted_at.is_(None),
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
        filters: StudentFilters | None = None,
    ) -> tuple[Sequence[Student], int]:
        """List students with pagination and filters."""
        stmt = select(Student).where(
            Student.school_id == school_id,
            Student.deleted_at.is_(None),
        ).options(selectinload(Student.guardians), selectinload(Student.documents))

        # Apply filters
        if filters:
            if filters.class_id:
                stmt = stmt.where(Student.class_id == filters.class_id)
            if filters.status:
                stmt = stmt.where(Student.status == filters.status)
            if filters.gender:
                stmt = stmt.where(Student.gender == filters.gender.lower())
            if filters.search:
                search_term = f"%{filters.search}%"
                stmt = stmt.where(
                    (Student.first_name.ilike(search_term))
                    | (Student.last_name.ilike(search_term))
                    | (Student.admission_number.ilike(search_term))
                )
            
            if getattr(filters, "guardian_id", None):
                from edulafia.modules.guardians.student_guardian import StudentGuardian
                stmt = stmt.join(
                    StudentGuardian, StudentGuardian.student_id == Student.id
                ).where(StudentGuardian.guardian_id == filters.guardian_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Student.created_at.desc())

        result = await self.db.execute(stmt)
        students = result.scalars().all()

        return students, total

    async def update(self, student: Student, data: dict) -> Student:
        """Update a student."""
        for key, value in data.items():
            if value is not None:
                setattr(student, key, value)
        await self.db.flush()
        await self.db.refresh(student)
        return student

    async def soft_delete(self, student: Student, deleted_by: UUID) -> Student:
        """Soft delete a student."""
        student.deleted_at = datetime.now(UTC)
        student.status = "inactive"
        student.updated_by = deleted_by
        await self.db.flush()
        await self.db.refresh(student)
        return student

    async def get_next_admission_number(self, school_id: UUID) -> int:
        """Get the next sequence number for admission numbers."""
        stmt = (
            select(func.count())
            .select_from(Student)
            .where(
                Student.school_id == school_id,
                Student.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return count + 1

    async def hard_delete(self, db: AsyncSession, student_id: UUID) -> bool:
        """Permanently delete a student record.
        
        Args:
            db: Database session
            student_id: ID of the student
            
        Returns:
            True if deleted, False if not found
        """
        query = select(Student).where(Student.id == student_id)
        result = await db.execute(query)
        student = result.scalar_one_or_none()
        
        if not student:
            return False
            
        await db.delete(student)
        await db.commit()
        return True


class StudentDocumentRepository:
    """Repository for managing student document data access."""

    async def get_by_student(
        self,
        db: AsyncSession,
        student_id: UUID,
    ) -> list[StudentDocument]:
        """Get all documents for a student.
        
        Args:
            db: Database session
            student_id: ID of the student
            
        Returns:
            List of student documents
        """
        query = select(StudentDocument).where(StudentDocument.student_id == student_id).order_by(StudentDocument.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(
        self,
        db: AsyncSession,
        student_id: UUID,
        document_in: dict[str, Any],
        uploaded_by: UUID | None = None,
    ) -> StudentDocument:
        """Create a new student document.
        
        Args:
            db: Database session
            student_id: ID of the student
            document_in: Document data
            uploaded_by: User ID who uploaded the document
            
        Returns:
            Created student document
        """
        db_doc = StudentDocument(
            student_id=student_id,
            uploaded_by=uploaded_by,
            **document_in,
        )
        db.add(db_doc)
        await db.commit()
        await db.refresh(db_doc)
        return db_doc

    async def delete(
        self,
        db: AsyncSession,
        document_id: UUID,
    ) -> bool:
        """Delete a student document.
        
        Args:
            db: Database session
            document_id: ID of the document
            
        Returns:
            True if deleted, False if not found
        """
        query = select(StudentDocument).where(StudentDocument.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            return False
            
        await db.delete(document)
        await db.commit()
        return True
