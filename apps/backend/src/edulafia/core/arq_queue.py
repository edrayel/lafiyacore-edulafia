from __future__ import annotations

from typing import Any
from uuid import UUID

from edulafia.config import settings

_pool = None


async def get_arq_pool():
    global _pool
    if _pool is None:
        from arq import create_pool
        from arq.connections import RedisSettings

        _pool = await create_pool(
            RedisSettings.from_dsn(settings.REDIS_URL),
        )
    return _pool


async def close_arq_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def enqueue_sentinel_email(to_email: str, subject: str, body: str) -> Any:
    pool = await get_arq_pool()
    return await pool.enqueue_job(
        "send_sentinel_email",
        to_email,
        subject,
        body,
    )


async def enqueue_generate_report(
    report_id: UUID,
    report_request: dict[str, Any],
    school_id: UUID,
) -> Any:
    pool = await get_arq_pool()
    return await pool.enqueue_job(
        "generate_report",
        str(report_id),
        report_request,
        str(school_id),
    )

