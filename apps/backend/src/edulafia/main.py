"""FastAPI application factory and lifespan management."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from edulafia.api.v1.router import api_router
from edulafia.config import settings
from edulafia.core.audit import AuditMiddleware
from edulafia.core.https import HTTPSMiddleware
from edulafia.core.logging import setup_logging
from edulafia.core.middleware import RequestLoggingMiddleware
from edulafia.core.redis_client import close_redis
from edulafia.core.security_headers import SecurityHeadersMiddleware
from edulafia.dependencies import CSRFProtectionMiddleware
from edulafia.database import engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown tasks."""
    setup_logging()
    logger.info(
        "EduLafia starting",
        extra={
            "version": settings.APP_VERSION,
            "env": settings.APP_ENV,
            "db_pool_size": settings.DATABASE_POOL_SIZE,
        },
    )
    yield
    await engine.dispose()
    await close_redis()
    logger.info("EduLafia shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Integrated school management and adolescent health surveillance platform",
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.APP_ENV != "production" else None,
        redoc_url="/redoc" if settings.APP_ENV != "production" else None,
        openapi_url="/openapi.json" if settings.APP_ENV != "production" else None,
        lifespan=lifespan,
    )

    # HTTPS enforcement middleware (must be first)
    app.add_middleware(HTTPSMiddleware)

    # Security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        max_age=600,
    )

    # CSRF protection middleware (only for mutating requests)
    app.add_middleware(CSRFProtectionMiddleware)

    # Request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Audit logging middleware
    app.add_middleware(AuditMiddleware)

    # Include API router
    app.include_router(api_router, prefix="/api")

    # Health check endpoints
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.APP_VERSION}

    @app.get("/ready")
    async def readiness_check():
        return {"status": "ready"}

    return app


app = create_app()
