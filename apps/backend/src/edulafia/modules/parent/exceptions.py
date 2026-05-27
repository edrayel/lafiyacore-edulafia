"""Custom exceptions for the Parent module."""


class ParentError(Exception):
    """Base exception for parent-related errors."""

    pass


class AuthenticationError(ParentError):
    """Base exception for authentication errors."""

    pass


class InvalidOTPError(AuthenticationError):
    """Raised when OTP is invalid."""

    def __init__(self):
        super().__init__("Invalid OTP code")


class ExpiredOTPError(AuthenticationError):
    """Raised when OTP has expired."""

    def __init__(self):
        super().__init__("OTP has expired")


class MaxAttemptsExceededError(AuthenticationError):
    """Raised when max verification attempts exceeded."""

    def __init__(self):
        super().__init__("Maximum verification attempts exceeded")


class RateLimitExceededError(AuthenticationError):
    """Raised when OTP request rate limit exceeded."""

    def __init__(self):
        super().__init__("Rate limit exceeded. Please try again later")


class OTPTemporarilyLockedError(AuthenticationError):
    """Raised when OTP verification is temporarily locked out."""

    def __init__(self):
        super().__init__("Too many attempts. Please try again later")


class SessionExpiredError(AuthenticationError):
    """Raised when session has expired."""

    def __init__(self):
        super().__init__("Session has expired. Please login again")


class SessionNotFoundError(AuthenticationError):
    """Raised when session is not found."""

    def __init__(self):
        super().__init__("Session not found")


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid."""

    def __init__(self):
        super().__init__("Invalid token")


class GuardianNotFoundError(ParentError):
    """Raised when guardian is not found."""

    def __init__(self, phone: str = None):
        self.phone = phone
        message = f"Guardian not found: {phone}" if phone else "Guardian not found"
        super().__init__(message)


class ChildAccessDeniedError(ParentError):
    """Raised when guardian tries to access unlinked child."""

    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Access denied to student {student_id}")


class NotificationNotFoundError(ParentError):
    """Raised when notification is not found."""

    def __init__(self, notification_id: str = None):
        self.notification_id = notification_id
        message = f"Notification not found: {notification_id}" if notification_id else "Notification not found"
        super().__init__(message)


class ExcusalNotFoundError(ParentError):
    """Raised when excusal is not found."""

    def __init__(self, excusal_id: str = None):
        self.excusal_id = excusal_id
        message = f"Excusal not found: {excusal_id}" if excusal_id else "Excusal not found"
        super().__init__(message)


class FeedbackNotFoundError(ParentError):
    """Raised when feedback is not found."""

    def __init__(self, feedback_id: str = None):
        self.feedback_id = feedback_id
        message = f"Feedback not found: {feedback_id}" if feedback_id else "Feedback not found"
        super().__init__(message)


class QuietHoursError(ParentError):
    """Raised when non-urgent notification blocked by quiet hours."""

    def __init__(self):
        super().__init__("Non-urgent notifications blocked during quiet hours (9PM-6AM)")


class NotificationDisabledError(ParentError):
    """Raised when notification type is disabled for guardian."""

    def __init__(self, notification_type: str):
        self.notification_type = notification_type
        super().__init__(f"Notifications of type '{notification_type}' are disabled")
