"""Data retention API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.data_retention.repository import RetentionPolicyRepository
from edulafia.modules.data_retention.schemas import (
    RetentionPolicyCreate,
    RetentionPolicyResponse,
    RetentionPolicyUpdate,
    DataSubjectRequestCreate,
    DataSubjectRequestResponse,
    ConsentRecordCreate,
    ConsentRecordResponse,
)
from edulafia.modules.data_retention.models import DataSubjectRequest, ConsentRecord
from edulafia.modules.data_retention.service import RetentionPolicyService

router = APIRouter(prefix="/data-retention", tags=["Data Retention"])


def get_retention_service(db: AsyncSession = Depends(get_db)) -> RetentionPolicyService:
    """Dependency to get RetentionPolicyService."""
    repository = RetentionPolicyRepository(db)
    return RetentionPolicyService(repository)


@router.post(
    "",
    response_model=RetentionPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a retention policy",
)
async def create_retention_policy(
    data: RetentionPolicyCreate,
    current_user: CurrentUser,
    service: RetentionPolicyService = Depends(get_retention_service),
) -> RetentionPolicyResponse:
    """Create a new data retention policy."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{policy_id}",
    response_model=RetentionPolicyResponse,
    summary="Get a retention policy by ID",
)
async def get_retention_policy(
    policy_id: UUID,
    current_user: CurrentUser,
    service: RetentionPolicyService = Depends(get_retention_service),
) -> RetentionPolicyResponse:
    """Get a retention policy by ID."""
    policy = await service.get_by_id(policy_id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retention policy not found",
        )
    return policy


@router.get(
    "",
    response_model=list[RetentionPolicyResponse],
    summary="List retention policies",
)
async def list_retention_policies(
    current_user: CurrentUser,
    service: RetentionPolicyService = Depends(get_retention_service),
) -> list[RetentionPolicyResponse]:
    """List all retention policies for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/{policy_id}",
    response_model=RetentionPolicyResponse,
    summary="Update a retention policy",
)
async def update_retention_policy(
    policy_id: UUID,
    data: RetentionPolicyUpdate,
    current_user: CurrentUser,
    service: RetentionPolicyService = Depends(get_retention_service),
) -> RetentionPolicyResponse:
    """Update a retention policy."""
    try:
        return await service.update(
            policy_id=policy_id,
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{policy_id}",
    summary="Delete a retention policy",
)
async def delete_retention_policy(
    policy_id: UUID,
    current_user: CurrentUser,
    service: RetentionPolicyService = Depends(get_retention_service),
) -> dict:
    """Delete a retention policy."""
    policy = await service.get_by_id(policy_id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Retention policy not found",
        )
    await service.delete(policy_id)
    return {"message": "Retention policy deleted"}


@router.post(
    "/dsr",
    response_model=DataSubjectRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a Data Subject Request (NDPA)",
)
async def create_data_subject_request(
    data: DataSubjectRequestCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> DataSubjectRequestResponse:
    """Submit a Data Subject Request (DSR) for access, correction, erasure, or portability."""
    dsr = DataSubjectRequest(
        requester_id=UUID(current_user["sub"]),
        request_type=data.request_type,
        details=data.details,
    )
    db.add(dsr)
    await db.commit()
    await db.refresh(dsr)
    return dsr


@router.post(
    "/consent",
    response_model=ConsentRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record parental consent (NDPA)",
)
async def create_consent_record(
    data: ConsentRecordCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> ConsentRecordResponse:
    """Record a parental consent for processing minors' data."""
    consent = ConsentRecord(
        student_id=data.student_id,
        guardian_id=data.guardian_id,
        consent_type=data.consent_type,
        status=data.status,
    )
    db.add(consent)
    await db.commit()
    await db.refresh(consent)
    return consent
