"""Redis connection pool and client."""

import redis.asyncio as aioredis

from edulafia.config import settings

redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get or create Redis connection."""
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None


async def is_blacklisted(jti: str) -> bool:
    """Check if a JWT ID is blacklisted.

    Raises:
        ConnectionError: If Redis is unavailable (fail-closed).
    """
    try:
        redis = await get_redis()
        return await redis.exists(f"blacklist:{jti}") > 0
    except Exception as e:
        logger = __import__("logging").getLogger(__name__)
        logger.error("Redis unavailable in is_blacklisted, rejecting token", extra={"error": str(e)})
        raise ConnectionError("Authentication service unavailable") from e


async def blacklist_token(token_jti: str, ttl: int = 900) -> None:
    """Add a token JTI to the blacklist with TTL."""
    client = await get_redis()
    await client.setex(f"blacklist:{token_jti}", ttl, "1")
