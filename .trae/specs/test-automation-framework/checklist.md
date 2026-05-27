# Checklist

- [x] The FastAPI backend uses `pytest`, `pytest-cov`, and `pytest-asyncio` for comprehensive unit and integration testing.
- [x] Backend tests cover edge cases (timezone issues, invalid payloads, missing permissions, webhook desync).
- [x] Backend TDD compliance is met, and a minimum coverage threshold (e.g., >80%) is enforced.
- [x] The web frontend is configured with Playwright for End-to-End (E2E) testing.
- [x] Local test server scripts accurately check port availability and lock ports to prevent collisions during execution.
- [x] E2E tests validate core user flows on desktop browsers (authentication, staff/health/finance dashboards).
- [x] Mobile automation tests (either via Playwright mobile emulation or a native tool like Detox) are implemented to verify touch interactions and responsive layouts.
- [x] A load/stress testing tool (e.g., Locust or k6) is configured and executed against critical backend endpoints.
- [x] Load testing results are documented and bottlenecks identified.
- [x] The test suites can be run locally via simple commands and are ready for CI/CD integration.