"""Authentication API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status

from edulafia.core.rate_limiter import rate_limit
from edulafia.core.cookies import clear_auth_cookies, set_auth_cookie, set_refresh_cookie
from edulafia.dependencies import CurrentUser, DBSession
from edulafia.modules.auth.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    TokenExpiredError,
    UserDeletedError,
    UserDisabledError,
    WeakPasswordError,
)
from edulafia.modules.auth.repository import AuthRepository
from edulafia.modules.auth.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
)
from edulafia.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: DBSession) -> AuthService:
    """Dependency for auth service."""
    return AuthService(repository=AuthRepository(db))


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60))])
async def login(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Authenticate user with email and password.

    Sets httpOnly cookies for access_token and refresh_token.
    """
    try:
        result = await service.login(data.email, data.password)
        set_auth_cookie(response, result["access_token"])
        set_refresh_cookie(response, result["refresh_token"])
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    except UserDisabledError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    except UserDeletedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deleted",
        )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(max_requests=10, window_seconds=60))])
async def refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Generate new access token from refresh cookie."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    try:
        result = await service.refresh(refresh_token)
        set_auth_cookie(response, result["access_token"])
        set_refresh_cookie(response, result["refresh_token"])
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except UserDisabledError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )


@router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(max_requests=10, window_seconds=60))])
async def logout(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Logout current user and blacklist tokens."""
    access_token = request.cookies.get("access_token", "")
    refresh_token = request.cookies.get("refresh_token")
    await service.logout(access_token, refresh_token)
    clear_auth_cookies(response)
    return {"message": "Logged out successfully"}


@router.post("/forgot-password", status_code=200, dependencies=[Depends(rate_limit(max_requests=3, window_seconds=300))])
async def forgot_password(
    data: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Request password reset email."""
    return await service.forgot_password(data.email)


@router.post("/reset-password", status_code=200, dependencies=[Depends(rate_limit(max_requests=5, window_seconds=300))])
async def reset_password(
    data: ResetPasswordRequest = Body(...),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Reset password using reset token."""
    try:
        return await service.reset_password(data.token, data.new_password)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    except UserDisabledError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/change-password", status_code=status.HTTP_200_OK, dependencies=[Depends(rate_limit(max_requests=5, window_seconds=300))])
async def change_password(
    data: ChangePasswordRequest,
    current_user: CurrentUser,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Change current user's password."""
    try:
        user_id = UUID(current_user["sub"])
        return await service.change_password(
            user_id=user_id,
            current_password=data.current_password,
            new_password=data.new_password,
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: CurrentUser,
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Get current user profile."""
    user_id = UUID(current_user["sub"])
    user = await service.get_current_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.model_validate(user)
