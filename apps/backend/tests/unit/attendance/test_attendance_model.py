"""Tests for AttendanceRecord model - written BEFORE implementation."""

from datetime import date

import pytest


class TestAttendanceRecordModel:
    """Test cases for AttendanceRecord model."""

    def test_attendance_record_model_exists(self):
        """Test that AttendanceRecord model class exists."""
        from edulafia.modules.attendance.models import AttendanceRecord
        assert AttendanceRecord is not None

    def test_attendance_record_has_required_fields(self):
        """Test that AttendanceRecord has all required fields."""
        from edulafia.modules.attendance.models import AttendanceRecord
        columns = AttendanceRecord.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'class_id', 'school_id', 'date',
            'status', 'recorded_by', 'sync_status', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"AttendanceRecord missing field: {field}"

    def test_attendance_record_has_optional_fields(self):
        """Test that AttendanceRecord has optional fields."""
        from edulafia.modules.attendance.models import AttendanceRecord
        columns = AttendanceRecord.__table__.columns.keys()

        optional_fields = [
            'period', 'reason_code', 'symptom_codes', 'notes',
            'edited_at', 'edited_by', 'edit_reason', 'device_id'
        ]
        for field in optional_fields:
            assert field in columns, f"AttendanceRecord missing field: {field}"

    def test_attendance_record_has_table_name(self):
        """Test that AttendanceRecord has correct table name."""
        from edulafia.modules.attendance.models import AttendanceRecord
        assert AttendanceRecord.__tablename__ == 'attendance_records'

    def test_attendance_record_has_timestamps(self):
        """Test that AttendanceRecord has timestamps."""
        from edulafia.modules.attendance.models import AttendanceRecord
        columns = AttendanceRecord.__table__.columns.keys()
        assert 'created_at' in columns
        assert 'updated_at' in columns

    def test_attendance_record_has_soft_delete(self):
        """Test that AttendanceRecord has soft delete."""
        from edulafia.modules.attendance.models import AttendanceRecord
        columns = AttendanceRecord.__table__.columns.keys()
        assert 'deleted_at' in columns


class TestAttendancePatternModel:
    """Test cases for AttendancePattern model."""

    def test_attendance_pattern_model_exists(self):
        """Test that AttendancePattern model class exists."""
        from edulafia.modules.attendance.models import AttendancePattern
        assert AttendancePattern is not None

    def test_attendance_pattern_has_required_fields(self):
        """Test that AttendancePattern has required fields."""
        from edulafia.modules.attendance.models import AttendancePattern
        columns = AttendancePattern.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'pattern_type',
            'pattern_details', 'severity', 'status', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"AttendancePattern missing field: {field}"

    def test_attendance_pattern_has_table_name(self):
        """Test that AttendancePattern has correct table name."""
        from edulafia.modules.attendance.models import AttendancePattern
        assert AttendancePattern.__tablename__ == 'attendance_patterns'


class TestAttendanceNotificationModel:
    """Test cases for AttendanceNotification model."""

    def test_attendance_notification_model_exists(self):
        """Test that AttendanceNotification model class exists."""
        from edulafia.modules.attendance.models import AttendanceNotification
        assert AttendanceNotification is not None

    def test_attendance_notification_has_required_fields(self):
        """Test that AttendanceNotification has required fields."""
        from edulafia.modules.attendance.models import AttendanceNotification
        columns = AttendanceNotification.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'guardian_id', 'notification_type',
            'channel', 'message_content', 'status', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"AttendanceNotification missing field: {field}"

    def test_attendance_notification_has_table_name(self):
        """Test that AttendanceNotification has correct table name."""
        from edulafia.modules.attendance.models import AttendanceNotification
        assert AttendanceNotification.__tablename__ == 'attendance_notifications'


class TestAttendanceConfigurationModel:
    """Test cases for AttendanceConfiguration model."""

    def test_attendance_configuration_model_exists(self):
        """Test that AttendanceConfiguration model class exists."""
        from edulafia.modules.attendance.models import AttendanceConfiguration
        assert AttendanceConfiguration is not None

    def test_attendance_configuration_has_required_fields(self):
        """Test that AttendanceConfiguration has required fields."""
        from edulafia.modules.attendance.models import AttendanceConfiguration
        columns = AttendanceConfiguration.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'marking_method', 'edit_window_hours',
            'notification_enabled', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"AttendanceConfiguration missing field: {field}"

    def test_attendance_configuration_has_table_name(self):
        """Test that AttendanceConfiguration has correct table name."""
        from edulafia.modules.attendance.models import AttendanceConfiguration
        assert AttendanceConfiguration.__tablename__ == 'attendance_configurations'


class TestAttendanceSchemas:
    """Test cases for Attendance schemas."""

    def test_attendance_mark_request_exists(self):
        """Test that AttendanceMarkRequest schema exists."""
        from edulafia.modules.attendance.schemas import AttendanceMarkRequest
        assert AttendanceMarkRequest is not None

    def test_attendance_mark_request_validates_status(self):
        """Test that AttendanceMarkRequest validates status."""
        from uuid import uuid4

        from pydantic import ValidationError

        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        with pytest.raises(ValidationError):
            AttendanceMarkRequest(
                student_id=uuid4(),
                class_id=uuid4(),
                date=date.today(),
                status="invalid_status",
            )

    def test_attendance_mark_request_validates_future_date(self):
        """Test that AttendanceMarkRequest rejects future dates."""
        from datetime import timedelta
        from uuid import uuid4

        from pydantic import ValidationError

        from edulafia.modules.attendance.schemas import AttendanceMarkRequest

        with pytest.raises(ValidationError):
            AttendanceMarkRequest(
                student_id=uuid4(),
                class_id=uuid4(),
                date=date.today() + timedelta(days=1),
                status="present",
            )

    def test_attendance_response_schema_exists(self):
        """Test that AttendanceRecordResponse schema exists."""
        from edulafia.modules.attendance.schemas import AttendanceRecordResponse
        assert AttendanceRecordResponse is not None

    def test_attendance_summary_response_exists(self):
        """Test that AttendanceSummaryResponse schema exists."""
        from edulafia.modules.attendance.schemas import AttendanceSummaryResponse
        assert AttendanceSummaryResponse is not None

    def test_attendance_update_request_requires_edit_reason(self):
        """Test that AttendanceUpdateRequest requires edit reason."""
        from pydantic import ValidationError

        from edulafia.modules.attendance.schemas import AttendanceUpdateRequest

        with pytest.raises(ValidationError):
            AttendanceUpdateRequest(status="present")
