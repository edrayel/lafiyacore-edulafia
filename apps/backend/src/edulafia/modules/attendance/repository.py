from __future__ import annotations
"""Attendance repository for data access operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.attendance.models import (
    AttendancePattern,
    AttendanceRecord,
)


class AttendanceRepository:
    """Repository for attendance database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AttendanceRecord:
        """Create a new attendance record."""
        record = AttendanceRecord(**data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def create_bulk(self, records: list[dict]) -> list[AttendanceRecord]:
        """Create multiple attendance records."""
        attendance_records = [AttendanceRecord(**data) for data in records]
        self.db.add_all(attendance_records)
        await self.db.flush()
        return attendance_records

    async def get_by_id(self, record_id: UUID, school_id: UUID) -> AttendanceRecord | None:
        """Get an attendance record by ID."""
        stmt = select(AttendanceRecord).where(
            AttendanceRecord.id == record_id,
            AttendanceRecord.school_id == school_id,
            AttendanceRecord.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_date(
        self, student_id: UUID, attendance_date: date
    ) -> AttendanceRecord | None:
        """Get attendance record for a student on a specific date."""
        stmt = select(AttendanceRecord).where(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.date == attendance_date,
            AttendanceRecord.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_for_student_date(
        self, student_id: UUID, attendance_date: date
    ) -> bool:
        """Check if attendance record exists for student on date."""
        stmt = (
            select(func.count())
            .select_from(AttendanceRecord)
            .where(
                AttendanceRecord.student_id == student_id,
                AttendanceRecord.date == attendance_date,
                AttendanceRecord.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() > 0

    async def list(
        self,
        school_id: UUID,
        filters: dict | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[AttendanceRecord], int]:
        """List attendance records with filters."""
        stmt = select(AttendanceRecord).where(
            AttendanceRecord.school_id == school_id,
            AttendanceRecord.deleted_at.is_(None),
        )

        if filters:
            if filters.get("student_id"):
                stmt = stmt.where(AttendanceRecord.student_id == filters["student_id"])
            if filters.get("class_id"):
                stmt = stmt.where(AttendanceRecord.class_id == filters["class_id"])
            if filters.get("date"):
                stmt = stmt.where(AttendanceRecord.date == filters["date"])
            if filters.get("start_date"):
                stmt = stmt.where(AttendanceRecord.date >= filters["start_date"])
            if filters.get("end_date"):
                stmt = stmt.where(AttendanceRecord.date <= filters["end_date"])
            if filters.get("status"):
                stmt = stmt.where(AttendanceRecord.status == filters["status"])
            if filters.get("reason_code"):
                stmt = stmt.where(AttendanceRecord.reason_code == filters["reason_code"])

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(AttendanceRecord.date.desc())

        result = await self.db.execute(stmt)
        records = result.scalars().all()

        return records, total

    async def update(self, record: AttendanceRecord, data: dict) -> AttendanceRecord:
        """Update an attendance record."""
        for key, value in data.items():
            if value is not None:
                setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_summary(
        self,
        school_id: UUID,
        class_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict:
        """Get attendance summary statistics."""
        stmt = select(
            func.count().label("total"),
            func.count().filter(AttendanceRecord.status == "present").label("present"),
            func.count().filter(AttendanceRecord.status == "absent").label("absent"),
            func.count().filter(AttendanceRecord.status == "late").label("late"),
            func.count().filter(AttendanceRecord.status == "excused").label("excused"),
        ).where(
            AttendanceRecord.school_id == school_id,
            AttendanceRecord.deleted_at.is_(None),
        )

        if class_id:
            stmt = stmt.where(AttendanceRecord.class_id == class_id)
        if start_date:
            stmt = stmt.where(AttendanceRecord.date >= start_date)
        if end_date:
            stmt = stmt.where(AttendanceRecord.date <= end_date)

        result = await self.db.execute(stmt)
        row = result.one()

        return {
            "total": row.total or 0,
            "present": row.present or 0,
            "absent": row.absent or 0,
            "late": row.late or 0,
            "excused": row.excused or 0,
        }

    async def get_consecutive_absences(
        self,
        student_id: UUID,
        days: int = 3,
    ) -> list[AttendanceRecord]:
        """Get consecutive absence records for a student."""
        stmt = (
            select(AttendanceRecord)
            .where(
                AttendanceRecord.student_id == student_id,
                AttendanceRecord.status == "absent",
                AttendanceRecord.deleted_at.is_(None),
            )
            .order_by(AttendanceRecord.date.desc())
            .limit(days)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_absent_with_symptoms(
        self,
        school_id: UUID,
        attendance_date: date,
    ) -> list[AttendanceRecord]:
        """Get all absent records with symptoms for a date (for Sentinel)."""
        stmt = select(AttendanceRecord).where(
            AttendanceRecord.school_id == school_id,
            AttendanceRecord.date == attendance_date,
            AttendanceRecord.status == "absent",
            AttendanceRecord.reason_code == "sick",
            AttendanceRecord.symptom_codes.isnot(None),
            AttendanceRecord.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_student_absence_rate(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date,
    ) -> float:
        """Calculate absence rate for a student."""
        stmt = select(
            func.count().label("total"),
            func.count().filter(AttendanceRecord.status == "absent").label("absent"),
        ).where(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.date >= start_date,
            AttendanceRecord.date <= end_date,
            AttendanceRecord.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        row = result.one()

        if row.total == 0:
            return 0.0
        return (row.absent / row.total) * 100


class AttendancePatternRepository:
    """Repository for attendance pattern database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AttendancePattern:
        """Create a new attendance pattern."""
        pattern = AttendancePattern(**data)
        self.db.add(pattern)
        await self.db.flush()
        await self.db.refresh(pattern)
        return pattern

    async def list(
        self,
        school_id: UUID,
        pattern_type: str | None = None,
        severity: str | None = None,
        status: str | None = None,
    ) -> list[AttendancePattern]:
        """List attendance patterns with filters."""
        stmt = select(AttendancePattern).where(
            AttendancePattern.school_id == school_id,
        )

        if pattern_type:
            stmt = stmt.where(AttendancePattern.pattern_type == pattern_type)
        if severity:
            stmt = stmt.where(AttendancePattern.severity == severity)
        if status:
            stmt = stmt.where(AttendancePattern.status == status)

        stmt = stmt.order_by(AttendancePattern.detected_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def acknowledge(self, pattern_id: UUID, user_id: UUID) -> AttendancePattern:
        """Acknowledge an attendance pattern."""
        stmt = select(AttendancePattern).where(AttendancePattern.id == pattern_id)
        result = await self.db.execute(stmt)
        pattern = result.scalar_one()

        pattern.status = "acknowledged"
        await self.db.flush()
        await self.db.refresh(pattern)
        return pattern
