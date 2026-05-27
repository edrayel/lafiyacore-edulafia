"""Cookie utilities for secure httpOnly cookie management."""

from fastapi import Response

from edulafia.config import settings


def set_auth_cookie(
    response: Response,
    token: str,
    cookie_name: str = "access_token",
    max_age: int = 900,
) -> None:
    """Set a secure httpOnly cookie on the response."""
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=max_age,
        path="/api",
    )


def set_refresh_cookie(
    response: Response,
    token: str,
    cookie_name: str = "refresh_token",
    max_age: int = 604800,
) -> None:
    """Set a secure httpOnly refresh token cookie."""
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=max_age,
        path="/api",
    )


def clear_auth_cookies(response: Response) -> None:
    """Clear authentication cookies from the response."""
    response.delete_cookie(key="access_token", path="/api")
    response.delete_cookie(key="refresh_token", path="/api")
