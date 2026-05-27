#!/bin/bash
set -e

echo "Running Locust Load Test..."
cd "$(dirname "$0")/../apps/backend"
uv run locust -f tests/load/locustfile.py --host=http://localhost:8000 --headless -u 50 -r 10 --run-time 30s --html=tests/load/report.html
echo "Load test complete! Report generated at apps/backend/tests/load/report.html"
