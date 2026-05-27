from __future__ import annotations
"""Health repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.health.models import (
    HealthScreening,
    Referral,
    SentinelConfiguration,
    SentinelSignal,
    SickBayVisit,
    StudentHealthProfile,
    VaccinationRecord,
)


class HealthProfileRepository:
    """Repository for student health profile database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_student(
        self,
        student_id: UUID,
        school_id: UUID | None = None,
    ) -> StudentHealthProfile | None:
        """Get health profile by student ID."""
        stmt = select(StudentHealthProfile).where(
            StudentHealthProfile.student_id == student_id,
            StudentHealthProfile.deleted_at.is_(None),
        )
        if school_id is not None:
            stmt = stmt.where(StudentHealthProfile.school_id == school_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> StudentHealthProfile:
        """Create a new health profile."""
        profile = StudentHealthProfile(**data)
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def update(self, profile: StudentHealthProfile, data: dict) -> StudentHealthProfile:
        """Update a health profile."""
        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)
        profile.version += 1
        await self.db.flush()
        await self.db.refresh(profile)
        return profile


class SickBayVisitRepository:
    """Repository for sick bay visit database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SickBayVisit:
        """Create a new sick bay visit."""
        visit = SickBayVisit(**data)
        self.db.add(visit)
        await self.db.flush()
        await self.db.refresh(visit)
        return visit

    async def get_by_id(self, visit_id: UUID, school_id: UUID) -> SickBayVisit | None:
        """Get a sick bay visit by ID."""
        stmt = select(SickBayVisit).where(
            SickBayVisit.id == visit_id,
            SickBayVisit.school_id == school_id,
            SickBayVisit.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        student_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        complaint_code: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[SickBayVisit], int]:
        """List sick bay visits with filters."""
        stmt = select(SickBayVisit).where(
            SickBayVisit.school_id == school_id,
            SickBayVisit.deleted_at.is_(None),
        )

        if student_id:
            stmt = stmt.where(SickBayVisit.student_id == student_id)
        if start_date:
            stmt = stmt.where(SickBayVisit.visit_date >= start_date)
        if end_date:
            stmt = stmt.where(SickBayVisit.visit_date <= end_date)
        if complaint_code:
            stmt = stmt.where(SickBayVisit.presenting_complaint_codes.contains([complaint_code]))

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(SickBayVisit.visit_date.desc())

        result = await self.db.execute(stmt)
        visits = result.scalars().all()

        return visits, total

    async def count_visits_for_student_term(
        self,
        student_id: UUID,
        term_start: date,
        term_end: date,
    ) -> int:
        """Count visits for a student in a term."""
        stmt = (
            select(func.count())
            .select_from(SickBayVisit)
            .where(
                SickBayVisit.student_id == student_id,
                SickBayVisit.visit_date >= term_start,
                SickBayVisit.visit_date <= term_end,
                SickBayVisit.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_visits_in_time_window(
        self,
        school_id: UUID,
        start_date: date,
        end_date: date,
        complaint_code: str | None = None,
    ) -> "list[SickBayVisit]":
        """Get visits in a time window for sentinel analysis."""
        stmt = select(SickBayVisit).where(
            SickBayVisit.school_id == school_id,
            SickBayVisit.visit_date >= start_date,
            SickBayVisit.visit_date <= end_date,
            SickBayVisit.deleted_at.is_(None),
        )

        if complaint_code:
            stmt = stmt.where(SickBayVisit.presenting_complaint_codes.contains([complaint_code]))

        stmt = stmt.order_by(SickBayVisit.visit_date, SickBayVisit.visit_time)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class HealthScreeningRepository:
    """Repository for health screening database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> HealthScreening:
        """Create a new health screening."""
        screening = HealthScreening(**data)
        self.db.add(screening)
        await self.db.flush()
        await self.db.refresh(screening)
        return screening

    async def get_by_student_term(
        self,
        student_id: UUID,
        term_id: UUID,
    ) -> HealthScreening | None:
        """Get screening by student and term."""
        stmt = select(HealthScreening).where(
            HealthScreening.student_id == student_id,
            HealthScreening.term_id == term_id,
            HealthScreening.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class ReferralRepository:
    """Repository for referral database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Referral:
        """Create a new referral."""
        referral = Referral(**data)
        self.db.add(referral)
        await self.db.flush()
        await self.db.refresh(referral)
        return referral

    async def get_by_id(self, referral_id: UUID, school_id: UUID) -> Referral | None:
        """Get a referral by ID."""
        stmt = select(Referral).where(
            Referral.id == referral_id,
            Referral.school_id == school_id,
            Referral.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID,
        status: str | None = None,
        student_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[Referral], int]:
        """List referrals with filters."""
        stmt = select(Referral).where(
            Referral.school_id == school_id,
            Referral.deleted_at.is_(None),
        )

        if status:
            stmt = stmt.where(Referral.status == status)
        if student_id:
            stmt = stmt.where(Referral.student_id == student_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(Referral.referral_date.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def update(self, referral: Referral, data: dict) -> Referral:
        """Update a referral."""
        for key, value in data.items():
            if value is not None:
                setattr(referral, key, value)
        await self.db.flush()
        await self.db.refresh(referral)
        return referral

    async def get_overdue_referrals(self, school_id: UUID) -> "list[Referral]":
        """Get referrals that are overdue (past follow-up date and not completed)."""
        stmt = select(Referral).where(
            Referral.school_id == school_id,
            Referral.follow_up_due_date < date.today(),
            Referral.status.notin_(["completed"]),
            Referral.reminder_sent == False,
            Referral.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class VaccinationRepository:
    """Repository for vaccination record database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> VaccinationRecord:
        """Create a new vaccination record."""
        record = VaccinationRecord(**data)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def create_many(self, records: list[dict]) -> list[VaccinationRecord]:
        """Create multiple vaccination records."""
        vaccination_records = [VaccinationRecord(**data) for data in records]
        self.db.add_all(vaccination_records)
        await self.db.flush()
        return vaccination_records

    async def list_by_student(
        self,
        student_id: UUID,
        school_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[VaccinationRecord], int]:
        """Get paginated vaccination records for a student."""
        stmt = select(VaccinationRecord).where(
            VaccinationRecord.student_id == student_id,
            VaccinationRecord.deleted_at.is_(None),
        )
        if school_id:
            stmt = stmt.where(VaccinationRecord.school_id == school_id)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(VaccinationRecord.administration_date.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def get_coverage(
        self,
        school_id: UUID,
        vaccine_name: str | None = None,
    ) -> dict:
        """Get vaccination coverage statistics."""
        from sqlalchemy import text
        
        # Calculate total students
        total_stmt = text("SELECT COUNT(*) FROM students WHERE school_id = :school_id AND status = 'active'")
        total_res = await self.db.execute(total_stmt, {"school_id": str(school_id)})
        total_students = int(total_res.scalar() or 0)
        
        if total_students == 0:
            return {"total_students": 0, "vaccinated": 0, "coverage_percent": 0}
            
        # Calculate vaccinated
        if vaccine_name:
            vac_stmt = text("""
                SELECT COUNT(DISTINCT student_id) FROM vaccination_records
                WHERE school_id = :school_id AND vaccine_name = :vname AND status = 'completed'
            """)
            vac_res = await self.db.execute(vac_stmt, {"school_id": str(school_id), "vname": vaccine_name})
        else:
            vac_stmt = text("""
                SELECT COUNT(DISTINCT student_id) FROM vaccination_records
                WHERE school_id = :school_id AND status = 'completed'
            """)
            vac_res = await self.db.execute(vac_stmt, {"school_id": str(school_id)})
            
        vaccinated = int(vac_res.scalar() or 0)
        
        return {
            "total_students": total_students,
            "vaccinated": vaccinated,
            "coverage_percent": round((vaccinated / total_students) * 100, 2) if total_students > 0 else 0.0
        }


class SentinelSignalRepository:
    """Repository for sentinel signal database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SentinelSignal:
        """Create a new sentinel signal."""
        signal = SentinelSignal(**data)
        self.db.add(signal)
        await self.db.flush()
        await self.db.refresh(signal)
        return signal

    async def get_by_id(self, signal_id: UUID) -> SentinelSignal | None:
        """Get a sentinel signal by ID."""
        stmt = select(SentinelSignal).where(SentinelSignal.id == signal_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        school_id: UUID | None = None,
        lga: str | None = None,
        state: str | None = None,
        status: str | None = None,
        alert_tier: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[SentinelSignal]:
        """List sentinel signals with filters."""
        stmt = select(SentinelSignal)

        if school_id:
            stmt = stmt.where(SentinelSignal.school_ids.contains([school_id]))
        if lga:
            stmt = stmt.where(SentinelSignal.lga == lga)
        if state:
            stmt = stmt.where(SentinelSignal.state == state)
        if status:
            stmt = stmt.where(SentinelSignal.status == status)
        if alert_tier:
            stmt = stmt.where(SentinelSignal.alert_tier == alert_tier)
        if start_date:
            stmt = stmt.where(SentinelSignal.date_generated >= start_date)
        if end_date:
            stmt = stmt.where(SentinelSignal.date_generated <= end_date)

        stmt = stmt.order_by(SentinelSignal.date_generated.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def acknowledge(self, signal_id: UUID, user_id: UUID, notes: str | None = None) -> SentinelSignal:
        """Acknowledge a sentinel signal."""
        stmt = select(SentinelSignal).where(SentinelSignal.id == signal_id)
        result = await self.db.execute(stmt)
        signal = result.scalar_one()

        signal.status = "acknowledged"
        signal.acknowledged_at = datetime.now(timezone.utc)
        signal.acknowledged_by = user_id
        signal.response_notes = notes

        await self.db.flush()
        await self.db.refresh(signal)
        return signal


class SentinelConfigurationRepository:
    """Repository for sentinel configuration database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SentinelConfiguration:
        """Create a new sentinel configuration."""
        config = SentinelConfiguration(**data)
        self.db.add(config)
        await self.db.flush()
        await self.db.refresh(config)
        return config

    async def get_active_config(
        self,
        school_id: UUID | None = None,
        symptom_category: str | None = None,
    ) -> SentinelConfiguration | None:
        """Get active sentinel configuration."""
        stmt = select(SentinelConfiguration).where(
            SentinelConfiguration.is_active == True,
        )

        if school_id:
            stmt = stmt.where(
                or_(
                    SentinelConfiguration.school_id == school_id,
                    SentinelConfiguration.school_id.is_(None),
                )
            )
        if symptom_category:
            stmt = stmt.where(SentinelConfiguration.symptom_category == symptom_category)

        stmt = stmt.order_by(SentinelConfiguration.school_id.desc().nullslast())
        stmt = stmt.limit(1)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, school_id: UUID | None = None) -> list[SentinelConfiguration]:
        """List sentinel configurations."""
        stmt = select(SentinelConfiguration).where(
            SentinelConfiguration.is_active == True,
        )

        if school_id:
            stmt = stmt.where(
                or_(
                    SentinelConfiguration.school_id == school_id,
                    SentinelConfiguration.school_id.is_(None),
                )
            )

        stmt = stmt.order_by(SentinelConfiguration.symptom_category)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
