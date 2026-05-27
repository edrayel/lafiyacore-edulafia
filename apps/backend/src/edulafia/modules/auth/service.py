"""Authentication service for login, logout, and token management."""

import logging
import traceback
from datetime import UTC, datetime, timedelta
from uuid import UUID

from edulafia.core.redis_client import blacklist_token, is_blacklisted
from edulafia.core.security import (
    create_access_token,
    create_refresh_token,
    create_user_token_payload,
    decode_token,
    hash_password,
    verify_password,
)
from edulafia.modules.auth.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserDeletedError,
    UserDisabledError,
    WeakPasswordError,
)
from edulafia.modules.auth.models import User
from edulafia.modules.auth.repository import AuthRepository

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication business logic."""

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    async def login(self, email: str, password: str) -> dict:
        """Authenticate user with email and password.

        Raises:
            InvalidCredentialsError: If email/password is wrong.
            UserDisabledError: If account is disabled.
            UserDeletedError: If account is soft-deleted.
        """
        user = await self.repository.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Invalid email or password")

        if user.deleted_at is not None:
            raise UserDeletedError("Account has been deleted")

        if user.status != "active":
            raise UserDisabledError("Account is disabled")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        # Update last login
        await self.repository.update_last_login(user.id)

        # Generate tokens
        payload = create_user_token_payload(
            user_id=user.id,
            role=user.role,
            school_id=user.school_id,
        )
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 15 * 60,  # 15 minutes
            "user": user,
        }

    async def refresh(self, refresh_token: str) -> dict:
        """Generate new access token from refresh token.

        Raises:
            InvalidTokenError: If refresh token is invalid.
            TokenExpiredError: If refresh token has expired.
        """
        try:
            payload = decode_token(refresh_token)
            jti = payload.get("jti")
            if jti and await is_blacklisted(jti):
                raise InvalidTokenError("Refresh token has been revoked")
        except ValueError:
            raise InvalidTokenError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token")

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Invalid token payload")

        # Verify user still exists and is active
        user = await self.repository.get_by_id(UUID(user_id))
        if user is None:
            raise InvalidTokenError("User not found")
        if user.status != "active":
            raise UserDisabledError("Account is disabled")

        # Generate new tokens with fresh payload
        new_payload = create_user_token_payload(
            user_id=user.id,
            role=user.role,
            school_id=user.school_id,
        )
        new_access_token = create_access_token(new_payload)
        new_refresh_token = create_refresh_token(new_payload)

        # Blacklist old refresh token
        if jti:
            exp = payload.get("exp", 0)
            ttl = max(0, int(exp) - int(datetime.now(UTC).timestamp()))
            await blacklist_token(jti, ttl)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": 15 * 60,
        }

    async def change_password(
        self,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> dict:
        """Change user password.

        Raises:
            InvalidCredentialsError: If current password is wrong.
            WeakPasswordError: If new password is too weak.
        """
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise InvalidCredentialsError("User not found")

        if not verify_password(current_password, user.password_hash):
            raise InvalidCredentialsError("Current password is incorrect")

        # Check new password is different
        if verify_password(new_password, user.password_hash):
            raise WeakPasswordError("New password must be different from current password")

        new_hash = hash_password(new_password)
        await self.repository.update_password(user_id, new_hash)

        return {"message": "Password changed successfully"}

    async def get_current_user(self, user_id: UUID) -> User | None:
        """Get current user profile by ID."""
        return await self.repository.get_by_id(user_id)

    async def forgot_password(self, email: str) -> dict:
        """Request password reset.

        Raises:
            UserNotFoundError: If user with email not found.
        """
        user = await self.repository.get_by_email(email)
        if user is None:
            # Return success message even if user doesn't exist to prevent email enumeration
            return {"message": "If an account exists with that email, a reset link has been sent"}

        # Generate password reset token (JWT with short expiry)
        reset_token = create_access_token(
            {"sub": str(user.id), "type": "reset"},
            expires_delta=timedelta(hours=1)  # 1-hour expiry
        )

        try:
            from edulafia.core.email import send_email_async
            from edulafia.config import settings
            reset_link = f"{settings.APP_URL}/reset-password?token={reset_token}"
            await send_email_async(
                to_email=email,
                subject="EduLafia - Password Reset Request",
                body=f"""
                <h2>Password Reset</h2>
                <p>You requested a password reset for your EduLafia account.</p>
                <p>Click the link below to reset your password (expires in 1 hour):</p>
                <p><a href="{reset_link}">{reset_link}</a></p>
                <p>If you did not request this, please ignore this email.</p>
                """
            )
        except Exception:
            logger.error(
                "Password reset email failed to send",
                extra={"email": email, "error": traceback.format_exc()},
            )
            return {"message": "Unable to send password reset email at this time. Please try again later."}

    async def reset_password(self, reset_token: str, new_password: str) -> dict:
        """Reset password using reset token.

        Raises:
            InvalidTokenError: If reset token is invalid or expired.
            WeakPasswordError: If new password is too weak.
        """
        try:
            payload = decode_token(reset_token)
            jti = payload.get("jti")
            if jti and await is_blacklisted(jti):
                raise InvalidTokenError("Reset token has been revoked")
        except ValueError:
            raise InvalidTokenError("Invalid or expired reset token")

        if payload.get("type") != "reset":
            raise InvalidTokenError("Token is not a valid reset token")

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Invalid token payload")

        # Verify user exists and is active
        user = await self.repository.get_by_id(UUID(user_id))
        if user is None:
            raise InvalidTokenError("User not found")
        if user.status != "active":
            raise UserDisabledError("Account is disabled")

        # Validate new password
        from edulafia.modules.auth.schemas import ResetPasswordRequest
        try:
            ResetPasswordRequest.validate_new_password(new_password)
        except Exception as e:
            raise WeakPasswordError(str(e))

        # Update password
        await self.repository.update_password(UUID(user_id), hash_password(new_password))

        # Blacklist reset token
        if jti:
            exp = payload.get("exp", 0)
            ttl = max(0, int(exp) - int(datetime.now(UTC).timestamp()))
            await blacklist_token(jti, ttl)

        return {"message": "Password reset successfully"}

    async def logout(self, access_token: str, refresh_token: str | None = None) -> dict:
        """Logout user by blacklisting tokens.

        Raises:
            InvalidTokenError: If access token is invalid.
        """
        try:
            payload = decode_token(access_token)
            jti = payload.get("jti")
            if jti:
                exp = payload.get("exp", 0)
                ttl = max(0, int(exp) - int(datetime.now(UTC).timestamp()))
                await blacklist_token(jti, ttl)
        except ValueError:
            raise InvalidTokenError("Invalid access token")

        if refresh_token:
            try:
                refresh_payload = decode_token(refresh_token)
                refresh_jti = refresh_payload.get("jti")
                if refresh_jti:
                    exp = refresh_payload.get("exp", 0)
                    ttl = max(0, int(exp) - int(datetime.now(UTC).timestamp()))
                    await blacklist_token(refresh_jti, ttl)
            except ValueError:
                logger.warning("Failed to decode refresh token during logout", exc_info=True)

        return {"message": "Logged out successfully"}
