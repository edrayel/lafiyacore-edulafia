"""Services for business logic operations."""

from decimal import Decimal
from uuid import UUID

from edulafia.modules.academics.exceptions import (
    DuplicateSubjectCodeError,
    SubjectNotFoundError,
)
from edulafia.modules.academics.grade_computation import GradeComputationService
from edulafia.modules.academics.repository import AcademicResultRepository, SubjectRepository
from edulafia.modules.academics.schemas import (
    AcademicResultResponse,
    SubjectCreate,
    SubjectResponse,
    SubjectUpdate,
)


class SubjectService:
    """Service for subject business logic."""

    def __init__(self, repository: SubjectRepository):
        self.repository = repository

    async def create(
        self,
        data: SubjectCreate,
        school_id: UUID,
        user_id: UUID,
    ) -> SubjectResponse:
        """Create a new subject."""
        # Check for duplicate code
        if await self.repository.exists_by_code(data.code, school_id):
            raise DuplicateSubjectCodeError(data.code)

        # Prepare data
        subject_data = data.model_dump()
        subject_data["school_id"] = school_id
        subject_data["created_by"] = user_id
        subject_data["updated_by"] = user_id

        # Create subject
        subject = await self.repository.create(subject_data)
        return SubjectResponse.model_validate(subject)

    async def get_by_id(
        self,
        subject_id: UUID,
        school_id: UUID,
    ) -> SubjectResponse | None:
        """Get a subject by ID."""
        subject = await self.repository.get_by_id(subject_id, school_id)
        if subject:
            return SubjectResponse.model_validate(subject)
        return None

    async def list_subjects(
        self,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
        is_core: bool | None = None,
    ) -> dict:
        """List subjects with pagination and optional filter."""
        subjects, total = await self.repository.list(
            school_id=school_id,
            page=page,
            per_page=per_page,
            is_core=is_core,
        )

        pages = (total + per_page - 1) // per_page

        return {
            "items": [SubjectResponse.model_validate(s) for s in subjects],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }

    async def update(
        self,
        subject_id: UUID,
        data: SubjectUpdate,
        school_id: UUID,
        user_id: UUID,
    ) -> SubjectResponse:
        """Update a subject."""
        subject = await self.repository.get_by_id(subject_id, school_id)
        if not subject:
            raise SubjectNotFoundError(str(subject_id))

        # Prepare update data
        update_data = data.model_dump(exclude_none=True)
        update_data["updated_by"] = user_id

        updated_subject = await self.repository.update(subject, update_data)
        return SubjectResponse.model_validate(updated_subject)

    async def archive(
        self,
        subject_id: UUID,
        school_id: UUID,
    ) -> SubjectResponse:
        """Archive (soft delete) a subject."""
        subject = await self.repository.get_by_id(subject_id, school_id)
        if not subject:
            raise SubjectNotFoundError(str(subject_id))

        archived_subject = await self.repository.soft_delete(subject)
        return SubjectResponse.model_validate(archived_subject)


class AcademicResultService:
    """Service for academic result business logic."""

    def __init__(self, repository: AcademicResultRepository):
        self.repository = repository

    async def list_scores(
        self,
        class_id: UUID,
        subject_id: UUID,
        term_id: UUID,
        school_id: UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """List scores with pagination."""
        results, total = await self.repository.list_by_class_term_subject(
            class_id=class_id,
            term_id=term_id,
            subject_id=subject_id,
            school_id=school_id,
            page=page,
            per_page=per_page,
        )

        return {
            "items": [AcademicResultResponse.model_validate(r) for r in results],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }

    async def create_score(
        self,
        student_id: UUID,
        subject_id: UUID,
        class_id: UUID,
        term_id: UUID,
        academic_year_id: UUID,
        school_id: UUID,
        user_id: UUID,
        ca_scores: dict,
        exam_score: Decimal,
        flag: str | None = None,
    ) -> AcademicResultResponse:
        """Create an academic result with computed grade."""
        ca_total = sum(Decimal(str(v)) for v in ca_scores.values()) if ca_scores else Decimal("0")
        total_score = ca_total + exam_score
        grade_result = GradeComputationService.compute_grade(total_score)

        data = {
            "student_id": student_id,
            "subject_id": subject_id,
            "class_id": class_id,
            "term_id": term_id,
            "academic_year_id": academic_year_id,
            "school_id": school_id,
            "ca_scores": ca_scores,
            "ca_total": float(ca_total),
            "exam_score": float(exam_score),
            "total_score": float(total_score),
            "grade": grade_result["grade"],
            "class_rank": None,
            "flag": flag,
            "teacher_id": user_id,
            "created_by": user_id,
            "updated_by": user_id,
        }

        result = await self.repository.create(data)
        return AcademicResultResponse.model_validate(result)

    async def create_scores_bulk(
        self,
        subject_id: UUID,
        class_id: UUID,
        term_id: UUID,
        academic_year_id: UUID,
        school_id: UUID,
        user_id: UUID,
        score_entries: list[dict],
    ) -> list[AcademicResultResponse]:
        """Create multiple academic results with computed grades."""
        records = []
        for entry in score_entries:
            ca_scores = entry["ca_scores"]
            exam_score = entry["exam_score"]
            flag = entry.get("flag")

            ca_total = sum(Decimal(str(v)) for v in ca_scores.values()) if ca_scores else Decimal("0")
            total_score = ca_total + exam_score
            grade_result = GradeComputationService.compute_grade(total_score)

            records.append({
                "student_id": entry["student_id"],
                "subject_id": subject_id,
                "class_id": class_id,
                "term_id": term_id,
                "academic_year_id": academic_year_id,
                "school_id": school_id,
                "ca_scores": ca_scores,
                "ca_total": float(ca_total),
                "exam_score": float(exam_score),
                "total_score": float(total_score),
                "grade": grade_result["grade"],
                "class_rank": None,
                "flag": flag,
                "teacher_id": user_id,
                "created_by": user_id,
                "updated_by": user_id,
            })

        results = await self.repository.create_many(records)
        return [AcademicResultResponse.model_validate(r) for r in results]

    async def compute_grades_for_class(
        self,
        class_id: UUID,
        term_id: UUID,
        school_id: UUID | None = None,
        subject_id: UUID | None = None,
    ) -> dict:
        """Compute grades and ranks for all students in a class."""
        if subject_id:
            results = await self.repository.list_by_class_term_subject(class_id, term_id, subject_id)
            subjects = [subject_id]
        else:
            all_results = await self.repository.list_by_class_term_subject(class_id, term_id, subject_id)
            subjects = list(set(r.subject_id for r in all_results))
            results = all_results

        scores_by_subject = {}
        for result in results:
            if result.subject_id not in scores_by_subject:
                scores_by_subject[result.subject_id] = []
            scores_by_subject[result.subject_id].append({
                "result_id": result.id,
                "student_id": result.student_id,
                "total_score": Decimal(str(result.total_score)),
                "flag": result.flag,
            })

        total_updated = 0
        
        try:
            # We should wrap in a transaction, but the repository methods execute against `self.db` 
            # and flush. If an error occurs, the endpoint's global dependency will rollback or 
            # we can rollback here if we want explicit handling.
            # We'll rely on the bulk update.
            rank_updates = []
            for subj_id, scores in scores_by_subject.items():
                ranked = GradeComputationService.calculate_class_ranks(scores)
                for entry in ranked:
                    if entry["rank"] is not None:
                        rank_updates.append({"id": entry["result_id"], "class_rank": entry["rank"]})

            if rank_updates:
                total_updated = await self.repository.update_ranks(rank_updates)
                # Ensure the entire computation block is flushed/committed together.
                # The dependency usually commits, but if it fails, it rolls back all updates.
        except Exception:
            await self.repository.db.rollback()
            raise
                        
        # Automated alerts for >20% performance drop
        alerts_generated = 0
        from edulafia.modules.academics.models import ScoreEntry
        from sqlalchemy import select, func
        
        student_ids = list(set(r.student_id for r in results))
        
        # Fetch previous term average dynamically for ALL students in one query
        previous_avgs = {}
        if student_ids:
            stmt = select(ScoreEntry.student_id, func.avg(ScoreEntry.total_score)).where(
                ScoreEntry.student_id.in_(student_ids),
                ScoreEntry.term_id != term_id,
                ScoreEntry.total_score.is_not(None)
            ).group_by(ScoreEntry.student_id)
            prev_results = await self.repository.session.execute(stmt)
            previous_avgs = {row[0]: row[1] for row in prev_results}

        for student_id in student_ids:
            # 1. Fetch current term average
            current_term_results = [r for r in results if r.student_id == student_id and r.total_score is not None]
            if not current_term_results:
                continue
            current_avg = sum(float(r.total_score) for r in current_term_results) / len(current_term_results)
            
            # 2. Compare against previous term average
            previous_avg = previous_avgs.get(student_id)
            
            if previous_avg is not None and current_avg < float(previous_avg) * 0.8:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"PERFORMANCE ALERT: Student {student_id} dropped from {float(previous_avg):.1f} to {current_avg:.1f}")
                alerts_generated += 1

        return {
            "message": f"Grades computed and ranks updated for {total_updated} results. {alerts_generated} performance alerts generated.",
            "class_id": str(class_id),
            "term_id": str(term_id),
            "results_updated": total_updated,
            "alerts_generated": alerts_generated,
        }

    async def generate_report_card(
        self,
        student_id: UUID,
        term_id: UUID,
        school_id: UUID,
    ) -> dict:
        """Generate report card for a student for a specific term."""
        # Get all academic results for the student and term
        results = await self.repository.list_by_student_term(student_id, term_id)
        
        # Calculate overall average
        total_score = 0
        subject_count = 0
        subject_results = []
        
        for result in results:
            if result.flag not in ["ABS", "INC"]:  # Exclude absent or incomplete
                total_score += result.total_score
                subject_count += 1
                
            subject_results.append({
                "subject_id": str(result.subject_id),
                "subject_code": result.subject_code,
                "subject_name": result.subject_name,
                "ca_total": result.ca_total,
                "exam_score": result.exam_score,
                "total_score": result.total_score,
                "grade": result.grade,
                "class_rank": result.class_rank,
                "flag": result.flag,
            })
        
        # Calculate average
        average = round(total_score / subject_count, 2) if subject_count > 0 else 0
        
        # Determine overall grade
        overall_grade = GradeComputationService.compute_grade(Decimal(str(average)))["grade"]
        
        report_data = {
            "student_id": str(student_id),
            "term_id": str(term_id),
            "average": average,
            "overall_grade": overall_grade,
            "subject_count": subject_count,
            "subject_results": subject_results,
        }
        
        return report_data
