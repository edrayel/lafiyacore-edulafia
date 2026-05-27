"""Proprietor Pydantic schemas."""


from pydantic import BaseModel, ConfigDict, Field


class ProprietorDashboardSummary(BaseModel):
    """Schema for proprietor dashboard aggregated summary."""

    model_config = ConfigDict(from_attributes=True)

    total_students: int = Field(default=0)
    active_students: int = Field(default=0)
    total_staff: int = Field(default=0)
    total_revenue: float = Field(default=0.0)
    total_expenses: float = Field(default=0.0)
    outstanding_fees: float = Field(default=0.0)
    attendance_rate: float = Field(default=0.0)
    pending_leave_requests: int = Field(default=0)
    open_discipline_cases: int = Field(default=0)
    active_campaigns: int = Field(default=0)
    ongoing_projects: int = Field(default=0)


class ProprietorFinancialSummary(BaseModel):
    """Schema for proprietor financial summary."""

    model_config = ConfigDict(from_attributes=True)

    total_revenue: float = Field(default=0.0)
    total_expenses: float = Field(default=0.0)
    net_balance: float = Field(default=0.0)
    outstanding_fees: float = Field(default=0.0)
    payroll_total: float = Field(default=0.0)


class ProprietorEnrollmentSummary(BaseModel):
    """Schema for proprietor enrollment summary."""

    model_config = ConfigDict(from_attributes=True)

    total_students: int = Field(default=0)
    new_admissions: int = Field(default=0)
    graduations: int = Field(default=0)
    withdrawals: int = Field(default=0)
    enrollment_by_class: list = Field(default_factory=list)
    enrollment_by_gender: dict = Field(default_factory=dict)


class ProprietorAcademicSummary(BaseModel):
    """Schema for proprietor academic summary."""

    model_config = ConfigDict(from_attributes=True)

    attendance_rate: float = Field(default=0.0)
    open_discipline_cases: int = Field(default=0)
    pending_leave_requests: int = Field(default=0)
    active_clubs: int = Field(default=0)
    active_exam_registrations: int = Field(default=0)


class ProprietorOperationalSummary(BaseModel):
    """Schema for proprietor operational summary."""

    model_config = ConfigDict(from_attributes=True)

    active_campaigns: int = Field(default=0)
    ongoing_projects: int = Field(default=0)
    open_inspections: int = Field(default=0)
    pending_ministry_reports: int = Field(default=0)
