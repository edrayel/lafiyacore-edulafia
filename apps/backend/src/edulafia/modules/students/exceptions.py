"""Custom exceptions for the Students module."""


class StudentError(Exception):
    """Base exception for student-related errors."""

    pass


class StudentNotFoundError(StudentError):
    """Raised when a student is not found."""

    def __init__(self, student_id: str = None):
        self.student_id = student_id
        message = f"Student not found: {student_id}" if student_id else "Student not found"
        super().__init__(message)


class DuplicateAdmissionNumberError(StudentError):
    """Raised when attempting to create a student with duplicate admission number."""

    def __init__(self, admission_number: str):
        self.admission_number = admission_number
        super().__init__(f"Admission number already exists: {admission_number}")


class DuplicateNINError(StudentError):
    """Raised when attempting to create a student with duplicate NIN."""

    def __init__(self, nin: str):
        self.nin = nin
        super().__init__(f"NIN already exists: {nin}")


class InvalidStatusTransitionError(StudentError):
    """Raised when an invalid status transition is attempted."""

    def __init__(self, from_status: str, to_status: str):
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(f"Cannot transition from '{from_status}' to '{to_status}'")


class StudentArchivedError(StudentError):
    """Raised when attempting to modify an archived student."""

    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Cannot modify archived student: {student_id}")


class AgeValidationError(StudentError):
    """Raised when student age is outside valid range."""

    def __init__(self, age: int, min_age: int = 6, max_age: int = 20):
        self.age = age
        self.min_age = min_age
        self.max_age = max_age
        super().__init__(f"Student age {age} must be between {min_age} and {max_age}")
