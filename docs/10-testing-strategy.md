# EduLafia Testing Strategy

## Document Information

- **Version**: 1.1.0
- **Last Updated**: 2026-03-26
- **Status**: Draft
- **Development Style**: Test-First / TDD (Specification-Driven Development)
- **Purpose**: Define testing approach, frameworks, and standards for ensuring EduLafia quality and reliability. Tests serve as the primary specification for LLM code generation.

---

## Table of Contents

1. [Testing Overview](#1-testing-overview)
2. [TDD Workflow for LLM Code Generation](#2-tdd-workflow-for-llm-code-generation)
3. [Testing Pyramid](#3-testing-pyramid)
4. [Backend Testing (Python FastAPI)](#4-backend-testing-python-fastapi)
5. [Frontend Testing (React)](#5-frontend-testing-react)
6. [Integration Testing](#6-integration-testing)
7. [End-to-End Testing](#7-end-to-end-testing)
8. [Offline Sync Testing](#8-offline-sync-testing)
9. [Performance Testing](#9-performance-testing)
10. [Security Testing](#10-security-testing)
11. [Accessibility Testing](#11-accessibility-testing)
12. [Test Data Management](#12-test-data-management)
13. [CI/CD Integration](#13-cicd-integration)
14. [Coverage Requirements](#14-coverage-requirements)
15. [Implementation Checklists](#15-implementation-checklists)

---

## 1. Testing Overview

### 1.1 Development Style: Test-First / TDD

This project uses **Test-Driven Development (TDD)** as the primary development approach. This is especially important because **LLM code agents generate more accurate code when tests serve as specifications**.

#### Why TDD for LLM Code Generation

| Factor | Test-First (TDD) | Test-After |
|--------|------------------|------------|
| **LLM accuracy** | Higher - tests define exact behavior | Lower - implementation already exists |
| **Specification clarity** | Tests ARE the specification | Tests validate existing code |
| **Reduces hallucination** | Test failures catch wrong code immediately | Tests written to match existing (potentially buggy) code |
| **Iterative feedback** | LLM gets clear pass/fail per step | All-or-nothing validation |
| **Natural prompting** | "Make these tests pass" is unambiguous | "Build this feature" is open to interpretation |

#### TDD Workflow for EduLafia

```
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: Module Specification                                    │
│  Business rules, acceptance criteria, API contracts              │
│  (in docs/module-specifications/04-XX-*.md)                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 2: Write Tests FIRST                                       │
│  - Unit tests define expected behavior                           │
│  - Integration tests define API contracts                        │
│  - E2E tests define user workflows                               │
│  Tests are RED (failing) at this stage                           │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 3: LLM Generates Implementation                            │
│  Prompt: "Write code to make these tests pass"                   │
│  LLM writes service, router, model code                          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────┬─────────────────────────────────────┐
│  STEP 4: Validate          │                                     │
│  Run tests                 │                                     │
│  All pass? → Done ✅        │  Any fail? → Revise ❌               │
│                            │  (LLM analyzes failure, fixes code) │
└────────────────────────────┴─────────────────────────────────────┘
```

### 1.2 Testing Principles

| Principle | Description |
|-----------|-------------|
| **Test First** | Write tests BEFORE implementation. Tests are the specification. |
| **Test Often** | Run tests on every commit via CI |
| **Test Isolated** | Each test is independent, no shared state |
| **Test Realistic** | Use realistic data reflecting Nigerian school context |
| **Test Deterministic** | Same input always produces same result |
| **Acceptance → Tests** | Each acceptance criterion in module specs maps to a test case |

### 1.3 Test Categories

| Category | Scope | Frequency | Owner |
|----------|-------|-----------|-------|
| Unit Tests | Individual functions/classes | Every commit | Developer |
| Integration Tests | Component interactions | Every commit | Developer |
| E2E Tests | Full user workflows | Every PR | QA + Developer |
| Performance Tests | Load and stress | Weekly | DevOps |
| Security Tests | Vulnerability scanning | Weekly | Security |
| Offline Tests | Sync and offline behavior | Every PR | Developer |

---

## 2. TDD Workflow for LLM Code Generation

### 2.1 How Tests Drive Implementation

In this project, **tests are written first** and serve as the executable specification. The LLM code agent uses tests as the primary source of truth for what to build.

#### Test-First Development Flow

```
Module Spec (04-XX-*.md)
    │
    │  Extract acceptance criteria
    ▼
Test File (test_*.py / *.test.tsx)
    │
    │  Write failing tests that define:
    │  - Input/output expectations
    │  - Error handling behavior
    │  - Edge cases
    │  - Business rule validation
    ▼
Implementation (service.py / Component.tsx)
    │
    │  LLM generates code to satisfy tests
    ▼
Validation (pytest / vitest)
    │
    ├── All pass → Feature complete ✅
    └── Some fail → LLM revises and retries 🔄
```

### 2.2 Acceptance Criteria to Test Mapping

Each acceptance criterion in the module specifications maps directly to test cases:

| Module Spec Section | Test Type | Example |
|---------------------|-----------|---------|
| Functional Requirements → Acceptance Criteria | Unit Test | `test_create_student_success` |
| API Implementation → Endpoint Spec | API Test | `test_post_students_returns_201` |
| Business Rules | Unit Test | `test_duplicate_admission_raises_error` |
| UI Component Specs | Component Test | `test_student_form_renders_fields` |
| Integration Points | Integration Test | `test_attendance_triggers_sentinel` |

### 2.3 Test Naming Convention

Tests MUST follow this naming pattern for LLM clarity:

```python
# Pattern: test_<action>_<expected_result>
test_create_student_success
test_create_student_duplicate_admission_raises_error
test_get_student_unauthorized_returns_403
test_mark_attendance_offline_queues_for_sync
test_grade_computation_calculates_correct_average

# Pattern for edge cases: test_<action>_<condition>_<expected>
test_create_student_future_dob_raises_validation_error
test_list_students_pagination_returns_correct_page
test_attendance_absent_cluster_triggers_sentinel_alert
```

### 2.4 LLM Prompting Pattern

When using the LLM to generate implementation code, use this pattern:

```
Prompt Template:
────────────────────────────────────────────
Module: [module name]
Acceptance Criteria: [paste criteria from spec]

Tests are located at: [path to test file]
These tests are currently FAILING.

Generate the implementation code in [file path] 
to make all tests pass. Follow the coding standards 
in docs/07-coding-standards.md.
────────────────────────────────────────────
```

### 2.5 Test-First Rules

| Rule | Description |
|------|-------------|
| Tests before code | Always write tests before implementation |
| One test at a time | Add one failing test, implement, verify pass, repeat |
| No code without a test | Every function/endpoint must have at least one test |
| Tests as documentation | Tests should be readable and self-explanatory |
| Acceptance criteria = tests | Every acceptance criterion has a corresponding test |

---

## 3. Testing Pyramid

```
                    ┌─────────────┐
                    │   E2E Tests │  ~10% (Critical workflows)
                    │    (50+)    │
                    ├─────────────┤
                    │ Integration │  ~30% (API + DB + External)
                    │   Tests     │
                    │   (200+)    │
                    ├─────────────┤
                    │  Unit Tests │  ~60% (Functions, classes)
                    │   (1000+)   │
                    └─────────────┘
```

---

## 4. Backend Testing (Python FastAPI)

### 4.1 Framework and Tools

| Tool | Purpose |
|------|---------|
| pytest | Test runner and framework |
| pytest-asyncio | Async test support |
| pytest-cov | Coverage reporting |
| httpx | Async HTTP client for API testing |
| factory-boy | Test data factories |
| faker | Fake data generation |
| pytest-mock | Mocking and patching |
| freezegun | Time manipulation for tests |

### 4.2 Test File Structure

```
backend/
├── app/
│   ├── modules/
│   │   ├── students/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_router.py
│   │   │       ├── test_service.py
│   │   │       ├── test_models.py
│   │   │       └── factories.py
│   │   ├── attendance/
│   │   │   └── tests/
│   │   ├── grades/
│   │   │   └── tests/
│   │   ├── health/
│   │   │   └── tests/
│   │   ├── finance/
│   │   │   └── tests/
│   │   └── ...
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
└── pytest.ini
```

### 4.3 Test Configuration

```python
# pytest.ini
[pytest]
testpaths = tests app/modules
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    slow: marks tests as slow
    integration: marks integration tests
    e2e: marks end-to-end tests
addopts = --strict-markers -v
```

### 4.4 Shared Fixtures

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.database import get_db
from app.core.security import create_access_token

@pytest.fixture
async def db_session():
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Create an async test client."""
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers():
    """Create authentication headers for test user."""
    token = create_access_token(data={"sub": str(test_user_id), "role": "school_admin"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_school():
    """Create a sample school for testing."""
    return SchoolFactory.build()

@pytest.fixture
def sample_student(sample_school):
    """Create a sample student for testing."""
    return StudentFactory.build(school_id=sample_school.id)
```

### 4.5 Unit Test Example

```python
# app/modules/students/tests/test_service.py
import pytest
from unittest.mock import AsyncMock
from app.modules.students.service import StudentService
from app.modules.students.schemas import StudentCreate

class TestStudentService:
    
    @pytest.fixture
    def mock_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def service(self, mock_repo):
        return StudentService(repository=mock_repo)
    
    async def test_create_student_success(self, service, mock_repo):
        """Test successful student creation."""
        data = StudentCreate(
            first_name="Chioma",
            last_name="Okonkwo",
            admission_number="EDU/2026/001",
            date_of_birth=date(2012, 5, 15),
            gender="female",
            class_id=uuid4()
        )
        mock_repo.create.return_value = Student(id=uuid4(), **data.model_dump())
        
        result = await service.create(data, school_id=uuid4())
        
        assert result.first_name == "Chioma"
        assert result.last_name == "Okonkwo"
        mock_repo.create.assert_called_once()
    
    async def test_create_student_duplicate_admission(self, service, mock_repo):
        """Test duplicate admission number raises error."""
        mock_repo.get_by_admission.return_value = Student(id=uuid4())
        
        with pytest.raises(DuplicateAdmissionError):
            await service.create(valid_student_data, school_id=uuid4())
    
    async def test_get_student_by_id(self, service, mock_repo):
        """Test retrieving student by ID."""
        student_id = uuid4()
        mock_repo.get_by_id.return_value = Student(id=student_id, first_name="Test")
        
        result = await service.get_by_id(student_id)
        
        assert result.id == student_id
        mock_repo.get_by_id.assert_called_once_with(student_id)
```

### 4.6 API Test Example

```python
# app/modules/students/tests/test_router.py
import pytest
from httpx import AsyncClient

class TestStudentRouter:
    
    async def test_create_student(self, client: AsyncClient, auth_headers, sample_school):
        """Test POST /api/v1/students endpoint."""
        payload = {
            "first_name": "Emeka",
            "last_name": "Nwosu",
            "admission_number": "EDU/2026/042",
            "date_of_birth": "2011-08-20",
            "gender": "male",
            "class_id": str(sample_class_id)
        }
        
        response = await client.post(
            "/api/v1/students",
            json=payload,
            headers={**auth_headers, "X-School-ID": str(sample_school.id)}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "Emeka"
        assert data["admission_number"] == "EDU/2026/042"
    
    async def test_list_students_pagination(self, client: AsyncClient, auth_headers):
        """Test GET /api/v1/students with pagination."""
        response = await client.get(
            "/api/v1/students?page=1&per_page=20",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
    
    async def test_unauthorized_access(self, client: AsyncClient):
        """Test access without authentication returns 401."""
        response = await client.get("/api/v1/students")
        assert response.status_code == 401
    
    async def test_forbidden_school_access(self, client: AsyncClient, auth_headers):
        """Test accessing another school's data returns 403."""
        response = await client.get(
            f"/api/v1/students/{other_school_student_id}",
            headers=auth_headers
        )
        assert response.status_code == 403
```

---

## 5. Frontend Testing (React)

### 5.1 Framework and Tools

| Tool | Purpose |
|------|---------|
| Vitest | Test runner (fast, Vite-native) |
| React Testing Library | Component testing |
| MSW (Mock Service Worker) | API mocking |
| Playwright | E2E testing |
| Storybook | Component documentation and visual testing |
| jest-dom | Custom DOM matchers |

### 5.2 Test File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── students/
│   │   │   ├── StudentForm.tsx
│   │   │   ├── StudentForm.test.tsx
│   │   │   ├── StudentList.tsx
│   │   │   ├── StudentList.test.tsx
│   │   │   └── __mocks__/
│   │   ├── attendance/
│   │   │   └── ...
│   │   └── ...
│   ├── hooks/
│   │   ├── useStudents.ts
│   │   ├── useStudents.test.ts
│   │   └── ...
│   ├── services/
│   │   ├── api.ts
│   │   ├── api.test.ts
│   │   └── ...
│   └── stores/
│       ├── authStore.ts
│       ├── authStore.test.ts
│       └── ...
├── tests/
│   ├── setup.ts
│   ├── mocks/
│   │   ├── handlers.ts
│   │   ├── server.ts
│   │   └── data/
│   └── e2e/
│       ├── attendance.spec.ts
│       ├── grades.spec.ts
│       └── ...
└── vitest.config.ts
```

### 5.3 Component Test Example

```tsx
// src/components/students/StudentForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StudentForm } from './StudentForm';
import { server } from '../../../tests/mocks/server';
import { rest } from 'msw';

describe('StudentForm', () => {
  const mockOnSubmit = vi.fn();
  
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });
  
  it('renders all required fields', () => {
    render(<StudentForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/admission number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/date of birth/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/gender/i)).toBeInTheDocument();
  });
  
  it('validates required fields before submission', async () => {
    render(<StudentForm onSubmit={mockOnSubmit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/first name is required/i)).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
  
  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    render(<StudentForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/first name/i), 'Chioma');
    await user.type(screen.getByLabelText(/last name/i), 'Okonkwo');
    await user.type(screen.getByLabelText(/admission number/i), 'EDU/2026/001');
    await user.selectOptions(screen.getByLabelText(/gender/i), 'female');
    
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          first_name: 'Chioma',
          last_name: 'Okonkwo',
          admission_number: 'EDU/2026/001',
          gender: 'female',
        })
      );
    });
  });
  
  it('handles server validation errors', async () => {
    server.use(
      rest.post('/api/v1/students', (req, res, ctx) => {
        return res(
          ctx.status(422),
          ctx.json({
            detail: [{ field: 'admission_number', message: 'Already exists' }]
          })
        );
      })
    );
    
    const user = userEvent.setup();
    render(<StudentForm onSubmit={mockOnSubmit} />);
    
    // Fill and submit form
    await user.type(screen.getByLabelText(/first name/i), 'Test');
    await user.type(screen.getByLabelText(/last name/i), 'Student');
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/already exists/i)).toBeInTheDocument();
    });
  });
});
```

### 5.4 Hook Test Example

```tsx
// src/hooks/useStudents.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useStudents } from './useStudents';
import { server } from '../../tests/mocks/server';
import { rest } from 'msw';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useStudents', () => {
  it('fetches students successfully', async () => {
    const { result } = renderHook(() => useStudents(), {
      wrapper: createWrapper(),
    });
    
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    
    expect(result.current.data).toBeDefined();
    expect(result.current.data.items.length).toBeGreaterThan(0);
  });
  
  it('handles fetch error', async () => {
    server.use(
      rest.get('/api/v1/students', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );
    
    const { result } = renderHook(() => useStudents(), {
      wrapper: createWrapper(),
    });
    
    await waitFor(() => expect(result.current.isError).toBe(true));
  });
});
```

---

## 6. Integration Testing

### 6.1 Scope

Integration tests verify interactions between:
- API endpoints and database
- Service layer and external APIs (Termii, Paystack)
- Module interactions (e.g., attendance → LafiyaSentinel)
- Cache layer (Redis) operations

### 6.2 Database Integration Tests

```python
# tests/integration/test_student_db.py
import pytest
from app.modules.students.models import Student
from app.modules.students.repository import StudentRepository

@pytest.mark.integration
class TestStudentRepository:
    
    async def test_create_and_retrieve(self, db_session):
        """Test creating and retrieving a student from database."""
        repo = StudentRepository(db_session)
        student = Student(
            school_id=test_school_id,
            first_name="Adaeze",
            last_name="Eze",
            admission_number="EDU/2026/100",
            date_of_birth=date(2011, 3, 10),
            gender="female",
            class_id=test_class_id
        )
        
        created = await repo.create(student)
        retrieved = await repo.get_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.first_name == "Adaeze"
        assert retrieved.admission_number == "EDU/2026/100"
    
    async def test_list_with_filters(self, db_session, seed_students):
        """Test listing students with class filter."""
        repo = StudentRepository(db_session)
        
        results = await repo.list(
            school_id=test_school_id,
            class_id=test_class_id,
            page=1,
            per_page=10
        )
        
        assert results.total > 0
        assert all(s.class_id == test_class_id for s in results.items)
    
    async def test_soft_delete(self, db_session):
        """Test soft delete removes from active queries."""
        repo = StudentRepository(db_session)
        student = await repo.create(sample_student)
        
        await repo.soft_delete(student.id)
        
        retrieved = await repo.get_by_id(student.id)
        assert retrieved is None
        
        # Still exists in database
        raw = await db_session.get(Student, student.id)
        assert raw is not None
        assert raw.deleted_at is not None
```

### 6.3 External API Integration Tests

```python
# tests/integration/test_termii.py
import pytest
from unittest.mock import AsyncMock, patch
from app.modules.notifications.service import NotificationService

@pytest.mark.integration
class TestTermiiIntegration:
    
    @patch('app.modules.notifications.providers.termii.httpx.AsyncClient')
    async def test_send_sms_otp(self, mock_client):
        """Test sending SMS OTP via Termii."""
        mock_client.return_value.post.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"pinId": "abc123", "smsStatus": "Message Sent"}
        )
        
        service = NotificationService()
        result = await service.send_sms_otp("+2348012345678")
        
        assert result.success is True
        assert result.pin_id == "abc123"
    
    @patch('app.modules.notifications.providers.termii.httpx.AsyncClient')
    async def test_send_whatsapp_otp(self, mock_client):
        """Test sending WhatsApp OTP via Termii."""
        mock_client.return_value.post.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"pinId": "xyz789", "message_status": "success"}
        )
        
        service = NotificationService()
        result = await service.send_whatsapp_otp("+2348012345678")
        
        assert result.success is True
```

### 6.4 Module Interaction Tests

```python
# tests/integration/test_attendance_sentinel.py
import pytest
from app.modules.attendance.service import AttendanceService
from app.modules.health.service import LafiyaSentinelService

@pytest.mark.integration
class TestAttendanceSentinelIntegration:
    
    async def test_absence_cluster_triggers_sentinel(
        self, db_session, seed_class_with_students
    ):
        """
        Test that marking multiple absences in a class
        triggers a LafiyaSentinel cluster alert.
        """
        attendance_service = AttendanceService(db_session)
        sentinel_service = LafiyaSentinelService(db_session)
        
        # Mark 8 out of 20 students absent (40% absence rate)
        absent_student_ids = seed_class_with_students[:8]
        for student_id in absent_student_ids:
            await attendance_service.mark_attendance(
                student_id=student_id,
                date=date.today(),
                status="absent",
                marked_by=test_teacher_id
            )
        
        # Sentinel should have created an alert
        alerts = await sentinel_service.get_active_alerts(
            school_id=test_school_id,
            alert_type="absence_cluster"
        )
        
        assert len(alerts) > 0
        alert = alerts[0]
        assert alert.severity == "medium"
        assert alert.affected_count == 8
```

---

## 7. End-to-End Testing

### 7.1 Framework

Playwright for cross-browser E2E testing.

### 7.2 Critical Workflows

| Workflow | Priority | Tests |
|----------|----------|-------|
| School admin onboarding | P0 | Create school, add classes, invite teachers |
| Student enrollment | P0 | Create student, assign to class, link parent |
| Daily attendance | P0 | Teacher marks attendance, admin views report |
| Grade entry | P0 | Teacher enters CA and exam scores |
| Health visit | P0 | Nurse logs visit, sentinel alert triggers |
| Fee payment | P1 | Parent views fees, initiates payment |
| Offline attendance | P0 | Mark attendance offline, verify sync |
| Report generation | P1 | Generate and download student report |

### 7.3 E2E Test Example

```typescript
// tests/e2e/attendance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Attendance Marking', () => {
  test.beforeEach(async ({ page }) => {
    // Login as teacher
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'teacher@testschool.edu.ng');
    await page.fill('[data-testid="password"]', 'TestPassword123!');
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/dashboard');
  });
  
  test('teacher marks class attendance', async ({ page }) => {
    // Navigate to attendance
    await page.click('[data-testid="nav-attendance"]');
    await page.waitForURL('/attendance');
    
    // Select class
    await page.selectOption('[data-testid="class-select"]', 'JSS 2A');
    
    // Select today's date (default)
    const today = new Date().toISOString().split('T')[0];
    expect(await page.inputValue('[data-testid="date-input"]')).toBe(today);
    
    // Mark students as present/absent
    const studentRows = page.locator('[data-testid="student-row"]');
    const count = await studentRows.count();
    expect(count).toBeGreaterThan(0);
    
    // Mark first student as absent
    await studentRows.nth(0).locator('[data-testid="status-absent"]').check();
    await studentRows.nth(0).locator('[data-testid="absence-reason"]').selectOption('sick');
    
    // Mark all others as present
    for (let i = 1; i < count; i++) {
      await studentRows.nth(i).locator('[data-testid="status-present"]').check();
    }
    
    // Submit attendance
    await page.click('[data-testid="submit-attendance"]');
    
    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Attendance saved');
    
    // Verify summary
    await expect(page.locator('[data-testid="present-count"]')).toContainText(String(count - 1));
    await expect(page.locator('[data-testid="absent-count"]')).toContainText('1');
  });
  
  test('attendance works offline', async ({ page, context }) => {
    await page.click('[data-testid="nav-attendance"]');
    await page.selectOption('[data-testid="class-select"]', 'JSS 2A');
    
    // Go offline
    await context.setOffline(true);
    
    // Mark attendance
    const studentRows = page.locator('[data-testid="student-row"]');
    const count = await studentRows.count();
    for (let i = 0; i < count; i++) {
      await studentRows.nth(i).locator('[data-testid="status-present"]').check();
    }
    
    await page.click('[data-testid="submit-attendance"]');
    
    // Should show offline indicator
    await expect(page.locator('[data-testid="offline-indicator"]')).toBeVisible();
    await expect(page.locator('[data-testid="sync-pending"]')).toContainText('1');
    
    // Go back online
    await context.setOffline(false);
    
    // Wait for sync
    await expect(page.locator('[data-testid="sync-pending"]')).toContainText('0', { timeout: 30000 });
  });
});
```

### 7.4 E2E Test Data Setup

```typescript
// tests/e2e/fixtures/school.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  seededSchool: async ({ request }, use) => {
    // Create test school via API
    const school = await request.post('/api/v1/test/seed-school', {
      data: {
        name: 'Test Academy Lagos',
        classes: ['JSS 1A', 'JSS 2A', 'SSS 3B'],
        students_per_class: 20,
        teachers: 5,
      }
    });
    
    const schoolData = await school.json();
    await use(schoolData);
    
    // Cleanup
    await request.delete(`/api/v1/test/schools/${schoolData.id}`);
  },
});
```

---

## 8. Offline Sync Testing

### 8.1 Sync Test Scenarios

| Scenario | Description | Expected Behavior |
|----------|-------------|-------------------|
| Offline create | Create record while offline | Record saved locally, queued for sync |
| Offline update | Update record while offline | Update saved locally, queued for sync |
| Online sync | Come back online | All queued records sync to server |
| Conflict detection | Edit same record on two devices | Conflict record created |
| Conflict resolution | Resolve conflict manually | Merged record synced |
| Extended offline | Stay offline for 24+ hours | All data persists, syncs on reconnect |
| Partial sync | Sync interrupted mid-way | Resumes from last checkpoint |
| Storage limit | Local storage nearly full | Warning shown, old data archived |

### 8.2 Sync Test Implementation

```typescript
// tests/e2e/offline-sync.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Offline Sync', () => {
  
  test('data persists across offline period', async ({ page, context }) => {
    // Login online
    await page.goto('/login');
    await loginAsTeacher(page);
    
    // Go offline
    await context.setOffline(true);
    
    // Create student record offline
    await page.goto('/students/new');
    await page.fill('[data-testid="first-name"]', 'Offline');
    await page.fill('[data-testid="last-name"]', 'Student');
    await page.fill('[data-testid="admission-number"]', 'OFF/001');
    await page.click('[data-testid="save-button"]');
    
    // Verify saved locally
    await expect(page.locator('[data-testid="sync-status"]')).toContainText('pending');
    
    // Reload page (still offline)
    await page.reload();
    
    // Verify data persisted
    await page.goto('/students');
    await expect(page.locator('text=Offline Student')).toBeVisible();
    
    // Come back online
    await context.setOffline(false);
    
    // Wait for sync
    await page.waitForSelector('[data-testid="sync-status"]:text("synced")', { timeout: 30000 });
    
    // Verify synced by checking from another device/session
    const page2 = await context.newPage();
    await page2.goto('/students');
    await expect(page2.locator('text=Offline Student')).toBeVisible();
  });
  
  test('conflict resolution works', async ({ page, context, request }) => {
    // Create a student online
    const student = await request.post('/api/v1/students', {
      data: { first_name: 'Conflict', last_name: 'Test', /* ... */ }
    });
    const studentData = await student.json();
    
    // Open student on page
    await page.goto(`/students/${studentData.id}`);
    
    // Go offline
    await context.setOffline(true);
    
    // Edit offline
    await page.click('[data-testid="edit-button"]');
    await page.fill('[data-testid="last-name"]', 'Edited Offline');
    await page.click('[data-testid="save-button"]');
    
    // Simulate edit on server (another user)
    await request.put(`/api/v1/students/${studentData.id}`, {
      data: { last_name: 'Edited Online' }
    });
    
    // Come back online
    await context.setOffline(false);
    
    // Should show conflict resolution UI
    await expect(page.locator('[data-testid="conflict-dialog"]')).toBeVisible({ timeout: 30000 });
    await expect(page.locator('[data-testid="local-version"]')).toContainText('Edited Offline');
    await expect(page.locator('[data-testid="server-version"]')).toContainText('Edited Online');
    
    // Choose local version
    await page.click('[data-testid="use-local"]');
    await page.click('[data-testid="resolve-conflict"]');
    
    // Verify resolution
    await expect(page.locator('[data-testid="last-name-value"]')).toContainText('Edited Offline');
  });
});
```

---

## 9. Performance Testing

### 9.1 Tools

| Tool | Purpose |
|------|---------|
| k6 | Load testing and stress testing |
| Lighthouse | Frontend performance auditing |
| pytest-benchmark | Backend function benchmarking |

### 9.2 Load Test Scenarios

```javascript
// tests/performance/api-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // Less than 1% failures
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.edulafia.com';

export default function () {
  // Test student listing
  const res = http.get(`${BASE_URL}/api/v1/students?page=1&per_page=20`, {
    headers: { Authorization: `Bearer ${__ENV.AUTH_TOKEN}` },
  });
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### 9.3 Performance Benchmarks

| Endpoint | Target (p95) | Target (p99) |
|----------|-------------|-------------|
| GET /students | 200ms | 500ms |
| POST /students | 300ms | 600ms |
| GET /attendance | 200ms | 500ms |
| POST /attendance/bulk | 500ms | 1000ms |
| GET /grades | 300ms | 600ms |
| POST /grades/bulk | 800ms | 1500ms |
| POST /health-visits | 300ms | 600ms |
| GET /reports/transcript | 2000ms | 5000ms |
| POST /payments/initiate | 500ms | 1000ms |

---

## 10. Security Testing

See [09-security-guidelines.md](./09-security-guidelines.md) Section 12 for comprehensive security testing requirements.

### 10.1 Automated Security Tests

```python
# tests/security/test_auth.py
import pytest

@pytest.mark.security
class TestAuthentication:
    
    async def test_brute_force_protection(self, client):
        """Verify account locks after failed attempts."""
        for _ in range(5):
            await client.post("/api/v1/auth/login", json={
                "email": "test@test.com",
                "password": "wrong"
            })
        
        response = await client.post("/api/v1/auth/login", json={
            "email": "test@test.com",
            "password": "correct_password"
        })
        
        assert response.status_code == 429  # Too Many Requests
    
    async def test_token_expiration(self, client):
        """Verify expired tokens are rejected."""
        expired_token = create_expired_token(user_id="test")
        response = await client.get(
            "/api/v1/students",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

@pytest.mark.security
class TestAuthorization:
    
    async def test_horizontal_privilege_escalation(self, client):
        """Teacher from School A cannot access School B data."""
        token = create_token(user_id="teacher_a", school_id="school_a")
        response = await client.get(
            "/api/v1/students?school_id=school_b",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
    
    async def test_idor_protection(self, client):
        """User cannot access resource they don't own."""
        token = create_token(user_id="parent_1")
        other_student_id = "student_not_linked_to_parent_1"
        response = await client.get(
            f"/api/v1/students/{other_student_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
```

---

## 11. Accessibility Testing

### 11.1 Standards

WCAG 2.1 Level AA compliance.

### 11.2 Tools

| Tool | Purpose |
|------|---------|
| axe-core | Automated accessibility testing |
| pa11y-ci | CI accessibility audits |
| Lighthouse | Accessibility scoring |
| NVDA/VoiceOver | Manual screen reader testing |

### 11.3 Accessibility Test Example

```typescript
// tests/accessibility/forms.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  
  test('student form is accessible', async ({ page }) => {
    await page.goto('/students/new');
    
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    
    expect(results.violations).toEqual([]);
  });
  
  test('attendance page is keyboard navigable', async ({ page }) => {
    await page.goto('/attendance');
    
    // Tab through all interactive elements
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Verify focus is visible
    const focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(focused).not.toBe('BODY');
  });
});
```

---

## 12. Test Data Management

### 12.1 Factory Pattern

```python
# app/modules/students/tests/factories.py
import factory
from faker import Faker
from app.modules.students.models import Student

fake = Faker('en_NG')  # Nigerian locale

class StudentFactory(factory.Factory):
    class Meta:
        model = Student
    
    id = factory.LazyFunction(uuid4)
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    admission_number = factory.Sequence(lambda n: f"EDU/2026/{n:04d}")
    date_of_birth = factory.LazyFunction(lambda: fake.date_of_birth(minimum_age=10, maximum_age=18))
    gender = factory.LazyFunction(lambda: random.choice(['male', 'female']))
    
    class Params:
        male = factory.Trait(gender='male', first_name=factory.LazyFunction(lambda: fake.first_name_male()))
        female = factory.Trait(gender='female', first_name=factory.LazyFunction(lambda: fake.first_name_female()))
```

### 12.2 Seed Data Scripts

```python
# tests/seeds/seed_school.py
async def seed_test_school(db_session, school_name="Test Academy"):
    """Create a fully seeded test school."""
    school = await create_school(db_session, name=school_name)
    classes = await create_classes(db_session, school.id, ['JSS 1A', 'JSS 2A', 'SSS 3B'])
    teachers = await create_teachers(db_session, school.id, count=5)
    students = []
    for cls in classes:
        batch = await create_students(db_session, school.id, cls.id, count=20)
        students.extend(batch)
    parents = await create_parents(db_session, students)
    fee_structures = await create_fee_structures(db_session, school.id, classes)
    
    return {
        'school': school,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'parents': parents,
        'fee_structures': fee_structures,
    }
```

---

## 13. CI/CD Integration

### 13.1 GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: edulafia_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
      redis:
        image: redis:7
        ports: ['6379:6379']
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml -m "not slow and not e2e"
      - uses: codecov/codecov-action@v4
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - run: npm run lint
      - run: npm run typecheck
  
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
  
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/python@master
      - uses: snyk/actions/node@master
```

---

## 14. Coverage Requirements

### 14.1 Minimum Coverage Targets

| Component | Line Coverage | Branch Coverage |
|-----------|:------------:|:---------------:|
| Backend services | 80% | 70% |
| Backend API routes | 90% | 80% |
| Frontend components | 75% | 65% |
| Frontend hooks/stores | 85% | 75% |
| Security-critical code | 95% | 90% |
| Sync engine | 90% | 85% |

### 14.2 Coverage Reporting

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 80%
```

---

## 15. Implementation Checklists

### 15.1 Test-First Development Process

- [ ] Read module specification acceptance criteria before writing any code
- [ ] Write failing tests that map 1:1 to each acceptance criterion
- [ ] Verify all tests fail (RED phase) before generating implementation
- [ ] Use test failures as the prompt for LLM code generation
- [ ] Verify all tests pass (GREEN phase) after implementation
- [ ] Refactor only after all tests pass
- [ ] Add edge case tests before moving to next feature

### 15.2 Backend Testing Setup

- [ ] Install pytest, pytest-asyncio, pytest-cov
- [ ] Configure pytest.ini with markers and paths
- [ ] Create shared conftest.py with DB fixtures
- [ ] Create factory-boy factories for all models
- [ ] Write unit tests for all service methods
- [ ] Write API tests for all endpoints
- [ ] Write integration tests for module interactions
- [ ] Write security tests for auth/authz
- [ ] Set up coverage reporting

### 15.3 Frontend Testing Setup

- [ ] Install Vitest, React Testing Library, MSW
- [ ] Configure vitest.config.ts
- [ ] Create MSW handlers for all API endpoints
- [ ] Write component tests for all forms
- [ ] Write hook tests for data fetching
- [ ] Write store tests for state management
- [ ] Set up Playwright for E2E tests
- [ ] Write E2E tests for critical workflows
- [ ] Set up axe-core for accessibility

### 15.4 Offline Testing Setup

- [ ] Write sync queue unit tests
- [ ] Write conflict resolution tests
- [ ] Write E2E offline attendance test
- [ ] Write E2E offline grade entry test
- [ ] Write E2E conflict resolution test
- [ ] Test storage limit behavior
- [ ] Test extended offline scenarios

### 15.5 CI/CD Testing Pipeline

- [ ] Configure GitHub Actions test workflow
- [ ] Add backend test job with Postgres service
- [ ] Add frontend test job
- [ ] Add E2E test job with Playwright
- [ ] Add security scanning job
- [ ] Configure coverage reporting to Codecov
- [ ] Add test status checks to PR requirements

---

**End of Testing Strategy (v1.1.0 - Test-First / TDD)**
