# EduLafia Platform - Module Specification: Student Information System (M1)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M1 - Student Information System (SIS)
- **Priority:** High (Core Module)

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Data Model Implementation](#3-data-model-implementation)
4. [API Implementation](#4-api-implementation)
5. [Business Logic Implementation](#5-business-logic-implementation)
6. [UI Component Specifications](#6-ui-component-specifications)
7. [Testing Requirements](#7-testing-requirements)
8. [Security Considerations](#8-security-considerations)
9. [Performance Requirements](#9-performance-requirements)
10. [Integration Points](#10-integration-points)
11. [Implementation Checklist](#11-implementation-checklist)

## 1. Module Overview

### 1.1 Purpose
The Student Information System (SIS) is the foundation module of EduLafia. It provides comprehensive digital student profiles, guardian management, document storage, and student lifecycle management. This module is the data foundation for all other modules.

### 1.2 Scope
- Student profile management (CRUD operations)
- Guardian/parent management
- Document attachment and storage
- Student status lifecycle management
- Batch import/export functionality
- Student search and reporting
- NIN (National Identification Number) linkage
- Student ID card generation

### 1.3 Dependencies
- **Required Modules:** None (foundational module)
- **Dependent Modules:** All other modules depend on SIS data
- **External Dependencies:** Storage service for documents, SMS/WhatsApp for notifications

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Student Profile Management
```yaml
Feature: Student Profile Management
Description: Create, read, update, and archive student records
Acceptance Criteria:
  - Create comprehensive student profile with all required fields
  - Generate unique student ID (school-prefixed, sequential)
  - Validate all required fields before creation
  - Support optional fields (NIN, photo, etc.)
  - Maintain audit trail for all changes
  - Prevent deletion, only allow status change to inactive
```

#### 2.1.2 Guardian Management
```yaml
Feature: Guardian Management
Description: Manage parent/guardian information linked to students
Acceptance Criteria:
  - Support up to 2 guardians per student
  - Required fields: name, relationship, phone number
  - Optional fields: email, WhatsApp number, occupation
  - Auto-provision guardian portal access when WhatsApp number provided
  - Allow emergency contact designation
  - Maintain guardian-student relationship history
```

#### 2.1.3 Document Management
```yaml
Feature: Document Management
Description: Attach and manage student documents
Acceptance Criteria:
  - Support multiple document types (admission letter, birth certificate, etc.)
  - Accept scanned documents and photos
  - Store documents securely with access controls
  - Allow download of original documents
  - Maintain document version history
  - Limit file size to 10MB per document
```

#### 2.1.4 Student Status Management
```yaml
Feature: Student Status Management
Description: Track student lifecycle from admission to graduation/exit
Acceptance Criteria:
  - Statuses: active, inactive, graduated, withdrawn, transferred, deceased
  - Only allow status transitions based on business rules
  - Maintain complete history of status changes
  - Auto-update status based on academic year progression
  - Flag students with unusual status patterns
```

### 2.2 Business Rules

#### 2.2.1 Student Creation Rules
1. **Guardian Requirement:** A student cannot be enrolled without at least one active guardian contact with a phone number
2. **Unique Admission Number:** System-generated, school-prefixed, sequential format: `{SCHOOL_CODE}-{SEQUENCE}`
3. **Age Validation:** Student must be between 6 and 20 years old at admission
4. **Class Assignment:** Student must be assigned to a valid class within the school
5. **Date Validation:** Admission date cannot be in the future

#### 2.2.2 Student ID Generation Rules
```python
# Algorithm for student ID generation
def generate_admission_number(school_code: str, school_id: UUID) -> str:
    """
    Generate unique admission number for a student.
    
    Format: {SCHOOL_CODE}-{SEQUENCE}
    Example: ESS001-0001
    
    Rules:
    1. Get next sequence number for the school
    2. Pad with zeros to 4 digits
    3. Combine with school code
    """
    # Get max sequence for school
    max_sequence = get_max_sequence(school_id)
    next_sequence = max_sequence + 1
    
    # Format: 4-digit sequence
    sequence_str = f"{next_sequence:04d}"
    
    return f"{school_code}-{sequence_str}"
```

#### 2.2.3 Data Validation Rules
```python
VALIDATION_RULES = {
    "first_name": {
        "required": True,
        "min_length": 1,
        "max_length": 100,
        "pattern": r"^[a-zA-Z\s\-']+$"
    },
    "last_name": {
        "required": True,
        "min_length": 1,
        "max_length": 100,
        "pattern": r"^[a-zA-Z\s\-']+$"
    },
    "date_of_birth": {
        "required": True,
        "type": "date",
        "min_age": 6,
        "max_age": 20,
        "cannot_be_future": True
    },
    "gender": {
        "required": True,
        "allowed_values": ["male", "female"]
    },
    "nin": {
        "required": False,
        "pattern": r"^\d{11}$",
        "unique": True
    },
    "phone": {
        "required": True,
        "pattern": r"^\+234\d{10}$",
        "country_code": "+234"
    }
}
```

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Students table (already defined in data-model.md)
-- Key fields for SIS implementation:
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    class_id UUID REFERENCES classes(id),
    admission_number VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    nationality VARCHAR(100) DEFAULT 'Nigerian',
    state_of_origin VARCHAR(100),
    lga VARCHAR(100),
    address TEXT,
    photo_url VARCHAR(500),
    blood_group VARCHAR(5),
    genotype VARCHAR(5) CHECK (genotype IN ('AA', 'AS', 'SS', 'SC', 'AC')),
    chronic_conditions TEXT[],
    allergies TEXT[],
    current_medications TEXT[],
    emergency_notes TEXT,
    nin VARCHAR(11) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'graduated', 'withdrawn', 'transferred', 'deceased')),
    admission_date DATE NOT NULL,
    graduation_date DATE,
    previous_school VARCHAR(255),
    transfer_notes TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, admission_number)
);

-- Guardians table (already defined in data-model.md)
-- Student-Guardian relationship table (already defined in data-model.md)
-- Student documents table (already defined in data-model.md)
```

### 3.2 Indexes for SIS
```sql
-- Performance indexes for SIS queries
CREATE INDEX idx_students_school_id ON students(school_id);
CREATE INDEX idx_students_class_id ON students(class_id);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_admission_number ON students(admission_number);
CREATE INDEX idx_students_nin ON students(nin);
CREATE INDEX idx_students_name_search ON students USING gin(to_tsvector('english', first_name || ' ' || last_name));
CREATE INDEX idx_students_school_status ON students(school_id, status);

-- Guardian indexes
CREATE INDEX idx_guardians_phone ON guardians(phone);
CREATE INDEX idx_guardians_email ON guardians(email);

-- Document indexes
CREATE INDEX idx_student_documents_student_id ON student_documents(student_id);
CREATE INDEX idx_student_documents_type ON student_documents(document_type);
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Student CRUD Endpoints
```yaml
Endpoints:
  POST /api/v1/students:
    - Description: Create a new student
    - Request Body: StudentCreate schema
    - Response: StudentResponse schema
    - Auth: Required (school_admin, teacher)
    - Validation: Full validation per business rules
    - Side Effects:
      - Generate admission number
      - Create guardian records
      - Send welcome notification to guardian
      - Log audit trail

  GET /api/v1/students/{student_id}:
    - Description: Get student by ID
    - Response: StudentDetailResponse schema
    - Auth: Required (with permission check)
    - Includes: Guardian info, class info, recent activity

  GET /api/v1/students:
    - Description: List students with filtering
    - Query Parameters: school_id, class_id, status, search, page, limit
    - Response: Paginated list of students
    - Auth: Required

  PATCH /api/v1/students/{student_id}:
    - Description: Update student information
    - Request Body: StudentUpdate schema (partial)
    - Response: Updated StudentResponse
    - Auth: Required (school_admin)
    - Validation: Only allowed fields can be updated
    - Side Effects: Update audit trail, version increment

  DELETE /api/v1/students/{student_id}:
    - Description: Archive student (soft delete)
    - Request Body: { "status": "inactive", "reason": "..." }
    - Auth: Required (school_admin)
    - Business Rule: Cannot delete, only archive
    - Side Effects:
      - Set status to inactive
      - Set deleted_at timestamp
      - Log archival reason
```

#### 4.1.2 Guardian Endpoints
```yaml
Endpoints:
  POST /api/v1/students/{student_id}/guardians:
    - Description: Add guardian to student
    - Request Body: GuardianCreate schema
    - Response: GuardianResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Maximum 2 guardians per student
      - At least one guardian must be primary contact
      - Phone number required
    - Side Effects:
      - Create guardian record
      - Create student_guardian relationship
      - Auto-provision portal access if WhatsApp number provided

  GET /api/v1/students/{student_id}/guardians:
    - Description: List guardians for student
    - Response: List of GuardianResponse

  PATCH /api/v1/guardians/{guardian_id}:
    - Description: Update guardian information
    - Request Body: GuardianUpdate schema
    - Response: Updated GuardianResponse

  DELETE /api/v1/students/{student_id}/guardians/{guardian_id}:
    - Description: Remove guardian from student
    - Auth: Required (school_admin)
    - Business Rule: Cannot remove last guardian
```

#### 4.1.3 Document Endpoints
```yaml
Endpoints:
  POST /api/v1/students/{student_id}/documents:
    - Description: Upload student document
    - Request Body: Multipart form with file
    - Query Parameters: document_type
    - Response: DocumentResponse schema
    - Auth: Required (school_admin, nurse for medical records)
    - File Limits: Max 10MB, allowed types: pdf, jpg, png, doc
    - Storage: Secure cloud storage with access controls
    - Side Effects:
      - Upload file to storage service
      - Create document metadata record
      - Generate thumbnail for images

  GET /api/v1/students/{student_id}/documents:
    - Description: List student documents
    - Query Parameters: document_type (optional filter)
    - Response: List of DocumentResponse

  GET /api/v1/students/{student_id}/documents/{document_id}:
    - Description: Download document
    - Response: File download with proper content-type
    - Auth: Required (with access control)

  DELETE /api/v1/students/{student_id}/documents/{document_id}:
    - Description: Delete document
    - Auth: Required (school_admin)
    - Side Effects: Remove file from storage, delete metadata
```

#### 4.1.4 Batch Operations
```yaml
Endpoints:
  POST /api/v1/students/batch-import:
    - Description: Import students from CSV
    - Request Body: Multipart form with CSV file
    - Query Parameters: school_id, class_id
    - Response: ImportResult schema
    - Auth: Required (school_admin)
    - Features:
      - Validate CSV format
      - Detect duplicate admission numbers
      - Generate import report
      - Rollback on critical errors
    - CSV Format:
      first_name,last_name,date_of_birth,gender,guardian_name,guardian_phone
      John,Doe,2010-01-15,male,James Doe,+2348012345678

  GET /api/v1/students/export:
    - Description: Export students to CSV
    - Query Parameters: school_id, class_id, status, format
    - Response: CSV file download
    - Auth: Required (school_admin)
    - Export Fields: All student fields + guardian info

  POST /api/v1/students/{student_id}/transfer:
    - Description: Transfer student to another school
    - Request Body: { "to_school_id": "...", "reason": "..." }
    - Response: TransferResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Cannot transfer if fees outstanding
      - Generate transfer document package
      - Update status to "transferred"
      - Notify receiving school
```

#### 4.1.5 Search and Reporting
```yaml
Endpoints:
  GET /api/v1/students/search:
    - Description: Advanced student search
    - Query Parameters: query, filters, page, limit
    - Response: Paginated search results
    - Features:
      - Full-text search on name, admission number
      - Filter by class, status, gender, age range
      - Search guardian information
      - Result ranking by relevance

  GET /api/v1/students/{student_id}/profile-card:
    - Description: Generate student profile card
    - Query Parameters: format (pdf, png)
    - Response: File download
    - Features:
      - School branding
      - Student photo
      - QR code with student ID
      - Emergency contact info

  GET /api/v1/students/reports/age-distribution:
    - Description: Age distribution report
    - Query Parameters: school_id, class_id, academic_year
    - Response: Age distribution data
    - Use: For EMIS reporting

  GET /api/v1/students/reports/gender-distribution:
    - Description: Gender distribution report
    - Query Parameters: school_id, class_id, academic_year
    - Response: Gender distribution data
```

## 5. Business Logic Implementation

### 5.1 Student Creation Logic
```python
class StudentService:
    async def create_student(
        self,
        student_data: StudentCreate,
        school_id: UUID,
        created_by: UUID
    ) -> Student:
        """Create a new student record."""
        
        # 1. Validate school exists and is active
        school = await self.school_service.get_school(school_id)
        if not school.is_active:
            raise ValidationError("School is not active")
        
        # 2. Validate class belongs to school
        if student_data.class_id:
            class_ = await self.class_service.get_class(student_data.class_id)
            if class_.school_id != school_id:
                raise ValidationError("Class does not belong to school")
        
        # 3. Validate guardian requirements
        if not student_data.guardians or len(student_data.guardians) == 0:
            raise ValidationError("At least one guardian is required")
        
        # 4. Validate date of birth
        age = calculate_age(student_data.date_of_birth)
        if age < 6 or age > 20:
            raise ValidationError(f"Student age {age} is outside allowed range (6-20)")
        
        # 5. Generate admission number
        admission_number = await self.generate_admission_number(school_id)
        
        # 6. Create student record
        student = Student(
            school_id=school_id,
            class_id=student_data.class_id,
            admission_number=admission_number,
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            date_of_birth=student_data.date_of_birth,
            gender=student_data.gender,
            admission_date=student_data.admission_date,
            created_by=created_by
        )
        
        self.session.add(student)
        await self.session.flush()  # Get student ID
        
        # 7. Create guardian records
        for guardian_data in student_data.guardians:
            guardian = await self.guardian_service.create_guardian(
                guardian_data,
                student.id,
                created_by
            )
        
        # 8. Send welcome notification
        await self.notification_service.send_welcome_notification(
            student=student,
            guardians=student_data.guardians
        )
        
        # 9. Log audit trail
        await self.audit_service.log(
            action="student_created",
            resource_type="student",
            resource_id=student.id,
            details={
                "admission_number": admission_number,
                "school_id": str(school_id),
                "created_by": str(created_by)
            }
        )
        
        await self.session.commit()
        return student
    
    async def generate_admission_number(self, school_id: UUID) -> str:
        """Generate unique admission number for school."""
        school = await self.school_service.get_school(school_id)
        
        # Get max sequence for school
        result = await self.session.execute(
            select(Student.admission_number)
            .where(Student.school_id == school_id)
            .order_by(Student.admission_number.desc())
            .limit(1)
        )
        
        last_number = result.scalar()
        
        if last_number:
            # Extract sequence from last number
            sequence = int(last_number.split('-')[-1])
            next_sequence = sequence + 1
        else:
            next_sequence = 1
        
        return f"{school.code}-{next_sequence:04d}"
```

### 5.2 Student Search Logic
```python
class StudentSearchService:
    async def search_students(
        self,
        school_id: UUID,
        query: Optional[str] = None,
        filters: Optional[StudentFilters] = None,
        page: int = 1,
        limit: int = 20
    ) -> PaginatedResult[Student]:
        """Search students with filters and pagination."""
        
        # Base query
        base_query = select(Student).where(
            Student.school_id == school_id,
            Student.deleted_at.is_(None)
        )
        
        # Apply text search
        if query:
            search_vector = func.to_tsvector(
                'english',
                Student.first_name + ' ' + Student.last_name
            )
            search_query = func.plainto_tsquery('english', query)
            
            base_query = base_query.where(
                search_vector.op('@@')(search_query)
            )
        
        # Apply filters
        if filters:
            if filters.class_id:
                base_query = base_query.where(Student.class_id == filters.class_id)
            if filters.status:
                base_query = base_query.where(Student.status == filters.status)
            if filters.gender:
                base_query = base_query.where(Student.gender == filters.gender)
            if filters.age_min or filters.age_max:
                if filters.age_min:
                    min_date = date.today() - timedelta(days=filters.age_max * 365)
                    base_query = base_query.where(Student.date_of_birth >= min_date)
                if filters.age_max:
                    max_date = date.today() - timedelta(days=filters.age_min * 365)
                    base_query = base_query.where(Student.date_of_birth <= max_date)
        
        # Get total count
        count_query = select(func.count()).select_from(base_query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * limit
        paginated_query = base_query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.session.execute(paginated_query)
        students = result.scalars().all()
        
        return PaginatedResult(
            items=students,
            total=total,
            page=page,
            limit=limit,
            pages=(total + limit - 1) // limit
        )
```

## 6. UI Component Specifications

### 6.1 Student List Component
```typescript
interface StudentListProps {
  schoolId: string;
  classId?: string;
  onStudentSelect: (student: Student) => void;
}

// Component Requirements:
// 1. Display paginated list of students
// 2. Support search functionality
// 3. Filter by class, status, gender
// 4. Sort by name, admission number, class
// 5. Bulk selection for batch operations
// 6. Export to CSV button
// 7. Import from CSV button
// 8. Responsive design for mobile
```

### 6.2 Student Form Component
```typescript
interface StudentFormProps {
  mode: 'create' | 'edit';
  student?: Student;
  schoolId: string;
  onSuccess: (student: Student) => void;
  onCancel: () => void;
}

// Form Sections:
// 1. Basic Information (name, DOB, gender)
// 2. Contact Information (address, phone)
// 3. Academic Information (class, admission date)
// 4. Health Information (blood group, genotype)
// 5. Guardian Information (dynamic, up to 2)
// 6. Document Upload (optional)
// 7. Notes and Additional Information

// Validation:
// - Real-time validation on blur
// - Submit validation for all fields
// - Error highlighting
// - Success feedback
```

### 6.3 Student Profile Component
```typescript
interface StudentProfileProps {
  studentId: string;
}

// Profile Sections:
// 1. Header (photo, name, status, quick actions)
// 2. Personal Information (read-only)
// 3. Guardian Information (with contact buttons)
// 4. Academic Summary (current class, recent results)
// 5. Attendance Summary (current term rate)
// 6. Health Summary (recent visits, alerts)
// 7. Documents (list with download)
// 8. Activity Timeline (recent actions)
// 9. Edit Button (opens edit modal)
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for StudentService
class TestStudentService:
    async def test_create_student_success(self):
        """Test successful student creation."""
        pass
    
    async def test_create_student_without_guardian_fails(self):
        """Test that student creation fails without guardian."""
        pass
    
    async def test_generate_admission_number_unique(self):
        """Test that admission numbers are unique."""
        pass
    
    async def test_create_student_duplicate_admission_fails(self):
        """Test that duplicate admission numbers fail."""
        pass
    
    async def test_update_student_success(self):
        """Test successful student update."""
        pass
    
    async def test_archive_student_success(self):
        """Test successful student archiving."""
        pass
    
    async def test_search_students_with_filters(self):
        """Test student search with various filters."""
        pass
```

### 7.2 Integration Tests
```python
class TestStudentAPI:
    async def test_create_student_endpoint(self):
        """Test POST /api/v1/students endpoint."""
        pass
    
    async def test_get_student_endpoint(self):
        """Test GET /api/v1/students/{id} endpoint."""
        pass
    
    async def test_batch_import_endpoint(self):
        """Test POST /api/v1/students/batch-import endpoint."""
        pass
    
    async def test_student_export_endpoint(self):
        """Test GET /api/v1/students/export endpoint."""
        pass
```

### 7.3 E2E Tests
```typescript
describe('Student Management Flow', () => {
  it('should create a new student successfully', async () => {
    // 1. Navigate to student creation page
    // 2. Fill in required fields
    // 3. Add guardian information
    // 4. Submit form
    // 5. Verify success message
    // 6. Verify student appears in list
  });
  
  it('should edit student information', async () => {
    // 1. Navigate to student profile
    // 2. Click edit button
    // 3. Modify fields
    // 4. Save changes
    // 5. Verify changes reflected
  });
  
  it('should search for students', async () => {
    // 1. Enter search query
    // 2. Apply filters
    // 3. Verify search results
    // 4. Clear search
  });
});
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for SIS module
SIS_PERMISSIONS = {
    "school_admin": [
        "student:create",
        "student:read",
        "student:update",
        "student:archive",
        "student:import",
        "student:export",
        "guardian:create",
        "guardian:read",
        "guardian:update",
        "document:create",
        "document:read",
        "document:delete"
    ],
    "teacher": [
        "student:read",
        "student:read:class_only",
        "guardian:read:class_only"
    ],
    "nurse": [
        "student:read",
        "student:read:health_only",
        "document:create:medical",
        "document:read:medical"
    ],
    "bursar": [
        "student:read",
        "student:read:financial_summary"
    ],
    "parent": [
        "student:read:own_child",
        "guardian:read:own"
    ]
}
```

### 8.2 Data Privacy
```python
# Sensitive data handling
SENSITIVE_FIELDS = [
    "nin",  # National Identification Number
    "blood_group",
    "genotype",
    "chronic_conditions",
    "allergies",
    "current_medications",
    "emergency_notes"
]

# Encryption for sensitive fields
ENCRYPTED_FIELDS = [
    "nin",
    "emergency_notes"
]

# Access logging for sensitive data
SENSITIVE_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Student List Load:
    - Target: < 2 seconds for 1000 students
    - Pagination: 20 items per page
    - Search: < 1 second response time
  
  Student Creation:
    - Target: < 3 seconds
    - Includes: Validation, ID generation, guardian creation
  
  Batch Import:
    - Target: 100 students in < 30 seconds
    - Validation: Per student with error reporting
    - Rollback: On critical errors
  
  Student Search:
    - Target: < 500ms response time
    - Full-text search across name fields
    - Support for partial matches
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed data
CACHE_CONFIG = {
    "student_profile": {
        "ttl": 300,  # 5 minutes
        "key": "student:{student_id}:profile"
    },
    "student_list": {
        "ttl": 60,  # 1 minute
        "key": "school:{school_id}:students:page:{page}:filters:{filters_hash}"
    },
    "admission_number_sequence": {
        "ttl": 3600,  # 1 hour
        "key": "school:{school_id}:admission_sequence"
    }
}

# Cache invalidation on updates
async def invalidate_student_cache(student_id: UUID):
    """Invalidate all caches related to a student."""
    cache_keys = [
        f"student:{student_id}:profile",
        # Invalidate related caches
    ]
    await cache.delete_many(cache_keys)
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
INTEGRATIONS = {
    "attendance": {
        "student_id": "foreign key",
        "status_check": "student must be active",
        "notification": "on status change"
    },
    "academics": {
        "student_id": "foreign key",
        "class_validation": "student must be in class",
        "status_check": "student must be active"
    },
    "finance": {
        "student_id": "foreign key",
        "balance_check": "before transfer/archival",
        "notification": "on new student"
    },
    "health": {
        "student_id": "foreign key",
        "profile_sync": "health data linked to student",
        "notification": "on health alerts"
    },
    "sentinel": {
        "student_id": "foreign key",
        "attendance_data": "for surveillance analysis"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_INTEGRATIONS = {
    "termii": {
        "purpose": "SMS notifications",
        "triggers": ["student_created", "guardian_updated"]
    },
    "whatsapp": {
        "purpose": "WhatsApp notifications",
        "triggers": ["student_created", "status_change"]
    },
    "storage": {
        "purpose": "Document storage",
        "provider": "AWS S3 / Nigerian cloud",
        "security": "encrypted at rest"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create Student model and schema
- [ ] Implement StudentService with all methods
- [ ] Create Student API endpoints
- [ ] Implement guardian management
- [ ] Implement document management
- [ ] Add batch import/export functionality
- [ ] Implement search functionality
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create StudentList component
- [ ] Create StudentForm component
- [ ] Create StudentProfile component
- [ ] Create GuardianForm component
- [ ] Create DocumentUpload component
- [ ] Implement search and filters
- [ ] Add pagination
- [ ] Implement batch import UI
- [ ] Add export functionality
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Testing Tasks
- [ ] Unit tests for StudentService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for student workflow
- [ ] Performance testing
- [ ] Security testing
- [ ] Accessibility testing

### 11.4 Documentation Tasks
- [ ] API documentation
- [ ] User manual
- [ ] Admin guide
- [ ] Troubleshooting guide
- [ ] Video tutorials

---

*This module specification provides a comprehensive guide for implementing the Student Information System. Follow these requirements to ensure consistent implementation across the platform.*

---

**End of Student Information System (M1) Specification**