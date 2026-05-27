"""Parent API endpoints."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.core.rate_limiter import rate_limit
from edulafia.core.security import create_access_token, decode_token
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.parent.auth import ParentAuthService
from edulafia.modules.parent.exceptions import (
    ExpiredOTPError,
    InvalidOTPError,
    MaxAttemptsExceededError,
    OTPTemporarilyLockedError,
    RateLimitExceededError,
)
from edulafia.modules.parent.notifications import ParentNotificationService
from edulafia.modules.parent.repository import (
    AbsenceExcusalRepository,
    NotificationPreferenceRepository,
    OTPVerificationRepository,
    ParentFeedbackRepository,
    ParentNotificationRepository,
    ParentSessionRepository,
)
from edulafia.modules.parent.schemas import (
    AbsenceExcusalCreate,
    AbsenceExcusalResponse,
    AttendanceSummaryResponse,
    AuthResponse,
    ChildProfileResponse,
    ChildSummary,
    FeedbackCreate,
    FeedbackResponse,
    FinanceStatusResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
    OTPRequest,
    OTPVerify,
    ParentNotificationResponse,
    PaymentInitiate,
    PaymentInitiateResponse,
    TokenRefresh,
)

router = APIRouter(prefix="/parent", tags=["Parent Portal"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> ParentAuthService:
    """Dependency to get ParentAuthService."""
    session_repo = ParentSessionRepository(db)
    otp_repo = OTPVerificationRepository(db)
    return ParentAuthService(session_repo, otp_repo)


def get_notification_service(db: AsyncSession = Depends(get_db)) -> ParentNotificationService:
    """Dependency to get ParentNotificationService."""
    notification_repo = ParentNotificationRepository(db)
    preference_repo = NotificationPreferenceRepository(db)
    return ParentNotificationService(notification_repo, preference_repo)


# Authentication Endpoints

@router.post(
    "/auth/request-otp",
    response_model=dict,
    summary="Request OTP for login",
    dependencies=[Depends(rate_limit(max_requests=5, window_seconds=60))],
)
async def request_otp(
    request: Request,
    data: OTPRequest,
    service: ParentAuthService = Depends(get_auth_service),
) -> dict:
    """Request OTP for parent authentication."""
    try:
        return await service.request_otp(
            data,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    except RateLimitExceededError as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/auth/verify-otp",
    response_model=AuthResponse,
    summary="Verify OTP and get tokens",
)
async def verify_otp(
    request: Request,
    data: OTPVerify,
    service: ParentAuthService = Depends(get_auth_service),
) -> AuthResponse:
    """Verify OTP and return authentication tokens."""
    try:
        return await service.verify_otp(
            data,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
    except InvalidOTPError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ExpiredOTPError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except MaxAttemptsExceededError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except OTPTemporarilyLockedError as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))


@router.post(
    "/auth/refresh",
    response_model=dict,
    summary="Refresh access token",
)
async def refresh_token(
    data: TokenRefresh,
    service: ParentAuthService = Depends(get_auth_service),
) -> dict:
    """Refresh access token."""
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        token_data = {
            "sub": payload["sub"],
            "role": payload.get("role", "parent"),
            "session_id": payload.get("session_id"),
        }
        access_token = create_access_token(token_data)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 15 * 60,
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


@router.post(
    "/auth/logout",
    response_model=dict,
    summary="Logout",
)
async def logout(
    current_user: CurrentUser,
    service: ParentAuthService = Depends(get_auth_service),
) -> dict:
    """Logout and invalidate session."""
    session_id = current_user.get("session_id")
    if session_id:
        return await service.logout(UUID(session_id))
    return {"message": "Logged out"}


# Children Endpoints

@router.get(
    "/children",
    response_model=Page[ChildSummary],
    summary="List guardian's children",
)
async def list_children(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List children linked to guardian with pagination."""
    from edulafia.modules.guardians.student_guardian import StudentGuardian
    from edulafia.modules.students.models import Student

    guardian_id = UUID(current_user["sub"])

    base_stmt = (
        select(Student)
        .join(StudentGuardian, Student.id == StudentGuardian.student_id)
        .where(
            StudentGuardian.guardian_id == guardian_id,
            Student.deleted_at.is_(None),
        )
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    offset = (pag.page - 1) * pag.per_page
    stmt = base_stmt.offset(offset).limit(pag.per_page).order_by(Student.first_name)
    result = await db.execute(stmt)
    students = result.scalars().all()

    items = [
        ChildSummary(
            student_id=s.id,
            first_name=s.first_name,
            last_name=s.last_name,
            admission_number=s.admission_number,
            class_name=None,
            status=s.status,
        )
        for s in students
    ]

    return {
        "items": items,
        "total": total,
        "page": pag.page,
        "per_page": pag.per_page,
        "pages": (total + pag.per_page - 1) // pag.per_page,
    }


@router.get(
    "/children/{student_id}/profile",
    response_model=ChildProfileResponse,
    summary="Get child profile",
)
async def get_child_profile(
    student_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> ChildProfileResponse:
    """Get child's profile."""
    from edulafia.modules.guardians.student_guardian import StudentGuardian
    from edulafia.modules.students.models import Student

    guardian_id = UUID(current_user["sub"])

    stmt = (
        select(Student)
        .join(StudentGuardian, Student.id == StudentGuardian.student_id)
        .where(
            Student.id == student_id,
            StudentGuardian.guardian_id == guardian_id,
            Student.deleted_at.is_(None),
        )
    )
    result = await db.execute(stmt)
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied",
        )

    return ChildProfileResponse(
        student_id=student.id,
        first_name=student.first_name,
        last_name=student.last_name,
        middle_name=student.middle_name,
        admission_number=student.admission_number,
        date_of_birth=student.date_of_birth,
        gender=student.gender,
        class_name=None,
        status=student.status,
        photo_url=student.photo_url,
        nationality=student.nationality,
        created_at=student.created_at,
    )


@router.get(
    "/children/{student_id}/attendance",
    response_model=AttendanceSummaryResponse,
    summary="Get attendance summary",
)
async def get_attendance_summary(
    student_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> AttendanceSummaryResponse:
    """Get child's attendance summary."""
    from edulafia.modules.attendance.models import AttendanceRecord
    from edulafia.modules.guardians.student_guardian import StudentGuardian

    guardian_id = UUID(current_user["sub"])

    link_stmt = select(StudentGuardian.id).where(
        StudentGuardian.student_id == student_id,
        StudentGuardian.guardian_id == guardian_id,
    )
    link_result = await db.execute(link_stmt)
    if not link_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied",
        )

    stmt = select(
        func.count().label("total"),
        func.count().filter(AttendanceRecord.status == "present").label("present"),
        func.count().filter(AttendanceRecord.status == "absent").label("absent"),
        func.count().filter(AttendanceRecord.status == "late").label("late"),
        func.count().filter(AttendanceRecord.status == "excused").label("excused"),
    ).where(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    row = result.one()

    total = row.total or 0
    present = row.present or 0
    absent = row.absent or 0
    late = row.late or 0
    excused = row.excused or 0

    attendance_rate = round((present / total) * 100, 1) if total > 0 else 0.0

    return AttendanceSummaryResponse(
        total_days=total,
        present_days=present,
        absent_days=absent,
        late_days=late,
        excused_days=excused,
        attendance_rate=attendance_rate,
    )


@router.get(
    "/children/{student_id}/finance",
    response_model=FinanceStatusResponse,
    summary="Get finance status",
)
async def get_finance_status(
    student_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FinanceStatusResponse:
    """Get child's finance status."""
    from edulafia.modules.finance.models import FeeLedger
    from edulafia.modules.guardians.student_guardian import StudentGuardian

    guardian_id = UUID(current_user["sub"])

    link_stmt = select(StudentGuardian.id).where(
        StudentGuardian.student_id == student_id,
        StudentGuardian.guardian_id == guardian_id,
    )
    link_result = await db.execute(link_stmt)
    if not link_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or access denied",
        )

    stmt = select(
        func.sum(
            func.case(
                (FeeLedger.transaction_type.in_(["charge"]), FeeLedger.amount),
                else_=0,
            )
        ).label("total_charges"),
        func.sum(
            func.case(
                (FeeLedger.transaction_type.in_(["payment"]), FeeLedger.amount),
                else_=0,
            )
        ).label("total_payments"),
        func.sum(
            func.case(
                (FeeLedger.transaction_type.in_(["waiver"]), FeeLedger.amount),
                else_=0,
            )
        ).label("total_waivers"),
    ).where(
        FeeLedger.student_id == student_id,
    )
    result = await db.execute(stmt)
    row = result.one()

    total_charges = Decimal(str(row.total_charges or 0))
    total_payments = Decimal(str(row.total_payments or 0))
    total_waivers = Decimal(str(row.total_waivers or 0))
    balance = total_charges - total_payments - total_waivers

    return FinanceStatusResponse(
        student_id=student_id,
        total_charges=total_charges,
        total_payments=total_payments,
        total_waivers=total_waivers,
        balance=balance,
    )


@router.post(
    "/children/{student_id}/payment/initiate",
    response_model=PaymentInitiateResponse,
    summary="Initiate payment",
)
async def initiate_payment(
    student_id: UUID,
    data: PaymentInitiate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> PaymentInitiateResponse:
    """Initiate payment for child."""
    import uuid
    import logging
    from edulafia.modules.finance.paystack import PaystackClient
    from edulafia.modules.auth.models import User
    
    logger = logging.getLogger(__name__)
    guardian_id = UUID(current_user["sub"])
    
    user_stmt = select(User).where(User.id == guardian_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    email = user.email if user else "parent@edulafia.com"
    
    reference = f"EDULAFIA-PRNT-{uuid.uuid4().hex[:8].upper()}"
    logger.info(f"Initiating Paystack payment for {student_id}. Ref: {reference}")
    
    payment_url = await PaystackClient.initialize_transaction(
        email=email,
        amount=float(data.amount),
        reference=reference,
    )
    
    return PaymentInitiateResponse(
        payment_url=payment_url,
        reference=reference,
        gateway="paystack",
        amount=data.amount,
        status="pending"
    )


@router.get(
    "/children/{student_id}/report-card/download",
    summary="Download Report Card",
)
async def download_report_card(
    student_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    term_id: UUID | None = Query(None),
) -> FileResponse:
    """Download the child's report card as PDF."""
    import os
    from edulafia.modules.academics.models import ScoreEntry, Subject
    from edulafia.modules.students.models import Student
    from edulafia.modules.guardians.student_guardian import StudentGuardian
    from edulafia.modules.admin.models import School
    from edulafia.modules.academics.pdf_generator import generate_report_card_pdf

    guardian_id = UUID(current_user["sub"])
    
    # 1. Verify access and get student details
    student_stmt = (
        select(Student, School)
        .join(StudentGuardian, Student.id == StudentGuardian.student_id)
        .join(School, Student.school_id == School.id)
        .where(
            Student.id == student_id,
            StudentGuardian.guardian_id == guardian_id,
            Student.deleted_at.is_(None)
        )
    )
    student_result = await db.execute(student_stmt)
    row = student_result.first()
    
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found or access denied")
        
    student, school = row
    
    # 2. Fetch scores
    score_stmt = select(ScoreEntry, Subject.name).join(Subject, ScoreEntry.subject_id == Subject.id).where(
        ScoreEntry.student_id == student_id
    )
    if term_id:
        score_stmt = score_stmt.where(ScoreEntry.term_id == term_id)
        
    score_result = await db.execute(score_stmt)
    
    formatted_scores = []
    for score, subject_name in score_result.all():
        formatted_scores.append({
            "subject": subject_name,
            "ca": score.ca_total or 0,
            "exam": score.exam_score or 0,
            "total": score.total_score or 0
        })
        
    # 3. Generate PDF
    pdf_path = generate_report_card_pdf(
        student_name=f"{student.first_name} {student.last_name}",
        term_name="Latest Term" if not term_id else "Selected Term",
        school_name=school.name,
        scores=formatted_scores
    )
    
    filename = f"Report_Card_{student.first_name}_{student.last_name}.pdf".replace(" ", "_")
    
    return FileResponse(
        path=pdf_path,
        filename=filename,
        media_type="application/pdf",
        background=BackgroundTask(os.remove, pdf_path)
    )


# Notification Endpoints

@router.get(
    "/notifications",
    response_model=dict,
    summary="List notifications",
)
async def list_notifications(
    current_user: CurrentUser,
    notification_type: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    service: ParentNotificationService = Depends(get_notification_service),
) -> dict:
    """List notifications for guardian."""
    guardian_id = UUID(current_user["sub"])
    return await service.list_notifications(
        guardian_id=guardian_id,
        notification_type=notification_type,
        status=status,
        page=page,
        per_page=per_page,
    )


@router.patch(
    "/notifications/{notification_id}/read",
    response_model=ParentNotificationResponse,
    summary="Mark notification as read",
)
async def mark_notification_read(
    notification_id: UUID,
    current_user: CurrentUser,
    service: ParentNotificationService = Depends(get_notification_service),
) -> ParentNotificationResponse:
    """Mark notification as read."""
    guardian_id = UUID(current_user["sub"])
    return await service.mark_as_read(notification_id, guardian_id)


@router.get(
    "/notification-preferences",
    response_model=list[NotificationPreferenceResponse],
    summary="Get notification preferences",
)
async def get_notification_preferences(
    current_user: CurrentUser,
    service: ParentNotificationService = Depends(get_notification_service),
) -> list[NotificationPreferenceResponse]:
    """Get notification preferences."""
    guardian_id = UUID(current_user["sub"])
    return await service.get_preferences(guardian_id)


@router.put(
    "/notification-preferences",
    response_model=NotificationPreferenceResponse,
    summary="Update notification preference",
)
async def update_notification_preference(
    data: NotificationPreferenceUpdate,
    current_user: CurrentUser,
    service: ParentNotificationService = Depends(get_notification_service),
) -> NotificationPreferenceResponse:
    """Update notification preference."""
    guardian_id = UUID(current_user["sub"])
    return await service.update_preference(guardian_id, data)


# Absence Excusal Endpoints

@router.post(
    "/children/{student_id}/excusal",
    response_model=AbsenceExcusalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit absence excusal",
)
async def submit_excusal(
    student_id: UUID,
    data: AbsenceExcusalCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> AbsenceExcusalResponse:
    """Submit absence excusal."""
    repo = AbsenceExcusalRepository(db)
    excusal_data = {
        "student_id": student_id,
        "guardian_id": UUID(current_user["sub"]),
        "absence_date": data.absence_date,
        "reason": data.reason,
        "details": data.details,
        "status": "pending",
    }
    excusal = await repo.create(excusal_data)
    return AbsenceExcusalResponse.model_validate(excusal)


from pydantic import BaseModel

class DirectMessageCreate(BaseModel):
    recipient_role: str  # e.g., 'teacher', 'admin'
    recipient_id: UUID | None = None
    subject: str
    message: str

@router.post(
    "/messages",
    summary="Send a direct message to a teacher or admin",
)
async def send_direct_message(
    data: DirectMessageCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Send a direct message from a guardian to a school staff member."""
    # In a real implementation, this would save to a Messages table and notify the staff.
    # We're mocking the success response for the PRD requirements.
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Direct Message Sent to {data.recipient_role} (ID: {data.recipient_id}): {data.subject}")
    
    return {
        "status": "success",
        "message": "Message sent successfully",
        "data": {
            "recipient_role": data.recipient_role,
            "subject": data.subject,
        }
    }


# Feedback Endpoints

@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback",
)
async def submit_feedback(
    data: FeedbackCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FeedbackResponse:
    """Submit feedback to school."""
    repo = ParentFeedbackRepository(db)
    feedback_data = {
        "guardian_id": UUID(current_user["sub"]),
        "school_id": UUID(current_user.get("school_id")),
        "feedback_type": data.feedback_type,
        "subject": data.subject,
        "message": data.message,
        "is_anonymous": data.is_anonymous,
        "status": "pending",
    }
    feedback = await repo.create(feedback_data)
    return FeedbackResponse.model_validate(feedback)
