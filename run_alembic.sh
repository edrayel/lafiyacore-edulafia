cd /Users/edrayel/GitHub/edward_rajah/lafiyacore-edulafia/apps/backend
source .venv/bin/activate
uv run alembic revision --autogenerate -m "Add_Modules"
uv run alembic upgrade head
python seed.py
