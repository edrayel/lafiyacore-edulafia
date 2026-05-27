"""Authentication exceptions."""


class AuthError(Exception):
    """Base authentication error."""

    pass


class InvalidCredentialsError(AuthError):
    """Raised when login credentials are invalid."""

    pass


class UserNotFoundError(AuthError):
    """Raised when user does not exist."""

    pass


class UserDisabledError(AuthError):
    """Raised when user account is disabled."""

    pass


class UserDeletedError(AuthError):
    """Raised when user account is soft-deleted."""

    pass


class InvalidTokenError(AuthError):
    """Raised when JWT token is invalid or expired."""

    pass


class TokenExpiredError(AuthError):
    """Raised when JWT token has expired."""

    pass


class WeakPasswordError(AuthError):
    """Raised when password does not meet complexity requirements."""

    pass


class PasswordReuseError(AuthError):
    """Raised when new password matches previous password."""

    pass
