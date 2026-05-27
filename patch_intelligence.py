import os

file_path = 'apps/backend/src/edulafia/modules/intelligence/service.py'
with open(file_path, 'r') as f:
    content = f.read()

new_imports = """
import json
from edulafia.core.redis_client import redis_client
"""

if 'from edulafia.core.redis_client' not in content:
    content = content.replace('from edulafia.modules.intelligence.repository import IntelligenceRepository', new_imports + '\nfrom edulafia.modules.intelligence.repository import IntelligenceRepository')

old_get = """    async def get_dashboard_metrics(self, school_id: UUID) -> DashboardMetricsResponse:
        \"\"\"Get aggregated metrics for the intelligence dashboard.\"\"\"
        metrics = await self.repository.get_dashboard_metrics(school_id)
        return DashboardMetricsResponse.model_validate(metrics)"""

new_get = """    async def get_dashboard_metrics(self, school_id: UUID) -> DashboardMetricsResponse:
        \"\"\"Get aggregated metrics for the intelligence dashboard with Redis caching.\"\"\"
        cache_key = f"dashboard_metrics:{school_id}"
        
        # Try to get from cache first
        try:
            if redis_client.redis:
                cached_data = await redis_client.redis.get(cache_key)
                if cached_data:
                    import logging
                    logging.getLogger(__name__).info(f"Cache hit for {cache_key}")
                    return DashboardMetricsResponse.model_validate(json.loads(cached_data))
        except Exception:
            pass # Ignore cache read errors
            
        metrics = await self.repository.get_dashboard_metrics(school_id)
        response = DashboardMetricsResponse.model_validate(metrics)
        
        # Save to cache for 15 minutes
        try:
            if redis_client.redis:
                await redis_client.redis.setex(
                    cache_key,
                    900,
                    response.model_dump_json()
                )
        except Exception:
            pass # Ignore cache write errors
            
        return response"""

if 'redis_client.redis.get' not in content:
    content = content.replace(old_get, new_get)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched intelligence caching")
