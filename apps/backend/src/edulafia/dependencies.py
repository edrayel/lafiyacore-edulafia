"""Shared FastAPI dependencies for dependency injection."""

import logging

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from edulafia.core.redis_client import is_blacklisted
from edulafia.core.security import decode_token
from edulafia.database import get_db

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

DBSession = Annotated[AsyncSession, Depends(get_db)]
AuthToken = Annotated[HTTPAuthorizationCredentials, Depends(security)]


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """Validates Origin/Referer header on mutating requests to prevent CSRF.

    Skips validation when Origin is absent (non-browser clients like mobile apps).
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def __init__(self, app):
        super().__init__(app)
        from edulafia.config import settings
        self._allowed_origins = settings.CORS_ORIGINS

    async def dispatch(self, request: Request, call_next):
        if request.method not in self.SAFE_METHODS:
            origin = request.headers.get("origin")
            referer = request.headers.get("referer")

            if origin:
                if not self._is_allowed(origin):
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": "CSRF check failed: unknown origin"},
                        headers={
                            "Access-Control-Allow-Origin": ", ".join(self._allowed_origins),
                            "Access-Control-Allow-Credentials": "true",
                        },
                    )
            elif referer:
                if not self._is_allowed(referer):
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": "CSRF check failed: unknown referer"},
                        headers={
                            "Access-Control-Allow-Origin": ", ".join(self._allowed_origins),
                            "Access-Control-Allow-Credentials": "true",
                        },
                    )
        return await call_next(request)

    def _is_allowed(self, url: str) -> bool:
        for allowed in self._allowed_origins:
            if url.startswith(allowed):
                return True
        return False


async def get_current_user(
    request: Request,
    auth_token: AuthToken = None,
) -> dict:
    """Extract and validate the current user from JWT token (cookie or header)."""
    token = None

    if auth_token:
        token = auth_token.credentials
    else:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_token(token)
        token_type = payload.get("type")
        if token_type and token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        jti = payload.get("jti")
        if jti and await is_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return payload
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Auth dependency error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


CurrentUser = Annotated[dict, Depends(get_current_user)]


def require_role(*roles: str):
    """Dependency factory that requires specific user roles."""

    def role_checker(current_user: CurrentUser) -> dict:
        user_role = current_user.get("role")
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return Depends(role_checker)
