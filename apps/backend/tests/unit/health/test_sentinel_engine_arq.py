from unittest.mock import AsyncMock
from uuid import uuid4

import pytest


class FakeSignal:
    def __init__(self, alert_tier: str):
        self.id = uuid4()
        self.alert_tier = alert_tier
        self.threshold_type = "school_cluster"


@pytest.mark.asyncio
async def test_sentinel_trigger_alerts_enqueues_email(monkeypatch):
    from edulafia.modules.health.sentinel import SentinelEngine
    from edulafia.core import arq_queue

    enqueue_mock = AsyncMock()
    monkeypatch.setattr(arq_queue, "enqueue_sentinel_email", enqueue_mock)

    engine = SentinelEngine(
        visit_repo=AsyncMock(),
        signal_repo=AsyncMock(),
        config_repo=AsyncMock(),
    )

    # Act
    await engine.trigger_alerts(FakeSignal(alert_tier="school"))

    # Assert
    assert enqueue_mock.await_count == 2

