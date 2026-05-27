"""Custom exceptions for the Health module."""


class HealthError(Exception):
    """Base exception for health-related errors."""

    pass


class HealthProfileNotFoundError(HealthError):
    """Raised when a health profile is not found."""

    def __init__(self, student_id: str = None):
        self.student_id = student_id
        message = f"Health profile not found: {student_id}" if student_id else "Health profile not found"
        super().__init__(message)


class SickBayVisitNotFoundError(HealthError):
    """Raised when a sick bay visit is not found."""

    def __init__(self, visit_id: str = None):
        self.visit_id = visit_id
        message = f"Sick bay visit not found: {visit_id}" if visit_id else "Sick bay visit not found"
        super().__init__(message)


class ReferralNotFoundError(HealthError):
    """Raised when a referral is not found."""

    def __init__(self, referral_id: str = None):
        self.referral_id = referral_id
        message = f"Referral not found: {referral_id}" if referral_id else "Referral not found"
        super().__init__(message)


class NurseRoleRequiredError(HealthError):
    """Raised when non-nurse attempts health operation."""

    def __init__(self):
        super().__init__("Only users with Nurse or Health Officer role can perform this operation")


class InsufficientPermissionError(HealthError):
    """Raised when user lacks required permission."""

    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(f"Insufficient permission to access {resource}")


class ParentalConsentRequiredError(HealthError):
    """Raised when parental consent is required."""

    def __init__(self):
        super().__init__("Parental consent is required for this operation")


class SentinelSignalNotFoundError(HealthError):
    """Raised when a sentinel signal is not found."""

    def __init__(self, signal_id: str = None):
        self.signal_id = signal_id
        message = f"Sentinel signal not found: {signal_id}" if signal_id else "Sentinel signal not found"
        super().__init__(message)


class InvalidSymptomCodesError(HealthError):
    """Raised when symptom codes are invalid."""

    def __init__(self, codes: list[str]):
        self.codes = codes
        super().__init__(f"Invalid symptom codes: {', '.join(codes)}")
