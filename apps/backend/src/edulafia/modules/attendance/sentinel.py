"""LafiyaSentinel integration service for health surveillance."""

from datetime import date
from uuid import UUID

from edulafia.modules.attendance.models import AttendanceRecord
from edulafia.modules.attendance.repository import AttendanceRepository


class SentinelIntegrationService:
    """Service for integrating attendance data with LafiyaSentinel."""

    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    @staticmethod
    def is_sentinel_relevant(record: AttendanceRecord) -> bool:
        """Check if an attendance record is relevant for Sentinel analysis.

        Sentinel-relevant criteria:
        - Status is 'absent'
        - Reason code is 'sick'
        - Symptom codes are present
        """
        return (
            record.status == "absent"
            and record.reason_code == "sick"
            and record.symptom_codes is not None
            and len(record.symptom_codes) > 0
        )

    @staticmethod
    def extract_symptom_data(record: AttendanceRecord) -> dict:
        """Extract symptom data for Sentinel processing."""
        return {
            "student_id": str(record.student_id),
            "school_id": str(record.school_id),
            "class_id": str(record.class_id),
            "date": str(record.date),
            "symptom_codes": record.symptom_codes,
            "recorded_at": record.created_at.isoformat(),
        }

    async def check_immediate_alert_threshold(
        self,
        school_id: UUID,
        attendance_date: date,
        threshold_percent: float = 10.0,
    ) -> bool:
        """Check if immediate Sentinel alert threshold is met.

        Immediate alert triggers when same-day illness with symptoms
        exceeds threshold percentage of school student population.
        """
        from sqlalchemy import text

        from edulafia.database import AsyncSessionLocal

        # Get all absent with symptoms for the date
        absent_with_symptoms = await self.repository.get_absent_with_symptoms(
            school_id, attendance_date
        )

        affected_count = len(absent_with_symptoms)

        # Get total student count for the school
        async with AsyncSessionLocal() as db_session:
            result = await db_session.execute(text(
                "SELECT count(*) FROM students WHERE school_id = :school_id AND deleted_at IS NULL"
            ), {"school_id": str(school_id)})
            total_students = result.scalar() or 1

        # Calculate percentage and compare against threshold (default 10%)
        affected_percent = (affected_count / total_students) * 100
        threshold_percent = 10.0

        return affected_percent >= threshold_percent

    async def batch_analysis(
        self,
        school_id: UUID,
        start_date: date,
        end_date: date,
    ) -> list[dict]:
        """Perform batch analysis on attendance data for Sentinel.

        Groups by symptom profile and creates signals when threshold met.
        """
        # Get all absent with symptoms in date range
        signals = []

        current_date = start_date
        while current_date <= end_date:
            absent_records = await self.repository.get_absent_with_symptoms(
                school_id, current_date
            )

            # Group by symptom combination
            symptom_groups: dict[str, list] = {}
            for record in absent_records:
                if record.symptom_codes:
                    key = ",".join(sorted(record.symptom_codes))
                    if key not in symptom_groups:
                        symptom_groups[key] = []
                    symptom_groups[key].append(record)

            # Check each group for threshold
            for symptoms_key, records in symptom_groups.items():
                if len(records) >= 3:  # Threshold for signal
                    signals.append({
                        "date": str(current_date),
                        "symptoms": symptoms_key.split(","),
                        "affected_count": len(records),
                        "student_ids": [str(r.student_id) for r in records],
                        "class_ids": list(set(str(r.class_id) for r in records)),
                    })

            # Move to next date
            from datetime import timedelta
            current_date += timedelta(days=1)

        return signals

    async def process_attendance_for_sentinel(
        self,
        record: AttendanceRecord,
    ) -> dict | None:
        """Process an attendance record for Sentinel relevance.

        Returns Sentinel signal data if relevant, None otherwise.
        """
        if not self.is_sentinel_relevant(record):
            return None

        return {
            "signal_type": "attendance_illness",
            "data": self.extract_symptom_data(record),
            "timestamp": record.created_at.isoformat(),
        }

    async def get_illness_cluster_data(
        self,
        school_id: UUID,
        attendance_date: date,
    ) -> dict:
        """Get illness cluster data for a school on a specific date."""
        absent_records = await self.repository.get_absent_with_symptoms(
            school_id, attendance_date
        )

        # Group by symptom
        symptom_counts: dict[str, int] = {}
        for record in absent_records:
            if record.symptom_codes:
                for symptom in record.symptom_codes:
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1

        return {
            "date": str(attendance_date),
            "total_illness_absences": len(absent_records),
            "symptom_breakdown": symptom_counts,
            "records": [self.extract_symptom_data(r) for r in absent_records],
        }
