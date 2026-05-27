"""Tests for Parent models and schemas - written BEFORE implementation (TDD)."""


import pytest


class TestParentSessionModel:
    """Test cases for ParentSession model."""

    def test_parent_session_model_exists(self):
        """Test that ParentSession model class exists."""
        from edulafia.modules.parent.models import ParentSession
        assert ParentSession is not None

    def test_parent_session_has_required_fields(self):
        """Test that ParentSession has all required fields."""
        from edulafia.modules.parent.models import ParentSession
        columns = ParentSession.__table__.columns.keys()

        required_fields = [
            'id', 'guardian_id', 'session_token', 'expires_at',
            'last_activity_at', 'is_active', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"ParentSession missing field: {field}"

    def test_parent_session_has_table_name(self):
        """Test that ParentSession has correct table name."""
        from edulafia.modules.parent.models import ParentSession
        assert ParentSession.__tablename__ == 'guardian_portal_sessions'


class TestOTPVerificationModel:
    """Test cases for OTPVerification model."""

    def test_otp_verification_model_exists(self):
        """Test that OTPVerification model class exists."""
        from edulafia.modules.parent.models import OTPVerification
        assert OTPVerification is not None

    def test_otp_verification_has_required_fields(self):
        """Test that OTPVerification has all required fields."""
        from edulafia.modules.parent.models import OTPVerification
        columns = OTPVerification.__table__.columns.keys()

        required_fields = [
            'id', 'phone', 'otp_code', 'purpose', 'expires_at',
            'attempts', 'max_attempts', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"OTPVerification missing field: {field}"

    def test_otp_verification_has_table_name(self):
        """Test that OTPVerification has correct table name."""
        from edulafia.modules.parent.models import OTPVerification
        assert OTPVerification.__tablename__ == 'otp_verifications'


class TestParentNotificationModel:
    """Test cases for ParentNotification model."""

    def test_parent_notification_model_exists(self):
        """Test that ParentNotification model class exists."""
        from edulafia.modules.parent.models import ParentNotification
        assert ParentNotification is not None

    def test_parent_notification_has_required_fields(self):
        """Test that ParentNotification has all required fields."""
        from edulafia.modules.parent.models import ParentNotification
        columns = ParentNotification.__table__.columns.keys()

        required_fields = [
            'id', 'guardian_id', 'notification_type', 'title', 'message',
            'channel', 'priority', 'status', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"ParentNotification missing field: {field}"

    def test_parent_notification_has_table_name(self):
        """Test that ParentNotification has correct table name."""
        from edulafia.modules.parent.models import ParentNotification
        assert ParentNotification.__tablename__ == 'parent_notifications'


class TestAbsenceExcusalModel:
    """Test cases for AbsenceExcusal model."""

    def test_absence_excusal_model_exists(self):
        """Test that AbsenceExcusal model class exists."""
        from edulafia.modules.parent.models import AbsenceExcusal
        assert AbsenceExcusal is not None

    def test_absence_excusal_has_required_fields(self):
        """Test that AbsenceExcusal has all required fields."""
        from edulafia.modules.parent.models import AbsenceExcusal
        columns = AbsenceExcusal.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'guardian_id', 'absence_date',
            'reason', 'status', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"AbsenceExcusal missing field: {field}"

    def test_absence_excusal_has_table_name(self):
        """Test that AbsenceExcusal has correct table name."""
        from edulafia.modules.parent.models import AbsenceExcusal
        assert AbsenceExcusal.__tablename__ == 'absence_excusals'


class TestParentSchemas:
    """Test cases for Parent schemas."""

    def test_otp_request_schema_exists(self):
        """Test that OTPRequest schema exists."""
        from edulafia.modules.parent.schemas import OTPRequest
        assert OTPRequest is not None

    def test_otp_request_validates_phone(self):
        """Test that OTPRequest validates phone format."""
        from pydantic import ValidationError

        from edulafia.modules.parent.schemas import OTPRequest

        with pytest.raises(ValidationError):
            OTPRequest(phone="08012345678")  # Missing +234

    def test_otp_request_validates_phone_digits(self):
        """Test that OTPRequest validates phone digits."""
        from pydantic import ValidationError

        from edulafia.modules.parent.schemas import OTPRequest

        with pytest.raises(ValidationError):
            OTPRequest(phone="+2348012345")  # Too short

    def test_otp_request_accepts_valid_phone(self):
        """Test that OTPRequest accepts valid phone."""
        from edulafia.modules.parent.schemas import OTPRequest

        otp = OTPRequest(phone="+2348012345678")
        assert otp.phone == "+2348012345678"

    def test_auth_response_schema_exists(self):
        """Test that AuthResponse schema exists."""
        from edulafia.modules.parent.schemas import AuthResponse
        assert AuthResponse is not None

    def test_absence_excusal_create_schema_exists(self):
        """Test that AbsenceExcusalCreate schema exists."""
        from edulafia.modules.parent.schemas import AbsenceExcusalCreate
        assert AbsenceExcusalCreate is not None

    def test_feedback_create_validates_type(self):
        """Test that FeedbackCreate validates feedback type."""
        from pydantic import ValidationError

        from edulafia.modules.parent.schemas import FeedbackCreate

        with pytest.raises(ValidationError):
            FeedbackCreate(
                feedback_type="invalid",
                subject="Test",
                message="Test message",
            )

    def test_feedback_create_accepts_valid_types(self):
        """Test that FeedbackCreate accepts valid types."""
        from edulafia.modules.parent.schemas import FeedbackCreate

        for ftype in ["complaint", "suggestion", "praise", "question"]:
            feedback = FeedbackCreate(
                feedback_type=ftype,
                subject="Test",
                message="Test message",
            )
            assert feedback.feedback_type == ftype
