"""Staff Attendance API endpoints."""

from datetime import timezone, UTC, date, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.staff.repository import (
    StaffRepository,
    TeacherAttendanceRepository,
)
from edulafia.modules.staff.schemas import (
    TeacherAttendanceResponse,
    TeacherCheckIn,
)

router = APIRouter(prefix="/staff/attendance", tags=["Staff Attendance"])


def get_attendance_repo(db: AsyncSession = Depends(get_db)) -> TeacherAttendanceRepository:
    """Dependency to get TeacherAttendanceRepository."""
    return TeacherAttendanceRepository(db)


def get_staff_repo(db: AsyncSession = Depends(get_db)) -> StaffRepository:
    """Dependency to get StaffRepository."""
    return StaffRepository(db)


@router.post(
    "/check-in",
    response_model=TeacherAttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Teacher check-in",
)
async def teacher_check_in(
    data: TeacherCheckIn,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> TeacherAttendanceResponse:
    """Record teacher check-in."""
    attendance_repo = get_attendance_repo(db)
    staff_repo = get_staff_repo(db)

    staff_id_str = current_user.get("staff_id")
    if not staff_id_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff ID not found in token",
        )

    staff = await staff_repo.get_by_id(UUID(staff_id_str), UUID(current_user["school_id"]))
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    today = date.today()
    existing = await attendance_repo.get_by_staff_date(staff.id, today)

    now = datetime.now(UTC)

    if existing:
        update_data = {
            "check_in_time": now,
            "check_in_method": data.check_in_method,
            "status": "present",
        }
        attendance = await attendance_repo.update(existing, update_data)
    else:
        attendance_data = {
            "staff_id": staff.id,
            "school_id": UUID(current_user["school_id"]),
            "date": today,
            "check_in_time": now,
            "check_in_method": data.check_in_method,
            "status": "present",
            "recorded_by": UUID(current_user["sub"]),
        }
        attendance = await attendance_repo.create(attendance_data)

    return TeacherAttendanceResponse.model_validate(attendance)


@router.post(
    "/check-out",
    response_model=TeacherAttendanceResponse,
    summary="Teacher check-out",
)
async def teacher_check_out(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> TeacherAttendanceResponse:
    """Record teacher check-out."""
    attendance_repo = get_attendance_repo(db)
    staff_repo = get_staff_repo(db)

    staff_id_str = current_user.get("staff_id")
    if not staff_id_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff ID not found in token",
        )

    staff = await staff_repo.get_by_id(UUID(staff_id_str), UUID(current_user["school_id"]))
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    today = date.today()
    existing = await attendance_repo.get_by_staff_date(staff.id, today)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No check-in found for today")

    now = datetime.now(UTC)
    attendance = await attendance_repo.update(existing, {"check_out_time": now})
    return TeacherAttendanceResponse.model_validate(attendance)


@router.post(
    "/{staff_id}",
    response_model=TeacherAttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record teacher attendance",
)
async def record_teacher_attendance(
    staff_id: UUID,
    current_user: CurrentUser,
    attendance_date: date = Query(...),
    status: str = Query("present"),
    notes: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> TeacherAttendanceResponse:
    """Manually record teacher attendance (for admin use)."""
    attendance_repo = get_attendance_repo(db)
    staff_repo = get_staff_repo(db)

    staff = await staff_repo.get_by_id(staff_id, UUID(current_user["school_id"]))
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    existing = await attendance_repo.get_by_staff_date(staff_id, attendance_date)
    if existing:
        update_data = {"status": status, "notes": notes}
        attendance = await attendance_repo.update(existing, update_data)
    else:
        attendance_data = {
            "staff_id": staff_id,
            "school_id": UUID(current_user["school_id"]),
            "date": attendance_date,
            "status": status,
            "notes": notes,
            "recorded_by": UUID(current_user["sub"]),
        }
        attendance = await attendance_repo.create(attendance_data)

    return TeacherAttendanceResponse.model_validate(attendance)


@router.get(
    "",
    response_model=dict,
    summary="List teacher attendance",
)
async def list_teacher_attendance(
    current_user: CurrentUser,
    staff_id: UUID | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List teacher attendance records with filters."""
    attendance_repo = get_attendance_repo(db)
    records, total = await attendance_repo.list(
        school_id=UUID(current_user["school_id"]),
        staff_id=staff_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )

    return {
        "items": [TeacherAttendanceResponse.model_validate(r) for r in records],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


@router.get(
    "/{staff_id}",
    response_model=dict,
    summary="Get teacher attendance",
)
async def get_teacher_attendance(
    staff_id: UUID,
    current_user: CurrentUser,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get attendance records for a specific teacher."""
    attendance_repo = get_attendance_repo(db)
    records, total = await attendance_repo.list(
        school_id=UUID(current_user["school_id"]),
        staff_id=staff_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )

    return {
        "items": [TeacherAttendanceResponse.model_validate(r) for r in records],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }
