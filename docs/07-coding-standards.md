# EduLafia Platform - Coding Standards and Conventions

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. General Principles

### 1.1 Core Values
1. **Readability**: Code should be easy to read and understand
2. **Maintainability**: Code should be easy to modify and extend
3. **Consistency**: Follow consistent patterns throughout the codebase
4. **Simplicity**: Prefer simple, clear solutions over clever ones
5. **Documentation**: Code should be self-documenting where possible

### 1.2 Code Review Checklist
- [ ] Code follows these standards
- [ ] No security vulnerabilities introduced
- [ ] Proper error handling implemented
- [ ] Tests written for new functionality
- [ ] Documentation updated
- [ ] No commented-out code left behind
- [ ] No hardcoded values (use constants/config)
- [ ] Proper logging added

## 2. Python Standards (Backend)

### 2.1 Python Version
- **Minimum**: Python 3.11+
- **Use modern features**: Type hints, f-strings, dataclasses, etc.

### 2.2 Code Formatting
```python
# Use Black for formatting
# Line length: 88 characters
# Use double quotes for strings

# Good example
def calculate_attendance_rate(present_days: int, total_days: int) -> float:
    """Calculate attendance rate as percentage."""
    if total_days == 0:
        return 0.0
    return round(present_days / total_days * 100, 2)

# Bad example
def calcRate(p,t):
    if t==0:return 0
    return p/t*100
```

### 2.3 Naming Conventions
```python
# Variables and functions: snake_case
student_count = 10
def get_student_by_id(student_id: UUID) -> Student:

# Classes: PascalCase
class StudentInformationSystem:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_LOGIN_ATTEMPTS = 5
DEFAULT_PAGE_SIZE = 20

# Private methods/variables: leading underscore
def _validate_input(self, data: dict) -> bool:
    pass

# Type aliases: PascalCase
UserId = UUID
StudentId = UUID
```

### 2.4 Type Hints
```python
# Always use type hints for function signatures
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

# Good: All parameters and return types annotated
async def get_students(
    school_id: UUID,
    class_id: Optional[UUID] = None,
    status: str = "active",
    page: int = 1,
    limit: int = 20
) -> List[Student]:
    pass

# Bad: Missing type hints
async def get_students(school_id, class_id=None, status="active", page=1, limit=20):
    pass
```

### 2.5 Docstrings
```python
# Use Google-style docstrings
async def create_student(
    student_data: StudentCreate,
    school_id: UUID,
    created_by: UUID
) -> Student:
    """Create a new student record.
    
    Args:
        student_data: Student creation data
        school_id: UUID of the school
        created_by: UUID of the user creating the record
        
    Returns:
        Created student object
        
    Raises:
        ValidationError: If student data is invalid
        DuplicateError: If admission number already exists
    """
    pass
```

### 2.6 Error Handling
```python
# Use custom exception classes
class EduLafiaError(Exception):
    """Base exception for EduLafia."""
    pass

class ValidationError(EduLafiaError):
    """Raised when validation fails."""
    pass

class NotFoundError(EduLafiaError):
    """Raised when resource is not found."""
    pass

# Handle specific exceptions
async def get_student(student_id: UUID) -> Student:
    student = await db.students.find_one({"id": student_id})
    if not student:
        raise NotFoundError(f"Student {student_id} not found")
    return student
```

### 2.7 Async/Await
```python
# Use async/await for all I/O operations
import asyncio
import aiohttp

async def fetch_external_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Don't block the event loop
async def process_student(student_id: UUID) -> None:
    # Good: Use async database operations
    student = await db.students.find_one({"id": student_id})
    
    # Bad: Don't use blocking operations
    # time.sleep(1)  # This blocks!
```

### 2.8 Database Operations
```python
# Use SQLAlchemy 2.0 style
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

async def get_students_by_class(
    session: AsyncSession,
    class_id: UUID
) -> List[Student]:
    query = select(Student).where(
        Student.class_id == class_id,
        Student.status == "active"
    )
    result = await session.execute(query)
    return result.scalars().all()

# Use transactions for multiple operations
async def transfer_student(
    session: AsyncSession,
    student_id: UUID,
    new_class_id: UUID
) -> None:
    async with session.begin():
        # Update student class
        await session.execute(
            update(Student)
            .where(Student.id == student_id)
            .values(class_id=new_class_id)
        )
        
        # Create transfer record
        session.add(Transfer(
            student_id=student_id,
            from_class_id=old_class_id,
            to_class_id=new_class_id
        ))
```

### 2.9 Pydantic Models
```python
# Use Pydantic v2 for validation
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from datetime import date

class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str = Field(..., pattern="^(male|female)$")
    
class StudentCreate(StudentBase):
    school_id: UUID
    class_id: Optional[UUID] = None
    admission_date: date
    
class StudentResponse(StudentBase):
    id: UUID
    admission_number: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 3. TypeScript Standards (Frontend)

### 3.1 TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### 3.2 Naming Conventions
```typescript
// Variables and functions: camelCase
const studentCount = 10;
function getStudentById(id: string): Student {
    return students.find(s => s.id === id);
}

// Classes and types: PascalCase
class StudentService {
    // ...
}

interface Student {
    id: string;
    name: string;
}

type StudentStatus = 'active' | 'inactive' | 'graduated';

// Constants: UPPER_SNAKE_CASE
const MAX_LOGIN_ATTEMPTS = 5;
const DEFAULT_PAGE_SIZE = 20;

// Props interfaces: append 'Props'
interface StudentCardProps {
    student: Student;
    onClick: (id: string) => void;
}

// Event handlers: prefix with 'handle' or 'on'
const handleClick = (event: React.MouseEvent) => {
    // ...
};

<Button onClick={handleClick} />
```

### 3.3 Component Structure
```typescript
// Use functional components with hooks
import React, { useState, useEffect } from 'react';

interface StudentListProps {
    schoolId: string;
}

export const StudentList: React.FC<StudentListProps> = ({ schoolId }) => {
    // State hooks
    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    // Effect hooks
    useEffect(() => {
        fetchStudents();
    }, [schoolId]);
    
    // Functions
    const fetchStudents = async () => {
        try {
            setLoading(true);
            const data = await studentService.getBySchool(schoolId);
            setStudents(data);
        } catch (err) {
            setError('Failed to load students');
        } finally {
            setLoading(false);
        }
    };
    
    // Early returns for loading/error states
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;
    
    // Main render
    return (
        <div className="student-list">
            {students.map(student => (
                <StudentCard key={student.id} student={student} />
            ))}
        </div>
    );
};
```

### 3.4 State Management
```typescript
// Use Zustand for global state
import { create } from 'zustand';

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    token: null,
    isAuthenticated: false,
    
    login: async (email: string, password: string) => {
        const response = await authService.login(email, password);
        set({
            user: response.user,
            token: response.token,
            isAuthenticated: true,
        });
    },
    
    logout: () => {
        set({
            user: null,
            token: null,
            isAuthenticated: false,
        });
    },
}));

// Use React Query for server state
import { useQuery, useMutation } from '@tanstack/react-query';

export const useStudents = (schoolId: string) => {
    return useQuery({
        queryKey: ['students', schoolId],
        queryFn: () => studentService.getBySchool(schoolId),
    });
};

export const useCreateStudent = () => {
    return useMutation({
        mutationFn: studentService.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['students'] });
        },
    });
};
```

### 3.5 API Service Layer
```typescript
// Create organized service layer
import axios, { AxiosInstance } from 'axios';

class ApiService {
    private client: AxiosInstance;
    
    constructor() {
        this.client = axios.create({
            baseURL: import.meta.env.VITE_API_URL,
            timeout: 30000,
        });
        
        this.setupInterceptors();
    }
    
    private setupInterceptors() {
        // Request interceptor for auth
        this.client.interceptors.request.use((config) => {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
        
        // Response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    // Handle unauthorized
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }
        );
    }
    
    async get<T>(url: string, params?: any): Promise<T> {
        const response = await this.client.get<T>(url, { params });
        return response.data;
    }
    
    async post<T>(url: string, data?: any): Promise<T> {
        const response = await this.client.post<T>(url, data);
        return response.data;
    }
    
    // ... other methods
}

export const apiService = new ApiService();
```

### 3.6 Form Handling
```typescript
// Use React Hook Form with Zod validation
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const studentSchema = z.object({
    firstName: z.string().min(1, 'First name is required'),
    lastName: z.string().min(1, 'Last name is required'),
    dateOfBirth: z.string().refine((val) => !isNaN(Date.parse(val)), {
        message: 'Invalid date',
    }),
    gender: z.enum(['male', 'female']),
});

type StudentFormData = z.infer<typeof studentSchema>;

export const StudentForm: React.FC = () => {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<StudentFormData>({
        resolver: zodResolver(studentSchema),
    });
    
    const onSubmit = async (data: StudentFormData) => {
        try {
            await studentService.create(data);
            // Handle success
        } catch (error) {
            // Handle error
        }
    };
    
    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('firstName')} />
            {errors.firstName && <span>{errors.firstName.message}</span>}
            
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Save Student'}
            </button>
        </form>
    );
};
```

## 4. React Component Standards

### 4.1 Component Organization
```
components/
├── common/           # Reusable components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx
│   │   └── index.ts
│   └── index.ts
├── forms/            # Form components
├── layout/           # Layout components
└── data/             # Data display components
```

### 4.2 Component Props
```typescript
// Use interface for props
interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    loading?: boolean;
    onClick?: () => void;
    children: React.ReactNode;
}

// Destructure props in function signature
export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    onClick,
    children,
}) => {
    // Component implementation
};
```

### 4.3 Styling
```typescript
// Use Tailwind CSS classes
import clsx from 'clsx';

interface CardProps {
    className?: string;
    children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ className, children }) => {
    return (
        <div className={clsx(
            'bg-white rounded-lg shadow-md p-6',
            className
        )}>
            {children}
        </div>
    );
};

// Usage
<Card className="w-full max-w-md">
    Content
</Card>
```

### 4.4 Error Boundaries
```typescript
import React from 'react';

interface ErrorBoundaryProps {
    children: React.ReactNode;
}

interface ErrorBoundaryState {
    hasError: boolean;
    error: Error | null;
}

export class ErrorBoundary extends React.Component<
    ErrorBoundaryProps,
    ErrorBoundaryState
> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
    }
    
    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }
    
    render() {
        if (this.state.hasError) {
            return <h1>Something went wrong.</h1>;
        }
        
        return this.props.children;
    }
}
```

## 5. Testing Standards

### 5.1 Backend Testing
```python
# Use pytest for testing
import pytest
from httpx import AsyncClient

# Test file naming: test_*.py or *_test.py
# Test function naming: test_<function_name>_<scenario>

@pytest.mark.asyncio
async def test_create_student_success(client: AsyncClient):
    """Test successful student creation."""
    student_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "2010-01-15",
        "gender": "male",
        "school_id": str(uuid4()),
    }
    
    response = await client.post("/api/v1/students", json=student_data)
    
    assert response.status_code == 201
    assert response.json()["first_name"] == "John"
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_create_student_validation_error(client: AsyncClient):
    """Test student creation with invalid data."""
    student_data = {
        "first_name": "",  # Invalid: empty
        "last_name": "Doe",
    }
    
    response = await client.post("/api/v1/students", json=student_data)
    
    assert response.status_code == 422
    assert "first_name" in response.json()["error"]["details"]
```

### 5.2 Frontend Testing
```typescript
// Use Vitest for unit tests
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

// Test file naming: *.test.tsx or *.spec.tsx
// Test function naming: it('should <do something> when <condition>')

describe('StudentCard', () => {
    it('should display student name when provided', () => {
        const student = {
            id: '1',
            firstName: 'John',
            lastName: 'Doe',
        };
        
        render(<StudentCard student={student} />);
        
        expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    it('should call onClick when clicked', async () => {
        const handleClick = vi.fn();
        const student = {
            id: '1',
            firstName: 'John',
            lastName: 'Doe',
        };
        
        render(
            <StudentCard student={student} onClick={handleClick} />
        );
        
        await fireEvent.click(screen.getByRole('button'));
        
        expect(handleClick).toHaveBeenCalledWith('1');
    });
});
```

### 5.3 Integration Testing
```python
# Test complete workflows
@pytest.mark.asyncio
async def test_attendance_marking_workflow(client: AsyncClient):
    """Test complete attendance marking workflow."""
    # 1. Create school
    school_response = await client.post("/api/v1/schools", json={...})
    school_id = school_response.json()["id"]
    
    # 2. Create class
    class_response = await client.post("/api/v1/classes", json={
        "school_id": school_id,
        "name": "JSS1A",
    })
    class_id = class_response.json()["id"]
    
    # 3. Create students
    students = []
    for i in range(5):
        student_response = await client.post("/api/v1/students", json={
            "school_id": school_id,
            "class_id": class_id,
            "first_name": f"Student {i}",
            "last_name": "Test",
            "date_of_birth": "2010-01-15",
            "gender": "male",
        })
        students.append(student_response.json()["id"])
    
    # 4. Mark attendance
    attendance_data = {
        "class_id": class_id,
        "date": "2026-03-26",
        "period": 1,
        "records": [
            {"student_id": students[0], "status": "present"},
            {"student_id": students[1], "status": "absent", "reason_code": "sick"},
            {"student_id": students[2], "status": "present"},
            {"student_id": students[3], "status": "present"},
            {"student_id": students[4], "status": "present"},
        ],
    }
    
    attendance_response = await client.post(
        "/api/v1/attendance/mark",
        json=attendance_data
    )
    
    assert attendance_response.status_code == 201
    
    # 5. Verify attendance summary
    summary_response = await client.get(
        f"/api/v1/attendance/summary?class_id={class_id}"
    )
    
    summary = summary_response.json()
    assert summary["attendance_rate"] == 80.0  # 4 present out of 5
```

## 6. Security Standards

### 6.1 Input Validation
```python
# Always validate input
from pydantic import BaseModel, validator, Field

class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+234\d{10}$")
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

### 6.2 SQL Injection Prevention
```python
# Use parameterized queries
# Good: Using ORM
students = await session.execute(
    select(Student).where(Student.school_id == school_id)
)

# Good: Using parameterized query
query = "SELECT * FROM students WHERE school_id = %s"
await session.execute(query, (school_id,))

# Bad: String concatenation
# query = f"SELECT * FROM students WHERE school_id = '{school_id}'"
```

### 6.3 XSS Prevention
```typescript
// React escapes content by default
// Good: Safe
<div>{userInput}</div>

// Bad: Potentially unsafe
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// If you must use dangerouslySetInnerHTML, sanitize first
import DOMPurify from 'dompurify';

<div dangerouslySetInnerHTML={{ 
    __html: DOMPurify.sanitize(userInput) 
}} />
```

### 6.4 Authentication and Authorization
```python
# Use dependency injection for auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    user = await session.get(User, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# Use in endpoints
@app.get("/api/v1/students")
async def get_students(
    current_user: User = Depends(get_current_user),
    school_id: UUID = Depends(get_school_from_user)
):
    # User is already authenticated and authorized
    pass
```

## 7. Logging Standards

### 7.1 Python Logging
```python
import structlog

logger = structlog.get_logger()

# Use structured logging
logger.info(
    "student_created",
    student_id=student.id,
    school_id=school.id,
    created_by=current_user.id,
    admission_number=student.admission_number
)

# Log errors with context
try:
    await process_attendance(student_id, date)
except Exception as e:
    logger.error(
        "attendance_processing_failed",
        student_id=student_id,
        date=date,
        error=str(e),
        exc_info=True
    )
    raise
```

### 7.2 Frontend Logging
```typescript
// Use console with levels
const logger = {
    info: (message: string, data?: any) => {
        if (import.meta.env.DEV) {
            console.log(`[INFO] ${message}`, data);
        }
    },
    error: (message: string, error?: any) => {
        console.error(`[ERROR] ${message}`, error);
        // Send to error tracking service in production
        if (import.meta.env.PROD) {
            errorTrackingService.captureException(error);
        }
    },
    warn: (message: string, data?: any) => {
        console.warn(`[WARN] ${message}`, data);
    },
};

// Usage
try {
    await studentService.create(data);
    logger.info('Student created', { studentId: result.id });
} catch (error) {
    logger.error('Failed to create student', error);
    throw error;
}
```

## 8. Performance Standards

### 8.1 Database Queries
```python
# Use indexes for frequently queried fields
# Use selectinload for relationships to avoid N+1 queries
from sqlalchemy.orm import selectinload

async def get_students_with_class(session: AsyncSession, school_id: UUID):
    query = (
        select(Student)
        .options(selectinload(Student.class_))
        .where(Student.school_id == school_id)
    )
    result = await session.execute(query)
    return result.scalars().all()

# Use pagination for large datasets
async def get_students_paginated(
    session: AsyncSession,
    school_id: UUID,
    page: int = 1,
    limit: int = 20
):
    query = (
        select(Student)
        .where(Student.school_id == school_id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalars().all()
```

### 8.2 Frontend Performance
```typescript
// Use React.memo for expensive components
export const StudentList = React.memo(({ students }: StudentListProps) => {
    return (
        <div>
            {students.map(student => (
                <StudentCard key={student.id} student={student} />
            ))}
        </div>
    );
});

// Use useMemo for expensive calculations
const filteredStudents = useMemo(() => {
    return students.filter(student => 
        student.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
}, [students, searchTerm]);

// Use useCallback for event handlers
const handleClick = useCallback((studentId: string) => {
    navigate(`/students/${studentId}`);
}, [navigate]);
```

## 9. Git Standards

### 9.1 Commit Messages
```bash
# Format: <type>(<scope>): <description>

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code style changes (formatting, etc.)
# refactor: Code refactoring
# test: Adding or updating tests
# chore: Maintenance tasks
# perf: Performance improvements
# ci: CI/CD changes

# Examples:
feat(students): add batch import functionality
fix(attendance): resolve timezone issue in date handling
docs(readme): update installation instructions
refactor(api): improve error handling patterns
test(auth): add integration tests for login flow
```

### 9.2 Branch Naming
```bash
# Format: <type>/<ticket-id>-<description>

# Examples:
feature/EDU-123-student-management
bugfix/EDU-456-attendance-date-issue
hotfix/EDU-789-security-vulnerability
release/v1.2.0
```

## 10. Documentation Standards

### 10.1 Code Comments
```python
# Good: Explain why, not what
# We use a 24-hour edit window to allow honest corrections
# while preventing backdating of attendance records
EDIT_WINDOW_HOURS = 24

# Bad: Explain what (obvious from code)
# Increment counter by 1
counter += 1

# Use docstrings for public APIs
def calculate_attendance_rate(present_days: int, total_days: int) -> float:
    """Calculate attendance rate as a percentage.
    
    Args:
        present_days: Number of days student was present
        total_days: Total number of school days
        
    Returns:
        Attendance rate as percentage (0-100)
        
    Examples:
        >>> calculate_attendance_rate(8, 10)
        80.0
    """
    if total_days == 0:
        return 0.0
    return round(present_days / total_days * 100, 2)
```

### 10.2 API Documentation
```python
# Use FastAPI's automatic documentation
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get(
    "/students",
    response_model=List[StudentResponse],
    summary="Get list of students",
    description="Retrieve a paginated list of students for a school",
    responses={
        200: {"description": "Successful response"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    }
)
async def get_students(
    school_id: UUID,
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Get students for a school.
    
    This endpoint returns a paginated list of students.
    Requires authentication and appropriate permissions.
    """
    pass
```

---

*These coding standards ensure consistency, quality, and maintainability across the EduLafia codebase. All team members should follow these guidelines.*

---

**End of Coding Standards**