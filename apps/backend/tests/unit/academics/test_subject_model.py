"""Tests for Subject SQLAlchemy model - written BEFORE implementation."""


import pytest


class TestSubjectModel:
    """Test cases for Subject model structure and constraints."""

    def test_subject_model_exists(self):
        """Test that Subject model class exists."""
        from edulafia.modules.academics.models import Subject
        assert Subject is not None

    def test_subject_has_required_fields(self):
        """Test that Subject model has all required fields."""
        from edulafia.modules.academics.models import Subject
        columns = Subject.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'name', 'code', 'is_core',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"Subject model missing field: {field}"

    def test_subject_has_optional_fields(self):
        """Test that Subject model has optional fields."""
        from edulafia.modules.academics.models import Subject
        columns = Subject.__table__.columns.keys()

        optional_fields = [
            'description', 'waec_code', 'neco_code',
            'created_by', 'updated_by', 'deleted_at'
        ]
        for field in optional_fields:
            assert field in columns, f"Subject model missing optional field: {field}"

    def test_subject_default_is_core(self):
        """Test that is_core defaults to True."""
        from edulafia.modules.academics.models import Subject
        is_core_col = Subject.__table__.columns['is_core']
        assert is_core_col.default is not None
        assert is_core_col.default.arg == True

    def test_subject_has_table_name(self):
        """Test that Subject model has correct table name."""
        from edulafia.modules.academics.models import Subject
        assert Subject.__tablename__ == 'subjects'

    def test_subject_has_timestamps(self):
        """Test that Subject has created_at and updated_at fields."""
        from edulafia.modules.academics.models import Subject
        columns = Subject.__table__.columns.keys()
        assert 'created_at' in columns
        assert 'updated_at' in columns

    def test_subject_has_soft_delete(self):
        """Test that Subject has soft delete capability."""
        from edulafia.modules.academics.models import Subject
        columns = Subject.__table__.columns.keys()
        assert 'deleted_at' in columns


class TestSubjectSchema:
    """Test cases for Subject schema validation."""

    def test_subject_create_schema_exists(self):
        """Test that SubjectCreate schema exists."""
        from edulafia.modules.academics.schemas import SubjectCreate
        assert SubjectCreate is not None

    def test_create_subject_with_required_fields(self):
        """Test creating subject with all required fields."""

        from edulafia.modules.academics.schemas import SubjectCreate

        subject = SubjectCreate(
            name="Mathematics",
            code="MATH",
        )
        assert subject.name == "Mathematics"
        assert subject.code == "MATH"
        assert subject.is_core == True  # Default

    def test_create_subject_with_waec_code(self):
        """Test creating subject with WAEC code."""
        from edulafia.modules.academics.schemas import SubjectCreate

        subject = SubjectCreate(
            name="Mathematics",
            code="MATH",
            waec_code="402",
        )
        assert subject.waec_code == "402"

    def test_create_subject_with_neco_code(self):
        """Test creating subject with NECO code."""
        from edulafia.modules.academics.schemas import SubjectCreate

        subject = SubjectCreate(
            name="Mathematics",
            code="MATH",
            neco_code="MAT001",
        )
        assert subject.neco_code == "MAT001"

    def test_create_subject_without_name_fails(self):
        """Test that creating subject without name fails."""
        from pydantic import ValidationError

        from edulafia.modules.academics.schemas import SubjectCreate

        with pytest.raises(ValidationError):
            SubjectCreate(
                code="MATH",
            )

    def test_create_subject_without_code_fails(self):
        """Test that creating subject without code fails."""
        from pydantic import ValidationError

        from edulafia.modules.academics.schemas import SubjectCreate

        with pytest.raises(ValidationError):
            SubjectCreate(
                name="Mathematics",
            )

    def test_subject_code_max_length(self):
        """Test subject code max length validation."""
        from pydantic import ValidationError

        from edulafia.modules.academics.schemas import SubjectCreate

        with pytest.raises(ValidationError):
            SubjectCreate(
                name="Mathematics",
                code="A" * 21,  # Exceeds 20 char limit
            )

    def test_subject_name_max_length(self):
        """Test subject name max length validation."""
        from pydantic import ValidationError

        from edulafia.modules.academics.schemas import SubjectCreate

        with pytest.raises(ValidationError):
            SubjectCreate(
                name="A" * 101,  # Exceeds 100 char limit
                code="MATH",
            )

    def test_subject_response_schema_exists(self):
        """Test that SubjectResponse schema exists."""
        from edulafia.modules.academics.schemas import SubjectResponse
        assert SubjectResponse is not None

    def test_subject_update_schema_exists(self):
        """Test that SubjectUpdate schema exists."""
        from edulafia.modules.academics.schemas import SubjectUpdate
        assert SubjectUpdate is not None

    def test_subject_update_allows_partial(self):
        """Test that SubjectUpdate allows partial updates."""
        from edulafia.modules.academics.schemas import SubjectUpdate

        update = SubjectUpdate(name="Advanced Mathematics")
        assert update.name == "Advanced Mathematics"
        assert update.code is None


class TestAcademicResultModel:
    """Test cases for AcademicResult model."""

    def test_academic_result_model_exists(self):
        """Test that AcademicResult model class exists."""
        from edulafia.modules.academics.models import AcademicResult
        assert AcademicResult is not None

    def test_academic_result_has_required_fields(self):
        """Test that AcademicResult has all required fields."""
        from edulafia.modules.academics.models import AcademicResult
        columns = AcademicResult.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'subject_id', 'class_id',
            'term_id', 'school_id', 'ca_total', 'exam_score',
            'total_score', 'grade', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"AcademicResult missing field: {field}"

    def test_academic_result_has_table_name(self):
        """Test that AcademicResult has correct table name."""
        from edulafia.modules.academics.models import AcademicResult
        assert AcademicResult.__tablename__ == 'academic_results'


class TestGradingScaleModel:
    """Test cases for GradingScale model."""

    def test_grading_scale_model_exists(self):
        """Test that GradingScale model class exists."""
        from edulafia.modules.academics.models import GradingScale
        assert GradingScale is not None

    def test_grading_scale_has_required_fields(self):
        """Test that GradingScale has required fields."""
        from edulafia.modules.academics.models import GradingScale
        columns = GradingScale.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'name', 'is_default',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"GradingScale missing field: {field}"

    def test_grading_scale_has_table_name(self):
        """Test that GradingScale has correct table name."""
        from edulafia.modules.academics.models import GradingScale
        assert GradingScale.__tablename__ == 'grading_scales'


class TestReportCardModel:
    """Test cases for ReportCard model."""

    def test_report_card_model_exists(self):
        """Test that ReportCard model class exists."""
        from edulafia.modules.academics.models import ReportCard
        assert ReportCard is not None

    def test_report_card_has_required_fields(self):
        """Test that ReportCard has required fields."""
        from edulafia.modules.academics.models import ReportCard
        columns = ReportCard.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'term_id', 'school_id',
            'overall_average', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"ReportCard missing field: {field}"

    def test_report_card_has_table_name(self):
        """Test that ReportCard has correct table name."""
        from edulafia.modules.academics.models import ReportCard
        assert ReportCard.__tablename__ == 'report_cards'
