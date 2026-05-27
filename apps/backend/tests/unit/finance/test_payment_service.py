"""Tests for PaymentService - written BEFORE implementation (TDD)."""

from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest


@pytest.fixture
def mock_ledger_repo():
    """Create a mock fee ledger repository."""
    repo = AsyncMock()
    repo.get_next_receipt_number.return_value = "EDU-2026-000001"
    return repo


@pytest.fixture
def mock_scholarship_repo():
    """Create a mock student scholarship repository."""
    return AsyncMock()


@pytest.fixture
def service(mock_ledger_repo, mock_scholarship_repo):
    """Create PaymentService with mocked repositories."""
    from edulafia.modules.finance.service import PaymentService
    return PaymentService(mock_ledger_repo, mock_scholarship_repo)


def make_ledger_mock(
    id=None,
    student_id=None,
    transaction_type="payment",
    amount=10000,
    fee_category="tuition",
    payment_method="cash",
    payment_reference=None,
    receipt_number="EDU-2026-000001",
) -> MagicMock:
    """Create a properly configured FeeLedger mock."""
    mock = MagicMock()
    mock.id = id or uuid4()
    mock.student_id = student_id or uuid4()
    mock.school_id = uuid4()
    mock.transaction_date = datetime.now()
    mock.transaction_type = transaction_type
    mock.fee_category = fee_category
    mock.amount = amount
    mock.payment_method = payment_method
    mock.payment_reference = payment_reference
    mock.receipt_number = receipt_number
    mock.description = None
    mock.term_id = None
    mock.academic_year_id = None
    mock.recorded_by = uuid4()
    mock.gateway_reference = None
    mock.created_at = datetime.now()
    mock.updated_at = datetime.now()
    mock.gateway_response = {}  # Fix dict validation
    return mock


class TestPaymentService:
    """Test cases for PaymentService."""

    def test_payment_service_exists(self):
        """Test that PaymentService class exists."""
        from edulafia.modules.finance.service import PaymentService
        assert PaymentService is not None

    async def test_record_payment_success(self, service, mock_ledger_repo):
        """Test successful payment recording."""
        from edulafia.modules.finance.schemas import PaymentRecord

        mock_ledger_repo.create.return_value = make_ledger_mock(
            amount=10000,
            receipt_number="EDU-2026-000001",
        )

        data = PaymentRecord(
            student_id=uuid4(),
            amount=Decimal("10000"),
            payment_method="cash",
        )

        result = await service.record_payment(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
            user_role="bursar",
        )

        assert result.amount == 10000
        assert result.receipt_number == "EDU-2026-000001"

    async def test_record_payment_non_bursar_fails(self, service, mock_ledger_repo):
        """Test that non-bursar cannot record payment."""
        from edulafia.modules.finance.exceptions import BursarRoleRequiredError
        from edulafia.modules.finance.schemas import PaymentRecord

        data = PaymentRecord(
            student_id=uuid4(),
            amount=Decimal("10000"),
            payment_method="cash",
        )

        with pytest.raises(BursarRoleRequiredError):
            await service.record_payment(
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
                user_role="teacher",  # Not bursar
            )

    async def test_record_payment_exceeds_limit_fails(self, service, mock_ledger_repo):
        """Test that payment exceeding limit fails at schema level."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            from edulafia.modules.finance.schemas import PaymentRecord

            PaymentRecord(
                student_id=uuid4(),
                amount=Decimal("600000"),  # Exceeds 500,000 limit
                payment_method="cash",
            )

    async def test_record_payment_generates_receipt(self, service, mock_ledger_repo):
        """Test that payment generates receipt number."""
        from edulafia.modules.finance.schemas import PaymentRecord

        mock_ledger_repo.create.return_value = make_ledger_mock(receipt_number="EDU-2026-000001")

        data = PaymentRecord(
            student_id=uuid4(),
            amount=Decimal("5000"),
            payment_method="bank_transfer",
        )

        result = await service.record_payment(
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
            user_role="bursar",
        )

        assert result.receipt_number.startswith("EDU-")
        assert "2026" in result.receipt_number

    async def test_get_payment_by_id(self, service, mock_ledger_repo):
        """Test getting payment by ID."""
        payment_id = uuid4()
        mock_ledger_repo.get_by_id.return_value = make_ledger_mock(id=payment_id)

        result = await service.get_payment(
            payment_id=payment_id,
            school_id=uuid4(),
        )

        assert result.id == payment_id

    async def test_get_payment_not_found(self, service, mock_ledger_repo):
        """Test getting non-existent payment raises error."""
        from edulafia.modules.finance.exceptions import PaymentNotFoundError

        mock_ledger_repo.get_by_id.return_value = None

        with pytest.raises(PaymentNotFoundError):
            await service.get_payment(
                payment_id=uuid4(),
                school_id=uuid4(),
            )

    async def test_get_receipt_by_number(self, service, mock_ledger_repo):
        """Test getting receipt by receipt number."""
        mock_ledger_repo.get_by_receipt.return_value = make_ledger_mock(
            receipt_number="EDU-2026-000001"
        )

        result = await service.get_receipt(receipt_number="EDU-2026-000001")

        assert result.receipt_number == "EDU-2026-000001"

    async def test_reverse_payment_success(self, service, mock_ledger_repo):
        """Test successful payment reversal."""
        from edulafia.modules.finance.schemas import PaymentReversal

        mock_ledger_repo.get_by_id.return_value = make_ledger_mock(
            payment_method="cash",
            payment_reference="PAY-001",
        )
        mock_ledger_repo.create.return_value = make_ledger_mock(
            transaction_type="refund",
            amount=-10000,
        )

        data = PaymentReversal(reason="Duplicate payment")

        result = await service.reverse_payment(
            payment_id=uuid4(),
            data=data,
            school_id=uuid4(),
            user_id=uuid4(),
        )

        assert result.transaction_type == "refund"
        assert result.amount == -10000

    async def test_reverse_online_payment_requires_confirmation(self, service, mock_ledger_repo):
        """Test that online payment reversal requires gateway confirmation."""
        from edulafia.modules.finance.exceptions import OnlinePaymentReversalError
        from edulafia.modules.finance.schemas import PaymentReversal

        mock_ledger_repo.get_by_id.return_value = make_ledger_mock(
            payment_method="paystack",
        )

        data = PaymentReversal(reason="Refund requested")
        # No gateway_confirmation

        with pytest.raises(OnlinePaymentReversalError):
            await service.reverse_payment(
                payment_id=uuid4(),
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )

    async def test_get_student_balance(self, service, mock_ledger_repo):
        """Test getting student balance."""
        mock_ledger_repo.get_student_balance.return_value = {
            "student_name": "John Doe",
            "total_charges": 50000,
            "total_payments": 30000,
            "total_waivers": 5000,
            "balance": 15000,
        }
    
        result = await service.get_student_balance(student_id=uuid4())
    
        assert result.total_charges == Decimal("50000")
        assert result.total_payments == Decimal("30000")
        assert result.balance == Decimal("15000")
        assert result.student_name == "John Doe"


class TestScholarshipService:
    """Test cases for ScholarshipService."""

    @pytest.fixture
    def scholarship_service(self):
        """Create ScholarshipService with mocked repositories."""
        from edulafia.modules.finance.repository import (
            ScholarshipRepository,
            StudentScholarshipRepository,
        )
        from edulafia.modules.finance.service import ScholarshipService

        scholarship_repo = AsyncMock(spec=ScholarshipRepository)
        student_scholarship_repo = AsyncMock(spec=StudentScholarshipRepository)

        return ScholarshipService(scholarship_repo, student_scholarship_repo)

    def test_scholarship_service_exists(self):
        """Test that ScholarshipService class exists."""
        from edulafia.modules.finance.service import ScholarshipService
        assert ScholarshipService is not None

    async def test_create_scholarship_success(self, scholarship_service):
        """Test creating a scholarship."""
        from edulafia.modules.finance.schemas import ScholarshipCreate

        mock_scholarship = MagicMock()
        mock_scholarship.id = uuid4()
        mock_scholarship.name = "Academic Excellence"
        mock_scholarship.school_id = uuid4()
        mock_scholarship.amount = Decimal("50000")
        mock_scholarship.is_active = True
        mock_scholarship.donor_name = "ABC Foundation"
        mock_scholarship.description = None
        mock_scholarship.percentage = None
        mock_scholarship.created_at = datetime.now()
        mock_scholarship.updated_at = datetime.now()

        scholarship_service.scholarship_repo.create.return_value = mock_scholarship

        data = ScholarshipCreate(
            name="Academic Excellence",
            amount=Decimal("50000"),
            donor_name="ABC Foundation",
        )

        result = await scholarship_service.create_scholarship(
            data=data,
            school_id=uuid4(),
        )

        assert result.name == "Academic Excellence"
        assert result.amount == Decimal("50000")

    async def test_award_duplicate_scholarship_fails(self, scholarship_service):
        """Test that awarding duplicate scholarship fails."""
        from edulafia.modules.finance.exceptions import DuplicateScholarshipAwardError
        from edulafia.modules.finance.schemas import ScholarshipAward

        mock_scholarship = MagicMock()
        mock_scholarship.id = uuid4()

        scholarship_service.scholarship_repo.get_by_id.return_value = mock_scholarship
        scholarship_service.student_scholarship_repo.exists_duplicate.return_value = True

        data = ScholarshipAward(
            student_id=uuid4(),
            academic_year_id=uuid4(),
            amount_awarded=Decimal("50000"),
        )

        with pytest.raises(DuplicateScholarshipAwardError):
            await scholarship_service.award_scholarship(
                scholarship_id=uuid4(),
                data=data,
                school_id=uuid4(),
                user_id=uuid4(),
            )
