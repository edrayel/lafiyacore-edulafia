"""Tests for Finance models and schemas - written BEFORE implementation (TDD)."""

from decimal import Decimal
from uuid import uuid4

import pytest


class TestFeeScheduleModel:
    """Test cases for FeeSchedule model."""

    def test_fee_schedule_model_exists(self):
        """Test that FeeSchedule model class exists."""
        from edulafia.modules.finance.models import FeeSchedule
        assert FeeSchedule is not None

    def test_fee_schedule_has_required_fields(self):
        """Test that FeeSchedule has all required fields."""
        from edulafia.modules.finance.models import FeeSchedule
        columns = FeeSchedule.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'academic_year_id', 'name',
            'is_active', 'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"FeeSchedule missing field: {field}"

    def test_fee_schedule_has_table_name(self):
        """Test that FeeSchedule has correct table name."""
        from edulafia.modules.finance.models import FeeSchedule
        assert FeeSchedule.__tablename__ == 'fee_schedules'


class TestFeeLedgerModel:
    """Test cases for FeeLedger model."""

    def test_fee_ledger_model_exists(self):
        """Test that FeeLedger model class exists."""
        from edulafia.modules.finance.models import FeeLedger
        assert FeeLedger is not None

    def test_fee_ledger_has_required_fields(self):
        """Test that FeeLedger has all required fields."""
        from edulafia.modules.finance.models import FeeLedger
        columns = FeeLedger.__table__.columns.keys()

        required_fields = [
            'id', 'student_id', 'school_id', 'transaction_date',
            'transaction_type', 'fee_category', 'amount', 'recorded_by'
        ]
        for field in required_fields:
            assert field in columns, f"FeeLedger missing field: {field}"

    def test_fee_ledger_has_table_name(self):
        """Test that FeeLedger has correct table name."""
        from edulafia.modules.finance.models import FeeLedger
        assert FeeLedger.__tablename__ == 'fee_ledger'


class TestScholarshipModel:
    """Test cases for Scholarship model."""

    def test_scholarship_model_exists(self):
        """Test that Scholarship model class exists."""
        from edulafia.modules.finance.models import Scholarship
        assert Scholarship is not None

    def test_scholarship_has_required_fields(self):
        """Test that Scholarship has required fields."""
        from edulafia.modules.finance.models import Scholarship
        columns = Scholarship.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'name', 'is_active', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"Scholarship missing field: {field}"

    def test_scholarship_has_table_name(self):
        """Test that Scholarship has correct table name."""
        from edulafia.modules.finance.models import Scholarship
        assert Scholarship.__tablename__ == 'scholarships'


class TestPaymentConfigurationModel:
    """Test cases for PaymentConfiguration model."""

    def test_payment_configuration_model_exists(self):
        """Test that PaymentConfiguration model class exists."""
        from edulafia.modules.finance.models import PaymentConfiguration
        assert PaymentConfiguration is not None

    def test_payment_configuration_has_required_fields(self):
        """Test that PaymentConfiguration has required fields."""
        from edulafia.modules.finance.models import PaymentConfiguration
        columns = PaymentConfiguration.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'payment_gateway', 'is_active', 'created_at'
        ]
        for field in required_fields:
            assert field in columns, f"PaymentConfiguration missing field: {field}"

    def test_payment_configuration_has_table_name(self):
        """Test that PaymentConfiguration has correct table name."""
        from edulafia.modules.finance.models import PaymentConfiguration
        assert PaymentConfiguration.__tablename__ == 'payment_configurations'


class TestPaymentSchemas:
    """Test cases for Payment schemas."""

    def test_payment_record_schema_exists(self):
        """Test that PaymentRecord schema exists."""
        from edulafia.modules.finance.schemas import PaymentRecord
        assert PaymentRecord is not None

    def test_payment_record_validates_amount(self):
        """Test that PaymentRecord validates amount."""
        from pydantic import ValidationError

        from edulafia.modules.finance.schemas import PaymentRecord

        with pytest.raises(ValidationError):
            PaymentRecord(
                student_id=uuid4(),
                amount=0,  # Invalid - must be > 0
                payment_method="cash",
            )

    def test_payment_record_validates_max_amount(self):
        """Test that PaymentRecord validates max amount."""
        from pydantic import ValidationError

        from edulafia.modules.finance.schemas import PaymentRecord

        with pytest.raises(ValidationError):
            PaymentRecord(
                student_id=uuid4(),
                amount=Decimal("600000"),  # Exceeds 500,000 limit
                payment_method="cash",
            )

    def test_payment_record_validates_payment_method(self):
        """Test that PaymentRecord validates payment method."""
        from pydantic import ValidationError

        from edulafia.modules.finance.schemas import PaymentRecord

        with pytest.raises(ValidationError):
            PaymentRecord(
                student_id=uuid4(),
                amount=Decimal("1000"),
                payment_method="invalid_method",
            )

    def test_fee_ledger_response_exists(self):
        """Test that FeeLedgerResponse schema exists."""
        from edulafia.modules.finance.schemas import FeeLedgerResponse
        assert FeeLedgerResponse is not None

    def test_student_balance_response_exists(self):
        """Test that StudentBalanceResponse schema exists."""
        from edulafia.modules.finance.schemas import StudentBalanceResponse
        assert StudentBalanceResponse is not None


class TestScholarshipSchemas:
    """Test cases for Scholarship schemas."""

    def test_scholarship_create_schema_exists(self):
        """Test that ScholarshipCreate schema exists."""
        from edulafia.modules.finance.schemas import ScholarshipCreate
        assert ScholarshipCreate is not None

    def test_scholarship_response_exists(self):
        """Test that ScholarshipResponse schema exists."""
        from edulafia.modules.finance.schemas import ScholarshipResponse
        assert ScholarshipResponse is not None

    def test_scholarship_award_exists(self):
        """Test that ScholarshipAward schema exists."""
        from edulafia.modules.finance.schemas import ScholarshipAward
        assert ScholarshipAward is not None
