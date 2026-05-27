"""Redis-backed rate limiter middleware."""

import time
from collections.abc import Callable

import logging
from fastapi import HTTPException, Request, status

from edulafia.core.redis_client import get_redis

logger = logging.getLogger(__name__)


class RateLimiter:
    """Sliding window rate limiter using Redis."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_rate_limited(self, key: str) -> bool:
        """Check if the key has exceeded the rate limit.

        Raises:
            ConnectionError: If Redis is unavailable (fail-closed).
        """
        try:
            client = await get_redis()
            now = time.time()
            window_start = now - self.window_seconds

            pipe = client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {str(now): now})
            pipe.zcard(key)
            pipe.expire(key, self.window_seconds)
            results = await pipe.execute()

            request_count = results[2]
            return request_count > self.max_requests
        except Exception as e:
            logger.error(
                "Rate limiter error - rate limiting enabled by default",
                extra={"key": key, "error": str(e)},
            )
            return True


def rate_limit(max_requests: int = 10, window_seconds: int = 60) -> Callable:
    """Factory that returns a FastAPI dependency for rate limiting.

    Usage:
        @router.post("/login")
        async def login(
            data: LoginRequest,
            _rl: None = Depends(rate_limit(max_requests=5, window_seconds=900)),
        ):
            ...
    """
    limiter = RateLimiter(max_requests=max_requests, window_seconds=window_seconds)

    async def check_rate_limit(request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{request.url.path}:{client_ip}"

        try:
            limited = await limiter.is_rate_limited(key)
        except ConnectionError:
            logger.error("Redis unavailable - rate limiting cannot be enforced")
            limited = True

        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

    return check_rate_limit
