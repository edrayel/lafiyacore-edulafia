"""Tests for Intelligence models and schemas - written BEFORE implementation (TDD)."""

from uuid import uuid4

import pytest


class TestKPIDefinitionModel:
    """Test cases for KPIDefinition model."""

    def test_kpi_definition_model_exists(self):
        """Test that KPIDefinition model class exists."""
        from edulafia.modules.intelligence.models import KPIDefinition
        assert KPIDefinition is not None

    def test_kpi_definition_has_required_fields(self):
        """Test that KPIDefinition has all required fields."""
        from edulafia.modules.intelligence.models import KPIDefinition
        columns = KPIDefinition.__table__.columns.keys()

        required_fields = [
            'id', 'code', 'name', 'unit', 'source_module',
            'is_active', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"KPIDefinition missing field: {field}"

    def test_kpi_definition_has_table_name(self):
        """Test that KPIDefinition has correct table name."""
        from edulafia.modules.intelligence.models import KPIDefinition
        assert KPIDefinition.__tablename__ == 'kpi_definitions'


class TestSchoolKPISnapshotModel:
    """Test cases for SchoolKPISnapshot model."""

    def test_school_kpi_snapshot_model_exists(self):
        """Test that SchoolKPISnapshot model class exists."""
        from edulafia.modules.intelligence.models import SchoolKPISnapshot
        assert SchoolKPISnapshot is not None

    def test_school_kpi_snapshot_has_required_fields(self):
        """Test that SchoolKPISnapshot has all required fields."""
        from edulafia.modules.intelligence.models import SchoolKPISnapshot
        columns = SchoolKPISnapshot.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'kpi_id', 'snapshot_date',
            'value', 'status', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"SchoolKPISnapshot missing field: {field}"

    def test_school_kpi_snapshot_has_table_name(self):
        """Test that SchoolKPISnapshot has correct table name."""
        from edulafia.modules.intelligence.models import SchoolKPISnapshot
        assert SchoolKPISnapshot.__tablename__ == 'school_kpi_snapshots'


class TestLGAAggregateModel:
    """Test cases for LGAAggregate model."""

    def test_lga_aggregate_model_exists(self):
        """Test that LGAAggregate model class exists."""
        from edulafia.modules.intelligence.models import LGAAggregate
        assert LGAAggregate is not None

    def test_lga_aggregate_has_required_fields(self):
        """Test that LGAAggregate has all required fields."""
        from edulafia.modules.intelligence.models import LGAAggregate
        columns = LGAAggregate.__table__.columns.keys()

        required_fields = [
            'id', 'lga', 'state', 'aggregate_date', 'aggregate_level',
            'total_schools', 'total_students', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"LGAAggregate missing field: {field}"

    def test_lga_aggregate_has_table_name(self):
        """Test that LGAAggregate has correct table name."""
        from edulafia.modules.intelligence.models import LGAAggregate
        assert LGAAggregate.__tablename__ == 'lga_aggregates'


class TestReportTemplateModel:
    """Test cases for ReportTemplate model."""

    def test_report_template_model_exists(self):
        """Test that ReportTemplate model class exists."""
        from edulafia.modules.intelligence.models import ReportTemplate
        assert ReportTemplate is not None

    def test_report_template_has_required_fields(self):
        """Test that ReportTemplate has all required fields."""
        from edulafia.modules.intelligence.models import ReportTemplate
        columns = ReportTemplate.__table__.columns.keys()

        required_fields = [
            'id', 'name', 'report_type', 'layout', 'is_default',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"ReportTemplate missing field: {field}"

    def test_report_template_has_table_name(self):
        """Test that ReportTemplate has correct table name."""
        from edulafia.modules.intelligence.models import ReportTemplate
        assert ReportTemplate.__tablename__ == 'report_templates'


class TestIntelligenceSchemas:
    """Test cases for Intelligence schemas."""

    def test_kpi_response_exists(self):
        """Test that KPIResponse schema exists."""
        from edulafia.modules.intelligence.schemas import KPIResponse
        assert KPIResponse is not None

    def test_school_dashboard_response_exists(self):
        """Test that SchoolDashboardResponse schema exists."""
        from edulafia.modules.intelligence.schemas import SchoolDashboardResponse
        assert SchoolDashboardResponse is not None

    def test_lga_dashboard_response_exists(self):
        """Test that LGADashboardResponse schema exists."""
        from edulafia.modules.intelligence.schemas import LGADashboardResponse
        assert LGADashboardResponse is not None

    def test_sentinel_dashboard_response_exists(self):
        """Test that SentinelDashboardResponse schema exists."""
        from edulafia.modules.intelligence.schemas import SentinelDashboardResponse
        assert SentinelDashboardResponse is not None

    def test_report_generate_request_exists(self):
        """Test that ReportGenerateRequest schema exists."""
        from edulafia.modules.intelligence.schemas import ReportGenerateRequest
        assert ReportGenerateRequest is not None

    def test_report_generate_request_validates_type(self):
        """Test that ReportGenerateRequest validates report type."""
        from pydantic import ValidationError

        from edulafia.modules.intelligence.schemas import ReportGenerateRequest

        with pytest.raises(ValidationError):
            ReportGenerateRequest(report_type="invalid")

    def test_report_generate_request_validates_format(self):
        """Test that ReportGenerateRequest validates format."""
        from pydantic import ValidationError

        from edulafia.modules.intelligence.schemas import ReportGenerateRequest

        with pytest.raises(ValidationError):
            ReportGenerateRequest(report_type="school", format="invalid")

    def test_research_data_request_create_exists(self):
        """Test that ResearchDataRequestCreate schema exists."""
        from edulafia.modules.intelligence.schemas import ResearchDataRequestCreate
        assert ResearchDataRequestCreate is not None


class TestAnonymizer:
    """Test cases for data anonymization."""

    def test_anonymizer_exists(self):
        """Test that Anonymizer class exists."""
        from edulafia.modules.intelligence.anonymization import Anonymizer
        assert Anonymizer is not None

    def test_anonymize_for_lga_suppresses_low_counts(self):
        """Test LGA anonymization suppresses counts below threshold."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        data = {
            "total_students": 100,
            "total_sick_bay_visits": 3,  # Below suppression threshold of 5
            "avg_attendance_rate": 92.7,
        }

        result = Anonymizer.anonymize_for_lga(data)

        assert result["total_sick_bay_visits"] is None
        assert result["total_students"] == 100

    def test_anonymize_for_lga_hides_small_populations(self):
        """Test LGA anonymization hides data when population too small."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        data = {
            "total_students": 5,  # Below minimum of 10
            "total_sick_bay_visits": 2,
            "avg_attendance_rate": 80.0,
        }

        result = Anonymizer.anonymize_for_lga(data)

        assert result["total_students"] is None
        assert result["avg_attendance_rate"] is None

    def test_anonymize_for_state_hides_small_populations(self):
        """Test state anonymization hides data when population too small."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        data = {
            "total_students": 20,  # Below minimum of 30
            "total_sick_bay_visits": 5,
        }

        result = Anonymizer.anonymize_for_state(data)

        assert result["total_students"] is None

    def test_anonymize_for_research_removes_names(self):
        """Test research anonymization removes name fields."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        data = [
            {
                "student_id": uuid4(),
                "first_name": "Chioma",
                "last_name": "Okonkwo",
                "phone": "08012345678",
                "email": "chioma@example.com",
                "attendance_rate": 95.0,
                "lga": "Lagos Island",
                "state": "Lagos",
            }
        ] * 60  # Need at least 50 records

        result = Anonymizer.anonymize_for_research(data)

        # Check that names are removed
        for record in result:
            assert "first_name" not in record
            assert "last_name" not in record
            assert "phone" not in record
            assert "email" not in record
            assert "student_id" not in record

    def test_anonymize_for_research_requires_minimum_population(self):
        """Test research anonymization requires minimum population."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        data = [{"lga": "Test"}] * 10  # Below minimum of 50

        result = Anonymizer.anonymize_for_research(data)

        assert len(result) == 0

    def test_round_to_nearest(self):
        """Test rounding to nearest multiple."""
        from edulafia.modules.intelligence.anonymization import Anonymizer

        assert Anonymizer.round_to_nearest(7, 5) == 5
        assert Anonymizer.round_to_nearest(8, 5) == 10
        assert Anonymizer.round_to_nearest(13, 5) == 15
