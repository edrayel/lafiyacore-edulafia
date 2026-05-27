"""Tests for ParentAuthService - written BEFORE implementation (TDD)."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Needs proper DB setup")


@pytest.fixture
def mock_session_repo():
    """Create a mock session repository."""
    return AsyncMock()


@pytest.fixture
def mock_otp_repo():
    """Create a mock OTP repository."""
    repo = AsyncMock()
    repo.count_recent.return_value = 0
    repo.db = AsyncMock()
    execute_result = MagicMock()
    execute_result.scalar_one_or_none.return_value = uuid4()
    repo.db.execute.return_value = execute_result
    return repo


@pytest.fixture
def auth_service(mock_session_repo, mock_otp_repo):
    """Create ParentAuthService with mocked repositories."""
    from edulafia.modules.parent.auth import ParentAuthService
    return ParentAuthService(mock_session_repo, mock_otp_repo)


def make_otp_mock(
    id=None,
    phone="+2348012345678",
    otp_code="123456",
    guardian_id=None,
    expires_at=None,
    attempts=0,
    max_attempts=3,
) -> MagicMock:
    """Create a properly configured OTPVerification mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.guardian_id = guardian_id or uuid4()
    mock.phone = phone
    mock.otp_code = otp_code
    mock.purpose = "login"
    mock.expires_at = expires_at or (datetime.now(timezone.utc) + timedelta(minutes=10))
    mock.verified_at = None
    mock.attempts = attempts
    mock.max_attempts = max_attempts
    mock.created_at = datetime.now(timezone.utc)
    return mock


def make_session_mock(
    id=None,
    guardian_id=None,
    session_token="abc123",
    is_active=True,
) -> MagicMock:
    """Create a properly configured ParentSession mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.guardian_id = guardian_id or uuid4()
    mock.session_token = session_token
    mock.device_id = None
    mock.device_info = None
    mock.ip_address = None
    mock.user_agent = None
    mock.expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    mock.last_activity_at = datetime.now(timezone.utc)
    mock.is_active = is_active
    mock.created_at = datetime.now(timezone.utc)
    mock.updated_at = datetime.now(timezone.utc)
    return mock


class TestParentAuthService:
    """Test cases for ParentAuthService."""

    def test_auth_service_exists(self):
        """Test that ParentAuthService class exists."""
        from edulafia.modules.parent.auth import ParentAuthService
        assert ParentAuthService is not None

    from unittest.mock import patch

    @patch("edulafia.core.twilio_client.TwilioClient.send_sms", new_callable=AsyncMock)
    async def test_request_otp_success(self, mock_send_sms, auth_service, mock_otp_repo):
        """Test successful OTP request."""
        from unittest.mock import AsyncMock, patch

        from edulafia.modules.parent.schemas import OTPRequest

        mock_otp_repo.create.return_value = make_otp_mock()
        mock_send_sms.return_value = {}

        data = OTPRequest(phone="+2348012345678")

        with patch(
            "edulafia.core.rate_limiter.RateLimiter.is_rate_limited",
            new_callable=AsyncMock,
            return_value=False,
        ):
            result = await auth_service.request_otp(data)

        assert result["message"] == "OTP sent successfully"
        assert "expires_in" in result["data"]
        mock_otp_repo.create.assert_called_once()
        mock_send_sms.assert_called_once()

    async def test_request_otp_invalid_phone(self, auth_service, mock_otp_repo):
        """Test OTP request with invalid phone."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            from edulafia.modules.parent.schemas import OTPRequest
            OTPRequest(phone="08012345678")  # Missing +234

    async def test_request_otp_rate_limit_exceeded(self, auth_service, mock_otp_repo):
        """Test OTP request when rate limit exceeded."""
        from unittest.mock import AsyncMock, patch

        from edulafia.modules.parent.exceptions import RateLimitExceededError
        from edulafia.modules.parent.schemas import OTPRequest

        data = OTPRequest(phone="+2348012345678")

        async def _rate_limited_by_phone(key: str) -> bool:
            return ":otp_request:phone:" in key

        with patch(
            "edulafia.core.rate_limiter.RateLimiter.is_rate_limited",
            new_callable=AsyncMock,
            side_effect=_rate_limited_by_phone,
        ):
            with pytest.raises(RateLimitExceededError):
                await auth_service.request_otp(data, ip_address="203.0.113.10")

    async def test_request_otp_rate_limit_exceeded_per_ip(self, auth_service, mock_otp_repo):
        """Rate limit OTP requests per-IP."""
        from unittest.mock import AsyncMock, patch

        from edulafia.modules.parent.exceptions import RateLimitExceededError
        from edulafia.modules.parent.schemas import OTPRequest

        async def _rate_limited_by_ip(key: str) -> bool:
            return ":otp_request:ip:" in key

        mock_otp_repo.count_recent.return_value = 0
        data = OTPRequest(phone="+2348012345678")

        with patch(
            "edulafia.core.rate_limiter.RateLimiter.is_rate_limited",
            new_callable=AsyncMock,
            side_effect=_rate_limited_by_ip,
        ):
            with pytest.raises(RateLimitExceededError):
                await auth_service.request_otp(data, ip_address="203.0.113.10")

    async def test_request_otp_locked_out_by_ip(self, auth_service, mock_otp_repo):
        """Lock out OTP requests by IP."""
        from unittest.mock import AsyncMock, patch

        from edulafia.modules.parent.exceptions import OTPTemporarilyLockedError
        from edulafia.modules.parent.schemas import OTPRequest

        data = OTPRequest(phone="+2348012345678")

        class _FakeRedis:
            async def exists(self, key: str) -> int:
                return 1 if ":otp_request:lock:ip:" in key else 0

        with patch("edulafia.core.rate_limiter.get_redis", new_callable=AsyncMock, return_value=_FakeRedis()):
            with pytest.raises(OTPTemporarilyLockedError):
                await auth_service.request_otp(data, ip_address="203.0.113.10")

    async def test_verify_otp_success(self, auth_service, mock_otp_repo, mock_session_repo):
        """Test successful OTP verification."""
        from edulafia.modules.parent.schemas import OTPVerify

        guardian_id = uuid4()
        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            guardian_id=guardian_id,
        )
        mock_session_repo.create.return_value = make_session_mock(
            guardian_id=guardian_id,
        )

        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        result = await auth_service.verify_otp(data)

        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.guardian_id == guardian_id

    async def test_verify_otp_invalid_code(self, auth_service, mock_otp_repo):
        """Test OTP verification with invalid code."""
        from unittest.mock import AsyncMock, patch
        from edulafia.modules.parent.exceptions import InvalidOTPError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = make_otp_mock(otp_code="123456")

        data = OTPVerify(phone="+2348012345678", otp_code="000000")

        with patch.object(auth_service, "_record_otp_verify_failure", new_callable=AsyncMock) as mock_record_failure:
            with pytest.raises(InvalidOTPError):
                await auth_service.verify_otp(data, ip_address="203.0.113.10")
            mock_record_failure.assert_called_once_with(phone="+2348012345678", ip_address="203.0.113.10")

    async def test_verify_otp_not_found_records_failure(self, auth_service, mock_otp_repo):
        """Test OTP verification failure is recorded when OTP not found."""
        from unittest.mock import AsyncMock, patch
        from edulafia.modules.parent.exceptions import InvalidOTPError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = None
        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        with patch.object(auth_service, "_record_otp_verify_failure", new_callable=AsyncMock) as mock_record_failure:
            with pytest.raises(InvalidOTPError):
                await auth_service.verify_otp(data, ip_address="203.0.113.10")
            mock_record_failure.assert_called_once_with(phone="+2348012345678", ip_address="203.0.113.10")

    async def test_verify_otp_expired_records_failure(self, auth_service, mock_otp_repo):
        """Test OTP verification failure is recorded when OTP is expired."""
        from unittest.mock import AsyncMock, patch
        from edulafia.modules.parent.exceptions import ExpiredOTPError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        )
        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        with patch.object(auth_service, "_record_otp_verify_failure", new_callable=AsyncMock) as mock_record_failure:
            with pytest.raises(ExpiredOTPError):
                await auth_service.verify_otp(data, ip_address="203.0.113.10")
            mock_record_failure.assert_called_once_with(phone="+2348012345678", ip_address="203.0.113.10")

    async def test_verify_otp_max_attempts_records_failure(self, auth_service, mock_otp_repo):
        """Test OTP verification failure is recorded when max attempts exceeded."""
        from unittest.mock import AsyncMock, patch
        from edulafia.modules.parent.exceptions import MaxAttemptsExceededError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            attempts=3,
            max_attempts=3,
        )
        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        with patch.object(auth_service, "_record_otp_verify_failure", new_callable=AsyncMock) as mock_record_failure:
            with pytest.raises(MaxAttemptsExceededError):
                await auth_service.verify_otp(data, ip_address="203.0.113.10")
            mock_record_failure.assert_called_once_with(phone="+2348012345678", ip_address="203.0.113.10")

    async def test_verify_otp_expired(self, auth_service, mock_otp_repo):
        """Test OTP verification with expired OTP."""
        from edulafia.modules.parent.exceptions import ExpiredOTPError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),  # Expired
        )

        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        with pytest.raises(ExpiredOTPError):
            await auth_service.verify_otp(data)

    async def test_verify_otp_max_attempts_exceeded(self, auth_service, mock_otp_repo):
        """Test OTP verification when max attempts exceeded."""
        from edulafia.modules.parent.exceptions import MaxAttemptsExceededError
        from edulafia.modules.parent.schemas import OTPVerify

        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            attempts=3,
            max_attempts=3,
        )

        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        with pytest.raises(MaxAttemptsExceededError):
            await auth_service.verify_otp(data)

    async def test_verify_otp_locked_out_by_ip(self, auth_service, mock_otp_repo, mock_session_repo):
        """Lock out OTP verification attempts by IP."""
        from unittest.mock import AsyncMock, patch

        from edulafia.modules.parent.exceptions import OTPTemporarilyLockedError
        from edulafia.modules.parent.schemas import OTPVerify

        guardian_id = uuid4()
        mock_otp_repo.get_latest.return_value = make_otp_mock(
            otp_code="123456",
            guardian_id=guardian_id,
        )
        mock_session_repo.create.return_value = make_session_mock(
            guardian_id=guardian_id,
        )

        data = OTPVerify(phone="+2348012345678", otp_code="123456")

        class _FakeRedis:
            async def exists(self, key: str) -> int:
                return 1 if ":otp_verify:lock:ip:" in key else 0

        with patch("edulafia.core.rate_limiter.get_redis", new_callable=AsyncMock, return_value=_FakeRedis()):
            with pytest.raises(OTPTemporarilyLockedError):
                await auth_service.verify_otp(data, ip_address="203.0.113.10")

    def test_validate_nigerian_phone_valid(self, auth_service):
        """Test valid Nigerian phone format."""
        assert auth_service._validate_phone("+2348012345678") == True
        assert auth_service._validate_phone("+2347012345678") == True

    def test_validate_nigerian_phone_invalid(self, auth_service):
        """Test invalid Nigerian phone format."""
        assert auth_service._validate_phone("08012345678") == False
        assert auth_service._validate_phone("+234801234") == False
        assert auth_service._validate_phone("+23480123456789") == False

    def test_is_quiet_hours(self, auth_service):
        """Test quiet hours detection."""
        # This depends on current time, so just test the method exists
        result = auth_service.is_quiet_hours()
        assert isinstance(result, bool)


class TestParentNotificationService:
    """Test cases for ParentNotificationService."""

    @pytest.fixture
    def notification_service(self):
        """Create ParentNotificationService with mocked repositories."""
        from edulafia.modules.parent.notifications import ParentNotificationService

        notification_repo = AsyncMock()
        preference_repo = AsyncMock()

        return ParentNotificationService(notification_repo, preference_repo)

    def test_notification_service_exists(self):
        """Test that ParentNotificationService class exists."""
        from edulafia.modules.parent.notifications import ParentNotificationService
        assert ParentNotificationService is not None

    def test_is_urgent_health_notification(self, notification_service):
        """Test that health notifications are urgent."""
        assert notification_service._is_urgent("health_notification") == True
        assert notification_service._is_urgent("health_emergency") == True
        assert notification_service._is_urgent("safety_alert") == True

    def test_is_not_urgent_normal_types(self, notification_service):
        """Test that normal types are not urgent."""
        assert notification_service._is_urgent("absence") == False
        assert notification_service._is_urgent("academic") == False
        assert notification_service._is_urgent("payment_receipt") == False

    def test_is_quiet_hours(self, notification_service):
        """Test quiet hours detection."""
        result = notification_service._is_quiet_hours()
        assert isinstance(result, bool)
