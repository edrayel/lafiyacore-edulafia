cd /Users/edrayel/GitHub/edward_rajah/lafiyacore-edulafia/apps/backend
source .venv/bin/activate
set -a
source ../../.env.local
set +a
uvicorn edulafia.main:app --port 8003 --reload
