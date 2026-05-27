"""Custom exceptions for the Attendance module."""


class AttendanceError(Exception):
    """Base exception for attendance-related errors."""

    pass


class AttendanceNotFoundError(AttendanceError):
    """Raised when an attendance record is not found."""

    def __init__(self, record_id: str = None):
        self.record_id = record_id
        message = f"Attendance record not found: {record_id}" if record_id else "Attendance record not found"
        super().__init__(message)


class DuplicateAttendanceError(AttendanceError):
    """Raised when attempting to create duplicate attendance."""

    def __init__(self, student_id: str, attendance_date: str):
        self.student_id = student_id
        self.attendance_date = attendance_date
        super().__init__(f"Attendance already exists for student {student_id} on {attendance_date}")


class EditWindowExpiredError(AttendanceError):
    """Raised when attempting to edit attendance after edit window."""

    def __init__(self, edit_window_hours: int = 24):
        self.edit_window_hours = edit_window_hours
        super().__init__(f"Edit window of {edit_window_hours} hours has expired")


class TeacherNotAssignedError(AttendanceError):
    """Raised when teacher is not assigned to class."""

    def __init__(self, teacher_id: str, class_id: str):
        self.teacher_id = teacher_id
        self.class_id = class_id
        super().__init__(f"Teacher {teacher_id} is not assigned to class {class_id}")


class StudentNotEnrolledError(AttendanceError):
    """Raised when student is not enrolled in class."""

    def __init__(self, student_id: str, class_id: str):
        self.student_id = student_id
        self.class_id = class_id
        super().__init__(f"Student {student_id} is not enrolled in class {class_id}")


class FutureDateError(AttendanceError):
    """Raised when attempting to mark attendance for future dates."""

    def __init__(self):
        super().__init__("Cannot mark attendance for future dates")


class SymptomRequiredError(AttendanceError):
    """Raised when symptoms are required but not provided."""

    def __init__(self):
        super().__init__("Symptoms are required when reason is 'sick'")


class ReasonRequiredError(AttendanceError):
    """Raised when reason is required but not provided."""

    def __init__(self):
        super().__init__("Reason is required for absences")
