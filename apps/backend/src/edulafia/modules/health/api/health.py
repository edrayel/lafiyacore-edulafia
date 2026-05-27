"""Health API endpoints."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.health.exceptions import (
    NurseRoleRequiredError,
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
from edulafia.modules.health.service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


def get_health_service(db: AsyncSession = Depends(get_db)) -> HealthService:
    """Dependency to get HealthService."""
    profile_repo = HealthProfileRepository(db)
    visit_repo = SickBayVisitRepository(db)
    screening_repo = HealthScreeningRepository(db)
    referral_repo = ReferralRepository(db)
    vaccination_repo = VaccinationRepository(db)
    return HealthService(profile_repo, visit_repo, screening_repo, referral_repo, vaccination_repo)


# Student Health Profile

@router.get(
    "/students/{student_id}/profile",
    response_model=StudentHealthProfileResponse,
    summary="Get student health profile",
)
async def get_student_health_profile(
    student_id: UUID,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> StudentHealthProfileResponse:
    """Get student health profile with privacy controls."""
    profile = await service.get_student_profile(
        student_id=student_id,
        school_id=UUID(current_user["school_id"]),
        user_role=current_user.get("role", ""),
    )
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health profile not found")
    return profile


@router.post(
    "/students/{student_id}/profile",
    response_model=StudentHealthProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create student health profile",
)
async def create_student_health_profile(
    student_id: UUID,
    data: StudentHealthProfileCreate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> StudentHealthProfileResponse:
    """Create a new student health profile."""
    try:
        return await service.create_student_profile(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch(
    "/students/{student_id}/profile",
    response_model=StudentHealthProfileResponse,
    summary="Update student health profile",
)
async def update_student_health_profile(
    student_id: UUID,
    data: StudentHealthProfileUpdate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> StudentHealthProfileResponse:
    """Update a student health profile."""
    try:
        return await service.update_student_profile(
            student_id=student_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Sick Bay Visits

@router.post(
    "/sick-bay-visits",
    response_model=SickBayVisitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log sick bay visit",
)
async def log_sick_bay_visit(
    data: SickBayVisitCreate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> SickBayVisitResponse:
    """Log a sick bay visit."""
    try:
        return await service.log_sick_bay_visit(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
            user_role=current_user.get("role", ""),
        )
    except NurseRoleRequiredError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get(
    "/sick-bay-visits",
    response_model=dict,
    summary="List sick bay visits",
)
async def list_sick_bay_visits(
    current_user: CurrentUser,
    student_id: UUID | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    service: HealthService = Depends(get_health_service),
) -> dict:
    """List sick bay visits with filters."""
    return await service.list_sick_bay_visits(
        school_id=UUID(current_user["school_id"]),
        student_id=student_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )


# Health Screenings

@router.post(
    "/screenings",
    response_model=HealthScreeningResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Conduct health screening",
)
async def conduct_screening(
    data: HealthScreeningCreate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> HealthScreeningResponse:
    """Conduct a health screening."""
    try:
        return await service.conduct_screening(
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
            user_role=current_user.get("role", ""),
        )
    except NurseRoleRequiredError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post(
    "/screenings/bulk",
    response_model=list[HealthScreeningResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Conduct batch health screenings",
)
async def conduct_batch_screenings(
    data_list: list[HealthScreeningCreate],
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: HealthService = Depends(get_health_service),
) -> list[HealthScreeningResponse]:
    """Conduct health screenings for multiple students in batch mode, rolled back on any failure."""
    try:
        results = []
        for data in data_list:
            result = await service.conduct_screening(
                data=data,
                school_id=UUID(current_user["school_id"]),
                user_id=UUID(current_user["sub"]),
                user_role=current_user.get("role", ""),
            )
            results.append(result)
        await db.commit()
        return results
    except NurseRoleRequiredError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

# Referrals

@router.post(
    "/referrals",
    response_model=ReferralResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create referral",
)
async def create_referral(
    data: ReferralCreate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> ReferralResponse:
    """Create a referral."""
    return await service.create_referral(
        data=data,
        school_id=UUID(current_user["school_id"]),
        user_id=UUID(current_user["sub"]),
    )


@router.get(
    "/referrals",
    response_model=Page[ReferralResponse],
    summary="List referrals",
)
async def list_referrals(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    status: str | None = Query(None),
    student_id: UUID | None = Query(None),
    service: HealthService = Depends(get_health_service),
) -> dict:
    """List referrals with filters."""
    return await service.list_referrals(
        school_id=UUID(current_user["school_id"]),
        status=status,
        student_id=student_id,
        page=pag.page,
        per_page=pag.per_page,
    )


@router.patch(
    "/referrals/{referral_id}",
    response_model=ReferralResponse,
    summary="Update referral",
)
async def update_referral(
    referral_id: UUID,
    data: ReferralUpdate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> ReferralResponse:
    """Update a referral."""
    try:
        return await service.update_referral(
            referral_id=referral_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
        )
    except ReferralNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referral not found")


# Vaccinations

@router.post(
    "/vaccinations",
    response_model=VaccinationRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record vaccination",
)
async def record_vaccination(
    data: VaccinationRecordCreate,
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> VaccinationRecordResponse:
    """Record a vaccination."""
    return await service.record_vaccination(
        data=data,
        school_id=UUID(current_user["school_id"]),
    )


@router.post(
    "/vaccinations/batch-import",
    response_model=dict,
    summary="Batch import vaccinations",
)
async def batch_import_vaccinations(
    records: list[VaccinationRecordCreate],
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> dict:
    """Batch import vaccination records."""
    return await service.batch_import_vaccinations(
        records=records,
        school_id=UUID(current_user["school_id"]),
    )


@router.get(
    "/vaccinations/{student_id}",
    response_model=Page[VaccinationRecordResponse],
    summary="Get vaccination records",
)
async def get_vaccination_records(
    student_id: UUID,
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    service: HealthService = Depends(get_health_service),
) -> dict:
    """Get paginated vaccination records for a student."""
    return await service.get_vaccination_records(
        student_id=student_id,
        school_id=UUID(current_user["school_id"]),
        page=pag.page,
        per_page=pag.per_page,
    )


# Symptom Codes

@router.get(
    "/symptom-codes",
    response_model=list[dict],
    summary="Get symptom codes",
)
async def get_symptom_codes(
    current_user: CurrentUser,
    service: HealthService = Depends(get_health_service),
) -> list[dict]:
    """Get available symptom codes."""
    return await service.get_symptom_codes()
