# Seeding Demo Data

A comprehensive demo data generation script has been added to the root directory to populate your local database before client demos.

This script ensures your dashboards are fully populated with realistic data across multiple modules (Academics, Attendance, Health, Finance, etc.).

## What it Generates:
1. **School & Admin**: Ensures an active school and an `admin@demo.com` user exist.
2. **Academic Year**: Creates the current active `2023/2024` academic year.
3. **Classes**: Generates 6 core classes (`JSS 1` through `SS 3`).
4. **Students**: Generates 50 students with randomized names, genders, dates of birth, and distributes them across the classes.
5. **Attendance Records**: Simulates 30 days of historical daily attendance records for all 50 students (accounting for weekends), generating realistic absence/lateness rates.
6. **Health Records**: Generates 20 historical Sick Bay visits with randomized temperatures and symptoms to populate the Health Dashboard.
7. **Finance**: Creates a baseline active Fee Schedule.

## How to run it:

1. Ensure your `.env` file is loaded with the correct `DATABASE_URL`.
2. From the project root, run the script:

```bash
# If using the standard python environment:
export DATABASE_URL="postgresql+asyncpg://<YOUR_USER>:<YOUR_PASS>@localhost:5432/edulafia"
python3 generate_demo_data.py
```

*Note: The script uses raw parameterized SQL via SQLAlchemy, ensuring it maps perfectly to the database schema without needing complex ORM setups.*
