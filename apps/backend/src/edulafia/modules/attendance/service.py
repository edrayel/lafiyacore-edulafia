"""Attendance service for business logic operations."""

from datetime import timezone, date, datetime
from uuid import UUID

from edulafia.modules.attendance.exceptions import (
    AttendanceNotFoundError,
    DuplicateAttendanceError,
    EditWindowExpiredError,
    FutureDateError,
    ReasonRequiredError,
    SymptomRequiredError,
)
from edulafia.modules.attendance.repository import AttendanceRepository
import logging

logger = logging.getLogger(__name__)
from edulafia.modules.attendance.schemas import (
    AttendanceBulkMarkRequest,
    AttendanceFilters,
    AttendanceMarkRequest,
    AttendanceRecordResponse,
    AttendanceSummaryResponse,
    AttendanceUpdateRequest,
)


class AttendanceService:
    """Service for attendance business logic."""

    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    async def mark_attendance(
        self,
        data: AttendanceMarkRequest,
        school_id: UUID,
        user_id: UUID,
    ) -> AttendanceRecordResponse:
        """Mark attendance for a single student."""
        # Validate date
        if data.date > date.today():
            raise FutureDateError()

        # Check for duplicate
        if await self.repository.exists_for_student_date(data.student_id, data.date):
            raise DuplicateAttendanceError(str(data.student_id), str(data.date))

        # Validate reason for absence
        if data.status == "absent" and data.reason_code is None:
            raise ReasonRequiredError()

        # Validate symptoms for sick reason
        if data.reason_code == "sick" and not data.symptom_codes:
            raise SymptomRequiredError()

        # Create record
        record_data = data.model_dump()
        record_data["school_id"] = school_id
        record_data["recorded_by"] = user_id
        record_data["sync_status"] = "synced"

        record = await self.repository.create(record_data)
        
        # 3-day consecutive absence automated alert
        if data.status == "absent":
            recent_absences = await self.repository.get_consecutive_absences(data.student_id, 3)
            if len(recent_absences) >= 3:
                logger.warning(
                    f"ATTENDANCE ALERT: Student {data.student_id} has 3 consecutive absences. "
                    "SMS/WhatsApp notification is not implemented. "
                    "Configure a notification provider and wire ParentNotificationService to enable alerts."
                )
                
        return AttendanceRecordResponse.model_validate(record)

    async def bulk_mark_attendance(
        self,
        data: AttendanceBulkMarkRequest,
        school_id: UUID,
        user_id: UUID,
    ) -> list[AttendanceRecordResponse]:
        """Bulk mark attendance for a class."""
        # Validate date
        if data.date > date.today():
            raise FutureDateError()

        # Prepare records for bulk creation
        records = []
        for exception in data.exceptions:
            record_data = exception.model_dump()
            record_data["school_id"] = school_id
            record_data["recorded_by"] = user_id
            record_data["sync_status"] = "synced"
            records.append(record_data)

        created_records = await self.repository.create_bulk(records)
        
        # Check for 3-day consecutive absences for any newly absent students
        absent_student_ids = [r.student_id for r in created_records if r.status == "absent"]
        
        if absent_student_ids:
            for student_id in absent_student_ids:
                recent_absences = await self.repository.get_consecutive_absences(student_id, 3)
                if len(recent_absences) >= 3:
                    logger.warning(
                        f"ATTENDANCE ALERT: Student {student_id} has 3 consecutive absences. "
                        "SMS/WhatsApp notification is not implemented."
                    )

        return [AttendanceRecordResponse.model_validate(r) for r in created_records]

    async def update_attendance(
        self,
        record_id: UUID,
        data: AttendanceUpdateRequest,
        school_id: UUID,
        user_id: UUID,
        edit_window_hours: int = 24,
    ) -> AttendanceRecordResponse:
        """Update an attendance record within edit window."""
        record = await self.repository.get_by_id(record_id, school_id)
        if not record:
            raise AttendanceNotFoundError(str(record_id))

        # Check edit window
        time_since_creation = datetime.now(record.created_at.tzinfo) - record.created_at
        if time_since_creation.total_seconds() > edit_window_hours * 3600:
            raise EditWindowExpiredError(edit_window_hours)

        # Update record
        update_data = data.model_dump(exclude_none=True, exclude={"edit_reason"})
        update_data["edited_at"] = datetime.now(timezone.utc)
        update_data["edited_by"] = user_id
        update_data["edit_reason"] = data.edit_reason

        updated_record = await self.repository.update(record, update_data)
        return AttendanceRecordResponse.model_validate(updated_record)

    async def get_attendance(
        self,
        school_id: UUID,
        filters: AttendanceFilters | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """Get attendance records with filters and pagination."""
        filter_dict = filters.model_dump(exclude_none=True) if filters else None
        records, total = await self.repository.list(
            school_id=school_id,
            filters=filter_dict,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [AttendanceRecordResponse.model_validate(r) for r in records],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def get_summary(
        self,
        school_id: UUID,
        class_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> AttendanceSummaryResponse:
        """Get attendance summary statistics."""
        summary = await self.repository.get_summary(
            school_id=school_id,
            class_id=class_id,
            start_date=start_date,
            end_date=end_date,
        )

        total = summary["total"]
        attendance_rate = (summary["present"] / total * 100) if total > 0 else 0

        return AttendanceSummaryResponse(
            total_students=total,
            present=summary["present"],
            absent=summary["absent"],
            late=summary["late"],
            excused=summary["excused"],
            attendance_rate=round(attendance_rate, 2),
        )

    async def get_consecutive_absences(
        self,
        student_id: UUID,
        days: int = 3,
    ) -> list[AttendanceRecordResponse]:
        """Get consecutive absences for a student."""
        records = await self.repository.get_consecutive_absences(student_id, days)
        return [AttendanceRecordResponse.model_validate(r) for r in records]

    async def get_student_absence_rate(
        self,
        student_id: UUID,
        start_date: date,
        end_date: date,
    ) -> float:
        """Calculate absence rate for a student."""
        return await self.repository.get_student_absence_rate(
            student_id, start_date, end_date
        )
