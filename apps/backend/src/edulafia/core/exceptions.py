"""Centralized exception classes for the EduLafia backend."""


class ModuleError(Exception):
    """Base exception for all module-level errors."""

    pass


class NotFoundError(ModuleError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str, identifier: str = None):
        self.resource = resource
        self.identifier = identifier
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} not found: {identifier}"
        super().__init__(message)


class ValidationError(ModuleError):
    """Raised when input validation fails."""

    pass


class ConflictError(ModuleError):
    """Raised when a resource conflict occurs (e.g., duplicate unique field)."""

    pass


class PermissionDeniedError(ModuleError):
    """Raised when user lacks permission for an operation."""

    pass
