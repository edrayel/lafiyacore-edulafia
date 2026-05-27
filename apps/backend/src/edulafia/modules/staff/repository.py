from __future__ import annotations
"""Staff repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.academics.models import Subject
from edulafia.modules.staff.models import (
    CommunicationRecipient,
    Staff,
    StaffAssignment,
    StaffCommunication,
    TeacherAttendance,
    Timetable,
    TimetableEntry,
)


class StaffRepository:
    """Repository for staff database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Staff:
        """Create a new staff member."""
        staff = Staff(**data)
        self.db.add(staff)
        await self.db.flush()
        await self.db.refresh(staff)
        return staff

    async def get_by_id(self, staff_id: UUID, school_id: UUID) -> Staff | None:
        """Get staff by ID."""
        stmt = select(Staff).where(
            Staff.id == staff_id,
            Staff.school_id == school_id,
            Staff.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_staff_id(self, staff_id_code: str, school_id: UUID) -> Staff | None:
        """Get staff by staff ID code."""
        stmt = select(Staff).where(
            Staff.staff_id == staff_id_code,
            Staff.school_id == school_id,
            Staff.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_staff_id(self, staff_id_code: str, school_id: UUID) -> bool:
        """Check if staff ID exists."""
        stmt = (
            select(func.count())
            .select_from(Staff)
            .where(
                Staff.staff_id == staff_id_code,
                Staff.school_id == school_id,
                Staff.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() > 0

    async def list(
        self,
        school_id: UUID,
        role: str | None = None,
        department: str | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[Staff], int]:
        """List staff with filters."""
        stmt = select(Staff).where(
            Staff.school_id == school_id,
            Staff.deleted_at.is_(None),
        )

        if role:
            stmt = stmt.where(Staff.role == role)
        if department:
            stmt = stmt.where(Staff.department == department)
        if status:
            stmt = stmt.where(Staff.status == status)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Staff.last_name.asc())

        result = await self.db.execute(stmt)
        staff = result.scalars().all()

        return staff, total

    async def update(self, staff: Staff, data: dict) -> Staff:
        """Update staff."""
        for key, value in data.items():
            if value is not None:
                setattr(staff, key, value)
        staff.version += 1
        await self.db.flush()
        await self.db.refresh(staff)
        return staff

    async def deactivate(self, staff: Staff, reason: str, exit_date: date | None = None) -> Staff:
        """Deactivate staff."""
        staff.status = "inactive"
        staff.exit_date = exit_date or date.today()
        staff.exit_reason = reason
        staff.version += 1
        await self.db.flush()
        await self.db.refresh(staff)
        return staff

    async def get_next_staff_id(self, school_id: UUID, role_prefix: str = "STF") -> str:
        """Generate next staff ID."""
        stmt = (
            select(func.count())
            .select_from(Staff)
            .where(
                Staff.school_id == school_id,
                Staff.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        sequence = count + 1
        return f"{role_prefix}-{sequence:05d}"


class StaffAssignmentRepository:
    """Repository for staff assignment database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> StaffAssignment:
        """Create a new assignment."""
        assignment = StaffAssignment(**data)
        self.db.add(assignment)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def get_by_id(self, assignment_id: UUID) -> StaffAssignment | None:
        """Get assignment by ID."""
        stmt = select(StaffAssignment).where(StaffAssignment.id == assignment_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_duplicate(
        self,
        staff_id: UUID,
        class_id: UUID,
        subject_id: UUID | None,
        academic_year_id: UUID,
    ) -> bool:
        """Check if duplicate assignment exists."""
        stmt = (
            select(func.count())
            .select_from(StaffAssignment)
            .where(
                StaffAssignment.staff_id == staff_id,
                StaffAssignment.class_id == class_id,
                StaffAssignment.academic_year_id == academic_year_id,
                StaffAssignment.is_active == True,
            )
        )
        if subject_id:
            stmt = stmt.where(StaffAssignment.subject_id == subject_id)
        else:
            stmt = stmt.where(StaffAssignment.subject_id.is_(None))

        result = await self.db.execute(stmt)
        return result.scalar() > 0

    async def has_form_teacher(
        self,
        class_id: UUID,
        academic_year_id: UUID,
    ) -> bool:
        """Check if class already has a form teacher."""
        stmt = (
            select(func.count())
            .select_from(StaffAssignment)
            .where(
                StaffAssignment.class_id == class_id,
                StaffAssignment.academic_year_id == academic_year_id,
                StaffAssignment.is_form_teacher == True,
                StaffAssignment.is_active == True,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() > 0

    async def get_teacher_load(
        self,
        staff_id: UUID,
        academic_year_id: UUID,
    ) -> int:
        """Get current teaching load for a teacher."""
        stmt = (
            select(func.count())
            .select_from(StaffAssignment)
            .where(
                StaffAssignment.staff_id == staff_id,
                StaffAssignment.academic_year_id == academic_year_id,
                StaffAssignment.subject_id.isnot(None),
                StaffAssignment.is_active == True,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def list_assignments(
        self,
        school_id: UUID,
        staff_id: UUID | None = None,
        class_id: UUID | None = None,
        academic_year_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[StaffAssignment], int]:
        """List assignments with filters and pagination."""
        stmt = select(StaffAssignment).where(StaffAssignment.school_id == school_id).where(
            StaffAssignment.is_active == True,
        )

        if staff_id:
            stmt = stmt.where(StaffAssignment.staff_id == staff_id)
        if class_id:
            stmt = stmt.where(StaffAssignment.class_id == class_id)
        if academic_year_id:
            stmt = stmt.where(StaffAssignment.academic_year_id == academic_year_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(StaffAssignment.created_at.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def delete(self, assignment_id: UUID) -> bool:
        """Delete an assignment."""
        stmt = select(StaffAssignment).where(StaffAssignment.id == assignment_id)
        result = await self.db.execute(stmt)
        assignment = result.scalar_one_or_none()
        if assignment:
            assignment.is_active = False
            await self.db.flush()
            return True
        return False


class TimetableRepository:
    """Repository for timetable database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Timetable:
        """Create a new timetable."""
        timetable = Timetable(**data)
        self.db.add(timetable)
        await self.db.flush()
        await self.db.refresh(timetable)
        return timetable

    async def get_by_id(self, timetable_id: UUID) -> Timetable | None:
        """Get timetable by ID."""
        stmt = select(Timetable).where(Timetable.id == timetable_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_draft(
        self,
        class_id: UUID,
        academic_year_id: UUID,
        term_id: UUID,
    ) -> Timetable | None:
        """Get draft timetable for class/term."""
        stmt = select(Timetable).where(
            Timetable.class_id == class_id,
            Timetable.academic_year_id == academic_year_id,
            Timetable.term_id == term_id,
            Timetable.is_draft == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def publish(self, timetable_id: UUID, user_id: UUID) -> Timetable:
        """Publish a timetable."""
        stmt = select(Timetable).where(Timetable.id == timetable_id)
        result = await self.db.execute(stmt)
        timetable = result.scalar_one()

        timetable.is_published = True
        timetable.is_draft = False
        timetable.published_at = datetime.now(timezone.utc)
        timetable.published_by = user_id

        await self.db.flush()
        await self.db.refresh(timetable)
        return timetable


class TimetableEntryRepository:
    """Repository for timetable entry database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> TimetableEntry:
        """Create a new timetable entry."""
        entry = TimetableEntry(**data)
        self.db.add(entry)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def list_by_timetable(self, timetable_id: UUID) -> list[TimetableEntry]:
        """List entries for a timetable."""
        stmt = select(TimetableEntry).where(
            TimetableEntry.timetable_id == timetable_id,
        ).order_by(TimetableEntry.day_of_week, TimetableEntry.period_number)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_entries_with_names(self, timetable_id: UUID) -> list[dict]:
        """List timetable entries with resolved staff and subject names."""
        stmt = (
            select(
                TimetableEntry,
                Staff.first_name,
                Staff.last_name,
                Subject.name,
            )
            .join(Staff, TimetableEntry.staff_id == Staff.id)
            .join(Subject, TimetableEntry.subject_id == Subject.id)
            .where(TimetableEntry.timetable_id == timetable_id)
            .order_by(TimetableEntry.day_of_week, TimetableEntry.period_number)
        )
        result = await self.db.execute(stmt)
        enriched = []
        for entry, first_name, last_name, subject_name in result.all():
            d = {
                "id": entry.id,
                "timetable_id": entry.timetable_id,
                "day_of_week": entry.day_of_week,
                "period_number": entry.period_number,
                "start_time": entry.start_time,
                "end_time": entry.end_time,
                "subject_id": entry.subject_id,
                "staff_id": entry.staff_id,
                "room_number": entry.room_number,
                "notes": entry.notes,
                "is_break": entry.is_break,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
                "staff_name": f"{first_name} {last_name}",
                "subject_name": subject_name,
            }
            enriched.append(d)
        return enriched

    async def get_teacher_entries_on_day(
        self,
        timetable_id: UUID,
        staff_id: UUID,
        day_of_week: int,
    ) -> list[TimetableEntry]:
        """Get teacher entries on a specific day."""
        stmt = select(TimetableEntry).where(
            TimetableEntry.timetable_id == timetable_id,
            TimetableEntry.staff_id == staff_id,
            TimetableEntry.day_of_week == day_of_week,
        ).order_by(TimetableEntry.period_number)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_class_entries_on_period(
        self,
        timetable_id: UUID,
        day_of_week: int,
        period_number: int,
    ) -> TimetableEntry | None:
        """Get class entry on a specific period."""
        stmt = select(TimetableEntry).where(
            TimetableEntry.timetable_id == timetable_id,
            TimetableEntry.day_of_week == day_of_week,
            TimetableEntry.period_number == period_number,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_teacher_published_entries(
        self,
        staff_id: UUID,
        class_id: UUID | None = None,
        academic_year_id: UUID | None = None,
        term_id: UUID | None = None,
    ) -> list[TimetableEntry]:
        """Get timetable entries for a teacher from published timetables."""
        stmt = (
            select(TimetableEntry)
            .join(Timetable, TimetableEntry.timetable_id == Timetable.id)
            .where(
                TimetableEntry.staff_id == staff_id,
                Timetable.is_published == True,
            )
        )
        if class_id:
            stmt = stmt.where(Timetable.class_id == class_id)
        if academic_year_id:
            stmt = stmt.where(Timetable.academic_year_id == academic_year_id)
        if term_id:
            stmt = stmt.where(Timetable.term_id == term_id)

        stmt = stmt.order_by(TimetableEntry.day_of_week, TimetableEntry.period_number)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class TeacherAttendanceRepository:
    """Repository for teacher attendance database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> TeacherAttendance:
        """Create a new attendance record."""
        attendance = TeacherAttendance(**data)
        self.db.add(attendance)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def get_by_staff_date(self, staff_id: UUID, attendance_date: date) -> TeacherAttendance | None:
        """Get attendance by staff and date."""
        stmt = select(TeacherAttendance).where(
            TeacherAttendance.staff_id == staff_id,
            TeacherAttendance.date == attendance_date,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, attendance: TeacherAttendance, data: dict) -> TeacherAttendance:
        """Update attendance record."""
        for key, value in data.items():
            if value is not None:
                setattr(attendance, key, value)
        attendance.version += 1
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def list(
        self,
        school_id: UUID,
        staff_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[TeacherAttendance], int]:
        """List attendance records with filters."""
        stmt = select(TeacherAttendance).where(
            TeacherAttendance.school_id == school_id,
        )

        if staff_id:
            stmt = stmt.where(TeacherAttendance.staff_id == staff_id)
        if start_date:
            stmt = stmt.where(TeacherAttendance.date >= start_date)
        if end_date:
            stmt = stmt.where(TeacherAttendance.date <= end_date)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(TeacherAttendance.date.desc())

        result = await self.db.execute(stmt)
        records = result.scalars().all()

        return records, total


class StaffCommunicationRepository:
    """Repository for staff communication database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> StaffCommunication:
        """Create a new communication."""
        communication = StaffCommunication(**data)
        self.db.add(communication)
        await self.db.flush()
        await self.db.refresh(communication)
        return communication

    async def get_by_id(self, communication_id: UUID) -> StaffCommunication | None:
        """Get communication by ID."""
        stmt = select(StaffCommunication).where(StaffCommunication.id == communication_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        communication_type: str | None = None,
        priority: str | None = None,
    ) -> list[StaffCommunication]:
        """List communications with filters."""
        stmt = select(StaffCommunication).where(
            StaffCommunication.school_id == school_id,
        )

        if communication_type:
            stmt = stmt.where(StaffCommunication.communication_type == communication_type)
        if priority:
            stmt = stmt.where(StaffCommunication.priority == priority)

        stmt = stmt.order_by(StaffCommunication.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def add_recipients(
        self,
        communication_id: UUID,
        staff_ids: list[UUID],
    ) -> list[CommunicationRecipient]:
        """Add recipients to communication."""
        recipients = [
            CommunicationRecipient(
                communication_id=communication_id,
                staff_id=staff_id,
                status="sent",
                sent_at=datetime.now(timezone.utc),
            )
            for staff_id in staff_ids
        ]
        self.db.add_all(recipients)
        await self.db.flush()
        for recipient in recipients:
            await self.db.refresh(recipient)
        return recipients

    async def acknowledge(
        self,
        communication_id: UUID,
        staff_id: UUID,
    ) -> CommunicationRecipient | None:
        """Acknowledge a communication."""
        stmt = select(CommunicationRecipient).where(
            CommunicationRecipient.communication_id == communication_id,
            CommunicationRecipient.staff_id == staff_id,
        )
        result = await self.db.execute(stmt)
        recipient = result.scalar_one_or_none()

        if recipient:
            recipient.status = "acknowledged"
            recipient.read_at = datetime.now(timezone.utc)
            recipient.acknowledged_at = datetime.now(timezone.utc)
            await self.db.flush()
            await self.db.refresh(recipient)

        return recipient
