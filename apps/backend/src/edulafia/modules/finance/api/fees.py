"""Finance API endpoints."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.dependencies import CurrentUser
from edulafia.database import get_db
from edulafia.core.rate_limiter import rate_limit

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
from edulafia.modules.finance.service import (
    FeeService,
    PaymentService,
    ScholarshipService,
)

from edulafia.modules.finance.api.webhooks import router as webhooks_router

router = APIRouter(prefix="/finance", tags=["Finance"])
router.include_router(webhooks_router, prefix="", include_in_schema=True)


def get_fee_service(db: AsyncSession = Depends(get_db)) -> FeeService:
    """Dependency to get FeeService."""
    schedule_repo = FeeScheduleRepository(db)
    item_repo = FeeScheduleItemRepository(db)
    return FeeService(schedule_repo, item_repo)


def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    """Dependency to get PaymentService."""
    ledger_repo = FeeLedgerRepository(db)
    student_scholarship_repo = StudentScholarshipRepository(db)
    return PaymentService(ledger_repo, student_scholarship_repo)


def get_scholarship_service(db: AsyncSession = Depends(get_db)) -> ScholarshipService:
    """Dependency to get ScholarshipService."""
    scholarship_repo = ScholarshipRepository(db)
    student_scholarship_repo = StudentScholarshipRepository(db)
    return ScholarshipService(scholarship_repo, student_scholarship_repo)


@router.get(
    "/reports/debt",
    summary="Get Debt Collection Report",
)
async def get_debt_report(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    term_id: str | None = Query(None, description="Filter by specific term"),
    class_id: UUID | None = Query(None, description="Filter by class"),
) -> dict:
    """Generate a debt report showing students with outstanding balances."""
    from edulafia.modules.students.models import Student
    from edulafia.modules.finance.models import FeeLedger
    from sqlalchemy import select, func
    from decimal import Decimal

    school_id = UUID(current_user["school_id"])
    
    # We'll aggregate charges, payments, and waivers per student to find outstanding balances
    subquery_charges = (
        select(
            FeeLedger.student_id,
            func.sum(FeeLedger.amount).label("total_charges")
        )
        .where(FeeLedger.school_id == school_id)
        .where(FeeLedger.transaction_type == "charge")
        .group_by(FeeLedger.student_id)
        .subquery()
    )

    subquery_credits = (
        select(
            FeeLedger.student_id,
            func.sum(FeeLedger.amount).label("total_credits")
        )
        .where(FeeLedger.school_id == school_id)
        .where(FeeLedger.transaction_type.in_(["payment", "waiver"]))
        .group_by(FeeLedger.student_id)
        .subquery()
    )

    stmt = (
        select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.admission_number,
            func.coalesce(subquery_charges.c.total_charges, 0).label("charges"),
            func.coalesce(subquery_credits.c.total_credits, 0).label("credits"),
        )
        .outerjoin(subquery_charges, Student.id == subquery_charges.c.student_id)
        .outerjoin(subquery_credits, Student.id == subquery_credits.c.student_id)
        .where(Student.school_id == school_id)
    )

    if class_id:
        stmt = stmt.where(Student.current_class_id == class_id)

    result = await db.execute(stmt)
    debtors = []
    total_debt = Decimal("0")
    
    for row in result:
        charges = row.charges or 0
        credits = row.credits or 0
        balance = Decimal(str(charges)) - Decimal(str(credits))
        
        if balance > 0:
            # Query last payment date
            last_payment_stmt = select(func.max(FeeLedger.created_at)).where(
                FeeLedger.student_id == row.id,
                FeeLedger.transaction_type == "payment"
            )
            last_payment_result = await db.execute(last_payment_stmt)
            last_payment = last_payment_result.scalar_one_or_none()
            
            debtors.append({
                "student_id": str(row.id),
                "name": f"{row.first_name} {row.last_name}",
                "admission_number": row.admission_number,
                "amount_owed": float(balance),
                "last_payment_date": last_payment.isoformat() if last_payment else None,
            })
            total_debt += balance

    return {
        "status": "success",
        "data": {
            "total_debt": float(total_debt),
            "debtor_count": len(debtors),
            "debtors": debtors
        }
    }


# Fee Schedule Endpoints

@router.post(
    "/fee-schedules",
    response_model=FeeScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create fee schedule",
)
async def create_fee_schedule(
    data: FeeScheduleCreate,
    current_user: CurrentUser,
    service: FeeService = Depends(get_fee_service),
) -> FeeScheduleResponse:
    """Create a new fee schedule."""
    try:
        return await service.create_schedule(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateFeeCategoryError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(
    "/{student_id}/payments/online",
    response_model=dict,
    summary="Initiate online payment",
    dependencies=[Depends(rate_limit(max_requests=10, window_seconds=60))],
)
async def initiate_online_payment(
    data: PaymentRecord,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(get_payment_service),
) -> dict:
    """Initiate an online payment via gateway (Paystack integration)."""
    import uuid
    import logging
    from edulafia.modules.finance.paystack import PaystackClient
    from edulafia.modules.auth.models import User
    from sqlalchemy import select
    
    logger = logging.getLogger(__name__)
    
    user_id = UUID(current_user["sub"])
    user_stmt = select(User).where(User.id == user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    email = user.email if user else "user@edulafia.com"
    
    reference = f"EDULAFIA-{uuid.uuid4().hex[:8].upper()}"
    
    logger.info(f"Initiating Paystack payment. Ref: {reference}, Amount: {data.amount}")
    
    payment_url = await PaystackClient.initialize_transaction(
        email=email,
        amount=float(data.amount),
        reference=reference,
    )

    return {
        "status": "success",
        "message": "Payment initiated successfully",
        "data": {
            "payment_url": payment_url,
            "reference": reference,
            "amount": data.amount,
            "currency": "NGN"
        }
    }

@router.get(
    "/fee-schedules",
    response_model=Page[FeeScheduleResponse],
    summary="List fee schedules",
)
async def list_fee_schedules(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    academic_year_id: UUID | None = Query(None),
    is_active: bool | None = Query(None),
    service: FeeService = Depends(get_fee_service),
) -> dict:
    """List fee schedules with pagination."""
    return await service.list_schedules(
        school_id=UUID(current_user["school_id"]),
        academic_year_id=academic_year_id,
        is_active=is_active,
        page=pag.page,
        per_page=pag.per_page,
    )


@router.get(
    "/fee-schedules/{schedule_id}",
    response_model=FeeScheduleResponse,
    summary="Get fee schedule",
)
async def get_fee_schedule(
    schedule_id: UUID,
    current_user: CurrentUser,
    service: FeeService = Depends(get_fee_service),
) -> FeeScheduleResponse:
    """Get a fee schedule by ID."""
    try:
        return await service.get_schedule(
            schedule_id=schedule_id,
            school_id=UUID(current_user["school_id"]),
        )
    except FeeScheduleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fee schedule not found")


@router.post(
    "/fee-schedules/{schedule_id}/lock",
    response_model=FeeScheduleResponse,
    summary="Lock fee schedule",
)
async def lock_fee_schedule(
    schedule_id: UUID,
    current_user: CurrentUser,
    service: FeeService = Depends(get_fee_service),
) -> FeeScheduleResponse:
    """Lock a fee schedule."""
    try:
        return await service.lock_schedule(
            schedule_id=schedule_id,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except FeeScheduleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fee schedule not found")


@router.post(
    "/fee-schedules/copy",
    response_model=FeeScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Copy fee schedule",
)
async def copy_fee_schedule(
    data: FeeScheduleCopy,
    current_user: CurrentUser,
    service: FeeService = Depends(get_fee_service),
) -> FeeScheduleResponse:
    """Copy a fee schedule to a new academic year."""
    try:
        return await service.copy_schedule(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except FeeScheduleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fee schedule not found")


# Payment Endpoints

@router.post(
    "/payments",
    response_model=FeeLedgerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record payment",
    dependencies=[Depends(rate_limit(max_requests=30, window_seconds=60))],
)
async def record_payment(
    data: PaymentRecord,
    current_user: CurrentUser,
    service: PaymentService = Depends(get_payment_service),
) -> FeeLedgerResponse:
    """Record a payment."""
    try:
        return await service.record_payment(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
            user_role=current_user.get("role", ""),
        )
    except BursarRoleRequiredError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except PaymentExceedsLimitError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/payments",
    response_model=dict,
    summary="List payments",
)
async def list_payments(
    current_user: CurrentUser,
    student_id: UUID | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    service: PaymentService = Depends(get_payment_service),
) -> dict:
    """List payments with filters."""
    from datetime import datetime

    start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
    end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None

    return await service.list_payments(
        school_id=UUID(current_user["school_id"]),
        student_id=student_id,
        start_date=start_datetime,
        end_date=end_datetime,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/payments/{payment_id}",
    response_model=FeeLedgerResponse,
    summary="Get payment",
)
async def get_payment(
    payment_id: UUID,
    current_user: CurrentUser,
    service: PaymentService = Depends(get_payment_service),
) -> FeeLedgerResponse:
    """Get a payment by ID."""
    try:
        return await service.get_payment(
            payment_id=payment_id,
            school_id=UUID(current_user["school_id"]),
        )
    except PaymentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")


@router.post(
    "/payments/{payment_id}/reverse",
    response_model=FeeLedgerResponse,
    summary="Reverse payment",
)
async def reverse_payment(
    payment_id: UUID,
    data: PaymentReversal,
    current_user: CurrentUser,
    service: PaymentService = Depends(get_payment_service),
) -> FeeLedgerResponse:
    """Reverse a payment."""
    try:
        return await service.reverse_payment(
            payment_id=payment_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except PaymentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    except OnlinePaymentReversalError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Receipt Endpoints

@router.get(
    "/receipts/{receipt_number}",
    response_model=FeeLedgerResponse,
    summary="Get receipt",
)
async def get_receipt(
    receipt_number: str,
    current_user: CurrentUser,
    service: PaymentService = Depends(get_payment_service),
) -> FeeLedgerResponse:
    """Get a receipt by receipt number."""
    try:
        return await service.get_receipt(receipt_number=receipt_number)
    except PaymentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")


# Balance Endpoints

@router.get(
    "/students/{student_id}/balance",
    response_model=StudentBalanceResponse,
    summary="Get student balance",
)
async def get_student_balance(
    student_id: UUID,
    current_user: CurrentUser,
    term_id: UUID | None = Query(None),
    service: PaymentService = Depends(get_payment_service),
) -> StudentBalanceResponse:
    """Get student balance."""
    return await service.get_student_balance(
        student_id=student_id,
        term_id=term_id,
    )


# Scholarship Endpoints

@router.post(
    "/scholarships",
    response_model=ScholarshipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create scholarship",
)
async def create_scholarship(
    data: ScholarshipCreate,
    current_user: CurrentUser,
    service: ScholarshipService = Depends(get_scholarship_service),
) -> ScholarshipResponse:
    """Create a new scholarship."""
    return await service.create_scholarship(
        data=data,
        school_id=UUID(current_user["school_id"]),
    )


@router.get(
    "/scholarships",
    response_model=Page[ScholarshipResponse],
    summary="List scholarships",
)
async def list_scholarships(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    is_active: bool | None = Query(None),
    service: ScholarshipService = Depends(get_scholarship_service),
) -> dict:
    """List scholarships with pagination."""
    return await service.list_scholarships(
        school_id=UUID(current_user["school_id"]),
        is_active=is_active,
        page=pag.page,
        per_page=pag.per_page,
    )


@router.post(
    "/scholarships/{scholarship_id}/award",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Award scholarship",
)
async def award_scholarship(
    scholarship_id: UUID,
    data: ScholarshipAward,
    current_user: CurrentUser,
    service: ScholarshipService = Depends(get_scholarship_service),
) -> dict:
    """Award a scholarship to a student."""
    try:
        return await service.award_scholarship(
            scholarship_id=scholarship_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ScholarshipNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scholarship not found")
    except DuplicateScholarshipAwardError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/scholarships/{scholarship_id}/recipients",
    response_model=list[dict],
    summary="Get scholarship recipients",
)
async def get_scholarship_recipients(
    scholarship_id: UUID,
    current_user: CurrentUser,
    service: ScholarshipService = Depends(get_scholarship_service),
) -> list[dict]:
    """Get all recipients of a scholarship."""
    return await service.get_recipients(scholarship_id=scholarship_id, school_id=UUID(current_user["school_id"]))
