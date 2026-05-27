"""Health service for business logic operations."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from edulafia.modules.health.exceptions import (
    NurseRoleRequiredError,
    ReferralNotFoundError,
)
from edulafia.modules.health.repository import (
    HealthProfileRepository,
    HealthScreeningRepository,
    ReferralRepository,
    SickBayVisitRepository,
    VaccinationRepository,
)
from edulafia.modules.health.schemas import (
    HealthScreeningCreate,
    HealthScreeningResponse,
    ReferralCreate,
    ReferralResponse,
    ReferralUpdate,
    SickBayVisitCreate,
    SickBayVisitResponse,
    StudentHealthProfileCreate,
    StudentHealthProfileResponse,
    StudentHealthProfileUpdate,
    VaccinationRecordCreate,
    VaccinationRecordResponse,
)

# Standard symptom codes for Sentinel
STANDARD_SYMPTOM_CODES = [
    "fever", "cough", "runny_nose", "sore_throat", "headache",
    "body_ache", "vomiting", "diarrhea", "rash", "conjunctivitis",
    "fatigue", "abdominal_pain", "difficulty_breathing", "other",
]


class HealthService:
    """Service for health operations."""

    def __init__(
        self,
        profile_repo: HealthProfileRepository,
        visit_repo: SickBayVisitRepository,
        screening_repo: HealthScreeningRepository,
        referral_repo: ReferralRepository,
        vaccination_repo: VaccinationRepository,
    ):
        self.profile_repo = profile_repo
        self.visit_repo = visit_repo
        self.screening_repo = screening_repo
        self.referral_repo = referral_repo
        self.vaccination_repo = vaccination_repo

    async def get_student_profile(
        self,
        student_id: UUID,
        school_id: UUID,
        user_role: str,
    ) -> StudentHealthProfileResponse | None:
        """Get student health profile with privacy controls."""
        from edulafia.modules.health.exceptions import ParentalConsentRequiredError

        profile = await self.profile_repo.get_by_student(student_id, school_id=school_id)
        if not profile:
            return None

        # Check parental consent
        if not profile.parental_consent_given:
            raise ParentalConsentRequiredError()

        # Create response with privacy controls
        response = StudentHealthProfileResponse.model_validate(profile)

        # Filter sensitive data based on role
        if user_role not in ["nurse", "health_officer"]:
            response.genotype = None  # Only nurse can see genotype

        return response

    async def create_student_profile(
        self,
        data: StudentHealthProfileCreate,
        user_id: UUID,
    ) -> StudentHealthProfileResponse:
        """Create a new student health profile."""
        existing = await self.profile_repo.get_by_student(data.student_id)
        if existing:
            raise ValueError("Health profile already exists for this student")

        profile_data = data.model_dump()
        profile_data["created_by"] = user_id
        profile = await self.profile_repo.create(profile_data)
        return StudentHealthProfileResponse.model_validate(profile)

    async def update_student_profile(
        self,
        student_id: UUID,
        data: StudentHealthProfileUpdate,
        user_id: UUID,
    ) -> StudentHealthProfileResponse:
        """Update a student health profile."""
        profile = await self.profile_repo.get_by_student(student_id)
        if not profile:
            raise ValueError("Health profile not found")

        update_data = data.model_dump(exclude_none=True)
        update_data["updated_by"] = user_id
        updated_profile = await self.profile_repo.update(profile, update_data)
        return StudentHealthProfileResponse.model_validate(updated_profile)

    async def log_sick_bay_visit(
        self,
        data: SickBayVisitCreate,
        school_id: UUID,
        user_id: UUID,
        user_role: str,
    ) -> SickBayVisitResponse:
        """Log a sick bay visit."""
        # Check nurse authorization
        if user_role not in ["nurse", "health_officer"]:
            raise NurseRoleRequiredError()

        # Check if student is repeat visitor (>3 visits for same complaint)
        repeat_visitor = await self._check_repeat_visitor(
            school_id,
            data.student_id,
            data.presenting_complaint_codes,
        )

        # Determine if sentinel relevant
        is_sentinel_relevant = self._is_sentinel_relevant(
            data.presenting_complaint_codes,
            data.outcome,
        )

        # Create visit
        visit_data = {
            "student_id": data.student_id,
            "school_id": school_id,
            "visit_date": data.visit_date,
            "visit_time": data.visit_time,
            "presenting_complaint_codes": data.presenting_complaint_codes,
            "presenting_complaint_notes": data.presenting_complaint_notes,
            "temperature": float(data.temperature) if data.temperature else None,
            "blood_pressure_systolic": data.blood_pressure_systolic,
            "blood_pressure_diastolic": data.blood_pressure_diastolic,
            "pulse_rate": data.pulse_rate,
            "treatment_given": data.treatment_given,
            "outcome": data.outcome,
            "referred_to": data.referred_to,
            "is_sentinel_relevant": is_sentinel_relevant,
            "recorded_by": user_id,
        }

        visit = await self.visit_repo.create(visit_data)

        # Notify parent if treatment given or referred
        if data.treatment_given or data.outcome in ["sent_home", "referred", "hospitalized"]:
            await self._notify_parent_of_sick_bay_visit(
                student_id=data.student_id,
                school_id=school_id,
                visit_id=visit.id,
                outcome=data.outcome,
                treatment=data.treatment_given,
            )

        return SickBayVisitResponse.model_validate(visit)

    async def _notify_parent_of_sick_bay_visit(
        self,
        student_id: UUID,
        school_id: UUID,
        visit_id: UUID,
        outcome: str,
        treatment: str | None,
    ) -> None:
        """Notify parent about sick bay visit."""
        try:
            from sqlalchemy import text

            from edulafia.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db_session:
                # Find guardians linked to this student
                result = await db_session.execute(text("""
                    SELECT g.id, g.first_name, g.last_name, g.phone_number, g.whatsapp_number, g.portal_access
                    FROM guardians g
                    JOIN student_guardian sg ON g.id = sg.guardian_id
                    WHERE sg.student_id = :student_id
                      AND g.deleted_at IS NULL
                      AND g.portal_access = true
                    LIMIT 2
                """), {"student_id": str(student_id)})

                guardians = result.fetchall()

                if not guardians:
                    return

                # Create notification for each guardian using bulk insert
                message = (
                    f"Your child had a sick bay visit on {date.today()}. "
                    f"Outcome: {outcome.replace('_', ' ')}. "
                    f"Treatment: {treatment or 'None required'}. "
                    f"Please contact the school nurse if you have concerns."
                )
                
                insert_data = [
                    {
                        "guardian_id": str(guardian.id),
                        "student_id": str(student_id),
                        "message": message,
                    }
                    for guardian in guardians
                ]

                await db_session.execute(text("""
                    INSERT INTO parent_notifications
                        (id, guardian_id, student_id, notification_type, title, message, channel, priority, status, created_at, updated_at)
                    VALUES
                        (gen_random_uuid(), :guardian_id, :student_id, 'sick_bay_visit', 'Sick Bay Visit Notification', :message, 'whatsapp', 'high', 'pending', NOW(), NOW())
                """), insert_data)

                await db_session.commit()
        except Exception as e:
            # Don't fail the visit if notification fails
            import logging
            logging.getLogger(__name__).warning(f"Failed to notify parent of sick bay visit: {e}")

    async def _check_repeat_visitor(
        self,
        school_id: UUID,
        student_id: UUID,
        complaint_codes: list[str],
    ) -> bool:
        """Check if student is a repeat visitor (>3 visits for same complaint this term)."""
        term_end = date.today()
        term_start = date.today() - __import__("datetime").timedelta(days=90)
        
        try:
            from sqlalchemy import text

            from edulafia.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db_session:
                # Try to get actual academic year term dates if they exist
                term_stmt = text("""
                    SELECT start_date FROM academic_years 
                    WHERE school_id = :school_id AND is_current = true LIMIT 1
                """)
                term_res = await db_session.execute(term_stmt, {"school_id": str(school_id)})
                actual_start = term_res.scalar()
                if actual_start:
                    term_start = actual_start

            from edulafia.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db_session:
                result = await db_session.execute(text("""
                    SELECT t.start_date, t.end_date 
                    FROM terms t
                    JOIN academic_years a ON t.academic_year_id = a.id
                    WHERE a.school_id = :school_id 
                      AND t.is_current = true
                    LIMIT 1
                """), {"school_id": str(school_id)})
                
                term_data = result.fetchone()
                if term_data:
                    term_start = term_data.start_date
                    term_end = term_data.end_date
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to fetch current term: {e}")

        count = await self.visit_repo.count_visits_for_student_term(
            student_id, term_start, term_end
        )

        return count >= 3

    def _is_sentinel_relevant(
        self,
        complaint_codes: list[str],
        outcome: str,
    ) -> bool:
        """Determine if visit is sentinel relevant."""
        # Sentinel relevant if symptoms suggest communicable disease
        sentinel_symptoms = {"fever", "cough", "vomiting", "diarrhea", "rash"}
        return bool(set(complaint_codes) & sentinel_symptoms)

    async def list_sick_bay_visits(
        self,
        school_id: UUID,
        student_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> dict:
        """List sick bay visits with filters."""
        visits, total = await self.visit_repo.list(
            school_id=school_id,
            student_id=student_id,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [SickBayVisitResponse.model_validate(v) for v in visits],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def conduct_screening(
        self,
        data: HealthScreeningCreate,
        school_id: UUID,
        user_id: UUID,
        user_role: str,
    ) -> HealthScreeningResponse:
        """Conduct a health screening."""
        # Check nurse authorization
        if user_role not in ["nurse", "health_officer"]:
            raise NurseRoleRequiredError()

        # Calculate BMI if height and weight provided
        bmi = None
        if data.height and data.weight:
            height_m = float(data.height) / 100
            bmi = round(float(data.weight) / (height_m ** 2), 1)

        # Check for abnormal results and flags
        flags = list(data.flags) if data.flags else []
        follow_up_required = len(flags) > 0

        screening_data = {
            "student_id": data.student_id,
            "school_id": school_id,
            "screening_date": data.screening_date,
            "screening_type": data.screening_type,
            "height": float(data.height) if data.height else None,
            "weight": float(data.weight) if data.weight else None,
            "bmi": bmi,
            "muac": float(data.muac) if data.muac else None,
            "vision_left": float(data.vision_left) if data.vision_left else None,
            "vision_right": float(data.vision_right) if data.vision_right else None,
            "hearing_left": data.hearing_left,
            "hearing_right": data.hearing_right,
            "blood_pressure_systolic": data.blood_pressure_systolic,
            "blood_pressure_diastolic": data.blood_pressure_diastolic,
            "dental_notes": data.dental_notes,
            "sickle_cell_test_result": data.sickle_cell_test_result,
            "flags": flags,
            "follow_up_required": follow_up_required,
            "follow_up_notes": data.follow_up_notes,
            "conducted_by": user_id,
        }

        screening = await self.screening_repo.create(screening_data)
        return HealthScreeningResponse.model_validate(screening)

    async def create_referral(
        self,
        data: ReferralCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> ReferralResponse:
        """Create a referral."""
        referral_data = {
            "student_id": data.student_id,
            "sick_bay_visit_id": data.sick_bay_visit_id,
            "school_id": school_id,
            "referral_date": date.today(),
            "destination_facility": data.destination_facility,
            "reason": data.reason,
            "priority": data.priority,
            "status": "pending",
            "follow_up_due_date": data.follow_up_due_date,
            "created_by": user_id,
        }

        referral = await self.referral_repo.create(referral_data)
        return ReferralResponse.model_validate(referral)

    async def update_referral(
        self,
        referral_id: UUID,
        data: ReferralUpdate,
        school_id: UUID,
    ) -> ReferralResponse:
        """Update a referral."""
        referral = await self.referral_repo.get_by_id(referral_id, school_id)
        if not referral:
            raise ReferralNotFoundError(str(referral_id))

        update_data = data.model_dump(exclude_none=True)
        updated_referral = await self.referral_repo.update(referral, update_data)

        return ReferralResponse.model_validate(updated_referral)

    async def list_referrals(
        self,
        school_id: UUID,
        status: str | None = None,
        student_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List referrals with pagination."""
        referrals, total = await self.referral_repo.list(
            school_id=school_id,
            status=status,
            student_id=student_id,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [ReferralResponse.model_validate(r) for r in referrals],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def record_vaccination(
        self,
        data: VaccinationRecordCreate,
        school_id: UUID,
    ) -> VaccinationRecordResponse:
        """Record a vaccination."""
        vaccination_data = {
            "student_id": data.student_id,
            "school_id": school_id,
            "vaccine_name": data.vaccine_name,
            "vaccine_code": data.vaccine_code,
            "dose_number": data.dose_number,
            "administration_date": data.administration_date,
            "lot_number": data.lot_number,
            "administering_facility": data.administering_facility,
        }

        vaccination = await self.vaccination_repo.create(vaccination_data)
        return VaccinationRecordResponse.model_validate(vaccination)

    async def batch_import_vaccinations(
        self,
        records: list[VaccinationRecordCreate],
        school_id: UUID,
    ) -> dict:
        """Batch import vaccination records."""
        vaccination_data = [
            {
                "student_id": r.student_id,
                "school_id": school_id,
                "vaccine_name": r.vaccine_name,
                "vaccine_code": r.vaccine_code,
                "dose_number": r.dose_number,
                "administration_date": r.administration_date,
                "lot_number": r.lot_number,
                "administering_facility": r.administering_facility,
            }
            for r in records
        ]

        vaccinations = await self.vaccination_repo.create_many(vaccination_data)

        return {
            "success_count": len(vaccinations),
            "records": [VaccinationRecordResponse.model_validate(v) for v in vaccinations],
        }

    async def get_vaccination_records(
        self,
        student_id: UUID,
        school_id: UUID | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """Get paginated vaccination records for a student."""
        records, total = await self.vaccination_repo.list_by_student(
            student_id, school_id, page=page, per_page=per_page,
        )

        return {
            "items": [VaccinationRecordResponse.model_validate(r) for r in records],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def get_symptom_codes(self) -> list[dict]:
        """Get available symptom codes."""
        return [
            {"code": code, "description": code.replace("_", " ").title()}
            for code in STANDARD_SYMPTOM_CODES
        ]
