"""Academics API endpoints for scores and grades."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.academics.grade_computation import GradeComputationService
from edulafia.modules.academics.repository import AcademicResultRepository
from edulafia.modules.academics.schemas import (
    AcademicResultResponse,
    CAScoreBulkEntry,
    CAScoreEntry,
    ComputeGradesRequest,
)
from edulafia.modules.academics.service import AcademicResultService

router = APIRouter(prefix="/academics", tags=["Academics"])


def get_academic_result_service(db: AsyncSession = Depends(get_db)) -> AcademicResultService:
    """Dependency to get AcademicResultService."""
    repository = AcademicResultRepository(db)
    return AcademicResultService(repository)


from edulafia.modules.academics.models import Class, Term, AcademicYear
from sqlalchemy import select

@router.get("/classes", summary="Get all classes for a school")
async def get_classes(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Get all classes."""
    school_id = UUID(current_user["school_id"])
    stmt = select(Class).where(Class.school_id == school_id).order_by(Class.name)
    result = await db.execute(stmt)
    classes = result.scalars().all()
    return [{"id": str(c.id), "name": c.name} for c in classes]

@router.get(
    "/metadata",
    summary="Get academic metadata",
)
async def get_academic_metadata(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get active academic metadata (Class, Term, AcademicYear) for grade entry."""
    school_id = UUID(current_user["school_id"])
    
    # Year
    year_query = select(AcademicYear).where(
        AcademicYear.school_id == school_id,
        AcademicYear.is_active == True
    ).order_by(AcademicYear.created_at.desc()).limit(1)
    year = (await db.execute(year_query)).scalar_one_or_none()
    
    if not year:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active Academic Year found for this school. Please configure academic settings.",
        )
        
    # Term
    term_query = select(Term).where(
        Term.school_id == school_id,
        Term.academic_year_id == year.id,
        Term.is_active == True
    ).order_by(Term.created_at.desc()).limit(1)
    term = (await db.execute(term_query)).scalar_one_or_none()
    
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active Term found for the current Academic Year.",
        )
        
    # Class (First available class for the teacher/school)
    class_query = select(Class).where(Class.school_id == school_id).order_by(Class.name.asc()).limit(1)
    cls = (await db.execute(class_query)).scalar_one_or_none()
    
    if not cls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No classes found for this school.",
        )
        
    return {
        "academic_year": {"id": str(year.id), "name": year.name},
        "term": {"id": str(term.id), "name": term.name},
        "class": {"id": str(cls.id), "name": cls.name},
    }

@router.post(
    "/grades/compute",
    summary="Compute grades for a class",
)
async def compute_grades(
    data: ComputeGradesRequest,
    current_user: CurrentUser,
    service: AcademicResultService = Depends(get_academic_result_service),
) -> dict:
    """Compute grades for all students in a class for a term."""
    return await service.compute_grades_for_class(
        class_id=data.class_id,
        term_id=data.term_id,
        school_id=UUID(current_user["school_id"])
    )


@router.get(
    "/grades/scales",
    summary="Get grading scales",
)
async def get_grading_scales(
    current_user: CurrentUser,
) -> dict:
    """Get grading scales for the school."""
    rules = GradeComputationService.get_default_grading_rules()
    return {
        "scales": [
            {
                "name": "WAEC Standard",
                "is_default": True,
                "details": rules,
            }
        ]
    }


@router.post(
    "/scores",
    response_model=AcademicResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enter scores for a student",
)
async def enter_scores(
    data: CAScoreEntry,
    current_user: CurrentUser,
    service: AcademicResultService = Depends(get_academic_result_service),
) -> AcademicResultResponse:
    """Enter CA and exam scores for a student."""
    return await service.create_score(
        student_id=data.student_id,
        subject_id=data.subject_id,
        class_id=data.class_id,
        term_id=data.term_id,
        academic_year_id=data.academic_year_id,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
        ca_scores=data.ca_scores,
        exam_score=data.exam_score or Decimal("0"),
        flag=data.flag,
    )


@router.post(
    "/scores/bulk",
    response_model=list[AcademicResultResponse],
    summary="Enter scores for multiple students",
)
async def enter_scores_bulk(
    data: CAScoreBulkEntry,
    current_user: CurrentUser,
    service: AcademicResultService = Depends(get_academic_result_service),
) -> list[AcademicResultResponse]:
    """Enter scores for multiple students at once."""
    score_entries = [
        {
            "student_id": entry.student_id,
            "ca_scores": entry.ca_scores,
            "exam_score": entry.exam_score or Decimal("0"),
            "flag": entry.flag,
        }
        for entry in data.scores
    ]

    return await service.create_scores_bulk(
        subject_id=data.subject_id,
        class_id=data.class_id,
        term_id=data.term_id,
        academic_year_id=data.scores[0].academic_year_id if data.scores else None,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
        score_entries=score_entries,
    )


@router.get(
    "/report-cards/{student_id}/{term_id}",
    summary="Generate report card for student",
)
async def generate_report_card(
    student_id: UUID,
    term_id: UUID,
    current_user: CurrentUser,
    service: AcademicResultService = Depends(get_academic_result_service),
) -> dict:
    """Generate report card for a student for a specific term."""
    return await service.generate_report_card(
        student_id=student_id,
        term_id=term_id,
        school_id=UUID(current_user["school_id"]),
    )

from pydantic import BaseModel
class SendReportCardRequest(BaseModel):
    method: str

@router.post(
    "/report-cards/{student_id}/{term_id}/send",
    summary="Send report card via SMS or WhatsApp",
)
async def send_report_card(
    student_id: UUID,
    term_id: UUID,
    data: SendReportCardRequest,
    current_user: CurrentUser,
    service: AcademicResultService = Depends(get_academic_result_service),
) -> dict:
    """Send report card to student's guardian via specified method."""
    # This is a mock implementation of SMS/WhatsApp sending
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Simulating {data.method} delivery for student {student_id}.")
    
    return {
        "status": "success",
        "message": f"Report card successfully sent via {data.method}"
    }


@router.get(
    "/scores",
    response_model=Page[AcademicResultResponse],
    summary="Get scores for a class and subject",
)
async def get_scores(
    class_id: UUID,
    subject_id: UUID,
    term_id: UUID,
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    service: AcademicResultService = Depends(get_academic_result_service),
) -> dict:
    """Get scores for a class and subject with pagination."""
    return await service.list_scores(
        class_id=class_id,
        subject_id=subject_id,
        term_id=term_id,
        school_id=UUID(current_user["school_id"]),
        page=pag.page,
        per_page=pag.per_page,
    )
