"""Custom exceptions for the Guardians module."""


class GuardianError(Exception):
    """Base exception for guardian-related errors."""

    pass


class GuardianNotFoundError(GuardianError):
    """Raised when a guardian is not found."""

    def __init__(self, guardian_id: str = None):
        self.guardian_id = guardian_id
        message = f"Guardian not found: {guardian_id}" if guardian_id else "Guardian not found"
        super().__init__(message)


class DuplicateNINError(GuardianError):
    """Raised when attempting to create a guardian with duplicate NIN."""

    def __init__(self, nin: str):
        self.nin = nin
        super().__init__(f"NIN already exists: {nin}")


class GuardianLimitError(GuardianError):
    """Raised when the maximum number of guardians for a student is reached."""

    def __init__(self, max_guardians: int = 2):
        self.max_guardians = max_guardians
        super().__init__(f"Student already has maximum {max_guardians} guardians")


class GuardianArchivedError(GuardianError):
    """Raised when attempting to modify an archived guardian."""

    def __init__(self, guardian_id: str):
        self.guardian_id = guardian_id
        super().__init__(f"Cannot modify archived guardian: {guardian_id}")
