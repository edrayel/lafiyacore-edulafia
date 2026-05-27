"""Custom exceptions for the Finance module."""


class FinanceError(Exception):
    """Base exception for finance-related errors."""

    pass


class FeeScheduleNotFoundError(FinanceError):
    """Raised when a fee schedule is not found."""

    def __init__(self, schedule_id: str = None):
        self.schedule_id = schedule_id
        message = f"Fee schedule not found: {schedule_id}" if schedule_id else "Fee schedule not found"
        super().__init__(message)


class FeeScheduleLockedError(FinanceError):
    """Raised when attempting to modify a locked fee schedule."""

    def __init__(self, schedule_id: str):
        self.schedule_id = schedule_id
        super().__init__(f"Fee schedule {schedule_id} is locked and cannot be modified")


class DuplicateFeeCategoryError(FinanceError):
    """Raised when duplicate fee category exists for same class level."""

    def __init__(self, class_level: str, fee_category: str):
        self.class_level = class_level
        self.fee_category = fee_category
        super().__init__(f"Duplicate fee category '{fee_category}' for class level '{class_level}'")


class PaymentNotFoundError(FinanceError):
    """Raised when a payment is not found."""

    def __init__(self, payment_id: str = None):
        self.payment_id = payment_id
        message = f"Payment not found: {payment_id}" if payment_id else "Payment not found"
        super().__init__(message)


class PaymentExceedsLimitError(FinanceError):
    """Raised when payment amount exceeds maximum limit."""

    def __init__(self, amount: float, max_amount: float = 500000):
        self.amount = amount
        self.max_amount = max_amount
        super().__init__(f"Payment amount ₦{amount:,.2f} exceeds maximum limit of ₦{max_amount:,.2f}")


class InsufficientPermissionError(FinanceError):
    """Raised when user lacks required permission."""

    def __init__(self, message: str = "Insufficient permission"):
        super().__init__(message)


class BursarRoleRequiredError(FinanceError):
    """Raised when non-bursar attempts to record payment."""

    def __init__(self):
        super().__init__("Only users with Bursar role can record payments")


class StudentInactiveError(FinanceError):
    """Raised when attempting to process payment for inactive student."""

    def __init__(self, student_id: str):
        self.student_id = student_id
        super().__init__(f"Cannot process payment for inactive student: {student_id}")


class OnlinePaymentReversalError(FinanceError):
    """Raised when attempting to reverse online payment without confirmation."""

    def __init__(self):
        super().__init__("Online payment reversal requires gateway confirmation")


class GatewayNotConfiguredError(FinanceError):
    """Raised when payment gateway is not configured."""

    def __init__(self, gateway: str):
        self.gateway = gateway
        super().__init__(f"Payment gateway '{gateway}' is not configured for this school")


class InvalidWebhookSignatureError(FinanceError):
    """Raised when webhook signature is invalid."""

    def __init__(self, gateway: str):
        self.gateway = gateway
        super().__init__(f"Invalid webhook signature for {gateway}")


class DuplicateWebhookError(FinanceError):
    """Raised when webhook is a duplicate."""

    def __init__(self, reference: str):
        self.reference = reference
        super().__init__(f"Duplicate webhook for reference: {reference}")


class ScholarshipNotFoundError(FinanceError):
    """Raised when a scholarship is not found."""

    def __init__(self, scholarship_id: str = None):
        self.scholarship_id = scholarship_id
        message = f"Scholarship not found: {scholarship_id}" if scholarship_id else "Scholarship not found"
        super().__init__(message)


class DuplicateScholarshipAwardError(FinanceError):
    """Raised when same scholarship awarded twice in same year."""

    def __init__(self, student_id: str, scholarship_id: str, academic_year_id: str):
        self.student_id = student_id
        self.scholarship_id = scholarship_id
        self.academic_year_id = academic_year_id
        super().__init__(
            f"Scholarship {scholarship_id} already awarded to student {student_id} "
            f"for academic year {academic_year_id}"
        )
