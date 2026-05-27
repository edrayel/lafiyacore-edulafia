"""Tests for Health models and schemas - written BEFORE implementation (TDD)."""

from uuid import uuid4

import pytest


class TestStudentHealthProfileModel:
    """Test cases for StudentHealthProfile model."""

    def test_health_profile_model_exists(self):
        """Test that StudentHealthProfile model class exists."""
        from edulafia.modules.health.models import StudentHealthProfile
        assert StudentHealthProfile is not None

    def test_health_profile_has_required_fields(self):
        """Test that StudentHealthProfile has all required fields."""
        from edulafia.modules.health.models import StudentHealthProfile
        columns = StudentHealthProfile.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'parental_consent_given',
            'version', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"StudentHealthProfile missing field: {field}"

    def test_health_profile_has_table_name(self):
        """Test that StudentHealthProfile has correct table name."""
        from edulafia.modules.health.models import StudentHealthProfile
        assert StudentHealthProfile.__tablename__ == 'student_health_profiles'


class TestSickBayVisitModel:
    """Test cases for SickBayVisit model."""

    def test_sick_bay_visit_model_exists(self):
        """Test that SickBayVisit model class exists."""
        from edulafia.modules.health.models import SickBayVisit
        assert SickBayVisit is not None

    def test_sick_bay_visit_has_required_fields(self):
        """Test that SickBayVisit has all required fields."""
        from edulafia.modules.health.models import SickBayVisit
        columns = SickBayVisit.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'visit_date', 'visit_time',
            'presenting_complaint_codes', 'outcome', 'recorded_by',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"SickBayVisit missing field: {field}"

    def test_sick_bay_visit_has_table_name(self):
        """Test that SickBayVisit has correct table name."""
        from edulafia.modules.health.models import SickBayVisit
        assert SickBayVisit.__tablename__ == 'sick_bay_visits'


class TestHealthScreeningModel:
    """Test cases for HealthScreening model."""

    def test_health_screening_model_exists(self):
        """Test that HealthScreening model class exists."""
        from edulafia.modules.health.models import HealthScreening
        assert HealthScreening is not None

    def test_health_screening_has_required_fields(self):
        """Test that HealthScreening has all required fields."""
        from edulafia.modules.health.models import HealthScreening
        columns = HealthScreening.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'screening_date',
            'screening_type', 'conducted_by', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"HealthScreening missing field: {field}"

    def test_health_screening_has_table_name(self):
        """Test that HealthScreening has correct table name."""
        from edulafia.modules.health.models import HealthScreening
        assert HealthScreening.__tablename__ == 'health_screenings'


class TestReferralModel:
    """Test cases for Referral model."""

    def test_referral_model_exists(self):
        """Test that Referral model class exists."""
        from edulafia.modules.health.models import Referral
        assert Referral is not None

    def test_referral_has_required_fields(self):
        """Test that Referral has all required fields."""
        from edulafia.modules.health.models import Referral
        columns = Referral.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'referral_date',
            'destination_facility', 'reason', 'status', 'follow_up_due_date',
            'created_by', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"Referral missing field: {field}"

    def test_referral_has_table_name(self):
        """Test that Referral has correct table name."""
        from edulafia.modules.health.models import Referral
        assert Referral.__tablename__ == 'referrals'


class TestVaccinationRecordModel:
    """Test cases for VaccinationRecord model."""

    def test_vaccination_record_model_exists(self):
        """Test that VaccinationRecord model class exists."""
        from edulafia.modules.health.models import VaccinationRecord
        assert VaccinationRecord is not None

    def test_vaccination_record_has_required_fields(self):
        """Test that VaccinationRecord has all required fields."""
        from edulafia.modules.health.models import VaccinationRecord
        columns = VaccinationRecord.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'vaccine_name',
            'dose_number', 'administration_date', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"VaccinationRecord missing field: {field}"

    def test_vaccination_record_has_table_name(self):
        """Test that VaccinationRecord has correct table name."""
        from edulafia.modules.health.models import VaccinationRecord
        assert VaccinationRecord.__tablename__ == 'vaccination_records'


class TestSentinelSignalModel:
    """Test cases for SentinelSignal model."""

    def test_sentinel_signal_model_exists(self):
        """Test that SentinelSignal model class exists."""
        from edulafia.modules.health.models import SentinelSignal
        assert SentinelSignal is not None

    def test_sentinel_signal_has_required_fields(self):
        """Test that SentinelSignal has all required fields."""
        from edulafia.modules.health.models import SentinelSignal
        columns = SentinelSignal.__table__.columns.keys()

        required_fields = [
            'id', 'school_ids', 'date_generated', 'symptom_profile',
            'students_affected', 'threshold_type', 'alert_tier', 'status',
            'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"SentinelSignal missing field: {field}"

    def test_sentinel_signal_has_table_name(self):
        """Test that SentinelSignal has correct table name."""
        from edulafia.modules.health.models import SentinelSignal
        assert SentinelSignal.__tablename__ == 'sentinel_signals'


class TestHealthSchemas:
    """Test cases for Health schemas."""

    def test_sick_bay_visit_create_schema_exists(self):
        """Test that SickBayVisitCreate schema exists."""
        from edulafia.modules.health.schemas import SickBayVisitCreate
        assert SickBayVisitCreate is not None

    def test_sick_bay_visit_create_validates_outcome(self):
        """Test that SickBayVisitCreate validates outcome."""
        from pydantic import ValidationError

        from edulafia.modules.health.schemas import SickBayVisitCreate

        with pytest.raises(ValidationError):
            SickBayVisitCreate(
                student_id=uuid4(),
                presenting_complaint_codes=["fever"],
                outcome="invalid_outcome",
            )

    def test_health_screening_create_schema_exists(self):
        """Test that HealthScreeningCreate schema exists."""
        from edulafia.modules.health.schemas import HealthScreeningCreate
        assert HealthScreeningCreate is not None

    def test_referral_create_schema_exists(self):
        """Test that ReferralCreate schema exists."""
        from edulafia.modules.health.schemas import ReferralCreate
        assert ReferralCreate is not None

    def test_vaccination_record_create_schema_exists(self):
        """Test that VaccinationRecordCreate schema exists."""
        from edulafia.modules.health.schemas import VaccinationRecordCreate
        assert VaccinationRecordCreate is not None

    def test_sentinel_signal_response_exists(self):
        """Test that SentinelSignalResponse schema exists."""
        from edulafia.modules.health.schemas import SentinelSignalResponse
        assert SentinelSignalResponse is not None
