from unittest.mock import AsyncMock
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_enqueue_sentinel_email_enqueues_job(monkeypatch):
    from edulafia.core import arq_queue

    fake_pool = AsyncMock()
    monkeypatch.setattr(arq_queue, "get_arq_pool", AsyncMock(return_value=fake_pool))

    await arq_queue.enqueue_sentinel_email(
        to_email="admin@edulafia.edu.ng",
        subject="subject",
        body="<p>body</p>",
    )

    fake_pool.enqueue_job.assert_awaited_once()
    job_name = fake_pool.enqueue_job.call_args.args[0]
    assert job_name == "send_sentinel_email"


@pytest.mark.asyncio
async def test_enqueue_generate_report_enqueues_job(monkeypatch):
    from edulafia.core import arq_queue

    fake_pool = AsyncMock()
    monkeypatch.setattr(arq_queue, "get_arq_pool", AsyncMock(return_value=fake_pool))

    report_id = uuid4()
    school_id = uuid4()
    request_payload = {"report_type": "attendance", "parameters": {}, "format": "csv"}

    await arq_queue.enqueue_generate_report(
        report_id=report_id,
        report_request=request_payload,
        school_id=school_id,
    )

    fake_pool.enqueue_job.assert_awaited_once()
    job_name = fake_pool.enqueue_job.call_args.args[0]
    assert job_name == "generate_report"
