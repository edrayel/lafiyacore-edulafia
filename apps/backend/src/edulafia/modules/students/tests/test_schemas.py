from datetime import date, timedelta

import pytest

from edulafia.modules.students.schemas import StudentCreate, StudentFilters, StudentUpdate


class TestStudentCreate:
    def test_valid_student_create(self):
        data = StudentCreate(
            first_name="John",
            last_name="Doe",
            date_of_birth=date.today() - timedelta(days=365 * 14),
            gender="male",
            admission_number="EDU/2024/0001",
            admission_date=date.today(),
        )
        assert data.first_name == "John"
        assert data.gender == "male"

    def test_invalid_gender(self):
        with pytest.raises(ValueError, match="must be 'male' or 'female'"):
            StudentCreate(
                first_name="John",
                last_name="Doe",
                date_of_birth=date.today() - timedelta(days=365 * 14),
                gender="other",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
            )

    def test_date_of_birth_in_future(self):
        with pytest.raises(ValueError, match="cannot be in the future"):
            StudentCreate(
                first_name="John",
                last_name="Doe",
                date_of_birth=date.today() + timedelta(days=365),
                gender="male",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
            )

    def test_age_too_young(self):
        with pytest.raises(ValueError, match="between 6 and 20"):
            StudentCreate(
                first_name="Baby",
                last_name="Doe",
                date_of_birth=date.today() - timedelta(days=365 * 3),
                gender="female",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
            )

    def test_age_too_old(self):
        with pytest.raises(ValueError, match="between 6 and 20"):
            StudentCreate(
                first_name="Adult",
                last_name="Doe",
                date_of_birth=date.today() - timedelta(days=365 * 25),
                gender="male",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
            )

    def test_invalid_nin_too_short(self):
        with pytest.raises(ValueError, match="exactly 11 digits"):
            StudentCreate(
                first_name="John",
                last_name="Doe",
                date_of_birth=date.today() - timedelta(days=365 * 14),
                gender="male",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
                nin="1234567890",  # 10 digits to bypass min_length check and trigger validator
            )

    def test_invalid_nin_not_digits(self):
        with pytest.raises(ValueError, match="exactly 11 digits"):
            StudentCreate(
                first_name="John",
                last_name="Doe",
                date_of_birth=date.today() - timedelta(days=365 * 14),
                gender="male",
                admission_number="EDU/2024/0001",
                admission_date=date.today(),
                nin="1234567890a",
            )


class TestStudentUpdate:
    def test_partial_update(self):
        data = StudentUpdate(first_name="Jane")
        assert data.first_name == "Jane"
        assert data.last_name is None

    def test_update_gender_normalization(self):
        data = StudentUpdate(gender="MALE")
        assert data.gender == "male"


class TestStudentFilters:
    def test_empty_filters(self):
        filters = StudentFilters()
        assert filters.class_id is None
        assert filters.status is None
        assert filters.search is None

    def test_with_search(self):
        filters = StudentFilters(search="John")
        assert filters.search == "John"
