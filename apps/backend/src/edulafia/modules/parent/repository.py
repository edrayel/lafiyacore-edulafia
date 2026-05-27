from __future__ import annotations
"""Parent repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.parent.models import (
    AbsenceExcusal,
    NotificationPreference,
    OTPVerification,
    ParentFeedback,
    ParentNotification,
    ParentSession,
)


class ParentSessionRepository:
    """Repository for parent session database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ParentSession:
        """Create a new session."""
        session = ParentSession(**data)
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_by_token(self, session_token: str) -> ParentSession | None:
        """Get session by token."""
        stmt = select(ParentSession).where(
            ParentSession.session_token == session_token,
            ParentSession.is_active == True,
            ParentSession.expires_at > datetime.now(timezone.utc),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_sessions(self, guardian_id: UUID) -> list[ParentSession]:
        """Get all active sessions for guardian."""
        stmt = select(ParentSession).where(
            ParentSession.guardian_id == guardian_id,
            ParentSession.is_active == True,
            ParentSession.expires_at > datetime.now(timezone.utc),
        ).order_by(ParentSession.last_activity_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_activity(self, session_id: UUID) -> None:
        """Update last activity timestamp."""
        stmt = select(ParentSession).where(ParentSession.id == session_id)
        result = await self.db.execute(stmt)
        session = result.scalar_one()

        session.last_activity_at = datetime.now(timezone.utc)
        await self.db.flush()

    async def invalidate(self, session_id: UUID) -> None:
        """Invalidate a session."""
        stmt = select(ParentSession).where(ParentSession.id == session_id)
        result = await self.db.execute(stmt)
        session = result.scalar_one()

        session.is_active = False
        await self.db.flush()

    async def invalidate_all(self, guardian_id: UUID) -> int:
        """Invalidate all sessions for guardian."""
        sessions = await self.get_active_sessions(guardian_id)
        for session in sessions:
            session.is_active = False
        await self.db.flush()
        return len(sessions)


class OTPVerificationRepository:
    """Repository for OTP verification database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> OTPVerification:
        """Create a new OTP verification."""
        otp = OTPVerification(**data)
        self.db.add(otp)
        await self.db.flush()
        await self.db.refresh(otp)
        return otp

    async def get_latest(
        self,
        phone: str,
        purpose: str = "login",
    ) -> OTPVerification | None:
        """Get latest OTP for phone and purpose."""
        stmt = select(OTPVerification).where(
            OTPVerification.phone == phone,
            OTPVerification.purpose == purpose,
            OTPVerification.verified_at.is_(None),
        ).order_by(OTPVerification.created_at.desc()).limit(1)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def count_recent(
        self,
        phone: str,
        hours: int = 1,
    ) -> int:
        """Count recent OTP requests for rate limiting."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        stmt = (
            select(func.count())
            .select_from(OTPVerification)
            .where(
                OTPVerification.phone == phone,
                OTPVerification.created_at > cutoff,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def increment_attempts(self, otp_id: UUID) -> None:
        """Increment verification attempts."""
        stmt = select(OTPVerification).where(OTPVerification.id == otp_id)
        result = await self.db.execute(stmt)
        otp = result.scalar_one()

        otp.attempts += 1
        await self.db.flush()

    async def mark_verified(self, otp_id: UUID) -> None:
        """Mark OTP as verified."""
        stmt = select(OTPVerification).where(OTPVerification.id == otp_id)
        result = await self.db.execute(stmt)
        otp = result.scalar_one()

        otp.verified_at = datetime.now(timezone.utc)
        await self.db.flush()


class ParentNotificationRepository:
    """Repository for parent notification database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ParentNotification:
        """Create a new notification."""
        notification = ParentNotification(**data)
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification

    async def list(
        self,
        guardian_id: UUID,
        notification_type: str | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[ParentNotification], int]:
        """List notifications with filters."""
        stmt = select(ParentNotification).where(
            ParentNotification.guardian_id == guardian_id,
        )

        if notification_type:
            stmt = stmt.where(ParentNotification.notification_type == notification_type)
        if status:
            stmt = stmt.where(ParentNotification.status == status)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(ParentNotification.created_at.desc())

        result = await self.db.execute(stmt)
        notifications = result.scalars().all()

        return notifications, total

    async def mark_as_read(self, notification_id: UUID) -> ParentNotification:
        """Mark notification as read."""
        stmt = select(ParentNotification).where(ParentNotification.id == notification_id)
        result = await self.db.execute(stmt)
        notification = result.scalar_one()

        notification.status = "read"
        notification.read_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification

    async def count_today(self, guardian_id: UUID, is_urgent: bool = False) -> int:
        """Count notifications sent today."""
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count())
            .select_from(ParentNotification)
            .where(
                ParentNotification.guardian_id == guardian_id,
                ParentNotification.created_at > today_start,
                ParentNotification.priority != "urgent" if not is_urgent else True,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar()


class NotificationPreferenceRepository:
    """Repository for notification preference database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_default(self, guardian_id: UUID) -> list[NotificationPreference]:
        """Get preferences or create defaults."""
        stmt = select(NotificationPreference).where(
            NotificationPreference.guardian_id == guardian_id,
        )
        result = await self.db.execute(stmt)
        preferences = list(result.scalars().all())

        if not preferences:
            # Create default preferences
            default_types = ["absence", "academic", "health", "payment", "announcement"]
            default_channels = ["whatsapp", "in_app"]

            for notif_type in default_types:
                for channel in default_channels:
                    pref = NotificationPreference(
                        guardian_id=guardian_id,
                        notification_type=notif_type,
                        channel=channel,
                        is_enabled=True,
                    )
                    self.db.add(pref)
                    preferences.append(pref)

            await self.db.flush()

        return preferences

    async def update(
        self,
        guardian_id: UUID,
        notification_type: str,
        channel: str,
        is_enabled: bool,
    ) -> NotificationPreference:
        """Update or create a notification preference."""
        stmt = select(NotificationPreference).where(
            NotificationPreference.guardian_id == guardian_id,
            NotificationPreference.notification_type == notification_type,
            NotificationPreference.channel == channel,
        )
        result = await self.db.execute(stmt)
        preference = result.scalar_one_or_none()

        if preference:
            preference.is_enabled = is_enabled
        else:
            preference = NotificationPreference(
                guardian_id=guardian_id,
                notification_type=notification_type,
                channel=channel,
                is_enabled=is_enabled,
            )
            self.db.add(preference)

        await self.db.commit()
        await self.db.refresh(preference)
        return preference

    async def get_guardian_phone(self, guardian_id: UUID):
        from edulafia.modules.guardians.models import Guardian
        stmt = select(Guardian.phone_number).where(Guardian.id == guardian_id)
        result = await self.db.execute(stmt)
        row = result.first()
        if row:
            class DummyGuardian:
                pass
            g = DummyGuardian()
            g.phone_number = row[0]
            return g
        return None


class AbsenceExcusalRepository:
    """Repository for absence excusal database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AbsenceExcusal:
        """Create a new excusal."""
        excusal = AbsenceExcusal(**data)
        self.db.add(excusal)
        await self.db.flush()
        await self.db.refresh(excusal)
        return excusal

    async def list_by_student(self, student_id: UUID) -> list[AbsenceExcusal]:
        """List excuses for a student."""
        stmt = select(AbsenceExcusal).where(
            AbsenceExcusal.student_id == student_id,
        ).order_by(AbsenceExcusal.absence_date.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class ParentFeedbackRepository:
    """Repository for parent feedback database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ParentFeedback:
        """Create new feedback."""
        feedback = ParentFeedback(**data)
        self.db.add(feedback)
        await self.db.flush()
        await self.db.refresh(feedback)
        return feedback

    async def list_by_guardian(self, guardian_id: UUID) -> list[ParentFeedback]:
        """List feedback by guardian."""
        stmt = select(ParentFeedback).where(
            ParentFeedback.guardian_id == guardian_id,
        ).order_by(ParentFeedback.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
