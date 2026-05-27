"""Custom exceptions for the Staff module."""


class StaffError(Exception):
    """Base exception for staff-related errors."""

    pass


class StaffNotFoundError(StaffError):
    """Raised when staff member is not found."""

    def __init__(self, staff_id: str = None):
        self.staff_id = staff_id
        message = f"Staff not found: {staff_id}" if staff_id else "Staff not found"
        super().__init__(message)


class DuplicateStaffIdError(StaffError):
    """Raised when duplicate staff ID exists."""

    def __init__(self, staff_id: str):
        self.staff_id = staff_id
        super().__init__(f"Staff ID already exists: {staff_id}")


class AssignmentNotFoundError(StaffError):
    """Raised when assignment is not found."""

    def __init__(self, assignment_id: str = None):
        self.assignment_id = assignment_id
        message = f"Assignment not found: {assignment_id}" if assignment_id else "Assignment not found"
        super().__init__(message)


class DuplicateAssignmentError(StaffError):
    """Raised when duplicate assignment exists."""

    def __init__(self, staff_id: str, class_id: str, subject_id: str):
        self.staff_id = staff_id
        self.class_id = class_id
        self.subject_id = subject_id
        super().__init__(f"Assignment already exists for staff {staff_id} in class {class_id} for subject {subject_id}")


class TimetableNotFoundError(StaffError):
    """Raised when timetable is not found."""

    def __init__(self, timetable_id: str = None):
        self.timetable_id = timetable_id
        message = f"Timetable not found: {timetable_id}" if timetable_id else "Timetable not found"
        super().__init__(message)


class TimetableClashError(StaffError):
    """Raised when timetable clash is detected."""

    def __init__(self, clashes: list):
        self.clashes = clashes
        super().__init__(f"Timetable has {len(clashes)} clash(es)")


class TimetableAlreadyPublishedError(StaffError):
    """Raised when trying to modify published timetable."""

    def __init__(self, timetable_id: str):
        self.timetable_id = timetable_id
        super().__init__(f"Timetable {timetable_id} is already published")


class DraftTimetableExistsError(StaffError):
    """Raised when draft timetable already exists for class/term."""

    def __init__(self, class_id: str, term_id: str):
        self.class_id = class_id
        self.term_id = term_id
        super().__init__(f"Draft timetable already exists for class {class_id} and term {term_id}")


class FormTeacherAlreadyAssignedError(StaffError):
    """Raised when class already has a form teacher."""

    def __init__(self, class_id: str):
        self.class_id = class_id
        super().__init__(f"Class {class_id} already has a form teacher")


class TeacherNotQualifiedError(StaffError):
    """Raised when teacher is not qualified for subject."""

    def __init__(self, staff_id: str, subject_id: str):
        self.staff_id = staff_id
        self.subject_id = subject_id
        super().__init__(f"Teacher {staff_id} is not qualified for subject {subject_id}")


class MaxLoadExceededError(StaffError):
    """Raised when teacher exceeds maximum load."""

    def __init__(self, staff_id: str, current_load: int, max_load: int):
        self.staff_id = staff_id
        self.current_load = current_load
        self.max_load = max_load
        super().__init__(f"Teacher {staff_id} load ({current_load}) exceeds maximum ({max_load})")


class CheckInWindowClosedError(StaffError):
    """Raised when check-in window is closed."""

    def __init__(self):
        super().__init__("Check-in window is closed")


class AlreadyCheckedInError(StaffError):
    """Raised when teacher already checked in today."""

    def __init__(self, staff_id: str, date: str):
        self.staff_id = staff_id
        self.date = date
        super().__init__(f"Teacher {staff_id} already checked in on {date}")


class CommunicationNotFoundError(StaffError):
    """Raised when communication is not found."""

    def __init__(self, communication_id: str = None):
        self.communication_id = communication_id
        message = f"Communication not found: {communication_id}" if communication_id else "Communication not found"
        super().__init__(message)
