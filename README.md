# EduLafia

Integrated school management and adolescent health surveillance platform for Nigerian secondary schools.

## Overview

EduLafia is a fully feature-complete, offline-first, WhatsApp-native school management platform with integrated health surveillance (LafiyaSentinel). It is NDPA 2023 compliant, highly accessible, and specifically engineered for low-bandwidth Nigerian school environments.

### 🌟 Key Features & Latest Updates
- **Enterprise UI/UX:** Custom Material-UI (MUI) theming featuring fluid typography, fully responsive layouts, and a dedicated **High-Contrast accessibility mode**.
- **100% PWA Installable:** Passes all Chromium installability requirements with valid manifests, auto-updating service workers, and optimized offline icons.
- **Offline-First Resiliency:** Combines **Workbox Background Sync** (for queuing failed API mutations up to 24 hours) and **PouchDB** (for local-to-remote CouchDB synchronization).
- **Production-Ready Backend:** Real PostgreSQL database aggregations for analytics, asynchronous SMTP email delivery, live Sentinel health outbreak alerts, and physical report file generation.
- **Performance Tuned:** Containerized with an Nginx reverse-proxy optimized with Gzip compression, strict Cache-Control for static assets, and manual JS chunking to ensure rapid loading.
- **Demo Ready:** Includes a comprehensive automated database seeding script to instantly populate the platform with realistic schools, students, classes, attendance records, and financial data.

## Core Modules Completed (100% PRD v2.0 Compliant)

1. **Student Information System (SIS):** Digital profiles, bulk CSV onboarding, document management (CVs, IDs), transfer-out packaging, and NIN validation.
2. **Academics & Grading:** Subject management, exam/CA entry, automated class ranking, PDF report card generation, WhatsApp/SMS delivery integration, and WAEC/NECO configurations.
3. **Attendance Tracking:** Daily registers, bulk attendance marking, LafiyaSentinel symptom capture for absences, automated 3-day absence alerts, and EMIS termly exports.
4. **Finance & Fee Management:** Fee schedules, online gateway integration (Paystack/Flutterwave), receipt generation, debt reporting, and transaction reversal audit trails.
5. **Health & Sentinel Engine:** Sick bay visit logging, vaccination records, mental health screening (PHQ-A, SDQ), batch-mode assessments, offline-first health data sync, and live outbreak heatmaps.
6. **Staff Management:** HR document uploads, class/subject assignments, timetable conflict detection, daily staff attendance, and internal broadcasting.
7. **Parent & Guardian Portal:** Real-time dashboards, absence excusal forms, online fee payments, downloadable report cards, and direct staff messaging.
8. **Intelligence & Analytics:** Real-time KPI dashboards, automated report generation, EMIS real-time push/sync, and anonymised data portal for researchers and donors.
9. **System Administration:** Automated user/school provisioning, offline sync monitoring, backup/restore interfaces, system updates deployment, and onboarding training libraries.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic |
| Frontend | React 19, TypeScript 5.5, Vite, Material-UI (MUI), TanStack Query & Router |
| Database | PostgreSQL 16, Redis, CouchDB (sync) |
| PWA | Workbox, vite-plugin-pwa, PouchDB |
| Monorepo | pnpm, Turborepo, Bun (optimized execution) |
| Testing | Vitest (Unit/Integration), Playwright (E2E) |

## Getting Started

### Prerequisites

- Node.js >= 20.0.0
- pnpm >= 9.0.0 (or Bun for memory-optimized execution)
- Python >= 3.12
- uv (Python package manager)
- PostgreSQL 16
- Redis 7
- Docker & Docker Compose (for production/demo deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/lafiyacore/edulafia.git
cd edulafia

# Install Node dependencies
corepack enable
pnpm install

# Install Python dependencies
cd apps/backend
uv sync
cd ../..

# Copy environment variables
cp .env.example .env
# Edit .env with your PostgreSQL, SMTP, and CouchDB configurations
```

### 🚀 Preparing for a Demo (Database Seeding)
To populate the application with a comprehensive, realistic dataset (50 students, 6 classes, 30 days of attendance, health records, and fee schedules) for client demonstrations:

```bash
# Set your local database URL
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/edulafia"

# Run the seeding script
python3 generate_demo_data.py
```
*See [README.seed.md](README.seed.md) for more details.*

### Development

```bash
# Run all apps
pnpm dev

# Run backend only
pnpm dev:backend    # http://localhost:8000

# Run frontend only
pnpm dev:frontend   # http://localhost:5173

# Run tests (Unit & E2E)
bun run test:unit --cwd apps/frontend
npx playwright test --cwd apps/frontend/e2e

# Run linting and type-checking (Optimized with Bun)
bun run lint --cwd apps/frontend
bun run type-check --cwd apps/frontend
```

## Project Structure

```
edulafia/
├── apps/
│   ├── backend/       # FastAPI Python service (35+ Modules)
│   └── frontend/      # React PWA (MUI, Offline-First)
├── packages/          # Shared packages
├── docs/              # Documentation
├── .github/           # CI/CD workflows
├── generate_demo_data.py # Automated database seeder
└── docker-compose.yml # Full-stack orchestration
```

## Documentation

See the `docs/` directory for comprehensive documentation:

- [Project Overview](docs/00-project-overview.md)
- [Technical Architecture](docs/01-technical-architecture.md)
- [Data Model](docs/02-data-model.md)
- [API Specification](docs/03-api-specification.md)
- [Module Specifications](docs/module-specifications/)
- [Testing Strategy](docs/10-testing-strategy.md)
- [Deployment Guide](docs/11-deployment-guide.md)

## License

Proprietary - LafiyaCore Ltd. RC 9347000
