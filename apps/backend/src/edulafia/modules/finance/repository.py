from __future__ import annotations
"""Finance repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.finance.models import (
    FeeLedger,
    FeeSchedule,
    FeeScheduleItem,
    PaymentConfiguration,
    Scholarship,
    StudentScholarship,
)


class FeeScheduleRepository:
    """Repository for fee schedule database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> FeeSchedule:
        """Create a new fee schedule."""
        schedule = FeeSchedule(**data)
        self.db.add(schedule)
        await self.db.flush()
        await self.db.refresh(schedule)
        return schedule

    async def get_by_id(self, schedule_id: UUID, school_id: UUID) -> FeeSchedule | None:
        """Get a fee schedule by ID."""
        stmt = select(FeeSchedule).where(
            FeeSchedule.id == schedule_id,
            FeeSchedule.school_id == school_id,
            FeeSchedule.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        academic_year_id: UUID | None = None,
        is_active: bool | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[FeeSchedule], int]:
        """List fee schedules with filters and pagination."""
        stmt = select(FeeSchedule).where(
            FeeSchedule.school_id == school_id,
            FeeSchedule.deleted_at.is_(None),
        )

        if academic_year_id:
            stmt = stmt.where(FeeSchedule.academic_year_id == academic_year_id)
        if is_active is not None:
            stmt = stmt.where(FeeSchedule.is_active == is_active)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(FeeSchedule.created_at.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def lock(self, schedule_id: UUID, user_id: UUID) -> FeeSchedule:
        """Lock a fee schedule."""
        stmt = select(FeeSchedule).where(FeeSchedule.id == schedule_id)
        result = await self.db.execute(stmt)
        schedule = result.scalar_one()

        schedule.locked_at = datetime.now(timezone.utc)
        schedule.locked_by = user_id
        await self.db.flush()
        await self.db.refresh(schedule)
        return schedule

    async def update(self, schedule: FeeSchedule, data: dict) -> FeeSchedule:
        """Update a fee schedule."""
        for key, value in data.items():
            if value is not None:
                setattr(schedule, key, value)
        await self.db.flush()
        await self.db.refresh(schedule)
        return schedule


class FeeScheduleItemRepository:
    """Repository for fee schedule item database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(self, items: list[dict]) -> list[FeeScheduleItem]:
        """Create multiple fee schedule items."""
        fee_items = [FeeScheduleItem(**data) for data in items]
        self.db.add_all(fee_items)
        await self.db.flush()
        
        # Avoid N+1 refresh by selecting them back in one query if needed,
        # but flush() populates IDs and defaults, which is usually enough.
        return fee_items

    async def get_by_schedule(self, schedule_id: UUID) -> list[FeeScheduleItem]:
        """Get all items for a fee schedule."""
        stmt = select(FeeScheduleItem).where(
            FeeScheduleItem.fee_schedule_id == schedule_id,
            FeeScheduleItem.deleted_at.is_(None),
        ).order_by(FeeScheduleItem.class_level, FeeScheduleItem.fee_category)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def exists_duplicate(
        self,
        schedule_id: UUID,
        class_level: str,
        fee_category: str,
    ) -> bool:
        """Check if duplicate fee category exists for class level."""
        stmt = (
            select(func.count())
            .select_from(FeeScheduleItem)
            .where(
                FeeScheduleItem.fee_schedule_id == schedule_id,
                FeeScheduleItem.class_level == class_level,
                FeeScheduleItem.fee_category == fee_category,
                FeeScheduleItem.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() > 0


class FeeLedgerRepository:
    """Repository for fee ledger database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> FeeLedger:
        """Create a new fee ledger entry."""
        entry = FeeLedger(**data)
        self.db.add(entry)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def get_by_id(self, entry_id: UUID, school_id: UUID) -> FeeLedger | None:
        """Get a fee ledger entry by ID."""
        stmt = select(FeeLedger).where(
            FeeLedger.id == entry_id,
            FeeLedger.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_receipt(self, receipt_number: str) -> FeeLedger | None:
        """Get a fee ledger entry by receipt number."""
        stmt = select(FeeLedger).where(
            FeeLedger.receipt_number == receipt_number,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_gateway_reference(self, gateway_reference: str) -> FeeLedger | None:
        """Get a fee ledger entry by gateway reference."""
        stmt = select(FeeLedger).where(
            FeeLedger.gateway_reference == gateway_reference,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        student_id: UUID | None = None,
        transaction_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[FeeLedger], int]:
        """List fee ledger entries with filters."""
        stmt = select(FeeLedger).where(
            FeeLedger.school_id == school_id,
        )

        if student_id:
            stmt = stmt.where(FeeLedger.student_id == student_id)
        if transaction_type:
            stmt = stmt.where(FeeLedger.transaction_type == transaction_type)
        if start_date:
            stmt = stmt.where(FeeLedger.transaction_date >= start_date)
        if end_date:
            stmt = stmt.where(FeeLedger.transaction_date <= end_date)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(FeeLedger.transaction_date.desc())

        result = await self.db.execute(stmt)
        entries = result.scalars().all()

        return entries, total

    async def get_student_balance(
        self,
        student_id: UUID,
        term_id: UUID | None = None,
    ) -> dict:
        """Calculate student balance and get student name."""
        from edulafia.modules.students.models import Student
        
        stmt = select(
            Student.first_name,
            Student.last_name,
            func.sum(
                func.case(
                    (FeeLedger.transaction_type.in_(["charge"]), FeeLedger.amount),
                    else_=0,
                )
            ).label("total_charges"),
            func.sum(
                func.case(
                    (FeeLedger.transaction_type.in_(["payment"]), FeeLedger.amount),
                    else_=0,
                )
            ).label("total_payments"),
            func.sum(
                func.case(
                    (FeeLedger.transaction_type.in_(["waiver"]), FeeLedger.amount),
                    else_=0,
                )
            ).label("total_waivers"),
        ).select_from(Student).outerjoin(
            FeeLedger,
            (Student.id == FeeLedger.student_id) &
            (FeeLedger.term_id == term_id if term_id else True)
        ).where(
            Student.id == student_id,
            Student.deleted_at.is_(None)
        ).group_by(Student.first_name, Student.last_name)

        result = await self.db.execute(stmt)
        row = result.first()

        if not row:
            return {
                "student_name": "",
                "total_charges": 0,
                "total_payments": 0,
                "total_waivers": 0,
                "balance": 0,
            }

        charges = float(row.total_charges or 0)
        payments = float(row.total_payments or 0)
        waivers = float(row.total_waivers or 0)

        return {
            "student_name": f"{row.first_name} {row.last_name}".strip(),
            "total_charges": charges,
            "total_payments": payments,
            "total_waivers": waivers,
            "balance": charges - payments - waivers,
        }

    async def get_next_receipt_number(self, school_id: UUID, year: int) -> str:
        """Generate next receipt number for a school."""
        from sqlalchemy import text

        # Get school code
        school_result = await self.db.execute(text(
            "SELECT code FROM schools WHERE id = :school_id"
        ), {"school_id": str(school_id)})
        school_row = school_result.fetchone()
        school_code = school_row[0] if school_row else "EDU"

        # Count existing receipts for this school and year
        stmt = (
            select(func.count())
            .select_from(FeeLedger)
            .where(
                FeeLedger.school_id == school_id,
                FeeLedger.receipt_number.like(f"%-{year}-%"),
                FeeLedger.transaction_type == "payment",
            )
        )
        result = await self.db.execute(stmt)
        count = result.scalar()

        sequence = count + 1
        return f"{school_code}-{year}-{sequence:06d}"

    async def update(self, entry: FeeLedger, data: dict) -> FeeLedger:
        """Update a fee ledger entry."""
        for key, value in data.items():
            if value is not None:
                setattr(entry, key, value)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry


class ScholarshipRepository:
    """Repository for scholarship database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Scholarship:
        """Create a new scholarship."""
        scholarship = Scholarship(**data)
        self.db.add(scholarship)
        await self.db.flush()
        await self.db.refresh(scholarship)
        return scholarship

    async def get_by_id(self, scholarship_id: UUID, school_id: UUID) -> Scholarship | None:
        """Get a scholarship by ID."""
        stmt = select(Scholarship).where(
            Scholarship.id == scholarship_id,
            Scholarship.school_id == school_id,
            Scholarship.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        is_active: bool | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[Scholarship], int]:
        """List scholarships with filters and pagination."""
        stmt = select(Scholarship).where(
            Scholarship.school_id == school_id,
            Scholarship.deleted_at.is_(None),
        )

        if is_active is not None:
            stmt = stmt.where(Scholarship.is_active == is_active)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Scholarship.name.asc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total


class StudentScholarshipRepository:
    """Repository for student scholarship database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> StudentScholarship:
        """Create a new student scholarship."""
        student_scholarship = StudentScholarship(**data)
        self.db.add(student_scholarship)
        await self.db.flush()
        await self.db.refresh(student_scholarship)
        return student_scholarship

    async def exists_duplicate(
        self,
        student_id: UUID,
        scholarship_id: UUID,
        academic_year_id: UUID,
    ) -> bool:
        """Check if scholarship already awarded to student for year."""
        stmt = (
            select(func.count())
            .select_from(StudentScholarship)
            .where(
                StudentScholarship.student_id == student_id,
                StudentScholarship.scholarship_id == scholarship_id,
                StudentScholarship.academic_year_id == academic_year_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() > 0

    async def list_by_scholarship(
        self,
        scholarship_id: UUID,
        school_id: UUID,
    ) -> list[StudentScholarship]:
        """List all recipients of a scholarship."""
        stmt = select(StudentScholarship).join(StudentScholarship.scholarship).where(
            StudentScholarship.scholarship_id == scholarship_id,
            Scholarship.school_id == school_id,
        ).order_by(StudentScholarship.awarded_date.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class PaymentConfigurationRepository:
    """Repository for payment configuration database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_school_gateway(
        self,
        school_id: UUID,
        gateway: str,
    ) -> PaymentConfiguration | None:
        """Get payment configuration for school and gateway."""
        stmt = select(PaymentConfiguration).where(
            PaymentConfiguration.school_id == school_id,
            PaymentConfiguration.payment_gateway == gateway,
            PaymentConfiguration.is_active == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
