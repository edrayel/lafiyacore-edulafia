"""Intelligence & Analytics Pydantic schemas."""

from datetime import date as DateType
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

# KPI Schemas

class KPIResponse(BaseModel):
    """Schema for KPI response."""

    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    value: Decimal
    unit: str
    trend: str | None = None  # up, down, stable
    status: str  # critical, warning, normal
    previous_value: Decimal | None = None


class QuickStatsResponse(BaseModel):
    """Schema for quick stats response."""

    total_students: int
    total_teachers: int
    total_classes: int
    active_alerts: int


class AlertResponse(BaseModel):
    """Schema for alert response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    alert_type: str
    title: str
    message: str
    severity: str
    status: str
    created_at: datetime


class TrendDataPoint(BaseModel):
    """Schema for trend data point."""

    date: DateType
    value: Decimal
    label: str | None = None


class TrendResponse(BaseModel):
    """Schema for trend response."""

    metric_name: str
    data_points: list[TrendDataPoint]
    period: str  # daily, weekly, monthly


# Dashboard Schemas

class SchoolDashboardResponse(BaseModel):
    """Schema for school dashboard response."""

    kpis: list[KPIResponse]
    alerts: list[AlertResponse]
    trends: list[TrendResponse]
    quick_stats: QuickStatsResponse
    date: DateType
    last_updated: datetime
    cache_expires_at: datetime


class LGASchoolComparison(BaseModel):
    """Schema for LGA school comparison."""

    school_id: UUID
    school_name: str
    attendance_rate: Decimal | None = None
    sick_bay_visits: int = 0
    open_alerts: int = 0


class LGADashboardResponse(BaseModel):
    """Schema for LGA dashboard response."""

    lga: str
    state: str
    date: DateType
    total_schools: int
    total_students: int
    avg_attendance_rate: Decimal | None = None
    total_sick_bay_visits: int = 0
    total_collections: Decimal = Decimal("0")
    open_alerts: int = 0
    school_comparison: list[LGASchoolComparison] = []
    last_updated: datetime


class StateDashboardResponse(BaseModel):
    """Schema for state dashboard response."""

    state: str
    date: DateType
    total_lgas: int
    total_schools: int
    total_students: int
    avg_attendance_rate: Decimal | None = None
    total_sick_bay_visits: int = 0
    total_collections: Decimal = Decimal("0")
    open_alerts: int = 0
    last_updated: datetime


class SentinelDashboardResponse(BaseModel):
    """Schema for sentinel dashboard response."""

    date: DateType
    date_range_start: DateType
    date_range_end: DateType
    active_alerts: int
    recent_signals: int
    signals_by_tier: dict
    signals_by_status: dict
    trend_data: list[TrendDataPoint] = []
    last_updated: datetime


# Report Schemas

class ReportGenerateRequest(BaseModel):
    """Schema for report generation request."""

    report_type: str = Field(..., description="school, lga, state, sentinel")
    parameters: dict = Field(default={})
    format: str = Field(default="pdf", description="pdf, csv, xlsx")

    @field_validator("report_type")
    @classmethod
    def validate_report_type(cls, v: str) -> str:
        """Validate report type."""
        valid_types = ["school", "lga", "state", "sentinel", "attendance", "academic", "finance"]
        if v.lower() not in valid_types:
            raise ValueError(f"Report type must be one of: {', '.join(valid_types)}")
        return v.lower()

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Validate format."""
        valid_formats = ["pdf", "csv", "xlsx"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Format must be one of: {', '.join(valid_formats)}")
        return v.lower()


class ReportResponse(BaseModel):
    """Schema for report response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    report_type: str
    parameters: dict
    status: str
    file_format: str | None = None
    file_path: str | None = None
    progress_percent: int
    error_message: str | None = None
    expires_at: datetime | None = None
    created_at: datetime
    completed_at: datetime | None = None


class ReportTemplateResponse(BaseModel):
    """Schema for report template response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    report_type: str
    layout: dict
    is_default: bool
    is_system: bool
    created_at: datetime
    updated_at: datetime


# Research Schemas

class ResearchDataRequestCreate(BaseModel):
    """Schema for creating research data request."""

    request_title: str = Field(..., min_length=1, max_length=255)
    research_purpose: str = Field(..., min_length=1)
    data_categories: list[str] = Field(..., min_length=1)
    date_range_start: DateType
    date_range_end: DateType
    geographic_scope: dict | None = None
    ethics_approval_reference: str = Field(..., min_length=1)
    ethics_approval_date: DateType
    institution: str = Field(..., min_length=1)


class ResearchDataRequestResponse(BaseModel):
    """Schema for research data request response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    researcher_id: UUID
    request_title: str
    research_purpose: str
    data_categories: list[str]
    date_range_start: DateType
    date_range_end: DateType
    ethics_approval_reference: str
    institution: str
    status: str
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    data_file_path: str | None = None
    data_file_expires_at: datetime | None = None
    download_count: int
    max_downloads: int
    created_at: datetime
    updated_at: datetime


# Filter Schemas

class DashboardFilters(BaseModel):
    """Schema for dashboard filters."""

    date: DateType | None = None
    term_id: UUID | None = None
    start_date: DateType | None = None
    end_date: DateType | None = None


class SentinelFilters(BaseModel):
    """Schema for sentinel filters."""

    school_id: UUID | None = None
    lga: str | None = None
    state: str | None = None
    start_date: DateType | None = None
    end_date: DateType | None = None
    tier: str | None = None
    status: str | None = None
