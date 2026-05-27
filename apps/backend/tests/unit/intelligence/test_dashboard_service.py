"""Tests for DashboardService - written BEFORE implementation (TDD)."""

from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest


@pytest.fixture
def mock_kpi_repo():
    """Create a mock KPI definition repository."""
    return AsyncMock()


@pytest.fixture
def mock_snapshot_repo():
    """Create a mock KPI snapshot repository."""
    return AsyncMock()


@pytest.fixture
def mock_lga_repo():
    """Create a mock LGA aggregate repository."""
    return AsyncMock()


@pytest.fixture
def mock_state_repo():
    """Create a mock state aggregate repository."""
    return AsyncMock()


@pytest.fixture
def mock_report_repo():
    """Create a mock report repository."""
    return AsyncMock()


@pytest.fixture
def mock_template_repo():
    """Create a mock template repository."""
    return AsyncMock()


@pytest.fixture
def dashboard_service(
    mock_kpi_repo,
    mock_snapshot_repo,
    mock_lga_repo,
    mock_state_repo,
    mock_report_repo,
    mock_template_repo,
):
    """Create DashboardService with mocked repositories."""
    from edulafia.modules.intelligence.service import DashboardService
    return DashboardService(
        mock_kpi_repo,
        mock_snapshot_repo,
        mock_lga_repo,
        mock_state_repo,
        mock_report_repo,
        mock_template_repo,
    )


def make_kpi_snapshot_mock(
    kpi_id="ATTENDANCE_RATE",
    value=92.5,
    previous_value=90.0,
    trend="up",
    status="normal",
) -> MagicMock:
    """Create a properly configured KPI snapshot mock."""
    mock = MagicMock()
    mock.id = uuid4()
    mock.school_id = uuid4()
    mock.kpi_id = kpi_id
    mock.snapshot_date = date.today()
    mock.value = value
    mock.previous_value = previous_value
    mock.trend = trend
    mock.status = status
    return mock


class TestDashboardService:
    """Test cases for DashboardService."""

    def test_dashboard_service_exists(self):
        """Test that DashboardService class exists."""
        from edulafia.modules.intelligence.service import DashboardService
        assert DashboardService is not None

    async def test_get_school_dashboard_success(self, dashboard_service, mock_snapshot_repo, mock_kpi_repo):
        """Test successful school dashboard retrieval."""
        school_id = uuid4()
        mock_snapshot_repo.get_by_date.return_value = [
            make_kpi_snapshot_mock(kpi_id="ATTENDANCE_RATE", value=92.5),
        ]
        mock_snapshot_repo.get_student_count.return_value = 100
        mock_snapshot_repo.get_teacher_count.return_value = 10
        mock_snapshot_repo.get_class_count.return_value = 5
        mock_snapshot_repo.get_active_alert_count.return_value = 2

        mock_kpi_def = MagicMock()
        mock_kpi_def.code = "ATTENDANCE_RATE"
        mock_kpi_def.name = "Attendance Rate"
        mock_kpi_def.unit = "percent"
        mock_kpi_def.critical_threshold = 85.0
        mock_kpi_def.warning_threshold = 95.0
        mock_kpi_def.higher_is_better = True
        mock_kpi_repo.get_by_id.return_value = mock_kpi_def

        result = await dashboard_service.get_school_dashboard(school_id)

        assert result is not None
        assert result.date == date.today()
        assert len(result.kpis) == 1

    async def test_get_school_dashboard_with_date_filter(self, dashboard_service, mock_snapshot_repo):
        """Test school dashboard with date filter."""
        school_id = uuid4()
        target_date = date(2026, 3, 15)
        mock_snapshot_repo.get_by_date.return_value = []
        mock_snapshot_repo.get_student_count.return_value = 0
        mock_snapshot_repo.get_teacher_count.return_value = 0
        mock_snapshot_repo.get_class_count.return_value = 0
        mock_snapshot_repo.get_active_alert_count.return_value = 0

        from edulafia.modules.intelligence.schemas import DashboardFilters
        filters = DashboardFilters(date=target_date)

        result = await dashboard_service.get_school_dashboard(school_id, filters)

        assert result.date == target_date

    def test_get_kpi_status_critical(self, dashboard_service):
        """Test KPI status is critical when below threshold."""
        from edulafia.modules.intelligence.service import DEFAULT_KPIS

        kpi_config = DEFAULT_KPIS[0]  # ATTENDANCE_RATE

        # Below critical threshold of 85%
        status = dashboard_service._get_kpi_status(Decimal("80"), kpi_config)
        assert status == "critical"

    def test_get_kpi_status_warning(self, dashboard_service):
        """Test KPI status is warning when between thresholds."""
        from edulafia.modules.intelligence.service import DEFAULT_KPIS

        kpi_config = DEFAULT_KPIS[0]  # ATTENDANCE_RATE

        # Between warning (95%) and critical (85%)
        status = dashboard_service._get_kpi_status(Decimal("90"), kpi_config)
        assert status == "warning"

    def test_get_kpi_status_normal(self, dashboard_service):
        """Test KPI status is normal when above target."""
        from edulafia.modules.intelligence.service import DEFAULT_KPIS

        kpi_config = DEFAULT_KPIS[0]  # ATTENDANCE_RATE

        # Above warning threshold of 95%
        status = dashboard_service._get_kpi_status(Decimal("98"), kpi_config)
        assert status == "normal"

    def test_get_trend_up(self, dashboard_service):
        """Test trend is up when value increases."""
        trend = dashboard_service._get_trend(Decimal("95"), Decimal("90"))
        assert trend == "up"

    def test_get_trend_down(self, dashboard_service):
        """Test trend is down when value decreases."""
        trend = dashboard_service._get_trend(Decimal("85"), Decimal("90"))
        assert trend == "down"

    def test_get_trend_stable(self, dashboard_service):
        """Test trend is stable when value unchanged."""
        trend = dashboard_service._get_trend(Decimal("90"), Decimal("90"))
        assert trend == "stable"

    def test_get_trend_stable_when_no_previous(self, dashboard_service):
        """Test trend is stable when no previous value."""
        trend = dashboard_service._get_trend(Decimal("90"), None)
        assert trend == "stable"

    async def test_get_lga_dashboard_success(self, dashboard_service, mock_lga_repo):
        """Test successful LGA dashboard retrieval."""
        lga = "Lagos Island"
        state = "Lagos"

        mock_aggregate = MagicMock()
        mock_aggregate.lga = lga
        mock_aggregate.state = state
        mock_aggregate.aggregate_date = date.today()
        mock_aggregate.total_schools = 25
        mock_aggregate.total_students = 5000
        mock_aggregate.avg_attendance_rate = Decimal("91.5")
        mock_aggregate.total_sick_bay_visits = 45
        mock_aggregate.total_collections = Decimal("1500000")
        mock_aggregate.open_alerts_count = 2

        mock_lga_repo.get_by_lga_date.return_value = mock_aggregate

        result = await dashboard_service.get_lga_dashboard(lga, state)

        assert result.lga == lga
        assert result.total_schools == 25
        assert result.total_students == 5000

    async def test_get_lga_dashboard_empty(self, dashboard_service, mock_lga_repo):
        """Test LGA dashboard when no data exists."""
        mock_lga_repo.get_by_lga_date.return_value = None

        result = await dashboard_service.get_lga_dashboard("Unknown", "Unknown")

        assert result.total_schools == 0
        assert result.total_students == 0

    async def test_generate_report_enqueues_durable_job(self, dashboard_service, mock_report_repo, mock_template_repo, monkeypatch):
        from types import SimpleNamespace

        from edulafia.core import arq_queue
        from edulafia.modules.intelligence.schemas import ReportGenerateRequest

        enqueue_mock = AsyncMock()
        monkeypatch.setattr(arq_queue, "enqueue_generate_report", enqueue_mock)

        report_id = uuid4()
        user_id = uuid4()
        school_id = uuid4()

        mock_report_repo.create.return_value = SimpleNamespace(
            id=report_id,
            report_type="attendance",
            parameters={"format": "csv"},
            status="pending",
            progress_percent=0,
            created_at=datetime.utcnow(),
            file_format=None,
            file_path=None,
            error_message=None,
            expires_at=None,
            completed_at=None,
        )

        req = ReportGenerateRequest(report_type="attendance", parameters={}, format="csv")
        await dashboard_service.generate_report(req, user_id=user_id, school_id=school_id)

        enqueue_mock.assert_awaited_once()

    async def test_get_sentinel_dashboard_success(self, dashboard_service):
        """Test successful sentinel dashboard retrieval."""
        with patch("edulafia.database.AsyncSessionLocal") as mock_session:
            mock_ctx = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_ctx
            mock_ctx.execute.side_effect = [
                MagicMock(scalar=MagicMock(return_value=5)),  # active_alerts
                MagicMock(scalar=MagicMock(return_value=20)),  # recent_signals
                MagicMock(fetchall=MagicMock(return_value=[("school", 3), ("lga", 2)])),  # by tier
                MagicMock(fetchall=MagicMock(return_value=[("active", 5), ("resolved", 15)])),  # by status
            ]
            result = await dashboard_service.get_sentinel_dashboard()

        assert result is not None
        assert result.active_alerts == 5
        assert result.recent_signals == 20

    async def test_generate_report_success(self, dashboard_service, mock_report_repo, monkeypatch):
        """Test successful report generation."""
        from edulafia.modules.intelligence.schemas import ReportGenerateRequest
        from edulafia.core import arq_queue

        mock_report = MagicMock()
        mock_report.id = uuid4()
        mock_report.report_type = "school"
        mock_report.status = "pending"
        mock_report.progress_percent = 0
        mock_report.file_format = "pdf"
        mock_report.parameters = {}
        mock_report.created_at = datetime.now()
        mock_report.completed_at = None
        mock_report.expires_at = None
        mock_report.error_message = None
        mock_report.file_path = None

        mock_report_repo.create.return_value = mock_report
        
        enqueue_mock = AsyncMock()
        monkeypatch.setattr(arq_queue, "enqueue_generate_report", enqueue_mock)

        data = ReportGenerateRequest(
            report_type="school",
            parameters={"school_id": str(uuid4())},
            format="pdf",
        )

        result = await dashboard_service.generate_report(data, uuid4(), uuid4())

        assert result.report_type == "school"
        assert result.status == "pending"
        enqueue_mock.assert_awaited_once()
