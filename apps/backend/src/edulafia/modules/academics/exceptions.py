"""Custom exceptions for the Academics module."""


class AcademicsError(Exception):
    """Base exception for academics-related errors."""

    pass


class SubjectNotFoundError(AcademicsError):
    """Raised when a subject is not found."""

    def __init__(self, subject_id: str = None):
        self.subject_id = subject_id
        message = f"Subject not found: {subject_id}" if subject_id else "Subject not found"
        super().__init__(message)


class DuplicateSubjectCodeError(AcademicsError):
    """Raised when attempting to create a subject with duplicate code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Subject code already exists: {code}")


class AcademicResultNotFoundError(AcademicsError):
    """Raised when an academic result is not found."""

    def __init__(self, result_id: str = None):
        self.result_id = result_id
        message = f"Academic result not found: {result_id}" if result_id else "Academic result not found"
        super().__init__(message)


class ScoreLockError(AcademicsError):
    """Raised when attempting to modify locked scores."""

    def __init__(self, message: str = "Scores are locked for editing"):
        super().__init__(message)


class InvalidScoreError(AcademicsError):
    """Raised when a score is invalid."""

    def __init__(self, field: str, value: float, max_value: float):
        self.field = field
        self.value = value
        self.max_value = max_value
        super().__init__(f"{field} score {value} exceeds maximum {max_value}")


class MissingScoresError(AcademicsError):
    """Raised when not all scores are submitted."""

    def __init__(self, missing_count: int):
        self.missing_count = missing_count
        super().__init__(f"{missing_count} subject scores not yet submitted")


class GradingScaleError(AcademicsError):
    """Raised for grading scale validation errors."""

    pass


class ReportCardError(AcademicsError):
    """Raised for report card generation errors."""

    pass
