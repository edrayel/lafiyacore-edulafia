# EduLafia Platform - Module Specification: Teacher & Staff Management (M6)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M6 - Teacher & Staff Management
- **Priority:** Medium (Extended Module)

## 1. Module Overview

### 1.1 Purpose
The Teacher & Staff Management module provides comprehensive HR management for school staff including profile management, class and subject assignments, timetable construction, teacher attendance tracking, and staff communications. This module enables efficient school operations and teacher accountability.

### 1.2 Scope
- Staff profile management (teachers and non-teaching staff)
- Class and subject assignments
- Timetable builder with clash detection
- Timetable publication and viewing
- Teacher attendance tracking
- Staff communications and broadcasts
- Qualification and certification tracking
- Employment type management (permanent, contract, NYSC)

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information System)
- **Dependent Modules:** M2 (Academics - for teacher assignments), M3 (Attendance - for teacher marking)
- **External Dependencies:** WhatsApp for staff notifications

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Staff Profile Management
```yaml
Feature: Staff Profile Management
Description: Create and manage comprehensive staff profiles
Acceptance Criteria:
  - Full staff profile with personal and professional details
  - Staff ID generation (school-prefixed, sequential)
  - Qualifications and certifications
  - Subjects qualified for (with evidence)
  - Employment type: permanent, contract, NYSC, intern
  - Employment date and status
  - Contact information (phone, email, WhatsApp)
  - Next of kin/emergency contact
  - Document uploads (credentials, certificates)
  - Profile photo upload
  - Role-based access assignment
  - Staff status management (active, inactive, retired, terminated)
```

#### 2.1.2 Class and Subject Assignment
```yaml
Feature: Class and Subject Assignment
Description: Assign teachers to classes and subjects
Acceptance Criteria:
  - Assign teacher to specific classes (form teacher role)
  - Assign teacher to specific subjects per class
  - Multiple assignments per teacher
  - Academic year and term specific assignments
  - Override capability for substitute teachers
  - Assignment history tracking
  - Validation against teacher qualifications
  - Impact on attendance and grading module access
  - Bulk assignment capability
```

#### 2.1.3 Timetable Builder
```yaml
Feature: Timetable Builder
Description: Build and manage school timetables
Acceptance Criteria:
  - Drag-and-drop timetable construction
  - Clash detection (same teacher in two places; same class in two places)
  - Period configuration (start/end times, break periods)
  - Support for different timetable templates per class level
  - Room allocation (optional)
  - Teacher availability constraints
  - Save as draft before publishing
  - Copy timetable from previous term/year
  - Print-friendly timetable view
  - Mobile-optimized viewing
```

#### 2.1.4 Timetable Publication
```yaml
Feature: Timetable Publication
Description: Publish timetables for staff and student viewing
Acceptance Criteria:
  - Publish timetable to all affected teachers
  - Publish timetable to students in their portals
  - WhatsApp notification on publication
  - Update notifications when timetable changes
  - Version history for timetables
  - Effective date for timetable changes
  - Temporary timetable support (for exam periods, events)
  - Print/export capabilities
```

#### 2.1.5 Teacher Attendance Tracking
```yaml
Feature: Teacher Attendance Tracking
Description: Track teacher attendance and punctuality
Acceptance Criteria:
  - Daily teacher attendance register
  - Check-in/check-out timestamps
  - Multiple check-in methods: manual, QR code, geofencing
  - Late arrival flagging (configurable threshold)
  - Early departure flagging
  - Absence reason capture
  - Monthly attendance summary
  - Pattern detection (chronic absenteeism)
  - Integration with payroll (future)
  - Privacy controls (only admin sees full data)
```

#### 2.1.6 Staff Communications
```yaml
Feature: Staff Communications
Description: Internal communication tools for staff
Acceptance Criteria:
  - In-app messaging system
  - WhatsApp broadcast to all staff
  - Targeted broadcasts (by role, department, class)
  - Announcement board
  - Meeting scheduler
  - Document sharing
  - Read receipts for important communications
  - Acknowledgement required for critical announcements
  - Communication history and search
```

### 2.2 Business Rules

#### 2.2.1 Staff Profile Business Rules
1. **Unique Staff ID:** System-generated, school-prefixed, sequential format
2. **Qualification Validation:** Teaching staff must have minimum qualification (NCE, B.Ed, etc.)
3. **Employment Types:** Different rules for permanent, contract, NYSC staff
4. **Access Control:** Staff roles determine system access levels
5. **Document Retention:** Employment documents retained for 7 years after exit
6. **Background Check:** Optional but recommended for new hires
7. **Probation Period:** Configurable probation period for new staff

#### 2.2.2 Assignment Business Rules
1. **Qualification Check:** Teacher can only be assigned to subjects they're qualified for
2. **Maximum Load:** Configurable maximum teaching load per teacher (e.g., 30 periods/week)
3. **Form Teacher:** Each class must have exactly one form teacher
4. **Substitute Assignments:** Temporary assignments with start and end dates
5. **Assignment Conflict:** Cannot assign same teacher to overlapping periods
6. **Academic Year Reset:** Assignments reset each academic year (can copy from previous)
7. **Principal Override:** Principal can override qualification restrictions with justification

#### 2.2.3 Timetable Business Rules
1. **Clash Prevention:** System prevents scheduling clashes
2. **Break Periods:** Configurable break periods that cannot be scheduled
3. **Period Duration:** Standard period duration configurable per school
4. **Maximum Periods:** Maximum teaching periods per day per class
5. **Teacher Availability:** Teachers can mark unavailable periods
6. **Publication Requirement:** Timetable must be published before term begins
7. **Change Notification:** Teachers notified of timetable changes

#### 2.2.4 Attendance Business Rules
1. **Check-in Window:** Configurable check-in window (e.g., 7:00-8:00 AM)
2. **Late Threshold:** Configurable late threshold (e.g., 15 minutes after start)
3. **Absence Reason:** Required for absences
4. **Leave Management:** Integration with leave application system
5. **Monthly Report:** Automated monthly attendance report
6. **Chronic Absence:** Flag at >3 days unexcused absence per month
7. **Privacy:** Individual teacher attendance visible only to admin and the teacher

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Staff table
CREATE TABLE staff (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),  -- System access account
    staff_id VARCHAR(50) NOT NULL,  -- School-prefixed, sequential
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    whatsapp_phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')),
    address TEXT,
    photo_url VARCHAR(500),
    role VARCHAR(50) NOT NULL CHECK (role IN ('teacher', 'nurse', 'bursar', 'admin', 'accountant', 'librarian', 'lab_attendant', 'security', 'cleaner', 'other')),
    department VARCHAR(100),
    qualifications JSONB,  -- Array of qualification objects
    subjects UUID[],  -- Array of subject IDs qualified for
    employment_type VARCHAR(20) DEFAULT 'permanent' CHECK (employment_type IN ('permanent', 'contract', 'nysc', 'intern')),
    employment_date DATE,
    exit_date DATE,
    exit_reason VARCHAR(100),
    salary DECIMAL(12,2),
    bank_details JSONB,  -- Encrypted
    next_of_kin JSONB,
    emergency_contact JSONB,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'on_leave', 'terminated', 'retired')),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, staff_id)
);

-- Staff class assignments
CREATE TABLE staff_class_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    subject_id UUID REFERENCES subjects(id),
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    term_id UUID REFERENCES terms(id),
    assignment_type VARCHAR(20) DEFAULT 'regular' CHECK (assignment_type IN ('regular', 'substitute', 'temporary')),
    is_form_teacher BOOLEAN DEFAULT FALSE,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(staff_id, class_id, subject_id, academic_year_id)
);

-- Timetables
CREATE TABLE timetables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    term_id UUID NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    effective_from DATE NOT NULL,
    effective_to DATE,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE,
    published_by UUID REFERENCES users(id),
    version_number INTEGER DEFAULT 1,
    is_draft BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(class_id, academic_year_id, term_id, version_number)
);

-- Timetable entries
CREATE TABLE timetable_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timetable_id UUID NOT NULL REFERENCES timetables(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),  -- 1=Monday, 7=Sunday
    period_number INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    room_number VARCHAR(50),
    notes TEXT,
    is_break BOOLEAN DEFAULT FALSE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(timetable_id, day_of_week, period_number)
);

-- Indexes for timetable
CREATE INDEX idx_timetable_entries_staff ON timetable_entries(staff_id, day_of_week, period_number);
CREATE INDEX idx_timetable_entries_subject ON timetable_entries(subject_id);
CREATE INDEX idx_timetable_entries_timetable ON timetable_entries(timetable_id);

-- Teacher attendance
CREATE TABLE teacher_attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    check_in_time TIMESTAMP WITH TIME ZONE,
    check_out_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused', 'on_leave')),
    check_in_method VARCHAR(20) CHECK (check_in_method IN ('manual', 'qr_code', 'geofencing')),
    late_minutes INTEGER,
    early_departure_minutes INTEGER,
    reason_code VARCHAR(50),
    notes TEXT,
    recorded_by UUID REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    UNIQUE(staff_id, date)
);

-- Indexes for teacher attendance
CREATE INDEX idx_teacher_attendance_staff_date ON teacher_attendance(staff_id, date);
CREATE INDEX idx_teacher_attendance_school_date ON teacher_attendance(school_id, date);
CREATE INDEX idx_teacher_attendance_status ON teacher_attendance(status, date);

-- Staff communications
CREATE TABLE staff_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id),
    communication_type VARCHAR(50) NOT NULL CHECK (communication_type IN ('announcement', 'broadcast', 'message', 'meeting')),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    target_audience JSONB,  -- {roles: [], departments: [], individual_ids: []}
    channels TEXT[] DEFAULT ARRAY['in_app'],
    requires_acknowledgement BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    scheduled_for TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Communication recipients (for tracking)
CREATE TABLE communication_recipients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    communication_id UUID NOT NULL REFERENCES staff_communications(id) ON DELETE CASCADE,
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'sent' CHECK (status IN ('sent', 'delivered', 'read', 'acknowledged')),
    sent_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    UNIQUE(communication_id, staff_id)
);
```

### 3.2 Views for Staff Reporting
```sql
-- Staff assignment summary view
CREATE VIEW staff_assignment_summary AS
SELECT 
    s.id as staff_id,
    s.school_id,
    s.first_name,
    s.last_name,
    s.role,
    s.employment_type,
    COUNT(DISTINCT sca.class_id) as classes_assigned,
    COUNT(DISTINCT sca.subject_id) as subjects_assigned,
    COUNT(DISTINCT te.id) as periods_per_week,
    s.status
FROM staff s
LEFT JOIN staff_class_assignments sca ON s.id = sca.staff_id AND sca.is_active = TRUE
LEFT JOIN timetable_entries te ON s.id = te.staff_id
WHERE s.deleted_at IS NULL
GROUP BY s.id, s.school_id, s.first_name, s.last_name, s.role, s.employment_type, s.status;

-- Teacher attendance summary view
CREATE VIEW teacher_attendance_summary AS
SELECT 
    ta.staff_id,
    ta.school_id,
    DATE_TRUNC('month', ta.date) as month,
    COUNT(*) as total_days,
    COUNT(CASE WHEN ta.status = 'present' THEN 1 END) as present_days,
    COUNT(CASE WHEN ta.status = 'absent' THEN 1 END) as absent_days,
    COUNT(CASE WHEN ta.status = 'late' THEN 1 END) as late_days,
    COUNT(CASE WHEN ta.status = 'excused' THEN 1 END) as excused_days,
    AVG(ta.late_minutes) as avg_late_minutes,
    ROUND(
        COUNT(CASE WHEN ta.status = 'present' THEN 1 END) * 100.0 / COUNT(*),
        2
    ) as attendance_rate
FROM teacher_attendance ta
WHERE ta.deleted_at IS NULL
GROUP BY ta.staff_id, ta.school_id, DATE_TRUNC('month', ta.date);

-- Class teacher assignment view
CREATE VIEW class_teacher_assignments AS
SELECT 
    c.id as class_id,
    c.name as class_name,
    c.school_id,
    s.id as teacher_id,
    s.first_name,
    s.last_name,
    s.phone,
    s.whatsapp_phone
FROM classes c
JOIN staff_class_assignments sca ON c.id = sca.class_id AND sca.is_form_teacher = TRUE
JOIN staff s ON sca.staff_id = s.id
WHERE s.deleted_at IS NULL AND sca.is_active = TRUE;
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Staff Profile Endpoints
```yaml
Endpoints:
  POST /api/v1/staff:
    - Description: Create a new staff member
    - Request Body: StaffCreate schema
    - Response: StaffResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Generate unique staff ID
      - Create user account if email provided
      - Assign default role-based access
    - Side Effects:
      - Create staff record
      - Create user account (optional)
      - Send welcome notification

  GET /api/v1/staff:
    - Description: List staff for school
    - Query Parameters: school_id, role, department, status, employment_type
    - Response: Paginated list of StaffResponse
    - Auth: Required

  GET /api/v1/staff/{staff_id}:
    - Description: Get staff details
    - Response: StaffDetailResponse
    - Auth: Required

  PATCH /api/v1/staff/{staff_id}:
    - Description: Update staff information
    - Request Body: StaffUpdate schema
    - Auth: Required (school_admin, self)
    - Business Rules:
      - Staff can update own contact info
      - Admin can update all fields
      - Sensitive fields (salary) require admin

  POST /api/v1/staff/{staff_id}/documents:
    - Description: Upload staff document
    - Request Body: Multipart form with file
    - Query Parameters: document_type
    - Response: DocumentResponse schema
    - Auth: Required (school_admin)

  POST /api/v1/staff/{staff_id}/deactivate:
    - Description: Deactivate staff member
    - Request Body: { "reason": "...", "exit_date": "..." }
    - Auth: Required (school_admin)
    - Business Rules:
      - Check for active assignments
      - Reassign classes and subjects
      - Archive user access
```

#### 4.1.2 Assignment Endpoints
```yaml
Endpoints:
  POST /api/v1/staff/assignments:
    - Description: Create staff assignment
    - Request Body: StaffAssignmentCreate schema
    - Response: StaffAssignmentResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Validate teacher qualification for subject
      - Check for assignment conflicts
      - Limit maximum teaching load
    - Side Effects:
      - Create assignment record
      - Update teacher access permissions

  GET /api/v1/staff/assignments:
    - Description: List assignments
    - Query Parameters: staff_id, class_id, subject_id, academic_year_id
    - Response: List of StaffAssignmentResponse
    - Auth: Required

  DELETE /api/v1/staff/assignments/{assignment_id}:
    - Description: Remove assignment
    - Auth: Required (school_admin)
    - Business Rules:
      - Cannot remove if teacher has entered grades
      - Require reassignment of subjects

  POST /api/v1/staff/assignments/bulk:
    - Description: Bulk create assignments
    - Request Body: BulkAssignmentCreate schema
    - Response: BulkAssignmentResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Validate all assignments
      - Rollback on critical errors
```

#### 4.1.3 Timetable Endpoints
```yaml
Endpoints:
  POST /api/v1/staff/timetables:
    - Description: Create new timetable
    - Request Body: TimetableCreate schema
    - Response: TimetableResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Only one draft timetable per class per term
      - Can copy from previous term

  GET /api/v1/staff/timetables/{timetable_id}:
    - Description: Get timetable details
    - Response: TimetableDetailResponse
    - Auth: Required

  POST /api/v1/staff/timetables/{timetable_id}/entries:
    - Description: Add timetable entry
    - Request Body: TimetableEntryCreate schema
    - Response: TimetableEntryResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Check for clashes
      - Validate teacher availability
      - Validate room availability (if configured)

  PUT /api/v1/staff/timetables/{timetable_id}/publish:
    - Description: Publish timetable
    - Auth: Required (school_admin)
    - Business Rules:
      - Must have at least one entry per day
      - No unresolved clashes
      - Notify affected teachers

  GET /api/v1/staff/timetables/my-timetable:
    - Description: Get current teacher's timetable
    - Query Parameters: week_start
    - Response: TeacherTimetableResponse
    - Auth: Required (teacher)
    - Business Rules:
      - Shows only teacher's assigned periods
      - Includes form teacher responsibilities

  POST /api/v1/staff/timetables/validate:
    - Description: Validate timetable for clashes
    - Request Body: TimetableValidation schema
    - Response: ValidationResult schema
    - Auth: Required
    - Returns: List of detected clashes
```

#### 4.1.4 Teacher Attendance Endpoints
```yaml
Endpoints:
  POST /api/v1/staff/attendance/check-in:
    - Description: Check in teacher
    - Request Body: { "method": "qr_code", "qr_data": "..." }
    - Response: CheckInResponse schema
    - Auth: Required (teacher)
    - Business Rules:
      - Record check-in time
      - Calculate late minutes
      - Validate check-in window
    - Methods:
      - QR code scan
      - Manual (admin only)
      - Geofencing (future)

  POST /api/v1/staff/attendance/check-out:
    - Description: Check out teacher
    - Response: CheckOutResponse schema
    - Auth: Required (teacher)
    - Business Rules:
      - Record check-out time
      - Calculate early departure minutes

  GET /api/v1/staff/attendance:
    - Description: Get teacher attendance records
    - Query Parameters: staff_id, school_id, date_range, status
    - Response: Paginated list of AttendanceResponse
    - Auth: Required (school_admin, teacher for own)

  GET /api/v1/staff/attendance/summary:
    - Description: Get attendance summary
    - Query Parameters: staff_id, month, term_id
    - Response: AttendanceSummaryResponse
    - Auth: Required (school_admin, teacher for own)

  GET /api/v1/staff/attendance/report:
    - Description: Generate attendance report
    - Query Parameters: school_id, month, format
    - Response: AttendanceReport or CSV
    - Auth: Required (school_admin)
```

#### 4.1.5 Staff Communication Endpoints
```yaml
Endpoints:
  POST /api/v1/staff/communications:
    - Description: Create staff communication
    - Request Body: CommunicationCreate schema
    - Response: CommunicationResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Define target audience
      - Choose channels (in_app, whatsapp, sms)
      - Set priority level

  POST /api/v1/staff/communications/broadcast:
    - Description: Send broadcast to all staff
    - Request Body: BroadcastCreate schema
    - Response: BroadcastResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Optional role filtering
      - WhatsApp delivery confirmation
      - Acknowledgement tracking

  GET /api/v1/staff/communications:
    - Description: List communications
    - Query Parameters: type, priority, date_range
    - Response: List of CommunicationResponse
    - Auth: Required

  POST /api/v1/staff/communications/{communication_id}/acknowledge:
    - Description: Acknowledge communication
    - Auth: Required (staff)
    - Business Rules:
      - Record acknowledgement timestamp
      - Required for urgent communications
```

## 5. Business Logic Implementation

### 5.1 Timetable Clash Detection
```python
class TimetableService:
    async def detect_clashes(
        self,
        timetable_id: UUID,
        new_entry: TimetableEntryCreate
    ) -> List[Clash]:
        """Detect clashes for new timetable entry."""
        
        clashes = []
        
        # 1. Check teacher clash (same teacher, same time)
        teacher_clash = await self.session.execute(
            select(TimetableEntry)
            .where(
                TimetableEntry.timetable_id == timetable_id,
                TimetableEntry.staff_id == new_entry.staff_id,
                TimetableEntry.day_of_week == new_entry.day_of_week,
                TimetableEntry.period_number == new_entry.period_number,
                TimetableEntry.deleted_at.is_(None)
            )
        )
        
        existing_teacher_entry = teacher_clash.scalar()
        if existing_teacher_entry:
            clashes.append(Clash(
                type='teacher_clash',
                description=f"Teacher already assigned to period {new_entry.period_number}",
                existing_entry=existing_teacher_entry
            ))
        
        # 2. Check class clash (same class, same time)
        # Get class from timetable
        timetable = await self.session.get(Timetable, timetable_id)
        
        class_clash = await self.session.execute(
            select(TimetableEntry)
            .join(Timetable)
            .where(
                Timetable.class_id == timetable.class_id,
                TimetableEntry.day_of_week == new_entry.day_of_week,
                TimetableEntry.period_number == new_entry.period_number,
                TimetableEntry.deleted_at.is_(None),
                Timetable.deleted_at.is_(None)
            )
        )
        
        existing_class_entry = class_clash.scalar()
        if existing_class_entry:
            clashes.append(Clash(
                type='class_clash',
                description=f"Class already has period {new_entry.period_number} scheduled",
                existing_entry=existing_class_entry
            ))
        
        # 3. Check break period clash
        if await self.is_break_period(
            timetable.school_id,
            new_entry.day_of_week,
            new_entry.period_number
        ):
            clashes.append(Clash(
                type='break_period',
                description=f"Period {new_entry.period_number} is a break period"
            ))
        
        return clashes
    
    async def validate_teacher_load(
        self,
        staff_id: UUID,
        academic_year_id: UUID,
        term_id: UUID
    ) -> LoadValidation:
        """Validate teacher's teaching load."""
        
        # Count periods assigned
        result = await self.session.execute(
            select(func.count(TimetableEntry.id))
            .join(Timetable)
            .where(
                TimetableEntry.staff_id == staff_id,
                Timetable.academic_year_id == academic_year_id,
                Timetable.term_id == term_id,
                TimetableEntry.deleted_at.is_(None)
            )
        )
        
        periods_count = result.scalar()
        
        # Get school's maximum load configuration
        school_id = await self.get_staff_school_id(staff_id)
        max_load = await self.get_max_teaching_load(school_id)
        
        return LoadValidation(
            current_load=periods_count,
            max_load=max_load,
            is_valid=periods_count <= max_load,
            remaining=max_load - periods_count
        )
```

### 5.2 Teacher Attendance Logic
```python
class TeacherAttendanceService:
    async def check_in(
        self,
        staff_id: UUID,
        method: str,
        qr_data: Optional[str] = None
    ) -> CheckInResult:
        """Record teacher check-in."""
        
        # 1. Get staff and school info
        staff = await self.staff_service.get_staff(staff_id)
        school = await self.school_service.get_school(staff.school_id)
        
        # 2. Validate check-in window
        current_time = datetime.utcnow()
        check_in_window = await self.get_check_in_window(school.id)
        
        if not self.is_within_check_in_window(current_time, check_in_window):
            raise ValidationError("Outside check-in window")
        
        # 3. Validate QR code if method is QR
        if method == 'qr_code':
            if not await self.validate_qr_code(qr_data, staff_id):
                raise ValidationError("Invalid QR code")
        
        # 4. Check if already checked in today
        today = current_time.date()
        existing = await self.session.execute(
            select(TeacherAttendance)
            .where(
                TeacherAttendance.staff_id == staff_id,
                TeacherAttendance.date == today
            )
        )
        
        attendance = existing.scalar()
        
        if attendance:
            # Update check-in time
            attendance.check_in_time = current_time
            attendance.check_in_method = method
        else:
            # Create new attendance record
            attendance = TeacherAttendance(
                staff_id=staff_id,
                school_id=staff.school_id,
                date=today,
                check_in_time=current_time,
                check_in_method=method,
                status='present'
            )
            self.session.add(attendance)
        
        # 5. Calculate late minutes
        late_threshold = await self.get_late_threshold(staff.school_id)
        schedule_start = await self.get_schedule_start_time(staff.school_id)
        
        if current_time.time() > (schedule_start + timedelta(minutes=late_threshold)):
            late_minutes = (
                datetime.combine(today, current_time.time()) - 
                datetime.combine(today, schedule_start)
            ).total_seconds() / 60
            
            attendance.status = 'late'
            attendance.late_minutes = int(late_minutes)
        
        await self.session.commit()
        
        return CheckInResult(
            success=True,
            status=attendance.status,
            late_minutes=attendance.late_minutes,
            check_in_time=attendance.check_in_time
        )
    
    async def generate_monthly_report(
        self,
        school_id: UUID,
        month: date
    ) -> MonthlyAttendanceReport:
        """Generate monthly attendance report for all teachers."""
        
        # Get all staff
        staff_list = await self.get_school_staff(school_id)
        
        report_data = []
        for staff in staff_list:
            # Get attendance summary
            summary = await self.get_staff_attendance_summary(
                staff.id, month
            )
            
            report_data.append(TeacherAttendanceReport(
                staff_id=staff.id,
                staff_name=f"{staff.first_name} {staff.last_name}",
                role=staff.role,
                employment_type=staff.employment_type,
                total_working_days=summary.total_working_days,
                present_days=summary.present_days,
                absent_days=summary.absent_days,
                late_days=summary.late_days,
                excused_days=summary.excused_days,
                attendance_rate=summary.attendance_rate,
                avg_late_minutes=summary.avg_late_minutes
            ))
        
        return MonthlyAttendanceReport(
            school_id=school_id,
            month=month,
            teachers=report_data,
            overall_attendance_rate=self.calculate_overall_rate(report_data)
        )
```

## 6. UI Component Specifications

### 6.1 Staff Profile Component
```typescript
interface StaffProfileProps {
  staffId: string;
  editable?: boolean;
  onUpdate?: (staff: Staff) => void;
}

// Profile Sections:
// 1. Header (photo, name, role, status)
// 2. Personal information (contact, address)
// 3. Employment details (type, date, department)
// 4. Qualifications list
// 5. Subjects qualified for
// 6. Class assignments
// 7. Timetable view
// 8. Attendance summary
// 9. Documents list
// 10. Edit button (admin only)

// Staff Form:
interface StaffFormProps {
  mode: 'create' | 'edit';
  staff?: Staff;
  onSubmit: (data: StaffFormData) => void;
  onCancel: () => void;
}
```

### 6.2 Timetable Builder Component
```typescript
interface TimetableBuilderProps {
  classId: string;
  termId: string;
  onSave: (timetable: Timetable) => void;
  onPublish: () => void;
}

// Builder Features:
// 1. Weekly grid view (Mon-Fri, periods)
// 2. Subject palette (drag source)
// 3. Teacher selection modal
// 4. Room assignment (optional)
// 5. Clash highlighting
// 6. Break period configuration
// 7. Save draft button
// 8. Validate button
// 9. Publish button
// 10. Copy from previous term

// Timetable Entry:
interface TimetableEntryCellProps {
  entry?: TimetableEntry;
  onEdit: (entry: TimetableEntry) => void;
  onDelete: () => void;
  clash?: Clash;
}
```

### 6.3 Teacher Attendance Component
```typescript
interface TeacherAttendanceProps {
  schoolId: string;
  date: Date;
  onAttendanceMarked: (records: AttendanceRecord[]) => void;
}

// Attendance Interface:
// 1. Staff list with check-in status
// 2. Quick mark buttons (All Present, All Absent)
// 3. Individual marking with status selection
// 4. Late arrival time input
// 5. Reason capture for absences
// 6. QR code scanner (for check-in method)
// 7. Summary statistics
// 8. Submit button

// Monthly Report:
interface MonthlyReportProps {
  schoolId: string;
  month: Date;
  onExport: () => void;
}

// Report Features:
// 1. Teacher attendance table
// 2. Attendance rate charts
// 3. Late arrival analytics
// 4. Absence patterns
// 5. Department-wise breakdown
// 6. Export to PDF/CSV
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for TimetableService
class TestTimetableService:
    async def test_detect_teacher_clash(self):
        """Test teacher clash detection."""
        pass
    
    async def test_detect_class_clash(self):
        """Test class clash detection."""
        pass
    
    async def test_validate_teacher_load(self):
        """Test teacher load validation."""
        pass
    
    async def test_publish_timetable(self):
        """Test timetable publication."""
        pass

# Test cases for TeacherAttendanceService
class TestTeacherAttendanceService:
    async def test_check_in_success(self):
        """Test successful check-in."""
        pass
    
    async def test_check_in_outside_window(self):
        """Test check-in outside allowed window."""
        pass
    
    async def test_late_arrival_calculation(self):
        """Test late arrival calculation."""
        pass
    
    async def test_generate_monthly_report(self):
        """Test monthly report generation."""
        pass
```

### 7.2 Integration Tests
```python
class TestStaffAPI:
    async def test_create_staff_endpoint(self):
        """Test POST /api/v1/staff endpoint."""
        pass
    
    async def test_create_assignment_endpoint(self):
        """Test POST /api/v1/staff/assignments endpoint."""
        pass
    
    async def test_timetable_validation_endpoint(self):
        """Test POST /api/v1/staff/timetables/validate endpoint."""
        pass
    
    async def test_teacher_check_in_endpoint(self):
        """Test POST /api/v1/staff/attendance/check-in endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Staff module
STAFF_PERMISSIONS = {
    "school_admin": [
        "staff:create",
        "staff:read",
        "staff:update",
        "staff:delete",
        "staff:manage_assignments",
        "staff:manage_timetable",
        "staff:view_attendance",
        "staff:manage_communications"
    ],
    "teacher": [
        "staff:read:own",
        "staff:update:own_contact",
        "staff:read:own_timetable",
        "staff:read:own_attendance",
        "staff:check_in:own"
    ],
    "nurse": [
        "staff:read:own"
    ],
    "bursar": [
        "staff:read:own"
    ]
}
```

### 8.2 Data Privacy
```python
# Sensitive staff data handling
SENSITIVE_STAFF_DATA = [
    "salary",            # Compensation information
    "bank_details",      # Banking information
    "next_of_kin",       # Emergency contact details
    "performance_reviews" # Performance evaluations
]

# Encryption for sensitive fields
ENCRYPTED_STAFF_FIELDS = [
    "bank_details"
]

# Access logging for staff data
STAFF_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Staff Profile Operations:
    - Target: < 2 seconds for profile retrieval
    - Target: < 5 seconds for profile update
    - Search: < 1 second response time
  
  Timetable Operations:
    - Target: < 3 seconds for timetable retrieval
    - Target: < 5 seconds for clash validation
    - Target: < 10 seconds for timetable generation
    - Clashes: Real-time detection (< 500ms)
  
  Attendance Operations:
    - Target: < 2 seconds for check-in
    - Target: < 3 seconds for attendance marking
    - Target: < 10 seconds for monthly report
    - QR Validation: < 1 second
  
  Communication Operations:
    - Target: < 5 seconds for broadcast delivery
    - Target: < 3 seconds for message retrieval
    - WhatsApp: < 30 seconds for full staff broadcast
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed staff data
STAFF_CACHE_CONFIG = {
    "staff_profile": {
        "ttl": 300,  # 5 minutes
        "key": "staff:{staff_id}:profile"
    },
    "staff_assignments": {
        "ttl": 600,  # 10 minutes
        "key": "staff:{staff_id}:assignments:term:{term_id}"
    },
    "teacher_timetable": {
        "ttl": 300,  # 5 minutes
        "key": "teacher:{staff_id}:timetable:week:{week_start}"
    },
    "class_timetable": {
        "ttl": 300,  # 5 minutes
        "key": "class:{class_id}:timetable:term:{term_id}"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
STAFF_INTEGRATIONS = {
    "sis": {
        "student_data": "for form teacher access to student profiles"
    },
    "academics": {
        "teacher_assignments": "for grade entry permissions",
        "subject_assignments": "for teaching assignments"
    },
    "attendance": {
        "teacher_attendance": "track teacher presence",
        "class_attendance": "teacher marks student attendance"
    },
    "finance": {
        "staff_payroll": "future integration for payroll",
        "salary_data": "encrypted salary information"
    },
    "health": {
        "nurse_role": "school nurse access to health module"
    },
    "parent_portal": {
        "teacher_contact": "parent can contact class teacher",
        "timetable_view": "students view published timetable"
    },
    "sentinel": {
        "teacher_notifications": "alert teachers of health alerts"
    },
    "intelligence": {
        "staff_analytics": "provide data for staff dashboards",
        "attendance_analytics": "teacher attendance trends"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_STAFF_INTEGRATIONS = {
    "whatsapp": {
        "purpose": "Staff communications and notifications",
        "templates": [
            "staff_broadcast",
            "timetable_update",
            "meeting_invitation"
        ],
        "rate_limiting": "respect WhatsApp business limits"
    },
    "termii": {
        "purpose": "SMS backup for urgent staff communications",
        "templates": ["urgent_staff_alert", "attendance_reminder"],
        "fallback": "used when WhatsApp delivery fails"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create Staff model and schema
- [ ] Create StaffClassAssignment model and schema
- [ ] Create Timetable model and schema
- [ ] Create TimetableEntry model and schema
- [ ] Create TeacherAttendance model and schema
- [ ] Create StaffCommunication model and schema
- [ ] Implement StaffService
- [ ] Implement TimetableService
- [ ] Implement TeacherAttendanceService
- [ ] Implement CommunicationService
- [ ] Create staff API endpoints
- [ ] Create timetable API endpoints
- [ ] Create attendance API endpoints
- [ ] Create communication API endpoints
- [ ] Implement clash detection algorithm
- [ ] Implement teacher load validation
- [ ] Implement check-in/check-out logic
- [ ] Implement broadcast functionality
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create StaffProfile component
- [ ] Create StaffForm component
- [ ] Create TimetableBuilder component
- [ ] Create TimetableView component
- [ ] Create TeacherAttendance component
- [ ] Create StaffCommunications component
- [ ] Create MonthlyReport component
- [ ] Implement drag-and-drop timetable
- [ ] Implement QR code scanning
- [ ] Implement attendance dashboard
- [ ] Implement staff directory
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Testing Tasks
- [ ] Unit tests for StaffService
- [ ] Unit tests for TimetableService
- [ ] Unit tests for TeacherAttendanceService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for staff workflows
- [ ] Timetable clash detection testing
- [ ] Attendance tracking testing
- [ ] Performance testing
- [ ] Security testing

---

*This module specification provides a comprehensive guide for implementing the Teacher & Staff Management system. The module enables efficient school HR management with timetable optimization and teacher accountability features.*

---

**End of Teacher & Staff Management (M6) Specification**