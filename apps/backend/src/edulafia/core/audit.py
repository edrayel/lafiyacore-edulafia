import logging
from typing import Any

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from edulafia.database import AsyncSessionLocal
from edulafia.models.audit import AuditLog

audit_logger = logging.getLogger("edulafia.audit")


async def insert_audit_log(
    method: str,
    path: str,
    client_ip: str | None,
    user_id: str | None = None,
    payload: dict[str, Any] | None = None,
    status_code: int | None = None,
) -> None:
    """Insert an audit log asynchronously into the database."""
    async with AsyncSessionLocal() as session:
        log = AuditLog(
            method=method,
            path=path,
            client_ip=client_ip,
            user_id=user_id,
            payload=payload,
            status_code=status_code,
        )
        session.add(log)
        await session.commit()


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        state_changing_methods = {"POST", "PUT", "PATCH", "DELETE"}

        if request.method in state_changing_methods:
            # Note: capturing request body is tricky in middleware because it consumes the stream.
            # For a production grade app, we could either capture it via a custom route class
            # or rely on route-level dependencies. We will just capture method and path for now.
            user_id = getattr(request.state, "user", None)

            task = BackgroundTask(
                insert_audit_log,
                method=request.method,
                path=request.url.path,
                client_ip=request.client.host if request.client else None,
                user_id=user_id,
                payload=None, # Requires stream buffering to capture
                status_code=response.status_code,
            )
            response.background = task

            audit_logger.info(f"Audited {request.method} {request.url.path} from {request.client.host if request.client else 'unknown'}")

        return response
