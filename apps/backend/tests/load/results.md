# Load Testing Results

## Overview

Stress and load testing were conducted against the EduLafia FastAPI backend using [Locust](https://locust.io/).

## Tested Endpoints

1. **Authentication:** `/api/v1/auth/login`
2. **Intelligence Dashboards:**
   - `/api/v1/intelligence/school/{school_id}/dashboard`
   - `/api/v1/intelligence/sentinel/dashboard`
3. **Report Generation:** `/api/v1/intelligence/reports/generate`
4. **Finance Webhooks (Burst):** `/api/v1/webhooks/paystack`

## Test Configuration

- **Tool:** Locust
- **Simulated Users:** 50 concurrent users
- **Spawn Rate:** 10 users/second
- **Duration:** 30 seconds (baseline run)
- **Host:** `http://localhost:8001`

## Preliminary Findings & Bottlenecks

Based on the initial setup and simulated runs:

- **Authentication (`/login`):** Handles concurrent logins well. Bcrypt password hashing is CPU intensive and might become a bottleneck under extreme load (>500 concurrent logins/sec). Consider adjusting bcrypt work factor or scaling horizontally.
- **Dashboards:** Fast response times for basic aggregations, but complex time-series queries on large datasets may slow down. Indexing on `SchoolKPISnapshot` and `SickBayVisit` tables is crucial.
- **Report Generation:** The `/api/v1/intelligence/reports/generate` endpoint simulates PDF generation. This is typically a blocking or slow process. It should be offloaded to background tasks (e.g., Celery or ARQ) rather than processed synchronously in the request-response cycle to avoid tying up FastAPI workers.
- **Webhooks:** Fast throughput. Handling burst webhooks works smoothly. Validating HMAC signatures has minimal overhead. Database connection pooling handles concurrent transactions efficiently.

## Recommendations

1. **Horizontal Scaling:** Deploy multiple Uvicorn/Gunicorn worker processes to handle CPU-bound tasks like bcrypt and report rendering.
2. **Caching:** Implement Redis caching for dashboard endpoints (School and Sentinel dashboards) to reduce repetitive DB queries.
3. **Async Workers:** Offload report generation (`/reports/generate`) to background workers.
4. **Database Pooling:** Monitor and tune `DATABASE_POOL_SIZE` (currently controlled via `settings.DATABASE_POOL_SIZE`) to handle concurrent webhook bursts without exhausting PostgreSQL connections.

## How to Run

To execute the load tests locally, run:

```bash
./scripts/load_test.sh
```

Or manually:

```bash
cd apps/backend
uv run locust -f tests/load/locustfile.py --host=http://localhost:8001
```
