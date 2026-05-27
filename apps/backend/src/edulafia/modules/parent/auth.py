"""Parent authentication service for OTP-based login."""

import random
import string
from datetime import timezone, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
import structlog
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from edulafia.core import rate_limiter
from edulafia.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from edulafia.modules.parent.exceptions import (
    ExpiredOTPError,
    InvalidOTPError,
    InvalidTokenError,
    MaxAttemptsExceededError,
    OTPTemporarilyLockedError,
    RateLimitExceededError,
    SessionExpiredError,
)
from edulafia.modules.parent.models import ParentSession
from edulafia.modules.parent.repository import (
    OTPVerificationRepository,
    ParentSessionRepository,
)
from edulafia.modules.parent.schemas import (
    AuthResponse,
    ChildSummary,
    OTPRequest,
    OTPVerify,
)

logger = structlog.get_logger(__name__)

# Configuration
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 10
MAX_ATTEMPTS = 3
RATE_LIMIT_PER_HOUR = 3
OTP_REQUEST_IP_MAX_PER_HOUR = 15
OTP_VERIFY_FAILURE_MAX_PER_10_MINUTES = 10
OTP_VERIFY_LOCKOUT_SECONDS = 15 * 60
SESSION_EXPIRY_DAYS = 7
INACTIVITY_TIMEOUT_MINUTES = 30


class ParentAuthService:
    """Service for parent authentication."""

    def __init__(
        self,
        session_repo: ParentSessionRepository,
        otp_repo: OTPVerificationRepository,
    ):
        self.session_repo = session_repo
        self.otp_repo = otp_repo

    def _generate_otp(self) -> str:
        """Generate a random OTP code."""
        return ''.join(random.choices(string.digits, k=OTP_LENGTH))

    def _validate_phone(self, phone: str) -> bool:
        """Validate Nigerian phone number format."""
        if not phone.startswith("+234"):
            return False
        digits = phone[4:]
        return digits.isdigit() and len(digits) == 10

    def is_quiet_hours(self) -> bool:
        """Check if current time is during quiet hours (9PM-6AM)."""
        current_hour = datetime.now(timezone.utc).hour
        return current_hour >= 21 or current_hour < 6

    def is_urgent(self, notification_type: str) -> bool:
        """Check if notification type is urgent."""
        urgent_types = ["health_emergency", "safety_alert", "critical"]
        return notification_type.lower() in urgent_types

    async def request_otp(
        self,
        data: OTPRequest,
        send_sms_func=None,
        send_whatsapp_func=None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        """Request an OTP for authentication."""
        await self._enforce_otp_request_limits(phone=data.phone, ip_address=ip_address)
        # Validate phone format
        if not self._validate_phone(data.phone):
            raise ValueError("Invalid phone number format")

        from edulafia.modules.guardians.models import Guardian
        
        # Verify phone number belongs to a registered guardian
        stmt = select(Guardian.id).where(Guardian.phone_number == data.phone)
        result = await self.otp_repo.db.execute(stmt)
        guardian_id = result.scalar_one_or_none()
        
        if not guardian_id:
            # We throw 400 or 404 here, or generic message to prevent phone enumeration
            raise HTTPException(status_code=400, detail="Phone number not registered to any guardian.")

        # Generate OTP
        otp_code = self._generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)

        # Send OTP via preferred channel FIRST to prevent desync
        sent_via = "sms"
        try:
            from edulafia.core.twilio_client import TwilioClient
            await TwilioClient.send_sms(data.phone, f"Your Edulafia login OTP is: {otp_code}")
        except Exception as e:
            logger.error(
                "otp_request_send_failed",
                phone=data.phone,
                ip_address=ip_address or "unknown",
                user_agent=user_agent,
                error=str(e),
            )
            raise HTTPException(status_code=500, detail="Failed to deliver OTP message.")

        # Store OTP only after successful send
        otp_data = {
            "phone": data.phone,
            "otp_code": otp_code,
            "purpose": "login",
            "expires_at": expires_at,
            "max_attempts": MAX_ATTEMPTS,
        }
        await self.otp_repo.create(otp_data)

        logger.info(
            "otp_requested",
            phone=data.phone,
            ip_address=ip_address or "unknown",
            user_agent=user_agent,
            sent_via=sent_via,
        )
        return {
            "message": "OTP sent successfully",
            "data": {
                "phone": data.phone[:7] + "****" + data.phone[-3:],
                "sent_via": sent_via,
                "expires_in": OTP_EXPIRY_MINUTES * 60,
            },
        }

    async def verify_otp(
        self,
        data: OTPVerify,
        device_info: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuthResponse:
        """Verify OTP and create session."""
        await self._enforce_otp_verify_lockout(phone=data.phone, ip_address=ip_address)
        # Get latest OTP
        otp = await self.otp_repo.get_latest(data.phone, "login")
        if not otp:
            await self._record_otp_verify_failure(phone=data.phone, ip_address=ip_address)
            raise InvalidOTPError()

        # Check if expired
        if otp.expires_at < datetime.now(timezone.utc):
            await self._record_otp_verify_failure(phone=data.phone, ip_address=ip_address)
            raise ExpiredOTPError()

        # Check max attempts
        if otp.attempts >= otp.max_attempts:
            await self._record_otp_verify_failure(phone=data.phone, ip_address=ip_address)
            raise MaxAttemptsExceededError()

        # Verify OTP
        if otp.otp_code != data.otp_code:
            await self.otp_repo.increment_attempts(otp.id)
            await self._record_otp_verify_failure(phone=data.phone, ip_address=ip_address)
            raise InvalidOTPError()

        # Mark OTP as verified
        await self.otp_repo.mark_verified(otp.id)

        # Create session
        session_token = self._generate_session_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRY_DAYS)

        session_data = {
            "guardian_id": otp.guardian_id,
            "session_token": session_token,
            "device_info": device_info,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "expires_at": expires_at,
            "last_activity_at": datetime.now(timezone.utc),
        }
        session = await self.session_repo.create(session_data)

        # Generate JWT tokens
        token_data = {
            "sub": str(otp.guardian_id),
            "role": "parent",
            "session_id": str(session.id),
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        logger.info(
            "otp_verified",
            phone=data.phone,
            ip_address=ip_address or "unknown",
            user_agent=user_agent,
            guardian_id=str(otp.guardian_id) if otp.guardian_id else None,
        )
        # Get guardian info and children
        guardian_name = "Guardian"
        children = []

        if otp.guardian_id:
            try:
                from edulafia.database import AsyncSessionLocal
                from edulafia.modules.guardians.models import Guardian, StudentGuardian
                from edulafia.modules.students.models import Student

                async with AsyncSessionLocal() as db_session:
                    # Get guardian
                    stmt = select(Guardian).where(
                        Guardian.id == otp.guardian_id,
                        Guardian.deleted_at.is_(None),
                    )
                    result = await db_session.execute(stmt)
                    guardian = result.scalar_one_or_none()

                    if guardian:
                        guardian_name = f"{guardian.first_name} {guardian.last_name}"

                        # Get linked students
                        student_stmt = (
                            select(Student)
                            .join(StudentGuardian, Student.id == StudentGuardian.student_id)
                            .where(
                                StudentGuardian.guardian_id == otp.guardian_id,
                                Student.deleted_at.is_(None),
                            )
                            .options(selectinload(Student.class_))
                        )
                        student_result = await db_session.execute(student_stmt)
                        students = student_result.scalars().all()

                        for student in students:
                            class_name = student.class_.name if student.class_ else "Unknown"
                            children.append(ChildSummary(
                                student_id=student.id,
                                first_name=student.first_name,
                                last_name=student.last_name,
                                admission_number=student.admission_number,
                                class_name=class_name,
                                status=student.status,
                            ))
            except Exception as e:
                logger.error("otp_verify_guardian_lookup_failed", error=str(e))

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=15 * 60,  # 15 minutes
            guardian_id=otp.guardian_id,
            guardian_name=guardian_name,
            children=children,
        )

    def _generate_session_token(self) -> str:
        """Generate a random session token."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

    async def _enforce_otp_request_limits(self, phone: str, ip_address: str | None) -> None:
        client_ip = ip_address or "unknown"

        # Check lockouts first
        try:
            redis = await rate_limiter.get_redis()
            ip_lock_key = f"lockout:otp_request:lock:ip:{client_ip}"
            phone_lock_key = f"lockout:otp_request:lock:phone:{phone}"

            if await redis.exists(ip_lock_key) > 0:
                logger.warning("otp_request_locked_out", scope="ip", ip_address=client_ip)
                raise OTPTemporarilyLockedError()

            if await redis.exists(phone_lock_key) > 0:
                logger.warning("otp_request_locked_out", scope="phone", phone=phone)
                raise OTPTemporarilyLockedError()
        except OTPTemporarilyLockedError:
            raise
        except Exception as e:
            logger.error("otp_request_lockout_check_failed", error=str(e))

        ip_key = f"rate_limit:otp_request:ip:{client_ip}"
        phone_key = f"rate_limit:otp_request:phone:{phone}"

        ip_limiter = rate_limiter.RateLimiter(
            max_requests=OTP_REQUEST_IP_MAX_PER_HOUR,
            window_seconds=3600,
        )
        phone_limiter = rate_limiter.RateLimiter(
            max_requests=RATE_LIMIT_PER_HOUR,
            window_seconds=3600,
        )

        ip_limited = await ip_limiter.is_rate_limited(ip_key)
        phone_limited = await phone_limiter.is_rate_limited(phone_key)

        if not (ip_limited or phone_limited):
            return

        try:
            redis = await rate_limiter.get_redis()
            if ip_limited:
                ip_lock_key = f"lockout:otp_request:lock:ip:{client_ip}"
                await redis.setex(ip_lock_key, OTP_VERIFY_LOCKOUT_SECONDS, "1")
                logger.warning("otp_request_lockout_set", scope="ip", ip_address=client_ip)

            if phone_limited:
                phone_lock_key = f"lockout:otp_request:lock:phone:{phone}"
                await redis.setex(phone_lock_key, OTP_VERIFY_LOCKOUT_SECONDS, "1")
                logger.warning("otp_request_lockout_set", scope="phone", phone=phone)
        except Exception as e:
            logger.error("otp_request_lockout_set_failed", error=str(e))

        if ip_limited:
            logger.warning("otp_request_rate_limited", scope="ip", ip_address=client_ip)
            raise RateLimitExceededError()

        if phone_limited:
            logger.warning("otp_request_rate_limited", scope="phone", phone=phone)
            raise RateLimitExceededError()

    async def _enforce_otp_verify_lockout(self, phone: str, ip_address: str | None) -> None:
        client_ip = ip_address or "unknown"
        try:
            redis = await rate_limiter.get_redis()

            ip_lock_key = f"lockout:otp_verify:lock:ip:{client_ip}"
            phone_lock_key = f"lockout:otp_verify:lock:phone:{phone}"

            if await redis.exists(ip_lock_key) > 0:
                logger.warning("otp_verify_locked_out", scope="ip", ip_address=client_ip)
                raise OTPTemporarilyLockedError()

            if await redis.exists(phone_lock_key) > 0:
                logger.warning("otp_verify_locked_out", scope="phone", phone=phone)
                raise OTPTemporarilyLockedError()
        except OTPTemporarilyLockedError:
            raise
        except Exception as e:
            logger.error("otp_verify_lockout_check_failed", error=str(e))

    async def _record_otp_verify_failure(self, phone: str, ip_address: str | None) -> None:
        client_ip = ip_address or "unknown"
        logger.warning("otp_verify_failure_recorded", phone=phone, ip_address=client_ip)

        ip_failure_key = f"rate_limit:otp_verify_fail:ip:{client_ip}"
        phone_failure_key = f"rate_limit:otp_verify_fail:phone:{phone}"

        limiter = rate_limiter.RateLimiter(
            max_requests=OTP_VERIFY_FAILURE_MAX_PER_10_MINUTES,
            window_seconds=10 * 60,
        )

        ip_limited = await limiter.is_rate_limited(ip_failure_key)
        phone_limited = await limiter.is_rate_limited(phone_failure_key)

        if not (ip_limited or phone_limited):
            return

        try:
            redis = await rate_limiter.get_redis()
            if ip_limited:
                ip_lock_key = f"lockout:otp_verify:lock:ip:{client_ip}"
                await redis.setex(ip_lock_key, OTP_VERIFY_LOCKOUT_SECONDS, "1")
                logger.warning("otp_verify_lockout_set", scope="ip", ip_address=client_ip)

            if phone_limited:
                phone_lock_key = f"lockout:otp_verify:lock:phone:{phone}"
                await redis.setex(phone_lock_key, OTP_VERIFY_LOCKOUT_SECONDS, "1")
                logger.warning("otp_verify_lockout_set", scope="phone", phone=phone)
        except Exception as e:
            logger.error("otp_verify_lockout_set_failed", error=str(e))

    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token."""
        try:
            payload = decode_token(refresh_token)
        except ValueError:
            raise InvalidTokenError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token")

        guardian_id = payload.get("sub")
        if not guardian_id:
            raise InvalidTokenError("Invalid token payload")

        # Verify session still exists and is valid
        session_id = payload.get("session_id")
        if session_id:
            session = await self.session_repo.get_by_id(UUID(session_id))
            if not session or not session.is_active:
                raise SessionExpiredError("Session has expired")

        # Generate new tokens
        token_data = {
            "sub": guardian_id,
            "role": "parent",
            "session_id": session_id,
        }
        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "expires_in": 15 * 60,
        }

    async def logout(self, session_id: UUID) -> dict:
        """Invalidate session."""
        await self.session_repo.invalidate(session_id)
        return {"message": "Logged out successfully"}

    async def logout_all(self, guardian_id: UUID) -> dict:
        """Invalidate all sessions for guardian."""
        count = await self.session_repo.invalidate_all(guardian_id)
        return {"message": f"Logged out from {count} devices"}

    async def validate_session(self, session_token: str) -> ParentSession | None:
        """Validate session token."""
        session = await self.session_repo.get_by_token(session_token)
        if not session:
            return None

        # Check inactivity timeout
        timeout = timedelta(minutes=INACTIVITY_TIMEOUT_MINUTES)
        if datetime.now(timezone.utc) - session.last_activity_at > timeout:
            await self.session_repo.invalidate(session.id)
            return None

        # Update activity
        await self.session_repo.update_activity(session.id)
        return session
