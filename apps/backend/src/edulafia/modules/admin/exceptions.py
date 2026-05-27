"""Custom exceptions for the Admin module."""


class AdminError(Exception):
    """Base exception for admin-related errors."""

    pass


class SchoolProvisioningError(AdminError):
    """Base exception for school provisioning errors."""

    pass


class DuplicateSchoolError(SchoolProvisioningError):
    """Raised when school already exists."""

    def __init__(self, school_name: str):
        self.school_name = school_name
        super().__init__(f"School already exists: {school_name}")


class SchoolNotProvisionedError(SchoolProvisioningError):
    """Raised when school is not yet provisioned."""

    def __init__(self, school_id: str):
        self.school_id = school_id
        super().__init__(f"School not provisioned: {school_id}")


class SchoolAlreadyActiveError(SchoolProvisioningError):
    """Raised when school is already active."""

    def __init__(self, school_id: str):
        self.school_id = school_id
        super().__init__(f"School already active: {school_id}")


class OnboardingNotCompleteError(SchoolProvisioningError):
    """Raised when onboarding checklist is not complete."""

    def __init__(self, missing_steps: list[str]):
        self.missing_steps = missing_steps
        super().__init__(f"Onboarding not complete. Missing steps: {', '.join(missing_steps)}")


class UserManagementError(AdminError):
    """Base exception for user management errors."""

    pass


class DuplicateEmailError(UserManagementError):
    """Raised when email already exists."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email already exists: {email}")


class UserNotFoundError(UserManagementError):
    """Raised when user is not found."""

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        message = f"User not found: {user_id}" if user_id else "User not found"
        super().__init__(message)


class CannotDeactivateLastAdminError(UserManagementError):
    """Raised when trying to deactivate the last admin."""

    def __init__(self, school_id: str):
        self.school_id = school_id
        super().__init__(f"Cannot deactivate last admin for school: {school_id}")


class AccountLockedError(UserManagementError):
    """Raised when account is locked."""

    def __init__(self):
        super().__init__("Account is locked due to too many failed login attempts")


class SyncMonitoringError(AdminError):
    """Base exception for sync monitoring errors."""

    pass


class SyncTriggerError(SyncMonitoringError):
    """Raised when sync trigger fails."""

    def __init__(self, school_id: str, reason: str):
        self.school_id = school_id
        super().__init__(f"Failed to trigger sync for school {school_id}: {reason}")


class ConflictResolutionError(SyncMonitoringError):
    """Raised when conflict resolution fails."""

    def __init__(self, conflict_id: str):
        self.conflict_id = conflict_id
        super().__init__(f"Failed to resolve conflict: {conflict_id}")


class SentinelConfigError(AdminError):
    """Base exception for sentinel configuration errors."""

    pass


class ThresholdNotFoundError(SentinelConfigError):
    """Raised when threshold is not found."""

    def __init__(self, threshold_id: str = None):
        self.threshold_id = threshold_id
        message = f"Threshold not found: {threshold_id}" if threshold_id else "Threshold not found"
        super().__init__(message)


class ThresholdApprovalRequiredError(SentinelConfigError):
    """Raised when threshold change requires approval."""

    def __init__(self):
        super().__init__("Threshold changes require super admin approval")


class SystemUpdateError(AdminError):
    """Base exception for system update errors."""

    pass


class UpdateNotFoundError(SystemUpdateError):
    """Raised when update is not found."""

    def __init__(self, update_id: str = None):
        self.update_id = update_id
        message = f"Update not found: {update_id}" if update_id else "Update not found"
        super().__init__(message)


class UpdateDeploymentError(SystemUpdateError):
    """Raised when update deployment fails."""

    def __init__(self, update_id: str, reason: str):
        self.update_id = update_id
        super().__init__(f"Failed to deploy update {update_id}: {reason}")


class TrainingError(AdminError):
    """Base exception for training-related errors."""

    pass


class TrainingResourceNotFoundError(TrainingError):
    """Raised when training resource is not found."""

    def __init__(self, resource_id: str = None):
        self.resource_id = resource_id
        message = f"Training resource not found: {resource_id}" if resource_id else "Training resource not found"
        super().__init__(message)
