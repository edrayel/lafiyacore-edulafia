"""Tests for Staff models and schemas - written BEFORE implementation (TDD)."""

from uuid import uuid4

import pytest


class TestStaffModel:
    """Test cases for Staff model."""

    def test_staff_model_exists(self):
        """Test that Staff model class exists."""
        from edulafia.modules.staff.models import Staff
        assert Staff is not None

    def test_staff_has_required_fields(self):
        """Test that Staff has all required fields."""
        from edulafia.modules.staff.models import Staff
        columns = Staff.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'staff_id', 'first_name', 'last_name',
            'phone', 'gender', 'role', 'employment_type', 'status',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"Staff missing field: {field}"

    def test_staff_has_table_name(self):
        """Test that Staff has correct table name."""
        from edulafia.modules.staff.models import Staff
        assert Staff.__tablename__ == 'staff'


class TestStaffAssignmentModel:
    """Test cases for StaffAssignment model."""

    def test_staff_assignment_model_exists(self):
        """Test that StaffAssignment model class exists."""
        from edulafia.modules.staff.models import StaffAssignment
        assert StaffAssignment is not None

    def test_staff_assignment_has_required_fields(self):
        """Test that StaffAssignment has all required fields."""
        from edulafia.modules.staff.models import StaffAssignment
        columns = StaffAssignment.__table__.columns.keys()

        required_fields = [
            'id', 'staff_id', 'class_id', 'academic_year_id',
            'assignment_type', 'is_form_teacher', 'is_active',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"StaffAssignment missing field: {field}"

    def test_staff_assignment_has_table_name(self):
        """Test that StaffAssignment has correct table name."""
        from edulafia.modules.staff.models import StaffAssignment
        assert StaffAssignment.__tablename__ == 'staff_class_assignments'


class TestTimetableModel:
    """Test cases for Timetable model."""

    def test_timetable_model_exists(self):
        """Test that Timetable model class exists."""
        from edulafia.modules.staff.models import Timetable
        assert Timetable is not None

    def test_timetable_has_required_fields(self):
        """Test that Timetable has all required fields."""
        from edulafia.modules.staff.models import Timetable
        columns = Timetable.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'class_id', 'academic_year_id', 'term_id',
            'effective_from', 'is_published', 'is_draft', 'version_number',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"Timetable missing field: {field}"

    def test_timetable_has_table_name(self):
        """Test that Timetable has correct table name."""
        from edulafia.modules.staff.models import Timetable
        assert Timetable.__tablename__ == 'timetables'


class TestTimetableEntryModel:
    """Test cases for TimetableEntry model."""

    def test_timetable_entry_model_exists(self):
        """Test that TimetableEntry model class exists."""
        from edulafia.modules.staff.models import TimetableEntry
        assert TimetableEntry is not None

    def test_timetable_entry_has_required_fields(self):
        """Test that TimetableEntry has all required fields."""
        from edulafia.modules.staff.models import TimetableEntry
        columns = TimetableEntry.__table__.columns.keys()

        required_fields = [
            'id', 'timetable_id', 'day_of_week', 'period_number',
            'start_time', 'end_time', 'subject_id', 'staff_id',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"TimetableEntry missing field: {field}"

    def test_timetable_entry_has_table_name(self):
        """Test that TimetableEntry has correct table name."""
        from edulafia.modules.staff.models import TimetableEntry
        assert TimetableEntry.__tablename__ == 'timetable_entries'


class TestTeacherAttendanceModel:
    """Test cases for TeacherAttendance model."""

    def test_teacher_attendance_model_exists(self):
        """Test that TeacherAttendance model class exists."""
        from edulafia.modules.staff.models import TeacherAttendance
        assert TeacherAttendance is not None

    def test_teacher_attendance_has_required_fields(self):
        """Test that TeacherAttendance has all required fields."""
        from edulafia.modules.staff.models import TeacherAttendance
        columns = TeacherAttendance.__table__.columns.keys()

        required_fields = [
            'id', 'staff_id', 'school_id', 'date', 'status',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"TeacherAttendance missing field: {field}"

    def test_teacher_attendance_has_table_name(self):
        """Test that TeacherAttendance has correct table name."""
        from edulafia.modules.staff.models import TeacherAttendance
        assert TeacherAttendance.__tablename__ == 'teacher_attendance'


class TestStaffSchemas:
    """Test cases for Staff schemas."""

    def test_staff_create_schema_exists(self):
        """Test that StaffCreate schema exists."""
        from edulafia.modules.staff.schemas import StaffCreate
        assert StaffCreate is not None

    def test_staff_create_validates_gender(self):
        """Test that StaffCreate validates gender."""
        from pydantic import ValidationError

        from edulafia.modules.staff.schemas import StaffCreate

        with pytest.raises(ValidationError):
            StaffCreate(
                first_name="John",
                last_name="Doe",
                phone="08012345678",
                gender="invalid",
                role="teacher",
            )

    def test_staff_create_validates_role(self):
        """Test that StaffCreate validates role."""
        from pydantic import ValidationError

        from edulafia.modules.staff.schemas import StaffCreate

        with pytest.raises(ValidationError):
            StaffCreate(
                first_name="John",
                last_name="Doe",
                phone="08012345678",
                gender="male",
                role="invalid_role",
            )

    def test_staff_response_exists(self):
        """Test that StaffResponse schema exists."""
        from edulafia.modules.staff.schemas import StaffResponse
        assert StaffResponse is not None

    def test_staff_assignment_create_exists(self):
        """Test that StaffAssignmentCreate schema exists."""
        from edulafia.modules.staff.schemas import StaffAssignmentCreate
        assert StaffAssignmentCreate is not None

    def test_timetable_create_exists(self):
        """Test that TimetableCreate schema exists."""
        from edulafia.modules.staff.schemas import TimetableCreate
        assert TimetableCreate is not None

    def test_timetable_entry_create_validates_day(self):
        """Test that TimetableEntryCreate validates day of week."""
        from datetime import time

        from pydantic import ValidationError

        from edulafia.modules.staff.schemas import TimetableEntryCreate

        with pytest.raises(ValidationError):
            TimetableEntryCreate(
                day_of_week=8,  # Invalid
                period_number=1,
                start_time=time(8, 0),
                end_time=time(9, 0),
                subject_id=uuid4(),
                staff_id=uuid4(),
            )

    def test_teacher_attendance_response_exists(self):
        """Test that TeacherAttendanceResponse schema exists."""
        from edulafia.modules.staff.schemas import TeacherAttendanceResponse
        assert TeacherAttendanceResponse is not None
