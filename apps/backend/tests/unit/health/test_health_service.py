"""Tests for HealthService and SentinelEngine - written BEFORE implementation (TDD)."""

from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_profile_repo():
    """Create a mock health profile repository."""
    return AsyncMock()


@pytest.fixture
def mock_visit_repo():
    """Create a mock sick bay visit repository."""
    repo = AsyncMock()
    repo.count_visits_for_student_term.return_value = 0
    return repo


@pytest.fixture
def mock_screening_repo():
    """Create a mock health screening repository."""
    return AsyncMock()


@pytest.fixture
def mock_referral_repo():
    """Create a mock referral repository."""
    return AsyncMock()


@pytest.fixture
def mock_vaccination_repo():
    """Create a mock vaccination repository."""
    return AsyncMock()


@pytest.fixture
def health_service(
    mock_profile_repo,
    mock_visit_repo,
    mock_screening_repo,
    mock_referral_repo,
    mock_vaccination_repo,
):
    """Create HealthService with mocked repositories."""
    from edulafia.modules.health.service import HealthService
    return HealthService(
        mock_profile_repo,
        mock_visit_repo,
        mock_screening_repo,
        mock_referral_repo,
        mock_vaccination_repo,
    )


def make_visit_mock(
    id=None,
    student_id=None,
    complaint_codes=None,
    outcome="returned_to_class",
) -> MagicMock:
    """Create a properly configured SickBayVisit mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.student_id = student_id or uuid4()
    mock.school_id = uuid4()
    mock.visit_date = date.today()
    mock.visit_time = datetime.now().time()
    mock.presenting_complaint_codes = complaint_codes or ["fever"]
    mock.presenting_complaint_notes = None
    mock.temperature = None
    mock.blood_pressure_systolic = None
    mock.blood_pressure_diastolic = None
    mock.pulse_rate = None
    mock.treatment_given = None
    mock.outcome = outcome
    mock.referred_to = None
    mock.parent_notified = False
    mock.is_sentinel_relevant = False
    mock.recorded_by = uuid4()
    mock.created_at = datetime.now()
    mock.updated_at = datetime.now()
    return mock


class TestHealthService:
    """Test cases for HealthService."""

    def test_health_service_exists(self):
        """Test that HealthService class exists."""
        from edulafia.modules.health.service import HealthService
        assert HealthService is not None

    async def test_log_sick_bay_visit_success(self, health_service, mock_visit_repo):
        """Test successful sick bay visit logging."""
        from edulafia.modules.health.schemas import SickBayVisitCreate

        mock_visit_repo.create.return_value = make_visit_mock(
            complaint_codes=["fever"],
            outcome="returned_to_class",
        )

        data = SickBayVisitCreate(
            student_id=uuid4(),
            presenting_complaint_codes=["fever"],
            outcome="returned_to_class",
        )

        result = await health_service.log_sick_bay_visit(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
            user_role="nurse",
        )

        assert result.presenting_complaint_codes == ["fever"]
        assert result.outcome == "returned_to_class"

    async def test_log_sick_bay_visit_non_nurse_fails(self, health_service, mock_visit_repo):
        """Test that non-nurse cannot log sick bay visit."""
        from edulafia.modules.health.exceptions import NurseRoleRequiredError
        from edulafia.modules.health.schemas import SickBayVisitCreate

        data = SickBayVisitCreate(
            student_id=uuid4(),
            presenting_complaint_codes=["fever"],
            outcome="returned_to_class",
        )

        with pytest.raises(NurseRoleRequiredError):
            await health_service.log_sick_bay_visit(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
                user_role="teacher",  # Not nurse
            )

    async def test_log_sick_bay_visit_with_symptoms(self, health_service, mock_visit_repo):
        """Test logging sick bay visit with multiple symptoms."""
        from edulafia.modules.health.schemas import SickBayVisitCreate

        mock_visit_repo.create.return_value = make_visit_mock(
            complaint_codes=["fever", "cough", "headache"],
            outcome="sent_home",
        )

        data = SickBayVisitCreate(
            student_id=uuid4(),
            presenting_complaint_codes=["fever", "cough", "headache"],
            temperature=38.5,
            outcome="sent_home",
        )

        result = await health_service.log_sick_bay_visit(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
            user_role="nurse",
        )

        assert result.presenting_complaint_codes == ["fever", "cough", "headache"]
        assert result.outcome == "sent_home"

    async def test_conduct_screening_success(self, health_service, mock_screening_repo):
        """Test successful health screening."""
        from edulafia.modules.health.schemas import HealthScreeningCreate

        screening_mock = MagicMock()
        screening_mock.id = uuid4()
        screening_mock.student_id = uuid4()
        screening_mock.school_id = uuid4()
        screening_mock.screening_date = date.today()
        screening_mock.screening_type = "annual"
        screening_mock.height = 150
        screening_mock.weight = 45
        screening_mock.bmi = 20.0
        screening_mock.muac = None
        screening_mock.vision_left = None
        screening_mock.vision_right = None
        screening_mock.hearing_left = None
        screening_mock.hearing_right = None
        screening_mock.blood_pressure_systolic = None
        screening_mock.blood_pressure_diastolic = None
        screening_mock.dental_notes = None
        screening_mock.sickle_cell_test_result = None
        screening_mock.flags = []
        screening_mock.follow_up_required = False
        screening_mock.follow_up_notes = None
        screening_mock.conducted_by = uuid4()
        screening_mock.version = 1
        screening_mock.created_at = datetime.now()
        screening_mock.updated_at = datetime.now()

        mock_screening_repo.create.return_value = screening_mock

        data = HealthScreeningCreate(
            student_id=uuid4(),
            screening_type="annual",
            height=150,
            weight=45,
        )

        result = await health_service.conduct_screening(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
            user_role="nurse",
        )

        assert result.screening_type == "annual"
        assert result.bmi == 20.0

    async def test_create_referral_success(self, health_service, mock_referral_repo):
        """Test successful referral creation."""
        from edulafia.modules.health.schemas import ReferralCreate

        referral_mock = MagicMock()
        referral_mock.id = uuid4()
        referral_mock.student_id = uuid4()
        referral_mock.sick_bay_visit_id = None
        referral_mock.school_id = uuid4()
        referral_mock.referral_date = date.today()
        referral_mock.destination_facility = "General Hospital"
        referral_mock.reason = "Suspected malaria"
        referral_mock.priority = "urgent"
        referral_mock.status = "pending"
        referral_mock.follow_up_due_date = date.today()
        referral_mock.outcome_notes = None
        referral_mock.outcome_date = None
        referral_mock.reminder_sent = False
        referral_mock.created_by = uuid4()
        referral_mock.created_at = datetime.now()
        referral_mock.updated_at = datetime.now()

        mock_referral_repo.create.return_value = referral_mock

        data = ReferralCreate(
            student_id=uuid4(),
            destination_facility="General Hospital",
            reason="Suspected malaria",
            priority="urgent",
            follow_up_due_date=date.today(),
        )

        result = await health_service.create_referral(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.destination_facility == "General Hospital"
        assert result.status == "pending"

    async def test_record_vaccination_success(self, health_service, mock_vaccination_repo):
        """Test successful vaccination recording."""
        from edulafia.modules.health.schemas import VaccinationRecordCreate

        vaccination_mock = MagicMock()
        vaccination_mock.id = uuid4()
        vaccination_mock.student_id = uuid4()
        vaccination_mock.school_id = uuid4()
        vaccination_mock.vaccine_name = "Measles"
        vaccination_mock.vaccine_code = None
        vaccination_mock.dose_number = 1
        vaccination_mock.administration_date = date.today()
        vaccination_mock.lot_number = None
        vaccination_mock.administering_facility = None
        vaccination_mock.created_at = datetime.now()
        vaccination_mock.updated_at = datetime.now()

        mock_vaccination_repo.create.return_value = vaccination_mock

        data = VaccinationRecordCreate(
            student_id=uuid4(),
            vaccine_name="Measles",
            dose_number=1,
            administration_date=date.today(),
        )

        result = await health_service.record_vaccination(
            data=data,
            school_id=uuid4(),
        )

        assert result.vaccine_name == "Measles"
        assert result.dose_number == 1


class TestSentinelEngine:
    """Test cases for SentinelEngine."""

    @pytest.fixture
    def sentinel_engine(self):
        """Create SentinelEngine with mocked repositories."""
        from edulafia.modules.health.sentinel import SentinelEngine

        visit_repo = AsyncMock()
        signal_repo = AsyncMock()
        config_repo = AsyncMock()

        # Default config
        config = MagicMock()
        config.time_window_hours = 48
        config.cluster_threshold = 3
        config_repo.get_active_config.return_value = config

        return SentinelEngine(visit_repo, signal_repo, config_repo)

    def test_sentinel_engine_exists(self):
        """Test that SentinelEngine class exists."""
        from edulafia.modules.health.sentinel import SentinelEngine
        assert SentinelEngine is not None

    def test_combine_symptom_events(self, sentinel_engine):
        """Test combining symptom events from different sources."""
        visit1 = make_visit_mock(complaint_codes=["fever", "cough"])
        visit2 = make_visit_mock(complaint_codes=["vomiting"])

        events = sentinel_engine.combine_symptom_events([visit1, visit2])

        assert len(events) == 2
        assert events[0]["source"] == "sick_bay"

    def test_group_by_symptom_profile(self, sentinel_engine):
        """Test grouping visits by symptom profile."""
        visit1 = make_visit_mock(complaint_codes=["fever", "cough"])
        visit2 = make_visit_mock(complaint_codes=["fever", "cough"])
        visit3 = make_visit_mock(complaint_codes=["vomiting"])

        groups = sentinel_engine.group_by_symptom_profile([visit1, visit2, visit3])

        assert "cough,fever" in groups
        assert len(groups["cough,fever"]) == 2
        assert "vomiting" in groups
        assert len(groups["vomiting"]) == 1

    def test_calculate_percentage_affected(self, sentinel_engine):
        """Test percentage calculation."""
        result = sentinel_engine.calculate_percentage_affected(10, 100)
        assert result == 10.0

    def test_calculate_percentage_affected_zero_population(self, sentinel_engine):
        """Test percentage calculation with zero population."""
        result = sentinel_engine.calculate_percentage_affected(10, 0)
        assert result == 0.0

    async def test_analyze_school_signals_below_threshold(self, sentinel_engine):
        """Test that signals are not created below threshold."""
        sentinel_engine.visit_repo.get_visits_in_time_window.return_value = [
            make_visit_mock(complaint_codes=["fever"]),
            make_visit_mock(complaint_codes=["cough"]),
        ]

        signals = await sentinel_engine.analyze_school_signals(
            school_id=uuid4(),
            lga="Test LGA",
            state="Lagos",
        )

        assert len(signals) == 0  # Below threshold of 3

    async def test_create_signal(self, sentinel_engine):
        """Test creating a sentinel signal."""
        signal_mock = MagicMock()
        signal_mock.id = uuid4()
        signal_mock.alert_tier = "school"
        signal_mock.threshold_type = "school_cluster"
        signal_mock.status = "active"

        sentinel_engine.signal_repo.create.return_value = signal_mock

        result = await sentinel_engine.create_signal(
            school_ids=[uuid4()],
            symptom_profile={"symptoms": ["fever", "cough"], "count": 5},
            students_affected=5,
            threshold_type="school_cluster",
            alert_tier="school",
            lga="Test LGA",
            state="Lagos",
        )

        assert result["alert_tier"] == "school"
        assert result["status"] == "active"
