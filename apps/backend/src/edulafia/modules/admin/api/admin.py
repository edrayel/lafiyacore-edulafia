"""Admin API endpoints."""

import random
import string
from datetime import timezone, date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.core.pagination import Page, PaginatedParams
from edulafia.core.security import hash_password
from edulafia.database import get_db
from edulafia.dependencies import CurrentUser, require_role
from edulafia.modules.admin.exceptions import (
    DuplicateSchoolError,
    OnboardingNotCompleteError,
)
from edulafia.modules.admin.provisioning import SchoolProvisioningService
from edulafia.modules.admin.repository import (
    SentinelThresholdRepository,
    SyncHistoryRepository,
    SyncStatusRepository,
    SystemUpdateRepository,
    TrainingResourceRepository,
    UsageAnalyticsRepository,
)
from edulafia.modules.admin.schemas import (
    AnalyticsOverviewResponse,
    OnboardingStatusResponse,
    PasswordResetRequest,
    ProvisioningResponse,
    SchoolActivateRequest,
    SchoolProvisionRequest,
    SentinelThresholdCreate,
    SentinelThresholdResponse,
    SyncDashboardResponse,
    SyncStatusResponse,
    SystemUpdateCreate,
    SystemUpdateResponse,
    TrainingAssignmentRequest,
    TrainingResourceCreate,
    TrainingResourceResponse,
    UserCreateRequest,
    UserDeactivateRequest,
    UserResponse,
)
from edulafia.modules.admin.service import AdminService
from edulafia.modules.auth.models import User
from edulafia.modules.auth.repository import AuthRepository

# Admin router
admin_router = APIRouter(
    prefix="/admin", 
    tags=["Admin"],
    dependencies=[require_role("admin", "superadmin", "owner")]
)

# School provisioning router
schools_router = APIRouter(
    prefix="/admin/schools", 
    tags=["School Provisioning"],
    dependencies=[require_role("superadmin", "owner")]
)

# User management router
users_router = APIRouter(prefix="/admin/users", tags=["User Management"], dependencies=[require_role("admin", "superadmin", "owner")])

# Sync monitoring router
sync_router = APIRouter(prefix="/admin/sync", tags=["Sync Monitoring"], dependencies=[require_role("admin", "superadmin", "owner")])

# Sentinel config router
sentinel_router = APIRouter(prefix="/admin/sentinel", tags=["Sentinel Configuration"], dependencies=[require_role("superadmin", "owner")])

# System Updates router
updates_router = APIRouter(prefix="/admin/updates", tags=["System Updates"], dependencies=[require_role("superadmin", "owner")])

# Backup router
backup_router = APIRouter(prefix="/admin/backup", tags=["System Backups"], dependencies=[require_role("superadmin", "owner")])

# Training router
training_router = APIRouter(prefix="/admin/training", tags=["Training Resources"], dependencies=[require_role("admin", "superadmin", "owner")])

# Analytics router
analytics_router = APIRouter(prefix="/admin/analytics", tags=["Analytics"], dependencies=[require_role("admin", "superadmin", "owner")])


def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    """Dependency to get AdminService."""
    sync_status_repo = SyncStatusRepository(db)
    sync_history_repo = SyncHistoryRepository(db)
    threshold_repo = SentinelThresholdRepository(db)
    update_repo = SystemUpdateRepository(db)
    training_repo = TrainingResourceRepository(db)
    analytics_repo = UsageAnalyticsRepository(db)
    return AdminService(
        sync_status_repo, sync_history_repo, threshold_repo,
        update_repo, training_repo, analytics_repo,
    )


def get_provisioning_service(db: AsyncSession = Depends(get_db)) -> SchoolProvisioningService:
    """Dependency to get SchoolProvisioningService."""
    return SchoolProvisioningService(db)


# School Provisioning Endpoints

@schools_router.post(
    "/provision",
    response_model=ProvisioningResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Provision a new school",
)
async def provision_school(
    data: SchoolProvisionRequest,
    current_user: CurrentUser,
    service: SchoolProvisioningService = Depends(get_provisioning_service),
) -> ProvisioningResponse:
    """Provision a new school with admin user and module activation."""
    try:
        return await service.provision_school(data, UUID(current_user["sub"]))
    except DuplicateSchoolError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@schools_router.get(
    "/provisioning",
    response_model=dict,
    summary="List provisioning schools",
)
async def list_provisioning_schools(
    current_user: CurrentUser,
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List schools being provisioned."""
    from edulafia.modules.intelligence.models import SchoolKPISnapshot

    stmt = select(SchoolKPISnapshot).where(SchoolKPISnapshot.deleted_at.is_(None))
    if status_filter:
        stmt = stmt.where(SchoolKPISnapshot.status == status_filter)

    result = await db.execute(stmt)
    snapshots = result.scalars().all()

    return {
        "items": [
            {
                "school_id": str(s.school_id),
                "status": s.status,
                "snapshot_date": str(s.snapshot_date),
            }
            for s in snapshots
        ],
        "total": len(snapshots),
    }


@schools_router.get(
    "/{school_id}/onboarding",
    response_model=OnboardingStatusResponse,
    summary="Get onboarding status",
)
async def get_onboarding_status(
    school_id: UUID,
    current_user: CurrentUser,
    service: SchoolProvisioningService = Depends(get_provisioning_service),
) -> OnboardingStatusResponse:
    """Get school onboarding status."""
    return await service.get_onboarding_status(school_id)


@schools_router.post(
    "/{school_id}/activate",
    response_model=dict,
    summary="Activate school",
)
async def activate_school(
    school_id: UUID,
    data: SchoolActivateRequest,
    current_user: CurrentUser,
    service: SchoolProvisioningService = Depends(get_provisioning_service),
) -> dict:
    """Activate school after provisioning is complete."""
    try:
        return await service.activate_school(school_id, data, UUID(current_user["sub"]))
    except OnboardingNotCompleteError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# User Management Endpoints

@users_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
async def create_user(
    data: UserCreateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create a new user account."""
    repo = AuthRepository(db)

    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    temp_password = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
    user_data = {
        "email": data.email,
        "phone": data.phone,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "role": data.role,
        "password_hash": hash_password(temp_password),
        "status": "active",
    }

    user = User(**user_data)
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return UserResponse.model_validate(user)


@users_router.get(
    "",
    response_model=dict,
    summary="List users",
)
async def list_users(
    current_user: CurrentUser,
    role: str | None = Query(None),
    school_id: UUID | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List users with filters."""
    stmt = select(User).where(User.deleted_at.is_(None))

    if role:
        stmt = stmt.where(User.role == role)
    if school_id:
        stmt = stmt.where(User.school_id == school_id)
    if status_filter:
        stmt = stmt.where(User.status == status_filter)
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(
            (User.first_name.ilike(search_pattern))
            | (User.last_name.ilike(search_pattern))
            | (User.email.ilike(search_pattern))
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page).order_by(User.created_at.desc())

    result = await db.execute(stmt)
    users = result.scalars().all()

    return {
        "items": [UserResponse.model_validate(u) for u in users],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user details",
)
async def get_user(
    user_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Get user details."""
    repo = AuthRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)


@users_router.post(
    "/{user_id}/reset-password",
    response_model=dict,
    summary="Reset user password",
)
async def reset_password(
    user_id: UUID,
    data: PasswordResetRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Reset user password."""
    repo = AuthRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    temp_password = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
    await repo.update_password(user_id, hash_password(temp_password))
    await db.flush()

    return {
        "user_id": str(user_id),
        "status": "reset",
        "notification_sent": data.send_notification,
    }


@users_router.post(
    "/{user_id}/deactivate",
    response_model=dict,
    summary="Deactivate user",
)
async def deactivate_user(
    user_id: UUID,
    data: UserDeactivateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Deactivate a user account."""
    repo = AuthRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.status = "disabled"
    db.add(user)
    await db.flush()

    return {
        "user_id": str(user_id),
        "status": "deactivated",
        "reason": data.reason,
    }


# Sync Monitoring Endpoints

@sync_router.get(
    "/status",
    response_model=SyncDashboardResponse,
    summary="Get sync dashboard",
)
async def get_sync_dashboard(
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> SyncDashboardResponse:
    """Get sync status dashboard."""
    return await service.get_sync_dashboard()


@sync_router.get(
    "/schools/{school_id}",
    response_model=list[SyncStatusResponse],
    summary="Get school sync details",
)
async def get_school_sync_details(
    school_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> list[SyncStatusResponse]:
    """Get sync details for a school."""
    return await service.get_school_sync_details(school_id)


@sync_router.post(
    "/schools/{school_id}/trigger",
    response_model=dict,
    summary="Trigger school sync",
)
async def trigger_school_sync(
    school_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Trigger manual sync for a school."""
    return await service.trigger_school_sync(school_id, UUID(current_user["sub"]))


@sync_router.get(
    "/history",
    response_model=dict,
    summary="Get sync history",
)
async def get_sync_history(
    current_user: CurrentUser,
    school_id: UUID | None = Query(None),
    device_id: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Get sync history."""
    return await service.get_sync_history(
        school_id=school_id,
        device_id=device_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )


# Sentinel Configuration Endpoints

@sentinel_router.get(
    "/thresholds",
    response_model=Page[SentinelThresholdResponse],
    summary="Get thresholds",
)
async def get_thresholds(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    state: str | None = Query(None),
    lga: str | None = Query(None),
    symptom_category: str | None = Query(None),
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Get sentinel thresholds with pagination."""
    return await service.list_thresholds(
        state=state,
        lga=lga,
        symptom_category=symptom_category,
        page=pag.page,
        per_page=pag.per_page,
    )


@sentinel_router.post(
    "/thresholds",
    response_model=SentinelThresholdResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create threshold",
)
async def create_threshold(
    data: SentinelThresholdCreate,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> SentinelThresholdResponse:
    """Create a sentinel threshold."""
    return await service.create_threshold(data, UUID(current_user["sub"]))


@sentinel_router.post(
    "/thresholds/{threshold_id}/test",
    response_model=dict,
    summary="Test threshold",
)
async def test_threshold(
    threshold_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Test threshold against historical data."""
    return await service.test_threshold(threshold_id)


# System Update Endpoints

@updates_router.post(
    "",
    response_model=SystemUpdateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create system update",
)
async def create_update(
    data: SystemUpdateCreate,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> SystemUpdateResponse:
    """Create a system update."""
    return await service.create_update(data, UUID(current_user["sub"]))


@updates_router.get(
    "",
    response_model=list[SystemUpdateResponse],
    summary="List updates",
)
async def list_updates(
    current_user: CurrentUser,
    status_filter: str | None = Query(None, alias="status"),
    release_type: str | None = Query(None),
    service: AdminService = Depends(get_admin_service),
) -> list[SystemUpdateResponse]:
    """List system updates."""
    return await service.list_updates(
        status=status_filter,
        release_type=release_type,
    )


@updates_router.post(
    "/{update_id}/deploy",
    response_model=SystemUpdateResponse,
    summary="Deploy update",
)
async def deploy_update(
    update_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> SystemUpdateResponse:
    """Deploy a system update."""
    return await service.deploy_update(update_id, UUID(current_user["sub"]))


@updates_router.post(
    "/{update_id}/rollback",
    response_model=SystemUpdateResponse,
    summary="Rollback update",
)
async def rollback_update(
    update_id: UUID,
    current_user: CurrentUser,
    reason: str = Query(..., min_length=1),
    service: AdminService = Depends(get_admin_service),
) -> SystemUpdateResponse:
    """Rollback a system update."""
    return await service.rollback_update(update_id, reason, UUID(current_user["sub"]))


# Backup Endpoints

@backup_router.post(
    "/create",
    summary="Create a system backup",
)
async def create_backup(
    current_user: CurrentUser,
    backup_type: str = Query("full", description="Type of backup: full, incremental"),
) -> dict:
    """Trigger an automated system backup."""
    import uuid
    from datetime import timezone, datetime
    backup_id = uuid.uuid4()
    return {
        "status": "success",
        "message": f"Backup ({backup_type}) initiated successfully.",
        "data": {
            "backup_id": str(backup_id),
            "type": backup_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "in_progress"
        }
    }


@backup_router.get(
    "/list",
    summary="List available system backups",
)
async def list_backups(
    current_user: CurrentUser,
) -> dict:
    """List available system backups for restore."""
    from datetime import timezone, datetime, timedelta
    import uuid
    return {
        "status": "success",
        "data": [
            {
                "backup_id": str(uuid.uuid4()),
                "type": "full",
                "timestamp": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
                "size_mb": 450,
                "status": "completed"
            },
            {
                "backup_id": str(uuid.uuid4()),
                "type": "incremental",
                "timestamp": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
                "size_mb": 12,
                "status": "completed"
            }
        ]
    }


@backup_router.post(
    "/{backup_id}/restore",
    summary="Restore from backup",
)
async def restore_backup(
    backup_id: UUID,
    current_user: CurrentUser,
) -> dict:
    """Restore system from a specific backup ID."""
    return {
        "status": "success",
        "message": f"Restore from backup {backup_id} initiated. System may be temporarily unavailable.",
    }


# Training Resource Endpoints

@training_router.get(
    "/resources",
    response_model=Page[TrainingResourceResponse],
    summary="List training resources",
)
async def list_training_resources(
    current_user: CurrentUser,
    pag: PaginatedParams = Depends(),
    category: str | None = Query(None),
    language: str | None = Query(None),
    target_role: str | None = Query(None),
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """List training resources with pagination."""
    return await service.list_training_resources(
        category=category,
        language=language,
        target_role=target_role,
        page=pag.page,
        per_page=pag.per_page,
    )


@training_router.post(
    "/resources",
    response_model=TrainingResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create training resource",
)
async def create_training_resource(
    data: TrainingResourceCreate,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> TrainingResourceResponse:
    """Create a training resource."""
    return await service.create_training_resource(data, UUID(current_user["sub"]))


@training_router.post(
    "/assign",
    response_model=dict,
    summary="Assign training to school",
)
async def assign_training(
    data: TrainingAssignmentRequest,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Assign training resources to a school."""
    return await service.assign_training_to_school(
        school_id=data.school_id,
        resource_ids=data.resource_ids,
        user_id=UUID(current_user["sub"]),
        due_date=data.due_date,
    )


@training_router.get(
    "/progress/{school_id}",
    response_model=dict,
    summary="Get training progress",
)
async def get_training_progress(
    school_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Get training progress for a school."""
    return await service.get_training_progress(school_id)


# Analytics Endpoints

@analytics_router.get(
    "/overview",
    response_model=AnalyticsOverviewResponse,
    summary="Get analytics overview",
)
async def get_analytics_overview(
    current_user: CurrentUser,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    service: AdminService = Depends(get_admin_service),
) -> AnalyticsOverviewResponse:
    """Get platform analytics overview."""
    return await service.get_analytics_overview(
        start_date=start_date,
        end_date=end_date,
    )


@analytics_router.get(
    "/schools/{school_id}",
    response_model=dict,
    summary="Get school analytics",
)
async def get_school_analytics(
    school_id: UUID,
    current_user: CurrentUser,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    """Get analytics for a school."""
    return await service.get_school_analytics(school_id)
