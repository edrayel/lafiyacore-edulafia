"""Sentinel API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.health.repository import (
    SentinelConfigurationRepository,
    SentinelSignalRepository,
    SickBayVisitRepository,
)
from edulafia.modules.health.schemas import (
    SentinelAlertAcknowledge,
    SentinelConfigCreate,
    SentinelConfigResponse,
    SentinelSignalResponse,
)
from edulafia.modules.health.sentinel import SentinelEngine

router = APIRouter(prefix="/sentinel", tags=["Sentinel"])


def get_sentinel_engine(db: AsyncSession = Depends(get_db)) -> SentinelEngine:
    """Dependency to get SentinelEngine."""
    visit_repo = SickBayVisitRepository(db)
    signal_repo = SentinelSignalRepository(db)
    config_repo = SentinelConfigurationRepository(db)
    return SentinelEngine(visit_repo, signal_repo, config_repo)


@router.get(
    "/alerts",
    response_model=list[SentinelSignalResponse],
    summary="Get Sentinel alerts",
)
async def get_sentinel_alerts(
    current_user: CurrentUser,
    status_filter: str | None = Query(None, alias="status"),
    alert_tier: str | None = Query(None),
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> list[SentinelSignalResponse]:
    """Get Sentinel alerts with filters."""
    signals = await engine.signal_repo.list(
        school_id=UUID(current_user.get("school_id")) if current_user.get("school_id") else None,
        status=status_filter,
        alert_tier=alert_tier,
    )
    return [SentinelSignalResponse.model_validate(s) for s in signals]


@router.patch(
    "/alerts/{signal_id}/acknowledge",
    response_model=SentinelSignalResponse,
    summary="Acknowledge alert",
)
async def acknowledge_alert(
    signal_id: UUID,
    data: SentinelAlertAcknowledge,
    current_user: CurrentUser,
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> SentinelSignalResponse:
    """Acknowledge a Sentinel alert."""
    signal = await engine.signal_repo.acknowledge(
        signal_id=signal_id,
        user_id=UUID(current_user["sub"]),
        notes=data.response_notes,
    )
    return SentinelSignalResponse.model_validate(signal)


@router.get(
    "/dashboard",
    response_model=dict,
    summary="Get Sentinel dashboard",
)
async def get_sentinel_dashboard(
    current_user: CurrentUser,
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> dict:
    """Get Sentinel dashboard data."""
    return await engine.get_dashboard_data(
        school_id=UUID(current_user.get("school_id")) if current_user.get("school_id") else None,
    )


@router.post(
    "/analyze",
    response_model=dict,
    summary="Run Sentinel analysis",
)
async def run_sentinel_analysis(
    current_user: CurrentUser,
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> dict:
    """Run Sentinel analysis for current school."""
    school_id = UUID(current_user.get("school_id")) if current_user.get("school_id") else None
    if not school_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="School ID required")

    signals = await engine.analyze_school_signals(school_id=school_id)

    return {
        "message": f"Analysis complete, {len(signals)} signals detected",
        "signals": signals,
    }


@router.post(
    "/config",
    response_model=SentinelConfigResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Sentinel configuration",
)
async def create_sentinel_config(
    data: SentinelConfigCreate,
    current_user: CurrentUser,
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> SentinelConfigResponse:
    """Create a Sentinel configuration."""
    config_data = data.model_dump()
    config_data["school_id"] = data.school_id or UUID(current_user.get("school_id"))

    config = await engine.config_repo.create(config_data)
    return SentinelConfigResponse.model_validate(config)


@router.get(
    "/config",
    response_model=list[SentinelConfigResponse],
    summary="Get Sentinel configurations",
)
async def get_sentinel_configs(
    current_user: CurrentUser,
    engine: SentinelEngine = Depends(get_sentinel_engine),
) -> list[SentinelConfigResponse]:
    """Get Sentinel configurations."""
    school_id = UUID(current_user.get("school_id")) if current_user.get("school_id") else None
    configs = await engine.config_repo.list(school_id=school_id)
    return [SentinelConfigResponse.model_validate(c) for c in configs]
