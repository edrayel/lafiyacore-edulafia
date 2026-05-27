# EduLafia Platform - Module Specification: Academic & Grading System (M2)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M2 - Academic & Grading System
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
The Academic & Grading System manages all academic activities including continuous assessment (CA) scores, examination scores, grade computation, class ranking, and report card generation. This module provides the academic foundation for student performance tracking and EMIS reporting.

### 1.2 Scope
- Subject configuration and management
- CA score entry and configuration
- Exam score entry
- Automatic grade computation
- Class rank calculation
- Report card generation
- Academic transcripts
- Performance analytics
- WAEC/NECO alignment
- Historical academic records

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information System)
- **Dependent Modules:** M7 (Parent Portal - for results viewing), M8 (Intelligence - for analytics)
- **External Dependencies:** PDF generation service, WhatsApp/SMS for notifications

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Subject Configuration
```yaml
Feature: Subject Configuration
Description: Configure subjects per class per term, aligned with WAEC/NECO
Acceptance Criteria:
  - Create subjects with school-specific codes
  - Align with WAEC/NECO subject lists for SS1-SS3
  - Configure subjects per class level
  - Mark subjects as core or elective
  - Support subject reassignment between teachers
  - Maintain subject history across academic years
```

#### 2.1.2 CA Score Entry
```yaml
Feature: Continuous Assessment Score Entry
Description: Enter and manage CA scores for students
Acceptance Criteria:
  - Support configurable CA components (classwork, assignment, mid-term)
  - Allow schools to configure CA weighting percentages
  - Real-time validation of scores against maximum marks
  - Running total visible during entry
  - Lock scores after configurable period (default: 2 weeks after term end)
  - Support bulk entry for entire class
  - Track score entry timestamps and teacher attribution
```

#### 2.1.3 Exam Score Entry
```yaml
Feature: Examination Score Entry
Description: Enter end-of-term examination scores
Acceptance Criteria:
  - Enter exam scores per student per subject
  - Validate scores against maximum exam marks
  - Automatic grade computation with configured formula
  - Flag incomplete results (students who missed exams)
  - Support re-examination scenarios
  - Prevent score entry for students not enrolled in subject
  - Support score moderation and approval workflow
```

#### 2.1.4 Grade Computation
```yaml
Feature: Automatic Grade Computation
Description: Calculate grades based on configured grading scale
Acceptance Criteria:
  - Apply WAEC/NECO standard grading scale (A1-F9)
  - Support custom grading scales per school
  - Calculate total score (CA + Exam)
  - Assign letter grade based on total score
  - Compute class rank for each subject
  - Compute overall class rank
  - Handle tie-breaking in rankings
  - Support special flags (ABS for absent, INC for incomplete)
```

#### 2.1.5 Report Card Generation
```yaml
Feature: Report Card Generation
Description: Generate comprehensive report cards
Acceptance Criteria:
  - Generate PDF report card per student per term
  - Include all subjects with CA, exam, total, grade, rank
  - Include attendance summary
  - Include teacher and principal remarks
  - Include school branding and seal
  - Generate only after all teachers submit scores
  - Support bulk generation for entire class
  - Deliver via WhatsApp/SMS to guardians
  - Store generated PDFs for historical access
```

#### 2.1.6 Academic Transcripts
```yaml
Feature: Academic Transcript Generation
Description: Generate complete academic history
Acceptance Criteria:
  - Generate transcript from admission to current class
  - Include all terms and subjects
  - Calculate cumulative GPA (optional)
  - School watermark and authentication
  - Export as PDF
  - Support transcript requests for transfers
  - Include examination body alignment (WAEC/NECO)
```

### 2.2 Business Rules

#### 2.2.1 CA Configuration Rules
```python
# Default CA configuration (school can customize)
DEFAULT_CA_CONFIG = {
    "components": [
        {"name": "classwork", "max_score": 10, "weight_percent": 10},
        {"name": "assignment", "max_score": 10, "weight_percent": 10},
        {"name": "mid_term", "max_score": 10, "weight_percent": 10}
    ],
    "total_ca_max": 30,
    "exam_max": 70,
    "total_max": 100
}

# Business rule: CA weight must sum to 30% or configurable total
# Business rule: Exam weight must be 70% or complementary to CA
# Business rule: Total must always be 100 for WAEC/NECO alignment
```

#### 2.2.2 Grading Scale Rules
```python
# WAEC/NECO standard grading scale
WAEC_GRADING_SCALE = [
    {"grade": "A1", "min_score": 75, "max_score": 100, "remark": "Excellent"},
    {"grade": "B2", "min_score": 70, "max_score": 74.99, "remark": "Very Good"},
    {"grade": "B3", "min_score": 65, "max_score": 69.99, "remark": "Good"},
    {"grade": "C4", "min_score": 60, "max_score": 64.99, "remark": "Credit"},
    {"grade": "C5", "min_score": 55, "max_score": 59.99, "remark": "Credit"},
    {"grade": "C6", "min_score": 50, "max_score": 54.99, "remark": "Credit"},
    {"grade": "D7", "min_score": 45, "max_score": 49.99, "remark": "Pass"},
    {"grade": "E8", "min_score": 40, "max_score": 44.99, "remark": "Pass"},
    {"grade": "F9", "min_score": 0, "max_score": 39.99, "remark": "Fail"}
]

# Business rule: Grades must be locked once term begins
# Business rule: Custom scales must have admin override with reason
# Business rule: Special flags (ABS, INC) don't affect class ranking
```

#### 2.2.3 Score Entry Business Rules
1. **Teacher Restriction:** Teachers can only enter scores for subjects and classes they are assigned to
2. **Lock Period:** Scores locked for admin editing after configurable period (default: 2 weeks after term end)
3. **Approval Workflow:** Score changes after lock period require admin approval with reason
4. **Incomplete Results:** Students who miss exams get 'INC' flag, not zero score
5. **Absent Students:** Students absent for entire exam get 'ABS' flag
6. **Ranking Exclusion:** ABS/INC flags exclude students from class ranking
7. **Submission Requirement:** Report cards generated only after all subject teachers submit scores

#### 2.2.4 Report Card Rules
1. **Completion Requirement:** All subject scores must be submitted before report card generation
2. **Attendance Integration:** Attendance summary must be included
3. **Health Remarks:** Nurse remarks included if health alerts exist
4. **Principal Remarks:** Manual input required, not auto-generated
5. **Delivery:** WhatsApp delivery required, email optional
6. **Storage:** Generated PDFs stored for 7 years minimum
7. **Bulk Generation:** Support batch generation for entire class

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Subjects table
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL,
    description TEXT,
    is_core BOOLEAN DEFAULT TRUE,
    waec_code VARCHAR(20),
    neco_code VARCHAR(20),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, code)
);

-- Academic results table (from data-model.md)
CREATE TABLE academic_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    term_id UUID NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    ca_scores JSONB DEFAULT '{}',
    ca_total DECIMAL(5, 2),
    exam_score DECIMAL(5, 2),
    total_score DECIMAL(5, 2),
    grade VARCHAR(5),
    class_rank INTEGER,
    flag VARCHAR(10) CHECK (flag IN ('ABS', 'INC', 'CHEAT')),
    teacher_id UUID REFERENCES staff(id),
    submitted_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, subject_id, term_id)
);

-- Grading scales table
CREATE TABLE grading_scales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Grading scale details
CREATE TABLE grading_scale_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grading_scale_id UUID NOT NULL REFERENCES grading_scales(id) ON DELETE CASCADE,
    grade VARCHAR(5) NOT NULL,
    min_score DECIMAL(5, 2) NOT NULL,
    max_score DECIMAL(5, 2) NOT NULL,
    remark VARCHAR(50),
    position INTEGER NOT NULL,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Report cards table
CREATE TABLE report_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    term_id UUID NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    overall_average DECIMAL(5, 2),
    class_rank INTEGER,
    total_students INTEGER,
    attendance_summary JSONB,
    nurse_remark TEXT,
    principal_remark TEXT,
    generated_at TIMESTAMP WITH TIME ZONE,
    pdf_url VARCHAR(500),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, term_id)
);

-- CA configuration table
CREATE TABLE ca_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    term_id UUID NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    components JSONB NOT NULL DEFAULT '[]',
    total_ca_max DECIMAL(5, 2) NOT NULL DEFAULT 30,
    exam_max DECIMAL(5, 2) NOT NULL DEFAULT 70,
    total_max DECIMAL(5, 2) NOT NULL DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 3.2 Indexes for Academic Performance
```sql
-- Performance indexes for academic queries
CREATE INDEX idx_academic_results_student_term ON academic_results(student_id, term_id);
CREATE INDEX idx_academic_results_subject_term ON academic_results(subject_id, term_id);
CREATE INDEX idx_academic_results_class_term ON academic_results(class_id, term_id);
CREATE INDEX idx_academic_results_school_term ON academic_results(school_id, term_id);
CREATE INDEX idx_academic_results_grade ON academic_results(grade);

-- Unique constraint to prevent duplicate results
CREATE UNIQUE INDEX idx_academic_results_unique 
    ON academic_results(student_id, subject_id, term_id) 
    WHERE deleted_at IS NULL;

-- Report card indexes
CREATE INDEX idx_report_cards_student_term ON report_cards(student_id, term_id);
CREATE INDEX idx_report_cards_class_term ON report_cards(class_id, term_id);
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Subject Management Endpoints
```yaml
Endpoints:
  POST /api/v1/subjects:
    - Description: Create a new subject
    - Request Body: SubjectCreate schema
    - Response: SubjectResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Subject code must be unique within school
      - WAEC/NECO codes optional but recommended for SS1-SS3
    - Side Effects: None

  GET /api/v1/subjects:
    - Description: List subjects for school
    - Query Parameters: school_id, class_level, is_core
    - Response: List of SubjectResponse
    - Auth: Required

  GET /api/v1/subjects/{subject_id}:
    - Description: Get subject details
    - Response: SubjectDetailResponse
    - Auth: Required

  PATCH /api/v1/subjects/{subject_id}:
    - Description: Update subject
    - Request Body: SubjectUpdate schema
    - Auth: Required (school_admin)

  DELETE /api/v1/subjects/{subject_id}:
    - Description: Archive subject (soft delete)
    - Auth: Required (school_admin)
    - Business Rule: Cannot delete if active results exist
```

#### 4.1.2 CA Score Endpoints
```yaml
Endpoints:
  POST /api/v1/academics/ca-scores:
    - Description: Enter CA scores for class
    - Request Body: CAScoreEntry schema
    - Response: CAScoreResult schema
    - Auth: Required (teacher)
    - Business Rules:
      - Teacher must be assigned to subject and class
      - Scores validated against configured max scores
      - Running total calculated automatically
    - Side Effects:
      - Update academic_results table
      - Log score entry in audit trail
      - Trigger grade recalculation

  GET /api/v1/academics/ca-scores:
    - Description: Get CA scores for student/class
    - Query Parameters: student_id, class_id, subject_id, term_id
    - Response: List of CAScoreResponse
    - Auth: Required

  PUT /api/v1/academics/ca-scores/{result_id}:
    - Description: Update CA scores
    - Request Body: CAScoreUpdate schema
    - Auth: Required (teacher, school_admin)
    - Business Rules:
      - Check if scores are locked
      - Require admin override if locked
```

#### 4.1.3 Exam Score Endpoints
```yaml
Endpoints:
  POST /api/v1/academics/exam-scores:
    - Description: Enter exam scores for class
    - Request Body: ExamScoreEntry schema
    - Response: ExamScoreResult schema
    - Auth: Required (teacher)
    - Business Rules:
      - Validate scores against exam max
      - Flag students who missed exam as 'INC'
      - Calculate total score and grade
    - Side Effects:
      - Update academic_results table
      - Recalculate class ranks
      - Log score entry

  GET /api/v1/academics/exam-scores:
    - Description: Get exam scores
    - Query Parameters: student_id, class_id, subject_id, term_id
    - Response: List of ExamScoreResponse
    - Auth: Required
```

#### 4.1.4 Grade Computation Endpoints
```yaml
Endpoints:
  POST /api/v1/academics/grades/compute:
    - Description: Compute grades for class/term
    - Request Body: { "class_id": "...", "term_id": "..." }
    - Response: ComputationResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Apply grading scale
      - Calculate class ranks
      - Handle ABS/INC flags
    - Side Effects:
      - Update grades in academic_results
      - Update class_rank field
      - Log computation

  GET /api/v1/academics/grades/scales:
    - Description: Get grading scales for school
    - Query Parameters: school_id
    - Response: List of GradingScaleResponse
    - Auth: Required

  POST /api/v1/academics/grades/scales:
    - Description: Create custom grading scale
    - Request Body: GradingScaleCreate schema
    - Auth: Required (school_admin)
    - Business Rules:
      - No overlapping score ranges
      - All ranges must cover 0-100
```

#### 4.1.5 Report Card Endpoints
```yaml
Endpoints:
  POST /api/v1/academics/report-cards/generate:
    - Description: Generate report cards for class
    - Request Body: ReportCardGenerate schema
    - Response: GenerationResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - All subject scores must be submitted
      - Attendance data must be available
      - Nurse/principal remarks required
    - Side Effects:
      - Generate PDF for each student
      - Upload to storage
      - Send WhatsApp notification to guardians
      - Log generation

  GET /api/v1/academics/report-cards/{report_card_id}:
    - Description: Get report card details
    - Response: ReportCardResponse
    - Auth: Required

  GET /api/v1/academics/report-cards/{report_card_id}/pdf:
    - Description: Download report card PDF
    - Response: PDF file
    - Auth: Required
    - Business Rules:
      - Access controlled by role/relationship

  POST /api/v1/academics/report-cards/bulk-generate:
    - Description: Generate report cards for multiple students
    - Request Body: { "student_ids": [...], "term_id": "..." }
    - Response: BulkGenerationResult schema
    - Auth: Required (school_admin)
```

#### 4.1.6 Academic Transcript Endpoints
```yaml
Endpoints:
  GET /api/v1/academics/transcripts/{student_id}:
    - Description: Generate academic transcript
    - Query Parameters: format (pdf, json)
    - Response: Transcript data or PDF
    - Auth: Required
    - Business Rules:
      - Include all terms from admission
      - Calculate cumulative statistics
      - School watermark on PDF

  GET /api/v1/academics/transcripts/{student_id}/download:
    - Description: Download transcript PDF
    - Response: PDF file
    - Auth: Required
```

#### 4.1.7 Academic Analytics Endpoints
```yaml
Endpoints:
  GET /api/v1/academics/analytics/class-performance:
    - Description: Get class performance analytics
    - Query Parameters: class_id, term_id
    - Response: ClassPerformance schema
    - Includes:
      - Subject mean scores
      - Grade distribution
      - Top/bottom performers
      - Pass/fail rates

  GET /api/v1/academics/analytics/student-trend:
    - Description: Get student performance trend
    - Query Parameters: student_id
    - Response: StudentTrend schema
    - Includes:
      - Term-wise averages
      - Subject-wise performance
      - Improvement/decline indicators

  GET /api/v1/academics/analytics/subject-comparison:
    - Description: Compare subject performance
    - Query Parameters: school_id, term_id, class_level
    - Response: SubjectComparison schema
```

## 5. Business Logic Implementation

### 5.1 Grade Computation Logic
```python
class GradeComputationService:
    async def compute_grades(
        self,
        class_id: UUID,
        term_id: UUID,
        school_id: UUID
    ) -> ComputationResult:
        """Compute grades for all students in a class."""
        
        # 1. Get grading scale
        grading_scale = await self.get_grading_scale(school_id)
        
        # 2. Get all results for class
        results = await self.get_class_results(class_id, term_id)
        
        # 3. Compute grade for each result
        for result in results:
            if result.flag in ['ABS', 'INC']:
                continue
                
            # Calculate grade based on total score
            grade_info = self.calculate_grade(
                result.total_score, 
                grading_scale
            )
            result.grade = grade_info['grade']
        
        # 4. Calculate class ranks
        await self.calculate_class_ranks(results)
        
        # 5. Save results
        await self.save_results(results)
        
        return ComputationResult(
            processed=len(results),
            graded=len([r for r in results if r.grade]),
            flagged=len([r for r in results if r.flag])
        )
    
    def calculate_grade(self, score: float, grading_scale: List) -> dict:
        """Calculate grade from score using grading scale."""
        for grade_detail in grading_scale:
            if grade_detail['min_score'] <= score <= grade_detail['max_score']:
                return grade_detail
        return {'grade': 'F9', 'remark': 'Fail'}
    
    async def calculate_class_ranks(self, results: List[AcademicResult]):
        """Calculate class ranks for each subject and overall."""
        # Group by subject
        subject_groups = {}
        for result in results:
            if result.subject_id not in subject_groups:
                subject_groups[result.subject_id] = []
            subject_groups[result.subject_id].append(result)
        
        # Calculate subject ranks
        for subject_id, subject_results in subject_groups.items():
            # Sort by total score descending
            sorted_results = sorted(
                subject_results, 
                key=lambda x: x.total_score or 0, 
                reverse=True
            )
            
            # Assign ranks, handling ties
            current_rank = 1
            for i, result in enumerate(sorted_results):
                if i > 0 and result.total_score < sorted_results[i-1].total_score:
                    current_rank = i + 1
                result.class_rank = current_rank
        
        # Calculate overall ranks
        student_averages = {}
        for result in results:
            if result.student_id not in student_averages:
                student_averages[result.student_id] = []
            if result.total_score and result.flag not in ['ABS', 'INC']:
                student_averages[result.student_id].append(result.total_score)
        
        # Calculate average per student
        student_avg_list = []
        for student_id, scores in student_averages.items():
            if scores:
                avg = sum(scores) / len(scores)
                student_avg_list.append((student_id, avg))
        
        # Sort and assign overall ranks
        student_avg_list.sort(key=lambda x: x[1], reverse=True)
        current_rank = 1
        for i, (student_id, avg) in enumerate(student_avg_list):
            if i > 0 and avg < student_avg_list[i-1][1]:
                current_rank = i + 1
            # Update all results for this student with overall rank
            for result in results:
                if result.student_id == student_id:
                    result.overall_rank = current_rank
```

### 5.2 Report Card Generation Logic
```python
class ReportCardService:
    async def generate_report_card(
        self,
        student_id: UUID,
        term_id: UUID,
        principal_remark: Optional[str] = None,
        nurse_remark: Optional[str] = None
    ) -> ReportCard:
        """Generate report card for a student."""
        
        # 1. Validate all scores submitted
        if not await self.validate_scores_submitted(student_id, term_id):
            raise ValidationError("All subject scores must be submitted")
        
        # 2. Get student info
        student = await self.student_service.get_student(student_id)
        
        # 3. Get academic results
        results = await self.get_student_results(student_id, term_id)
        
        # 4. Get attendance summary
        attendance_summary = await self.attendance_service.get_summary(
            student_id, term_id
        )
        
        # 5. Calculate overall average
        valid_results = [r for r in results if r.flag not in ['ABS', 'INC']]
        if valid_results:
            overall_average = sum(r.total_score for r in valid_results) / len(valid_results)
        else:
            overall_average = 0
        
        # 6. Create report card record
        report_card = ReportCard(
            student_id=student_id,
            term_id=term_id,
            academic_year_id=results[0].academic_year_id if results else None,
            class_id=results[0].class_id if results else None,
            school_id=student.school_id,
            overall_average=overall_average,
            attendance_summary=attendance_summary,
            principal_remark=principal_remark,
            nurse_remark=nurse_remark
        )
        
        self.session.add(report_card)
        await self.session.flush()
        
        # 7. Generate PDF
        pdf_url = await self.generate_pdf(report_card, student, results)
        report_card.pdf_url = pdf_url
        report_card.generated_at = datetime.utcnow()
        
        # 8. Send to guardians
        await self.notify_guardians(student, report_card)
        
        await self.session.commit()
        return report_card
    
    async def generate_pdf(
        self, 
        report_card: ReportCard, 
        student: Student, 
        results: List[AcademicResult]
    ) -> str:
        """Generate PDF report card."""
        # Implementation using PDF library (e.g., WeasyPrint, ReportLab)
        # Include school branding, student info, results table
        # Upload to cloud storage and return URL
        pass
    
    async def notify_guardians(self, student: Student, report_card: ReportCard):
        """Send report card to guardians via WhatsApp."""
        guardians = await self.get_student_guardians(student.id)
        for guardian in guardians:
            if guardian.whatsapp_phone:
                await self.whatsapp_service.send_report_card(
                    guardian.whatsapp_phone,
                    student,
                    report_card
                )
```

### 5.3 Score Submission Validation
```python
class ScoreSubmissionService:
    async def validate_scores_submitted(
        self, 
        student_id: UUID, 
        term_id: UUID
    ) -> bool:
        """Validate all subject scores are submitted for student."""
        
        # 1. Get student's class
        student = await self.student_service.get_student(student_id)
        class_id = student.class_id
        
        # 2. Get all subjects for class
        subjects = await self.get_class_subjects(class_id, term_id)
        
        # 3. Check if all subjects have scores
        submitted_subjects = await self.get_submitted_subjects(
            student_id, term_id
        )
        
        # 4. Compare
        missing_subjects = set(subjects) - set(submitted_subjects)
        
        if missing_subjects:
            raise ValidationError(
                f"Missing scores for subjects: {', '.join(missing_subjects)}"
            )
        
        return True
    
    async def validate_teacher_access(
        self, 
        teacher_id: UUID, 
        subject_id: UUID, 
        class_id: UUID
    ) -> bool:
        """Validate teacher is assigned to subject and class."""
        assignment = await self.session.execute(
            select(StaffClassAssignment)
            .where(
                StaffClassAssignment.staff_id == teacher_id,
                StaffClassAssignment.class_id == class_id,
                StaffClassAssignment.subject_id == subject_id,
                StaffClassAssignment.is_active == True
            )
        )
        return assignment.scalar() is not None
```

## 6. UI Component Specifications

### 6.1 Score Entry Component
```typescript
interface ScoreEntryProps {
  classId: string;
  subjectId: string;
  termId: string;
  teacherId: string;
  onScoresSubmitted: () => void;
}

// Component Requirements:
// 1. Display student list with score input fields
// 2. CA component input fields (configurable)
// 3. Exam score input field
// 4. Real-time validation against max scores
// 5. Running total calculation
// 6. Bulk save functionality
// 7. Lock indicator for submitted scores
// 8. Export to Excel option
```

### 6.2 Report Card Preview Component
```typescript
interface ReportCardPreviewProps {
  studentId: string;
  termId: string;
  onGenerate: () => void;
  onSendToGuardians: () => void;
}

// Preview Sections:
// 1. Student header (photo, name, class)
// 2. Results table (subjects, CA, exam, total, grade, rank)
// 3. Overall average and class rank
// 4. Attendance summary
// 5. Remarks section (teacher, nurse, principal)
// 6. Generate PDF button
// 7. Send to guardians button
// 8. Print preview option
```

### 6.3 Academic Analytics Dashboard
```typescript
interface AcademicAnalyticsProps {
  schoolId: string;
  termId: string;
  classId?: string;
}

// Dashboard Components:
// 1. Class performance overview
// 2. Grade distribution chart
// 3. Subject performance comparison
// 4. Top performers list
// 5. At-risk students list
// 6. Performance trends over time
// 7. Pass/fail rates by subject
// 8. Export analytics report
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for GradeComputationService
class TestGradeComputationService:
    async def test_compute_grades_success(self):
        """Test successful grade computation."""
        pass
    
    async def test_calculate_grade_waec_scale(self):
        """Test grade calculation with WAEC scale."""
        pass
    
    async def test_calculate_class_ranks_with_ties(self):
        """Test rank calculation with tied scores."""
        pass
    
    async def test_handle_absent_students(self):
        """Test handling of absent students (ABS flag)."""
        pass
    
    async def test_handle_incomplete_results(self):
        """Test handling of incomplete results (INC flag)."""
        pass

# Test cases for ReportCardService
class TestReportCardService:
    async def test_generate_report_card_success(self):
        """Test successful report card generation."""
        pass
    
    async def test_generate_report_card_missing_scores_fails(self):
        """Test report card fails when scores missing."""
        pass
    
    async def test_notify_guardians_via_whatsapp(self):
        """Test WhatsApp notification to guardians."""
        pass
```

### 7.2 Integration Tests
```python
class TestAcademicAPI:
    async def test_ca_score_entry_endpoint(self):
        """Test POST /api/v1/academics/ca-scores endpoint."""
        pass
    
    async def test_exam_score_entry_endpoint(self):
        """Test POST /api/v1/academics/exam-scores endpoint."""
        pass
    
    async def test_report_card_generation_endpoint(self):
        """Test POST /api/v1/academics/report-cards/generate endpoint."""
        pass
    
    async def test_grade_computation_endpoint(self):
        """Test POST /api/v1/academics/grades/compute endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Academic module
ACADEMIC_PERMISSIONS = {
    "school_admin": [
        "academic:create",
        "academic:read",
        "academic:update",
        "academic:delete",
        "academic:compute_grades",
        "academic:generate_reports",
        "academic:configure_ca"
    ],
    "teacher": [
        "academic:read:class_only",
        "academic:create:ca_scores:own_subject",
        "academic:create:exam_scores:own_subject",
        "academic:read:own_subject_results"
    ],
    "nurse": [
        "academic:read:health_remarks"
    ],
    "bursar": [
        "academic:read:summary"
    ],
    "parent": [
        "academic:read:own_child",
        "academic:read:report_card:own_child"
    ],
    "student": [
        "academic:read:own_results"
    ]
}
```

### 8.2 Data Privacy
```python
# Sensitive academic data handling
SENSITIVE_ACADEMIC_DATA = [
    "individual_scores",  # Individual student scores
    "class_ranks",        # Class rankings
    "performance_trends", # Student performance trends
    "at_risk_students"    # Students at risk of failure
]

# Access logging for sensitive data
ACADEMIC_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Score Entry:
    - Target: < 2 seconds for single student entry
    - Target: < 10 seconds for bulk entry (45 students)
    - Validation: Real-time (< 100ms)
  
  Grade Computation:
    - Target: < 5 seconds for class of 45 students
    - Target: < 30 seconds for entire school
    - Ranking: Include in computation time
  
  Report Card Generation:
    - Target: < 30 seconds per student
    - Target: < 5 minutes for class of 45 students
    - PDF Generation: Include in timing
  
  Academic Analytics:
    - Target: < 3 seconds for class analytics
    - Target: < 10 seconds for school analytics
    - Caching: 1-hour cache for historical data
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed academic data
ACADEMIC_CACHE_CONFIG = {
    "grading_scale": {
        "ttl": 3600,  # 1 hour
        "key": "school:{school_id}:grading_scale"
    },
    "class_results": {
        "ttl": 300,  # 5 minutes
        "key": "class:{class_id}:term:{term_id}:results"
    },
    "student_transcript": {
        "ttl": 86400,  # 24 hours
        "key": "student:{student_id}:transcript"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
ACADEMIC_INTEGRATIONS = {
    "sis": {
        "student_data": "student enrollment, class assignment",
        "validation": "student must be active and enrolled"
    },
    "attendance": {
        "attendance_summary": "include in report cards",
        "absence_flags": "trigger INC flags for absent students"
    },
    "finance": {
        "academic_status": "check for fee clearance before results release",
        "scholarship_eligibility": "based on academic performance"
    },
    "health": {
        "health_alerts": "nurse remarks in report cards",
        "screening_results": "vision/hearing impact on academics"
    },
    "sentinel": {
        "absence_patterns": "correlate with academic performance",
        "illness_impact": "analyze impact on grades"
    },
    "parent_portal": {
        "results_delivery": "send report cards via WhatsApp",
        "performance_alerts": "notify parents of academic decline"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_ACADEMIC_INTEGRATIONS = {
    "pdf_generation": {
        "purpose": "Generate PDF report cards",
        "provider": "WeasyPrint or ReportLab",
        "security": "no data retention by provider"
    },
    "whatsapp": {
        "purpose": "Deliver report cards to parents",
        "templates": "report_card_notification",
        "rate_limiting": "respect WhatsApp limits"
    },
    "waec_neco": {
        "purpose": "Future exam result integration",
        "status": "planned for phase 2",
        "format": "API or batch import"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create Subject model and schema
- [ ] Create AcademicResult model and schema
- [ ] Create GradingScale model and schema
- [ ] Create ReportCard model and schema
- [ ] Implement GradeComputationService
- [ ] Implement ReportCardService
- [ ] Implement ScoreSubmissionService
- [ ] Create academic API endpoints
- [ ] Add CA score entry functionality
- [ ] Add exam score entry functionality
- [ ] Implement grade computation logic
- [ ] Implement report card generation
- [ ] Add academic transcript generation
- [ ] Add performance analytics
- [ ] Implement WhatsApp notifications
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create ScoreEntry component
- [ ] Create ReportCardPreview component
- [ ] Create AcademicAnalyticsDashboard component
- [ ] Create SubjectManagement component
- [ ] Create GradeScaleConfiguration component
- [ ] Implement real-time score validation
- [ ] Add bulk score entry
- [ ] Implement PDF preview
- [ ] Add export functionality
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Testing Tasks
- [ ] Unit tests for GradeComputationService
- [ ] Unit tests for ReportCardService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for academic workflow
- [ ] Performance testing
- [ ] Security testing

---

*This module specification provides a comprehensive guide for implementing the Academic & Grading System. Follow these requirements to ensure proper implementation that aligns with WAEC/NECO standards and Nigerian educational requirements.*

---

**End of Academic & Grading System (M2) Specification**