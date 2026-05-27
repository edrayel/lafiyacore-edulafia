"""Finance service for business logic operations."""

from datetime import timezone, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from edulafia.modules.finance.exceptions import (
    BursarRoleRequiredError,
    DuplicateFeeCategoryError,
    DuplicateScholarshipAwardError,
    FeeScheduleNotFoundError,
    OnlinePaymentReversalError,
    PaymentExceedsLimitError,
    PaymentNotFoundError,
    ScholarshipNotFoundError,
)
from edulafia.modules.finance.repository import (
    FeeLedgerRepository,
    FeeScheduleItemRepository,
    FeeScheduleRepository,
    ScholarshipRepository,
    StudentScholarshipRepository,
)
from edulafia.modules.finance.schemas import (
    FeeLedgerResponse,
    FeeScheduleCopy,
    FeeScheduleCreate,
    FeeScheduleResponse,
    PaymentRecord,
    PaymentReversal,
    ScholarshipAward,
    ScholarshipCreate,
    ScholarshipResponse,
    StudentBalanceResponse,
)
from edulafia.modules.students.models import Student


class FeeService:
    """Service for fee schedule management."""

    def __init__(
        self,
        schedule_repo: FeeScheduleRepository,
        item_repo: FeeScheduleItemRepository,
    ):
        self.schedule_repo = schedule_repo
        self.item_repo = item_repo

    async def create_schedule(
        self,
        data: FeeScheduleCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> FeeScheduleResponse:
        """Create a new fee schedule with items."""
        # Create schedule
        schedule_data = data.model_dump(exclude={"items"})
        schedule_data["school_id"] = school_id
        schedule_data["created_by"] = user_id
        schedule_data["updated_by"] = user_id

        schedule = await self.schedule_repo.create(schedule_data)

        # Check for duplicates in memory
        if data.items:
            seen_categories = set()
            for item in data.items:
                key = (item.class_level, item.fee_category)
                if key in seen_categories:
                    raise DuplicateFeeCategoryError(item.class_level, item.fee_category)
                seen_categories.add(key)

            items_data = [
                {
                    **item.model_dump(),
                    "fee_schedule_id": schedule.id,
                    "created_by": user_id,
                }
                for item in data.items
            ]
            await self.item_repo.create_many(items_data)

        return FeeScheduleResponse.model_validate(schedule)

    async def get_schedule(
        self,
        schedule_id: UUID,
        school_id: UUID,
    ) -> FeeScheduleResponse:
        """Get a fee schedule by ID."""
        schedule = await self.schedule_repo.get_by_id(schedule_id, school_id)
        if not schedule:
            raise FeeScheduleNotFoundError(str(schedule_id))
        return FeeScheduleResponse.model_validate(schedule)

    async def list_schedules(
        self,
        school_id: UUID,
        academic_year_id: UUID | None = None,
        is_active: bool | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List fee schedules with pagination."""
        schedules, total = await self.schedule_repo.list(
            school_id=school_id,
            academic_year_id=academic_year_id,
            is_active=is_active,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [FeeScheduleResponse.model_validate(s) for s in schedules],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def lock_schedule(
        self,
        schedule_id: UUID,
        school_id: UUID,
        user_id: UUID,
    ) -> FeeScheduleResponse:
        """Lock a fee schedule."""
        schedule = await self.schedule_repo.get_by_id(schedule_id, school_id)
        if not schedule:
            raise FeeScheduleNotFoundError(str(schedule_id))

        locked_schedule = await self.schedule_repo.lock(schedule_id, user_id)
        return FeeScheduleResponse.model_validate(locked_schedule)

    async def copy_schedule(
        self,
        data: FeeScheduleCopy,
        school_id: UUID,
        user_id: UUID,
    ) -> FeeScheduleResponse:
        """Copy a fee schedule to a new academic year."""
        # Get source schedule
        source = await self.schedule_repo.get_by_id(data.source_schedule_id, school_id)
        if not source:
            raise FeeScheduleNotFoundError(str(data.source_schedule_id))

        # Get source items
        source_items = await self.item_repo.get_by_schedule(source.id)

        # Create new schedule
        new_schedule_data = {
            "school_id": school_id,
            "academic_year_id": data.target_academic_year_id,
            "name": source.name,
            "description": source.description,
            "is_active": True,
            "created_by": user_id,
            "updated_by": user_id,
        }
        new_schedule = await self.schedule_repo.create(new_schedule_data)

        # Copy items with optional adjustment
        if source_items:
            items_data = []
            for item in source_items:
                amount = float(item.amount)
                if data.adjust_percentage:
                    amount = amount * (1 + float(data.adjust_percentage) / 100)

                items_data.append({
                    "fee_schedule_id": new_schedule.id,
                    "class_level": item.class_level,
                    "fee_category": item.fee_category,
                    "amount": amount,
                    "is_mandatory": item.is_mandatory,
                    "created_by": user_id,
                })

            await self.item_repo.create_many(items_data)

        return FeeScheduleResponse.model_validate(new_schedule)


class PaymentService:
    """Service for payment operations."""

    def __init__(
        self,
        ledger_repo: FeeLedgerRepository,
        student_scholarship_repo: StudentScholarshipRepository,
    ):
        self.ledger_repo = ledger_repo
        self.student_scholarship_repo = student_scholarship_repo

    async def record_payment(
        self,
        data: PaymentRecord,
        school_id: UUID,
        user_id: UUID,
        user_role: str,
    ) -> FeeLedgerResponse:
        """Record a payment."""
        # Check bursar role
        if user_role != "bursar":
            raise BursarRoleRequiredError()

        # Check amount limit
        if data.amount > 500000:
            raise PaymentExceedsLimitError(float(data.amount))

        # Generate receipt number
        receipt_number = await self.ledger_repo.get_next_receipt_number(
            school_id, datetime.now(timezone.utc).year
        )

        # Determine fee category
        fee_category = data.fee_category or "tuition"

        # Create ledger entry
        entry_data = {
            "student_id": data.student_id,
            "school_id": school_id,
            "term_id": data.term_id,
            "transaction_date": datetime.now(timezone.utc),
            "transaction_type": "payment",
            "fee_category": fee_category,
            "amount": float(data.amount),
            "payment_method": data.payment_method,
            "payment_reference": data.payment_reference,
            "receipt_number": receipt_number,
            "description": data.description,
            "recorded_by": user_id,
        }

        entry = await self.ledger_repo.create(entry_data)
        return FeeLedgerResponse.model_validate(entry)

    async def reverse_payment(
        self,
        payment_id: UUID,
        data: PaymentReversal,
        school_id: UUID,
        user_id: UUID,
    ) -> FeeLedgerResponse:
        """Reverse a payment."""
        # Get original payment
        payment = await self.ledger_repo.get_by_id(payment_id, school_id)
        if not payment:
            raise PaymentNotFoundError(str(payment_id))

        # Check if online payment needs gateway confirmation
        if payment.payment_method in ["paystack", "flutterwave", "remita"]:
            if not data.gateway_confirmation:
                raise OnlinePaymentReversalError()

        # Create reversal entry
        reversal_data = {
            "student_id": payment.student_id,
            "school_id": school_id,
            "term_id": payment.term_id,
            "transaction_date": datetime.now(timezone.utc),
            "transaction_type": "refund",
            "fee_category": payment.fee_category,
            "amount": -float(payment.amount),  # Negative amount for reversal
            "payment_method": payment.payment_method,
            "payment_reference": f"REV-{payment.payment_reference or payment.id}",
            "description": f"Reversal: {data.reason}",
            "recorded_by": user_id,
        }

        reversal = await self.ledger_repo.create(reversal_data)
        return FeeLedgerResponse.model_validate(reversal)

    async def get_payment(
        self,
        payment_id: UUID,
        school_id: UUID,
    ) -> FeeLedgerResponse:
        """Get a payment by ID."""
        entry = await self.ledger_repo.get_by_id(payment_id, school_id)
        if not entry:
            raise PaymentNotFoundError(str(payment_id))
        return FeeLedgerResponse.model_validate(entry)

    async def get_receipt(self, receipt_number: str) -> FeeLedgerResponse:
        """Get a payment by receipt number."""
        entry = await self.ledger_repo.get_by_receipt(receipt_number)
        if not entry:
            raise PaymentNotFoundError(receipt_number)
        return FeeLedgerResponse.model_validate(entry)

    async def list_payments(
        self,
        school_id: UUID,
        student_id: UUID | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List payments with filters."""
        entries, total = await self.ledger_repo.list(
            school_id=school_id,
            student_id=student_id,
            transaction_type="payment",
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [FeeLedgerResponse.model_validate(e) for e in entries],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def get_student_balance(
        self,
        student_id: UUID,
        term_id: UUID | None = None,
    ) -> StudentBalanceResponse:
        """Get student balance."""
        balance_data = await self.ledger_repo.get_student_balance(
            student_id, term_id
        )

        return StudentBalanceResponse(
            student_id=student_id,
            student_name=balance_data.get("student_name", ""),
            total_charges=Decimal(str(balance_data["total_charges"])),
            total_payments=Decimal(str(balance_data["total_payments"])),
            total_waivers=Decimal(str(balance_data["total_waivers"])),
            balance=Decimal(str(balance_data["balance"])),
            term_id=term_id,
        )


class ScholarshipService:
    """Service for scholarship operations."""

    def __init__(
        self,
        scholarship_repo: ScholarshipRepository,
        student_scholarship_repo: StudentScholarshipRepository,
    ):
        self.scholarship_repo = scholarship_repo
        self.student_scholarship_repo = student_scholarship_repo

    async def create_scholarship(
        self,
        data: ScholarshipCreate,
        school_id: UUID,
    ) -> ScholarshipResponse:
        """Create a new scholarship."""
        scholarship_data = data.model_dump()
        scholarship_data["school_id"] = school_id

        scholarship = await self.scholarship_repo.create(scholarship_data)
        return ScholarshipResponse.model_validate(scholarship)

    async def list_scholarships(
        self,
        school_id: UUID,
        is_active: bool | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List scholarships with pagination."""
        scholarships, total = await self.scholarship_repo.list(
            school_id=school_id,
            is_active=is_active,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [ScholarshipResponse.model_validate(s) for s in scholarships],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def award_scholarship(
        self,
        scholarship_id: UUID,
        data: ScholarshipAward,
        school_id: UUID,
        user_id: UUID,
    ) -> dict:
        """Award a scholarship to a student."""
        # Check scholarship exists
        scholarship = await self.scholarship_repo.get_by_id(scholarship_id, school_id)
        if not scholarship:
            raise ScholarshipNotFoundError(str(scholarship_id))

        # Check for duplicate
        if await self.student_scholarship_repo.exists_duplicate(
            data.student_id, scholarship_id, data.academic_year_id
        ):
            raise DuplicateScholarshipAwardError(
                str(data.student_id), str(scholarship_id), str(data.academic_year_id)
            )

        # Create student scholarship
        award_data = {
            "student_id": data.student_id,
            "scholarship_id": scholarship_id,
            "academic_year_id": data.academic_year_id,
            "amount_awarded": float(data.amount_awarded),
            "awarded_date": datetime.now(timezone.utc).date(),
            "awarded_by": user_id,
            "notes": data.notes,
        }

        student_scholarship = await self.student_scholarship_repo.create(award_data)

        return {
            "id": str(student_scholarship.id),
            "student_id": str(data.student_id),
            "scholarship_id": str(scholarship_id),
            "amount_awarded": float(data.amount_awarded),
            "message": "Scholarship awarded successfully",
        }

    async def get_recipients(
        self,
        scholarship_id: UUID,
        school_id: UUID,
    ) -> list[dict]:
        """Get all recipients of a scholarship."""
        recipients = await self.student_scholarship_repo.list_by_scholarship(
            scholarship_id, school_id=school_id
        )

        return [
            {
                "id": str(r.id),
                "student_id": str(r.student_id),
                "amount_awarded": float(r.amount_awarded),
                "awarded_date": str(r.awarded_date),
            }
            for r in recipients
        ]
