"""Tests for grade computation service - written BEFORE implementation (TDD)."""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return AsyncMock()


@pytest.fixture
def service():
    """Create GradeComputationService instance."""
    from edulafia.modules.academics.grade_computation import GradeComputationService
    return GradeComputationService


def make_grading_scale_mock():
    """Create a standard WAEC grading scale mock."""
    mock = MagicMock()
    mock.id = uuid4()
    mock.name = "WAEC Standard"
    mock.is_default = True
    mock.details = [
        MagicMock(grade="A1", min_score=Decimal("75"), max_score=Decimal("100"), remark="Excellent", position=1),
        MagicMock(grade="B2", min_score=Decimal("70"), max_score=Decimal("74"), remark="Very Good", position=2),
        MagicMock(grade="B3", min_score=Decimal("65"), max_score=Decimal("69"), remark="Good", position=3),
        MagicMock(grade="C4", min_score=Decimal("60"), max_score=Decimal("64"), remark="Credit", position=4),
        MagicMock(grade="C5", min_score=Decimal("55"), max_score=Decimal("59"), remark="Credit", position=5),
        MagicMock(grade="C6", min_score=Decimal("50"), max_score=Decimal("54"), remark="Credit", position=6),
        MagicMock(grade="D7", min_score=Decimal("45"), max_score=Decimal("49"), remark="Pass", position=7),
        MagicMock(grade="E8", min_score=Decimal("40"), max_score=Decimal("44"), remark="Pass", position=8),
        MagicMock(grade="F9", min_score=Decimal("0"), max_score=Decimal("39"), remark="Fail", position=9),
    ]
    return mock


class TestGradeComputationService:
    """Test cases for GradeComputationService."""

    def test_service_exists(self):
        """Test that GradeComputationService class exists."""
        from edulafia.modules.academics.grade_computation import GradeComputationService
        assert GradeComputationService is not None

    def test_calculate_grade_a1_boundary(self, service):
        """Test grade calculation at A1 boundary (75-100)."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("80"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "A1"
        assert result['remark'] == "Excellent"

    def test_calculate_grade_b2_boundary(self, service):
        """Test grade calculation at B2 boundary (70-74)."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("72"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "B2"
        assert result['remark'] == "Very Good"

    def test_calculate_grade_f9_boundary(self, service):
        """Test grade calculation at F9 boundary (0-39)."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("20"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "F9"
        assert result['remark'] == "Fail"

    def test_calculate_grade_exact_boundary_75(self, service):
        """Test grade calculation at exact boundary 75."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("75"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "A1"

    def test_calculate_grade_score_below_minimum(self, service):
        """Test grade calculation with score below 0."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("-5"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "F9"

    def test_calculate_grade_score_above_maximum(self, service):
        """Test grade calculation with score above 100."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        grading_rules = GradeComputationService.get_default_grading_rules()

        result = GradeComputationService.compute_grade(
            score=Decimal("105"),
            grading_rules=grading_rules,
        )

        assert result['grade'] == "A1"

    def test_calculate_total_score(self, service):
        """Test total score calculation (CA + Exam)."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        total = GradeComputationService.calculate_total_score(
            ca_total=Decimal("25"),
            exam_score=Decimal("60"),
        )

        assert total == Decimal("85")

    def test_calculate_total_score_with_default_weights(self, service):
        """Test total score with default CA=30%, Exam=70% weights."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        # CA raw score out of 30, Exam raw score out of 70
        total = GradeComputationService.calculate_weighted_total(
            ca_raw=Decimal("28"),
            exam_raw=Decimal("55"),
            ca_max=Decimal("30"),
            exam_max=Decimal("70"),
        )

        assert total == Decimal("83")

    def test_calculate_class_ranks_success(self, service):
        """Test class rank calculation."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        scores = [
            {"student_id": uuid4(), "total_score": Decimal("90")},
            {"student_id": uuid4(), "total_score": Decimal("85")},
            {"student_id": uuid4(), "total_score": Decimal("80")},
        ]

        ranked = GradeComputationService.calculate_class_ranks(scores)

        assert ranked[0]['rank'] == 1
        assert ranked[1]['rank'] == 2
        assert ranked[2]['rank'] == 3

    def test_calculate_class_ranks_with_ties(self, service):
        """Test class rank calculation with tied scores."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        scores = [
            {"student_id": uuid4(), "total_score": Decimal("90")},
            {"student_id": uuid4(), "total_score": Decimal("90")},  # Tie
            {"student_id": uuid4(), "total_score": Decimal("80")},
        ]

        ranked = GradeComputationService.calculate_class_ranks(scores)

        # Both 90s should be rank 1
        assert ranked[0]['rank'] == 1
        assert ranked[1]['rank'] == 1
        # 80 should be rank 3 (skip 2 due to tie)
        assert ranked[2]['rank'] == 3

    def test_calculate_class_ranks_excludes_absent(self, service):
        """Test that ABS flag is excluded from ranking."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        scores = [
            {"student_id": uuid4(), "total_score": Decimal("90"), "flag": None},
            {"student_id": uuid4(), "total_score": Decimal("0"), "flag": "ABS"},
            {"student_id": uuid4(), "total_score": Decimal("80"), "flag": None},
        ]

        ranked = GradeComputationService.calculate_class_ranks(scores)

        # Should only rank 2 students (ABS excluded)
        assert len([r for r in ranked if r.get('rank') is not None]) == 2

    def test_calculate_class_ranks_excludes_incomplete(self, service):
        """Test that INC flag is excluded from ranking."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        scores = [
            {"student_id": uuid4(), "total_score": Decimal("90"), "flag": None},
            {"student_id": uuid4(), "total_score": Decimal("0"), "flag": "INC"},
            {"student_id": uuid4(), "total_score": Decimal("80"), "flag": None},
        ]

        ranked = GradeComputationService.calculate_class_ranks(scores)

        # Should only rank 2 students (INC excluded)
        assert len([r for r in ranked if r.get('rank') is not None]) == 2

    def test_get_default_grading_rules(self, service):
        """Test getting default WAEC grading rules."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        rules = GradeComputationService.get_default_grading_rules()

        assert len(rules) == 9  # A1-F9
        assert rules[0]['grade'] == "A1"
        assert rules[-1]['grade'] == "F9"

    def test_validate_grading_scale_no_overlaps(self, service):
        """Test grading scale validation - no overlapping ranges."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        rules = GradeComputationService.get_default_grading_rules()

        is_valid = GradeComputationService.validate_grading_scale(rules)

        assert is_valid == True

    def test_validate_grading_scale_incomplete_coverage_fails(self, service):
        """Test grading scale validation - incomplete coverage fails."""
        from edulafia.modules.academics.grade_computation import GradeComputationService

        # Scale with gap
        invalid_rules = [
            {"grade": "A1", "min_score": 75, "max_score": 100, "remark": "Excellent"},
            {"grade": "F9", "min_score": 0, "max_score": 39, "remark": "Fail"},
            # Gap: 40-74
        ]

        is_valid = GradeComputationService.validate_grading_scale(invalid_rules)

        assert is_valid == False
