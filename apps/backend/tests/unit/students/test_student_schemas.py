"""Tests for Student Pydantic schemas - written BEFORE implementation."""

from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError


class TestStudentCreateSchema:
    """Test cases for StudentCreate schema validation."""

    def test_student_create_schema_exists(self):
        """Test that StudentCreate schema exists."""
        from edulafia.modules.students.schemas import StudentCreate
        assert StudentCreate is not None

    def test_create_student_with_required_fields(self):
        """Test creating student with all required fields passes validation."""
        from edulafia.modules.students.schemas import StudentCreate

        student = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4(),
            admission_date=date(2026, 1, 15),
        )
        assert student.first_name == "Chioma"
        assert student.last_name == "Okonkwo"

    def test_create_student_without_first_name_fails(self):
        """Test that creating student without first name raises validation error."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError) as exc_info:
            StudentCreate(
                last_name="Okonkwo",
                admission_number="EDU/2026/001",
                date_of_birth=date(2012, 5, 15),
                gender="female",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )
        assert "first_name" in str(exc_info.value)

    def test_create_student_without_last_name_fails(self):
        """Test that creating student without last name raises validation error."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError) as exc_info:
            StudentCreate(
                first_name="Chioma",
                admission_number="EDU/2026/001",
                date_of_birth=date(2012, 5, 15),
                gender="female",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )
        assert "last_name" in str(exc_info.value)

    def test_first_name_max_length(self):
        """Test that first name respects max length."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError):
            StudentCreate(
                first_name="A" * 101,  # Exceeds 100 char limit
                last_name="Okonkwo",
                admission_number="EDU/2026/001",
                date_of_birth=date(2012, 5, 15),
                gender="female",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )

    def test_date_of_birth_cannot_be_future(self):
        """Test that date of birth cannot be in the future."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError) as exc_info:
            StudentCreate(
                first_name="Chioma",
                last_name="Okonkwo",
                admission_number="EDU/2026/001",
                date_of_birth=date(2030, 5, 15),  # Future date
                gender="female",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )
        assert "date_of_birth" in str(exc_info.value).lower() or "future" in str(exc_info.value).lower()

    def test_age_must_be_between_6_and_20(self):
        """Test that student age must be between 6 and 20."""
        from edulafia.modules.students.schemas import StudentCreate

        # Too young (under 6)
        with pytest.raises(ValidationError):
            StudentCreate(
                first_name="Baby",
                last_name="Test",
                admission_number="EDU/2026/002",
                date_of_birth=date(2023, 1, 1),  # ~3 years old
                gender="male",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )

    def test_gender_validation(self):
        """Test that gender must be male or female."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError):
            StudentCreate(
                first_name="Chioma",
                last_name="Okonkwo",
                admission_number="EDU/2026/001",
                date_of_birth=date(2012, 5, 15),
                gender="other",  # Invalid
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
            )

    def test_optional_middle_name(self):
        """Test that middle name is optional."""
        from edulafia.modules.students.schemas import StudentCreate

        student = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4(),
            admission_date=date(2026, 1, 15),
            # middle_name not provided
        )
        assert student.middle_name is None

    def test_optional_nin_validation(self):
        """Test NIN validation when provided (11 digits)."""
        from edulafia.modules.students.schemas import StudentCreate

        # Valid NIN
        student = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4(),
            admission_date=date(2026, 1, 15),
            nin="12345678901",
        )
        assert student.nin == "12345678901"

    def test_nin_invalid_length_fails(self):
        """Test that NIN must be 11 digits."""
        from edulafia.modules.students.schemas import StudentCreate

        with pytest.raises(ValidationError):
            StudentCreate(
                first_name="Chioma",
                last_name="Okonkwo",
                admission_number="EDU/2026/001",
                date_of_birth=date(2012, 5, 15),
                gender="female",
                class_id=uuid4(),
                admission_date=date(2026, 1, 15),
                nin="12345",  # Invalid NIN
            )


class TestStudentResponseSchema:
    """Test cases for StudentResponse schema."""

    def test_student_response_schema_exists(self):
        """Test that StudentResponse schema exists."""
        from edulafia.modules.students.schemas import StudentResponse
        assert StudentResponse is not None

    def test_student_response_has_all_fields(self):
        """Test that StudentResponse has all expected fields."""
        from edulafia.modules.students.schemas import StudentResponse
        fields = StudentResponse.model_fields.keys()

        expected_fields = [
            'id', 'school_id', 'admission_number', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'status', 'admission_date'
        ]
        for field in expected_fields:
            assert field in fields, f"StudentResponse missing field: {field}"


class TestStudentUpdateSchema:
    """Test cases for StudentUpdate schema."""

    def test_student_update_schema_exists(self):
        """Test that StudentUpdate schema exists."""
        from edulafia.modules.students.schemas import StudentUpdate
        assert StudentUpdate is not None

    def test_update_allows_partial_updates(self):
        """Test that StudentUpdate allows partial field updates."""
        from edulafia.modules.students.schemas import StudentUpdate

        update = StudentUpdate(
            first_name="UpdatedName",
        )
        assert update.first_name == "UpdatedName"

    def test_update_admission_number_not_allowed(self):
        """Test that admission number cannot be updated."""
        from edulafia.modules.students.schemas import StudentUpdate
        fields = StudentUpdate.model_fields.keys()
        assert 'admission_number' not in fields or StudentUpdate.model_config.get('frozen', False)
