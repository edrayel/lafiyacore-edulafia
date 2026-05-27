"""Custom exceptions for the Intelligence module."""


class IntelligenceError(Exception):
    """Base exception for intelligence-related errors."""

    pass


class DashboardNotFoundError(IntelligenceError):
    """Raised when dashboard data is not found."""

    def __init__(self, dashboard_type: str):
        self.dashboard_type = dashboard_type
        super().__init__(f"Dashboard not found: {dashboard_type}")


class KPICalculationError(IntelligenceError):
    """Raised when KPI calculation fails."""

    def __init__(self, kpi_code: str, error: str):
        self.kpi_code = kpi_code
        super().__init__(f"KPI calculation failed for {kpi_code}: {error}")


class ReportNotFoundError(IntelligenceError):
    """Raised when report is not found."""

    def __init__(self, report_id: str = None):
        self.report_id = report_id
        message = f"Report not found: {report_id}" if report_id else "Report not found"
        super().__init__(message)


class ReportGenerationError(IntelligenceError):
    """Raised when report generation fails."""

    def __init__(self, report_id: str, error: str):
        self.report_id = report_id
        super().__init__(f"Report generation failed for {report_id}: {error}")


class ResearchRequestNotFoundError(IntelligenceError):
    """Raised when research request is not found."""

    def __init__(self, request_id: str = None):
        self.request_id = request_id
        message = f"Research request not found: {request_id}" if request_id else "Research request not found"
        super().__init__(message)


class InsufficientPopulationError(IntelligenceError):
    """Raised when population is below minimum threshold for anonymization."""

    def __init__(self, population: int, minimum: int):
        self.population = population
        self.minimum = minimum
        super().__init__(f"Population {population} is below minimum threshold {minimum}")


class DataExportLimitError(IntelligenceError):
    """Raised when export download limit is exceeded."""

    def __init__(self, download_count: int, max_downloads: int):
        self.download_count = download_count
        self.max_downloads = max_downloads
        super().__init__(f"Download limit exceeded: {download_count}/{max_downloads}")


class UnauthorizedAccessError(IntelligenceError):
    """Raised when user lacks required role for dashboard access."""

    def __init__(self, required_role: str):
        self.required_role = required_role
        super().__init__(f"Access denied. Required role: {required_role}")
