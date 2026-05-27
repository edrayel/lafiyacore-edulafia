"""Attendance API endpoints."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.attendance.exceptions import (
    AttendanceNotFoundError,
    DuplicateAttendanceError,
    EditWindowExpiredError,
    FutureDateError,
    ReasonRequiredError,
    SymptomRequiredError,
)
from edulafia.modules.attendance.repository import AttendanceRepository
from edulafia.modules.attendance.schemas import (
    AttendanceBulkMarkRequest,
    AttendanceFilters,
    AttendanceMarkRequest,
    AttendanceRecordResponse,
    AttendanceSummaryResponse,
    AttendanceUpdateRequest,
)
from edulafia.modules.attendance.service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def get_attendance_service(db: AsyncSession = Depends(get_db)) -> AttendanceService:
    """Dependency to get AttendanceService."""
    repository = AttendanceRepository(db)
    return AttendanceService(repository)


@router.post(
    "/mark",
    response_model=AttendanceRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance for a student",
)
async def mark_attendance(
    data: AttendanceMarkRequest,
    current_user: CurrentUser,
    service: AttendanceService = Depends(get_attendance_service),
) -> AttendanceRecordResponse:
    """Mark attendance for a single student."""
    try:
        return await service.mark_attendance(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except DuplicateAttendanceError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except FutureDateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SymptomRequiredError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except ReasonRequiredError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post(
    "/mark/bulk",
    response_model=list[AttendanceRecordResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Bulk mark attendance for a class",
)
async def bulk_mark_attendance(
    data: AttendanceBulkMarkRequest,
    current_user: CurrentUser,
    service: AttendanceService = Depends(get_attendance_service),
) -> list[AttendanceRecordResponse]:
    """Bulk mark attendance for a class."""
    try:
        return await service.bulk_mark_attendance(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except FutureDateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=dict,
    summary="Query attendance records",
)
async def get_attendance(
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    student_id: UUID | None = Query(None),
    class_id: UUID | None = Query(None),
    date: date | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    status: str | None = Query(None),
    service: AttendanceService = Depends(get_attendance_service),
) -> dict:
    """Query attendance records with filters."""
    filters = AttendanceFilters(
        student_id=student_id,
        class_id=class_id,
        date=date,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    return await service.get_attendance(
        school_id=UUID(current_user["school_id"]),
        filters=filters,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/summary",
    response_model=AttendanceSummaryResponse,
    summary="Get attendance summary",
)
async def get_attendance_summary(
    current_user: CurrentUser,
    class_id: UUID | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    service: AttendanceService = Depends(get_attendance_service),
) -> AttendanceSummaryResponse:
    """Get attendance summary statistics."""
    return await service.get_summary(
        school_id=UUID(current_user["school_id"]),
        class_id=class_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/emis-export",
    summary="Export attendance for EMIS",
)
async def export_emis_attendance(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    term_id: str | None = Query(None),
) -> dict:
    """Generate EMIS compatible attendance export."""
    from sqlalchemy import select, func
    from edulafia.modules.attendance.models import AttendanceRecord
    from edulafia.modules.students.models import Student
    from edulafia.modules.admin.models import School
    
    school_id = UUID(current_user["school_id"])
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Generating EMIS compatible export payload for Term: {start_date} to {end_date}, School: {school_id}")

    # Query attendance grouped by student, class, and gender
    stmt = (
        select(
            Student.current_class_id.label("class_id"),
            Student.gender,
            func.count(AttendanceRecord.id).label("total_records"),
            func.sum(func.case((AttendanceRecord.status == "present", 1), else_=0)).label("present_days"),
            func.sum(func.case((AttendanceRecord.status == "absent", 1), else_=0)).label("absent_days"),
        )
        .join(Student, Student.id == AttendanceRecord.student_id)
        .where(AttendanceRecord.school_id == school_id)
    )
    
    if start_date:
        stmt = stmt.where(AttendanceRecord.date >= start_date)
    if end_date:
        stmt = stmt.where(AttendanceRecord.date <= end_date)
        
    stmt = stmt.group_by(Student.current_class_id, Student.gender)
    result = await db.execute(stmt)
    
    # Format the data into EMIS schema
    school_stmt = select(School.name, School.lga, School.state).where(School.id == school_id)
    school_res = await db.execute(school_stmt)
    school_info = school_res.first()
    
    class_aggregates = {}
    for row in result:
        cls_id = str(row.class_id)
        if cls_id not in class_aggregates:
            class_aggregates[cls_id] = {
                "class_id": cls_id,
                "boys_present": 0,
                "boys_absent": 0,
                "girls_present": 0,
                "girls_absent": 0,
                "total_expected_days": 0
            }
            
        agg = class_aggregates[cls_id]
        if row.gender == "male":
            agg["boys_present"] += int(row.present_days or 0)
            agg["boys_absent"] += int(row.absent_days or 0)
        else:
            agg["girls_present"] += int(row.present_days or 0)
            agg["girls_absent"] += int(row.absent_days or 0)
            
        agg["total_expected_days"] = max(agg["total_expected_days"], int(row.total_records or 0))

    return {
        "status": "success",
        "data": {
            "metadata": {
                "school_id": str(school_id),
                "school_name": school_info.name if school_info else "Unknown",
                "lga": school_info.lga if school_info else "Unknown",
                "state": school_info.state if school_info else "Unknown",
                "term_id": term_id or "Current",
                "period": f"{start_date} to {end_date}" if start_date and end_date else "All Time",
                "generated_at": date.today().isoformat()
            },
            "class_aggregates": list(class_aggregates.values())
        }
    }


@router.patch(
    "/{attendance_id}",
    response_model=AttendanceRecordResponse,
    summary="Update attendance record",
)
async def update_attendance(
    attendance_id: UUID,
    data: AttendanceUpdateRequest,
    current_user: CurrentUser,
    service: AttendanceService = Depends(get_attendance_service),
) -> AttendanceRecordResponse:
    """Update an attendance record within edit window."""
    try:
        return await service.update_attendance(
            record_id=attendance_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except AttendanceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    except EditWindowExpiredError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
