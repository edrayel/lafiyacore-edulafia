FROM python:3.12-slim AS base
RUN pip install --no-cache-dir uv

FROM base AS builder
WORKDIR /app
COPY uv.lock ./uv.lock
COPY apps/backend/pyproject.toml ./pyproject.toml
RUN uv sync --no-dev --no-install-project

FROM base AS runtime
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY apps/backend/src/ src/
COPY apps/backend/alembic/ alembic/
COPY apps/backend/alembic.ini ./
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "edulafia.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
