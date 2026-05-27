# EduLafia Platform - Development Setup Guide

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. Prerequisites

### 1.1 System Requirements
- **Operating System**: macOS 12+, Ubuntu 20.04+, Windows 10+ (WSL2 recommended)
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 20GB free space
- **Internet**: Required for initial setup and package downloads

### 1.2 Software Requirements
- **Python**: 3.11 or higher
- **Node.js**: 18 LTS or higher
- **PostgreSQL**: 15 or higher
- **Redis**: 7 or higher
- **Docker**: 20.10 or higher (optional but recommended)
- **Git**: 2.30 or higher

### 1.3 Accounts Required
- GitHub account (for repository access)
- AWS account (for production deployment)
- Termii account (for SMS integration)
- Paystack account (for payment integration)

## 2. Repository Setup

### 2.1 Clone Repository
```bash
# Clone the main repository
git clone https://github.com/lafiyacore/edulafia.git
cd edulafia

# Initialize submodules
git submodule update --init --recursive
```

### 2.2 Project Structure
```
edulafia/
├── backend/               # Python FastAPI backend
│   ├── app/              # Application code
│   ├── tests/            # Test files
│   ├── alembic/          # Database migrations
│   ├── pyproject.toml    # Python dependencies
│   └── Dockerfile        # Backend Docker configuration
├── frontend/             # React PWA frontend
│   ├── src/              # Source code
│   ├── public/           # Static files
│   ├── package.json      # Node dependencies
│   └── Dockerfile        # Frontend Docker configuration
├── docs/                 # Documentation
├── docker-compose.yml    # Development environment
├── .env.example         # Environment variables template
└── README.md            # Project README
```

## 3. Backend Setup

### 3.1 Python Environment
```bash
# Install Python 3.11 (if not installed)
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# On macOS with Homebrew:
brew install python@3.11

# Install Poetry (Python package manager)
curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to use .venv in project directory
poetry config virtualenvs.in-project true
```

### 3.2 Backend Dependencies
```bash
cd backend

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell

# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install
```

### 3.3 Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

**Required Environment Variables:**
```env
# Database
DATABASE_URL=postgresql://edulafia:password@localhost:5432/edulafia
DATABASE_TEST_URL=postgresql://edulafia:password@localhost:5432/edulafia_test

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# External Services
TERMII_API_KEY=your-termii-api-key
TERMII_SENDER_ID=EduLafia
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# App Configuration
APP_NAME=EduLafia
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Email (for development)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
EMAILS_FROM_EMAIL=noreply@edulafia.ng
```

### 3.4 Database Setup
```bash
# Install PostgreSQL (if not installed)
# On Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib

# On macOS with Homebrew:
brew install postgresql@15

# Start PostgreSQL service
# Ubuntu/Debian:
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS:
brew services start postgresql@15

# Create database user
sudo -u postgres psql -c "CREATE USER edulafia WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER USER edulafia CREATEDB;"

# Create databases
sudo -u postgres psql -c "CREATE DATABASE edulafia OWNER edulafia;"
sudo -u postgres psql -c "CREATE DATABASE edulafia_test OWNER edulafia;"

# Enable extensions
sudo -u postgres psql -d edulafia -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
sudo -u postgres psql -d edulafia -c "CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";"
```

### 3.5 Redis Setup
```bash
# Install Redis (if not installed)
# On Ubuntu/Debian:
sudo apt install redis-server

# On macOS with Homebrew:
brew install redis

# Start Redis service
# Ubuntu/Debian:
sudo systemctl start redis
sudo systemctl enable redis

# macOS:
brew services start redis

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### 3.6 Database Migrations
```bash
# Run migrations
cd backend
poetry run alembic upgrade head

# Create new migration (when models change)
poetry run alembic revision --autogenerate -m "Description of changes"

# Apply new migration
poetry run alembic upgrade head

# Downgrade migration
poetry run alembic downgrade -1
```

### 3.7 Initial Data Setup
```bash
# Load initial data (roles, grading scales, etc.)
poetry run python scripts/load_initial_data.py

# Create super admin user
poetry run python scripts/create_admin.py \
    --email admin@edulafia.ng \
    --password admin123 \
    --first-name "System" \
    --last-name "Administrator"
```

### 3.8 Run Backend Server
```bash
# Start development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the make command
make run-backend

# Server will be available at:
# - API: http://localhost:8000/api/v1
# - Documentation: http://localhost:8000/docs
# - Alternative docs: http://localhost:8000/redoc
```

## 4. Frontend Setup

### 4.1 Node.js Environment
```bash
# Install Node.js 18 LTS (if not installed)
# Using nvm (recommended):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Verify installation
node --version  # Should be 18.x.x
npm --version   # Should be 9.x.x
```

### 4.2 Frontend Dependencies
```bash
cd frontend

# Install dependencies
npm install

# Install global packages (if needed)
npm install -g @vue/cli
```

### 4.3 Environment Configuration
```bash
# Copy environment template
cp .env.example .env.local

# Edit environment file
nano .env.local
```

**Frontend Environment Variables:**
```env
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=30000

# Application Configuration
VITE_APP_NAME=EduLafia
VITE_APP_VERSION=1.0.0
VITE_APP_ENV=development

# Feature Flags
VITE_ENABLE_OFFLINE_MODE=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_ANALYTICS=false

# External Services
VITE_PAYSTACK_PUBLIC_KEY=your-paystack-public-key
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-key (optional)

# PWA Configuration
VITE_PWA_NAME=EduLafia
VITE_PWA_SHORT_NAME=EduLafia
VITE_PWA_THEME_COLOR=#2563eb
VITE_PWA_BACKGROUND_COLOR=#ffffff
```

### 4.4 Run Frontend Development Server
```bash
# Start development server
npm run dev

# Or use the make command
make run-frontend

# Server will be available at:
# - Frontend: http://localhost:3000
# - With hot reload
```

### 4.5 Build for Production
```bash
# Build optimized production version
npm run build

# Preview production build
npm run preview

# Build for specific environment
npm run build -- --mode staging
```

## 5. Docker Setup (Alternative)

### 5.1 Docker Installation
```bash
# Install Docker Desktop (macOS/Windows)
# Or Docker Engine (Linux)

# Verify Docker installation
docker --version
docker-compose --version
```

### 5.2 Development with Docker
```bash
# Start all services
docker-compose up -d

# Start with rebuild
docker-compose up -d --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### 5.3 Docker Services
```yaml
# docker-compose.yml includes:
services:
  postgres:     # PostgreSQL database
  redis:        # Redis cache
  backend:      # FastAPI backend
  frontend:     # React frontend
  celery_worker: # Celery background worker
  celery_beat:  # Celery scheduled tasks
```

### 5.4 Docker Commands
```bash
# Run backend tests in Docker
docker-compose exec backend poetry run pytest

# Run frontend tests in Docker
docker-compose exec frontend npm test

# Access backend shell
docker-compose exec backend poetry shell

# Access database
docker-compose exec postgres psql -U edulafia edulafia

# Access Redis
docker-compose exec redis redis-cli
```

## 6. Testing Setup

### 6.1 Backend Testing
```bash
# Run all tests
cd backend
poetry run pytest

# Run specific test file
poetry run pytest tests/test_students.py

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test
poetry run pytest tests/test_students.py::test_create_student -v

# Run tests matching pattern
poetry run pytest -k "test_student"
```

### 6.2 Frontend Testing
```bash
# Run all tests
cd frontend
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- --testPathPattern=students
```

### 6.3 End-to-End Testing
```bash
# Install Cypress
cd frontend
npm install cypress --save-dev

# Open Cypress UI
npm run cypress:open

# Run headless tests
npm run cypress:run
```

## 7. Development Workflow

### 7.1 Git Workflow
```bash
# Create feature branch
git checkout -b feature/student-management

# Make changes and commit
git add .
git commit -m "feat: add student CRUD operations"

# Push to remote
git push origin feature/student-management

# Create pull request
# (via GitHub UI or GitHub CLI)
```

### 7.2 Commit Message Format
```bash
# Format: <type>(<scope>): <description>

# Examples:
feat(students): add batch import functionality
fix(attendance): resolve date timezone issue
docs(readme): update installation instructions
refactor(api): improve error handling
test(auth): add login integration tests
chore(deps): update dependencies
```

### 7.3 Code Quality Checks
```bash
# Backend
cd backend

# Run linting
poetry run ruff check app/

# Run formatting
poetry run black app/

# Run type checking
poetry run mypy app/

# Run security checks
poetry run bandit -r app/

# All checks in one command
make lint-backend
```

```bash
# Frontend
cd frontend

# Run linting
npm run lint

# Run formatting
npm run format

# Run type checking
npm run type-check

# All checks in one command
make lint-frontend
```

## 8. Database Management

### 8.1 Common Database Commands
```bash
# Connect to database
psql -U edulafia -d edulafia

# List all tables
\dt

# Describe table
\d students

# List users
\du

# Exit
\q
```

### 8.2 Database Backup and Restore
```bash
# Backup database
pg_dump -U edulafia edulafia > backup.sql

# Restore database
psql -U edulafia edulafia < backup.sql

# Backup specific table
pg_dump -U edulafia edulafia -t students > students_backup.sql
```

### 8.3 Database Reset
```bash
# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE edulafia;"
sudo -u postgres psql -c "CREATE DATABASE edulafia OWNER edulafia;"

# Run migrations
cd backend
poetry run alembic upgrade head

# Load initial data
poetry run python scripts/load_initial_data.py
```

## 9. API Development

### 9.1 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 9.2 API Testing
```bash
# Install httpie for API testing
pip install httpie

# Test authentication
http POST http://localhost:8000/api/v1/auth/login email="admin@edulafia.ng" password="admin123"

# Test with token
http GET http://localhost:8000/api/v1/students Authorization:"Bearer <token>"

# Test file upload
http --form POST http://localhost:8000/api/v1/students/batch-import file=@students.csv school_id="uuid"
```

### 9.3 API Versioning
```python
# API version is included in URL: /api/v1/
# When making breaking changes:
# 1. Create new version: /api/v2/
# 2. Maintain backward compatibility in v1
# 3. Deprecate v1 after migration period
```

## 10. Offline Development

### 10.1 Service Worker Development
```bash
# Service worker is in frontend/public/sw.js
# To test offline functionality:

# 1. Build production version
npm run build

# 2. Serve with a local server
npm run preview

# 3. Open DevTools > Application > Service Workers
# 4. Check "Offline" to test offline mode
```

### 10.2 IndexedDB Development
```bash
# Use browser DevTools to inspect IndexedDB
# Application > Storage > IndexedDB

# Database names:
# - edulafia_students
# - edulafia_attendance
# - edulafia_academics
# - edulafia_finance
# - edulafia_health
```

## 11. Monitoring and Debugging

### 11.1 Backend Logging
```bash
# View backend logs
tail -f backend/logs/app.log

# View specific log level
tail -f backend/logs/app.log | grep ERROR

# View Celery logs
tail -f backend/logs/celery.log
```

### 11.2 Frontend Debugging
```bash
# Enable Redux DevTools (if using Redux)
# Install browser extension

# Enable React DevTools
# Install browser extension

# Enable PWA debugging
# Chrome: chrome://serviceworker-internals/
# Firefox: about:debugging#workers
```

### 11.3 Performance Monitoring
```bash
# Backend performance
# Use Django Debug Toolbar equivalent for FastAPI
# Install: pip install fastapi-debugtoolbar

# Frontend performance
# Use Lighthouse in Chrome DevTools
# Run: npm run build && npm run preview
```

## 12. Common Issues and Solutions

### 12.1 Database Connection Issues
```bash
# Error: connection refused
# Solution: Start PostgreSQL service
sudo systemctl start postgresql

# Error: authentication failed
# Solution: Check pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Change: local all edulafia md5
# Then restart: sudo systemctl restart postgresql
```

### 12.2 Port Already in Use
```bash
# Error: Address already in use
# Find process using port
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### 12.3 Permission Issues
```bash
# Error: Permission denied
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x scripts/*.sh

# Fix virtual environment permissions
chmod -R 755 .venv
```

### 12.4 Module Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in virtual environment
poetry shell

# Or install missing package
poetry add package-name

# For frontend:
npm install package-name
```

## 13. Development Makefile

### 13.1 Available Commands
```makefile
# Backend commands
run-backend:      # Run backend development server
test-backend:     # Run backend tests
lint-backend:     # Run backend linting
format-backend:   # Format backend code

# Frontend commands
run-frontend:     # Run frontend development server
test-frontend:    # Run frontend tests
lint-frontend:    # Run frontend linting
format-frontend:  # Format frontend code

# Docker commands
docker-up:        # Start all Docker services
docker-down:      # Stop all Docker services
docker-logs:      # View Docker logs

# Database commands
db-migrate:       # Run database migrations
db-reset:         # Reset database
db-backup:        # Backup database

# Utility commands
install:          # Install all dependencies
clean:            # Clean build artifacts
```

### 13.2 Using Make Commands
```bash
# View available commands
make help

# Run specific command
make run-backend
make test-frontend
make docker-up
```

## 14. Next Steps

### 14.1 After Setup
1. Read `07-coding-standards.md` for code style guidelines
2. Review `02-data-model.md` for database schema
3. Check `03-api-specification.md` for API endpoints
4. Start with module specifications in `04-module-specifications/`

### 14.2 Development Order
1. Set up backend API structure
2. Implement authentication system
3. Build core modules (SIS, Attendance, Academics)
4. Implement offline-first functionality
5. Add integrations (SMS, WhatsApp, payments)
6. Build frontend PWA
7. Write tests
8. Deploy to staging

---

*This development setup guide provides everything needed to start developing the EduLafia platform. Follow these steps carefully to ensure a consistent development environment across the team.*

---

**End of Development Setup Guide**