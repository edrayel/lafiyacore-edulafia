# EduLafia Platform - Technical Architecture Specification

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. Architecture Overview

### 1.1 System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (PWA)                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    React + TypeScript                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │  Teacher UI │  │  Admin UI   │  │  Parent UI   │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               Offline Storage Layer                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │ IndexedDB   │  │  PouchDB    │  │   Cache      │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS (TLS 1.3)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (API Gateway)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   FastAPI (Python)                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │   Auth      │  │   Routes    │  │  Middleware   │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Business Logic Layer                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │  Modules    │  │  Services   │  │  Validators  │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │ PostgreSQL  │  │    Redis    │  │    Celery    │  │  │
│  │  (Primary)  │  │   (Cache)   │  │  (Tasks)     │  │  │
│  └─────────────┘  └─────────────┘  └──────────────┘  │  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Integration Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  Termii     │  │  Paystack   │  │  WhatsApp    │  │  │
│  │   (SMS)     │  │  (Payments) │  │    API       │  │  │
│  └─────────────┘  └─────────────┘  └──────────────┘  │  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles
1. **Offline-First**: All core functionality works without internet
2. **Security by Design**: NDPA 2023 compliance from the start
3. **Scalability**: Designed for 1,000+ schools
4. **Maintainability**: Clean separation of concerns
5. **Testability**: Comprehensive testing at all layers

## 2. Technology Stack

### 2.1 Backend Technology
```yaml
Framework: Python 3.11+
Web Framework: FastAPI 0.104+
Database ORM: SQLAlchemy 2.0+
Database: PostgreSQL 15+
Cache: Redis 7+
Task Queue: Celery 5.3+
Migration: Alembic 1.12+
Authentication: JWT (PyJWT)
Validation: Pydantic 2.0+
```

### 2.2 Frontend Technology
```yaml
Framework: React 18+
Language: TypeScript 5.0+
Build Tool: Vite 5.0+
State Management: Zustand
Routing: React Router 6
Styling: Tailwind CSS 3.4+
Forms: React Hook Form
HTTP Client: Axios
Offline: PouchDB 9.0+
```

### 2.3 Development Tools
```yaml
Version Control: Git
Package Manager: Poetry (backend), npm (frontend)
Code Formatting: Black (Python), Prettier (TypeScript)
Linting: Ruff (Python), ESLint (TypeScript)
Testing: Pytest (backend), Vitest (frontend), Cypress (E2E)
CI/CD: GitHub Actions
Containerization: Docker, Docker Compose
```

## 3. Backend Architecture

### 3.1 FastAPI Application Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py            # Base model with common fields
│   │   ├── user.py            # User and role models
│   │   ├── school.py          # School-related models
│   │   ├── student.py         # Student models
│   │   ├── academic.py        # Academic models
│   │   ├── attendance.py      # Attendance models
│   │   ├── finance.py         # Finance models
│   │   ├── health.py          # Health models
│   │   └── sentinel.py        # Sentinel surveillance models
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── school.py
│   │   ├── student.py
│   │   ├── academic.py
│   │   ├── attendance.py
│   │   ├── finance.py
│   │   ├── health.py
│   │   └── sentinel.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── users.py      # User management
│   │   │   ├── schools.py    # School management
│   │   │   ├── students.py   # Student management
│   │   │   ├── academics.py  # Academic management
│   │   │   ├── attendance.py # Attendance management
│   │   │   ├── finance.py    # Finance management
│   │   │   ├── health.py     # Health management
│   │   │   ├── sentinel.py   # Sentinel alerts
│   │   │   └── reports.py    # Reporting endpoints
│   │   └── deps.py           # Dependencies
│   ├── core/                 # Core business logic
│   │   ├── __init__.py
│   │   ├── security.py       # Security utilities
│   │   ├── auth.py           # Authentication logic
│   │   ├── rbac.py           # Role-based access control
│   │   ├── audit.py          # Audit logging
│   │   └── utils.py          # Utility functions
│   ├── services/             # Business services
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── academic.py
│   │   ├── attendance.py
│   │   ├── finance.py
│   │   ├── health.py
│   │   ├── sentinel.py
│   │   └── notifications.py
│   ├── integrations/         # External integrations
│   │   ├── __init__.py
│   │   ├── termii.py        # SMS integration
│   │   ├── whatsapp.py      # WhatsApp integration
│   │   ├── paystack.py      # Payment integration
│   │   └── emis.py          # EMIS export
│   └── tasks/               # Celery tasks
│       ├── __init__.py
│       ├── sentinel.py      # Sentinel analysis tasks
│       ├── reports.py       # Report generation tasks
│       └── notifications.py # Notification tasks
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                  # Test files
├── pyproject.toml         # Python dependencies
└── docker-compose.yml     # Development environment
```

### 3.2 Database Design Principles
1. **Normalization**: 3NF for transactional data
2. **Denormalization**: Strategic denormalization for reporting
3. **Indexing**: Composite indexes for common queries
4. **Partitioning**: Time-based partitioning for attendance and fee records
5. **Soft Deletes**: Never delete records, only mark as inactive

### 3.3 API Design Principles
1. **RESTful**: Standard REST conventions
2. **Versioned**: API versioning (v1, v2, etc.)
3. **Paginated**: All list endpoints support pagination
4. **Filterable**: Query parameters for filtering
5. **Sortable**: Sorting support where applicable
6. **Idempotent**: PUT and DELETE operations are idempotent

## 4. Frontend Architecture

### 4.1 PWA Architecture
```typescript
// Service Worker Registration
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => {
      console.log('SW registered:', registration);
    })
    .catch(error => {
      console.log('SW registration failed:', error);
    });
}

// IndexedDB Schema
const dbSchema = {
  students: { keyPath: 'id', indexes: ['schoolId', 'classId'] },
  attendance: { keyPath: 'id', indexes: ['studentId', 'date', 'schoolId'] },
  academics: { keyPath: 'id', indexes: ['studentId', 'termId'] },
  finance: { keyPath: 'id', indexes: ['studentId', 'schoolId'] },
  health: { keyPath: 'id', indexes: ['studentId', 'schoolId'] }
};
```

### 4.2 Offline-First Strategy
1. **Local Storage**: All write operations go to IndexedDB first
2. **Sync Queue**: Operations queued for sync when online
3. **Conflict Resolution**: Last-write-wins for most fields
4. **Background Sync**: Service Worker handles background sync
5. **Sync Status**: Visual indicators for sync status

### 4.3 Component Architecture
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # Shared components
│   │   ├── layout/           # Layout components
│   │   ├── forms/            # Form components
│   │   └── data/             # Data display components
│   ├── pages/                # Page components
│   │   ├── auth/             # Authentication pages
│   │   ├── dashboard/        # Dashboard pages
│   │   ├── students/         # Student management
│   │   ├── academics/        # Academic management
│   │   ├── attendance/       # Attendance management
│   │   ├── finance/          # Finance management
│   │   ├── health/           # Health management
│   │   └── admin/            # Administration pages
│   ├── stores/               # State management
│   ├── hooks/                # Custom hooks
│   ├── services/             # API services
│   ├── utils/                # Utility functions
│   └── types/                # TypeScript types
```

## 5. Data Architecture

### 5.1 Database Schema Design
```sql
-- Example: Student table with audit fields
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id),
    class_id UUID REFERENCES classes(id),
    admission_number VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'graduated', 'withdrawn', 'transferred')),
    nin VARCHAR(11) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_students_school_id ON students(school_id);
CREATE INDEX idx_students_class_id ON students(class_id);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_admission_number ON students(admission_number);
```

### 5.2 Data Partitioning Strategy
```sql
-- Partition attendance by month for performance
CREATE TABLE attendance_records (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL,
    date DATE NOT NULL,
    -- other columns
) PARTITION BY RANGE (date);

-- Create monthly partitions
CREATE TABLE attendance_records_2026_01 
    PARTITION OF attendance_records
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

## 6. Security Architecture

### 6.1 Authentication Flow
```
1. User submits credentials
2. Backend validates credentials
3. Backend generates JWT token (15 min expiry)
4. Backend generates refresh token (7 day expiry)
5. Frontend stores tokens in secure storage
6. Frontend includes JWT in Authorization header
7. Backend validates JWT on each request
8. Frontend refreshes JWT using refresh token
```

### 6.2 Authorization Model
```python
# Role-based access control
ROLES = {
    'super_admin': ['*'],
    'school_admin': ['school:*', 'student:*', 'attendance:*', 'academic:*', 'finance:*', 'health:*'],
    'teacher': ['attendance:mark', 'academic:grade', 'student:read'],
    'nurse': ['health:*', 'student:read', 'attendance:read'],
    'bursar': ['finance:*', 'student:read'],
    'parent': ['student:read:own', 'attendance:read:own', 'academic:read:own'],
    'student': ['student:read:own', 'academic:read:own']
}
```

### 6.3 Data Encryption
```python
# Field-level encryption for sensitive data
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# Usage for sensitive health data
health_profile = {
    'blood_group': encryption_service.encrypt('O+'),
    'genotype': encryption_service.encrypt('AA')
}
```

## 7. Integration Architecture

### 7.1 External Service Integration Pattern
```python
# Generic integration service
class IntegrationService:
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.session = aiohttp.ClientSession()
    
    async def send(self, endpoint: str, data: dict) -> dict:
        async with self.session.post(
            f"{self.config.base_url}/{endpoint}",
            json=data,
            headers=self.config.headers
        ) as response:
            return await response.json()
    
    async def health_check(self) -> bool:
        # Check if service is available
        pass

# Specific integrations
class TermiiService(IntegrationService):
    async def send_sms(self, to: str, message: str) -> dict:
        return await self.send('sms/send', {
            'to': to,
            'message': message,
            'from': self.config.sender_id
        })
```

### 7.2 Webhook Handling
```python
# Payment webhook handler
@app.post("/webhooks/paystack")
async def paystack_webhook(request: Request):
    # Verify webhook signature
    signature = request.headers.get('x-paystack-signature')
    if not verify_signature(signature, await request.body()):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse event
    event = await request.json()
    
    # Process event
    if event['event'] == 'charge.success':
        await process_successful_payment(event['data'])
    
    return {"status": "success"}
```

## 8. Monitoring and Observability

### 8.1 Logging Strategy
```python
# Structured logging
import structlog

logger = structlog.get_logger()

# Usage
logger.info(
    "attendance_marked",
    student_id=student_id,
    class_id=class_id,
    teacher_id=teacher_id,
    status=status
)

# Audit logging
class AuditLogger:
    def log(self, action: str, user_id: str, resource_id: str, details: dict):
        audit_log = AuditLog(
            action=action,
            user_id=user_id,
            resource_id=resource_id,
            details=details,
            ip_address=get_client_ip(),
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
```

### 8.2 Health Checks
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": check_database_connection(),
        "redis": check_redis_connection(),
        "celery": check_celery_connection()
    }
```

## 9. Deployment Architecture

### 9.1 AWS Infrastructure
```yaml
# Docker Compose for development
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: edulafia
      POSTGRES_USER: edulafia
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
  
  celery_worker:
    build: ./backend
    command: celery -A app.tasks worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://edulafia:${DB_PASSWORD}@postgres/edulafia
      REDIS_URL: redis://redis:6379/0
  
  celery_beat:
    build: ./backend
    command: celery -A app.tasks beat --loglevel=info
    environment:
      DATABASE_URL: postgresql://edulafia:${DB_PASSWORD}@postgres/edulafia
      REDIS_URL: redis://redis:6379/0
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://edulafia:${DB_PASSWORD}@postgres/edulafia
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://backend:8000/api/v1

volumes:
  postgres_data:
```

### 9.2 Production Deployment
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edulafia-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: edulafia-backend
  template:
    metadata:
      labels:
        app: edulafia-backend
    spec:
      containers:
      - name: backend
        image: edulafia/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: edulafia-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## 10. Performance Requirements

### 10.1 Backend Performance
- API response time: < 200ms (95th percentile)
- Database query time: < 50ms (95th percentile)
- Concurrent users: 1,000+
- Request throughput: 1,000 requests/second

### 10.2 Frontend Performance
- First Contentful Paint: < 1.5 seconds
- Time to Interactive: < 3 seconds
- Offline load time: < 1 second
- Bundle size: < 500KB gzipped

### 10.3 Database Performance
- Connection pool: 100 connections
- Query optimization: All queries use indexes
- Connection timeout: 30 seconds
- Statement timeout: 60 seconds

## 11. Disaster Recovery

### 11.1 Backup Strategy
- Database backup: Daily full backup, hourly incremental
- Backup retention: 30 days
- Backup location: S3 with cross-region replication
- Recovery time objective: 4 hours
- Recovery point objective: 1 hour

### 11.2 High Availability
- Database: PostgreSQL with streaming replication
- Application: Multiple instances behind load balancer
- Cache: Redis Sentinel for high availability
- File storage: S3 with versioning enabled

## 12. Compliance Requirements

### 12.1 NDPA 2023 Compliance
- Data residency: All data in Nigeria (AWS af-south-1)
- Consent management: Explicit consent for data processing
- Data subject rights: Access, correction, deletion capabilities
- Breach notification: 72-hour notification to NDPC
- Data protection officer: Designated DPO with contact published

### 12.2 Security Standards
- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Authentication: Multi-factor for admin users
- Session management: 30-minute timeout
- Audit logging: All data access logged

---

*This document provides the technical foundation for implementing the EduLafia platform. All implementation decisions should align with this architecture specification.*

---

**End of Technical Architecture**