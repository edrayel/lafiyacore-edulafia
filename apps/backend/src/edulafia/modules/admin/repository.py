from __future__ import annotations
"""Admin repository for data access operations."""

from collections.abc import Sequence
from datetime import timezone, date, datetime
from typing import Any, List
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.admin.models import (
    SchoolTrainingAssignment,
    SentinelThreshold,
    SyncHistory,
    SyncStatus,
    SystemUpdate,
    TrainingResource,
    UsageAnalytics,
)


class SyncStatusRepository:
    """Repository for sync status database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SyncStatus:
        """Create a new sync status."""
        status = SyncStatus(**data)
        self.db.add(status)
        await self.db.flush()
        await self.db.refresh(status)
        return status

    async def get_by_school(self, school_id: UUID) -> List[SyncStatus]:
        """Get all sync statuses for a school."""
        stmt = select(SyncStatus).where(
            SyncStatus.school_id == school_id,
        ).order_by(SyncStatus.last_sync_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_schools_with_issues(self) -> List[SyncStatus]:
        """Get sync statuses with issues."""
        stmt = select(SyncStatus).where(
            SyncStatus.sync_status.in_(["failed", "conflict"]),
        ).order_by(SyncStatus.updated_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_status(self) -> dict:
        """Count sync statuses by status."""
        stmt = select(
            SyncStatus.sync_status,
            func.count().label("count"),
        ).group_by(SyncStatus.sync_status)

        result = await self.db.execute(stmt)
        rows = result.all()

        return {row.sync_status: row.count for row in rows}

    async def update(self, status: SyncStatus, data: dict) -> SyncStatus:
        """Update sync status."""
        for key, value in data.items():
            if value is not None:
                setattr(status, key, value)
        await self.db.flush()
        await self.db.refresh(status)
        return status


class SyncHistoryRepository:
    """Repository for sync history database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SyncHistory:
        """Create a new sync history entry."""
        history = SyncHistory(**data)
        self.db.add(history)
        await self.db.flush()
        await self.db.refresh(history)
        return history

    async def list(
        self,
        school_id: UUID | None = None,
        device_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> tuple[Sequence[SyncHistory], int]:
        """List sync history with filters."""
        stmt = select(SyncHistory)

        if school_id:
            stmt = stmt.where(SyncHistory.school_id == school_id)
        if device_id:
            stmt = stmt.where(SyncHistory.device_id == device_id)
        if start_date:
            stmt = stmt.where(SyncHistory.sync_start >= start_date)
        if end_date:
            stmt = stmt.where(SyncHistory.sync_start <= end_date)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(SyncHistory.created_at.desc())

        result = await self.db.execute(stmt)
        records = result.scalars().all()

        return records, total


class SentinelThresholdRepository:
    """Repository for sentinel threshold database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SentinelThreshold:
        """Create a new threshold."""
        threshold = SentinelThreshold(**data)
        self.db.add(threshold)
        await self.db.flush()
        await self.db.refresh(threshold)
        return threshold

    async def get_by_id(self, threshold_id: UUID) -> SentinelThreshold | None:
        """Get threshold by ID."""
        stmt = select(SentinelThreshold).where(
            SentinelThreshold.id == threshold_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        state: str | None = None,
        lga: str | None = None,
        symptom_category: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[SentinelThreshold], int]:
        """List thresholds with filters and pagination."""
        stmt = select(SentinelThreshold).where(
            SentinelThreshold.is_active == True,
        )

        if state:
            stmt = stmt.where(SentinelThreshold.state == state)
        if lga:
            stmt = stmt.where(SentinelThreshold.lga == lga)
        if symptom_category:
            stmt = stmt.where(SentinelThreshold.symptom_category == symptom_category)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(SentinelThreshold.created_at.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def deactivate(self, threshold_id: UUID) -> SentinelThreshold:
        """Deactivate a threshold."""
        threshold = await self.get_by_id(threshold_id)
        threshold.is_active = False
        threshold.effective_to = date.today()
        await self.db.flush()
        await self.db.refresh(threshold)
        return threshold


class SystemUpdateRepository:
    """Repository for system update database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SystemUpdate:
        """Create a new system update."""
        update = SystemUpdate(**data)
        self.db.add(update)
        await self.db.flush()
        await self.db.refresh(update)
        return update

    async def get_by_id(self, update_id: UUID) -> SystemUpdate | None:
        """Get update by ID."""
        stmt = select(SystemUpdate).where(SystemUpdate.id == update_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        status: str | None = None,
        release_type: str | None = None,
    ) -> List[SystemUpdate]:
        """List updates with filters."""
        stmt = select(SystemUpdate)

        if status:
            stmt = stmt.where(SystemUpdate.status == status)
        if release_type:
            stmt = stmt.where(SystemUpdate.release_type == release_type)

        stmt = stmt.order_by(SystemUpdate.created_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(self, update: SystemUpdate, data: dict) -> SystemUpdate:
        """Update a system update."""
        for key, value in data.items():
            if value is not None:
                setattr(update, key, value)
        await self.db.flush()
        await self.db.refresh(update)
        return update


class TrainingResourceRepository:
    """Repository for training resource database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> TrainingResource:
        """Create a new training resource."""
        resource = TrainingResource(**data)
        self.db.add(resource)
        await self.db.flush()
        await self.db.refresh(resource)
        return resource

    async def get_by_id(self, resource_id: UUID) -> TrainingResource | None:
        """Get resource by ID."""
        stmt = select(TrainingResource).where(
            TrainingResource.id == resource_id,
            TrainingResource.is_active == True,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        category: str | None = None,
        language: str | None = None,
        target_role: str | None = None,
        target_module: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[Sequence[TrainingResource], int]:
        """List training resources with filters and pagination."""
        stmt = select(TrainingResource).where(
            TrainingResource.is_active == True,
        )

        if category:
            stmt = stmt.where(TrainingResource.category == category)
        if language:
            stmt = stmt.where(TrainingResource.language == language)
        if target_role:
            stmt = stmt.where(TrainingResource.target_role == target_role)
        if target_module:
            stmt = stmt.where(TrainingResource.target_module == target_module)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        stmt = stmt.order_by(TrainingResource.created_at.desc())

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        return items, total

    async def assign_to_school(
        self,
        school_id: UUID,
        resource_id: UUID,
        assigned_by: UUID,
        due_date: date | None = None,
    ) -> SchoolTrainingAssignment:
        """Assign a training resource to a school."""
        assignment = SchoolTrainingAssignment(
            school_id=school_id,
            resource_id=resource_id,
            assigned_by=assigned_by,
            assigned_at=datetime.now(timezone.utc),
            due_date=due_date,
            status="assigned",
        )
        self.db.add(assignment)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def get_school_assignments(
        self,
        school_id: UUID,
        status: str | None = None,
    ) -> List[SchoolTrainingAssignment]:
        """Get training assignments for a school."""
        stmt = select(SchoolTrainingAssignment).where(
            SchoolTrainingAssignment.school_id == school_id,
        )

        if status:
            stmt = stmt.where(SchoolTrainingAssignment.status == status)

        stmt = stmt.order_by(SchoolTrainingAssignment.assigned_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class UsageAnalyticsRepository:
    """Repository for usage analytics database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> UsageAnalytics:
        """Create a new analytics entry."""
        analytics = UsageAnalytics(**data)
        self.db.add(analytics)
        await self.db.flush()
        await self.db.refresh(analytics)
        return analytics

    async def get_school_metrics(
        self,
        school_id: UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> List[UsageAnalytics]:
        """Get metrics for a school."""
        stmt = select(UsageAnalytics).where(
            UsageAnalytics.school_id == school_id,
        )

        if start_date:
            stmt = stmt.where(UsageAnalytics.metric_date >= start_date)
        if end_date:
            stmt = stmt.where(UsageAnalytics.metric_date <= end_date)

        stmt = stmt.order_by(UsageAnalytics.metric_date.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def aggregate_platform_metrics(
        self,
        metric_name: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict:
        """Aggregate metrics across all schools."""
        stmt = select(
            func.count(UsageAnalytics.school_id.distinct()).label("school_count"),
            func.sum(UsageAnalytics.metric_value).label("total"),
            func.avg(UsageAnalytics.metric_value).label("average"),
        ).where(
            UsageAnalytics.metric_name == metric_name,
        )

        if start_date:
            stmt = stmt.where(UsageAnalytics.metric_date >= start_date)
        if end_date:
            stmt = stmt.where(UsageAnalytics.metric_date <= end_date)

        result = await self.db.execute(stmt)
        row = result.one()

        return {
            "school_count": row.school_count or 0,
            "total": float(row.total or 0),
            "average": float(row.average or 0),
        }
