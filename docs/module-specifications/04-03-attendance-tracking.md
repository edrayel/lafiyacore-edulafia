# EduLafia Platform - Module Specification: Attendance & Absence Tracking (M3)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M3 - Attendance & Absence Tracking
- **Priority:** High (Core Module)
- **LafiyaSentinel Layer:** YES — Absence data feeds Sentinel Engine

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Data Model Implementation](#3-data-model-implementation)
4. [API Implementation](#4-api-implementation)
5. [Sentinel Integration Implementation](#5-sentinel-integration-implementation)
6. [UI Component Specifications](#6-ui-component-specifications)
7. [Testing Requirements](#7-testing-requirements)
8. [Security Considerations](#8-security-considerations)
9. [Performance Requirements](#9-performance-requirements)
10. [Integration Points](#10-integration-points)
11. [Implementation Checklist](#11-implementation-checklist)

## 1. Module Overview

### 1.1 Purpose
The Attendance & Absence Tracking module provides comprehensive daily attendance management, pattern detection, parent notifications, and feeds critical data to the LafiyaSentinel surveillance engine. This module is essential for both school operations and public health surveillance.

### 1.2 Scope
- Daily attendance marking (per period or per day)
- Structured absence reason capture
- Illness symptom capture (Sentinel input)
- Attendance pattern detection
- Parent notifications (WhatsApp/SMS)
- EMIS data export
- Attendance-health correlation
- Attendance analytics and reporting

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information System)
- **Dependent Modules:** M5 (Health - for Sentinel), M7 (Parent Portal), M8 (Intelligence)
- **External Dependencies:** WhatsApp Business API, Termii SMS, Sentinel Engine

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Daily Attendance Marking
```yaml
Feature: Daily Attendance Marking
Description: Mark attendance for students daily
Acceptance Criteria:
  - Mark attendance per class per period (or per day at form teacher level)
  - Support mobile and tablet marking
  - Offline-capable with sync when online
  - Single tap per student for quick marking
  - Real-time validation of student enrollment
  - Timestamp each attendance record
  - Track which teacher marked attendance
  - Support multiple marking methods (dropdown, swipe, QR code)
```

#### 2.1.2 Structured Absence Reason Capture
```yaml
Feature: Structured Absence Reason Capture
Description: Capture structured reasons for absences
Acceptance Criteria:
  - Dropdown with predefined reasons: Sick, Family Reason, Unknown, Excused, Suspended
  - Free-text notes field for additional details
  - Required reason for absences, optional for presence
  - Reason codes aligned with Sentinel surveillance taxonomy
  - Audit trail for reason changes
  - 24-hour edit window for corrections
```

#### 2.1.3 Illness Symptom Capture (Sentinel Input)
```yaml
Feature: Illness Symptom Capture
Description: Capture symptoms when student is absent due to sickness
Acceptance Criteria:
  - Only appear when 'Sick' reason selected
  - Checklist of standardized symptoms:
    - Fever, Cough, Vomiting, Diarrhea, Rash
    - Headache, Body ache, Runny nose, Conjunctivitis
    - Other (with free text)
  - Multiple symptoms can be selected
  - Symptom data feeds directly to Sentinel Engine
  - Symptoms timestamped with absence record
  - Symptom data used for outbreak pattern detection
```

#### 2.1.4 Attendance Pattern Detection
```yaml
Feature: Attendance Pattern Detection
Description: Detect unusual attendance patterns
Acceptance Criteria:
  - Detect absence every same weekday (chronic pattern)
  - Correlate absences with sick bay visits
  - Flag chronic absenteeism at >20% term absence rate
  - Detect sudden spikes in class/school absence rates
  - Generate alerts for unusual patterns
  - Historical pattern analysis
  - Pattern correlation with academic performance
```

#### 2.1.5 Parent Notifications
```yaml
Feature: Parent Notifications
Description: Notify parents of absences
Acceptance Criteria:
  - WhatsApp + SMS sent within 30 minutes of absence marking
  - Include student name, class, date
  - Include reason (if provided)
  - Include reply link for excusal
  - 3-day consecutive absence alert to admin, teacher, and parent
  - Weekly attendance summary to parents
  - Opt-out option for parents (with school approval)
  - Delivery confirmation tracking
```

#### 2.1.6 EMIS Export
```yaml
Feature: EMIS Data Export
Description: Export attendance data in EMIS format
Acceptance Criteria:
  - Termly attendance data export
  - EMIS-compatible CSV format
  - Include school code, class, gender split, termly rate
  - Match Federal Ministry of Education EMIS standards
  - Automated export generation
  - Historical data retention for EMIS reporting
  - Support for state-specific EMIS variations
```

#### 2.1.7 Attendance-Health Correlation
```yaml
Feature: Attendance-Health Correlation
Description: Correlate attendance patterns with health data
Acceptance Criteria:
  - Flag when absence pattern correlates with sick bay visits
  - Connect chronic absences to known health conditions
  - Alert school nurse of students with frequent illness absences
  - Correlate with vaccination status
  - Support health intervention planning
  - Integrate with Sentinel surveillance alerts
```

### 2.2 Business Rules

#### 2.2.1 Attendance Marking Business Rules
1. **Teacher Restriction:** Only assigned teachers can mark attendance for their classes
2. **Time Window:** Attendance can be marked from 7:00 AM to 9:00 AM (configurable)
3. **Edit Window:** 24-hour edit window for corrections, after which only admin can edit
4. **Audit Trail:** All attendance changes logged with user, timestamp, and reason
5. **Offline Marking:** Attendance can be marked offline, syncs when connectivity available
6. **Validation:** Cannot mark attendance for students not enrolled in the class
7. **Bulk Marking:** Support marking entire class as present with individual exceptions

#### 2.2.2 Absence Reason Business Rules
1. **Required Field:** Reason required for all absences
2. **Symptom Required:** Symptoms required when reason is 'Sick'
3. **Excused Absences:** Can be pre-approved via parent portal
4. **Suspension Tracking:** Suspensions tracked separately with documentation
5. **Unknown Reason:** Allowed but flagged for follow-up
6. **Reason Change:** Reasons can be updated within edit window with audit

#### 2.2.3 Notification Business Rules
1. **30-Minute Window:** Notifications sent within 30 minutes of marking
2. **3-Day Consecutive:** Alert triggered after 3 consecutive days absent
3. **Parent Opt-Out:** Parents can opt-out of daily notifications (not 3-day alerts)
4. **Delivery Confirmation:** Track delivery status of notifications
5. **Retry Logic:** Failed notifications retried up to 3 times
6. **Quiet Hours:** No notifications between 9:00 PM and 6:00 AM

#### 2.2.4 Sentinel Integration Business Rules
1. **Real-time Data:** Attendance data feeds Sentinel Engine in near real-time
2. **Symptom Threshold:** Symptoms trigger Sentinel analysis when threshold reached
3. **Cluster Detection:** Absence clusters with similar symptoms trigger alerts
4. **Geographic Mapping:** School location used for geographic cluster analysis
5. **Baseline Calibration:** Historical data used to establish normal absence rates
6. **False Positive Reduction:** Multiple data points required before alert generation

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Attendance records (partitioned by date for performance)
CREATE TABLE attendance_records (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    period INTEGER,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    reason_code VARCHAR(50) CHECK (reason_code IN ('sick', 'family', 'unknown', 'excused', 'suspended')),
    symptom_codes TEXT[],  -- Array of symptom codes for Sentinel
    notes TEXT,
    recorded_by UUID NOT NULL REFERENCES users(id),
    edited_at TIMESTAMP WITH TIME ZONE,
    edited_by UUID REFERENCES users(id),
    edit_reason TEXT,
    -- Sync fields for offline
    device_id VARCHAR(255),
    sync_status VARCHAR(20) DEFAULT 'synced',
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    PRIMARY KEY (id, date)  -- Partition key
) PARTITION BY RANGE (date);

-- Create monthly partitions for 2026
CREATE TABLE attendance_records_2026_01 
    PARTITION OF attendance_records
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE attendance_records_2026_02 
    PARTITION OF attendance_records
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Continue for all months...

-- Indexes for attendance performance
CREATE INDEX idx_attendance_student_date ON attendance_records(student_id, date);
CREATE INDEX idx_attendance_class_date ON attendance_records(class_id, date);
CREATE INDEX idx_attendance_school_date ON attendance_records(school_id, date);
CREATE INDEX idx_attendance_status_date ON attendance_records(status, date);
CREATE INDEX idx_attendance_reason_date ON attendance_records(reason_code, date);
CREATE INDEX idx_attendance_symptoms ON attendance_records USING GIN(symptom_codes);
CREATE INDEX idx_attendance_sync ON attendance_records(sync_status) WHERE sync_status != 'synced';

-- Unique constraint: one attendance record per student per date
CREATE UNIQUE INDEX idx_attendance_unique_student_date 
    ON attendance_records(student_id, date) 
    WHERE deleted_at IS NULL;

-- Attendance patterns table (for pattern detection)
CREATE TABLE attendance_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    pattern_type VARCHAR(50) NOT NULL CHECK (pattern_type IN ('chronic_absence', 'same_day_absence', 'illness_cluster')),
    pattern_details JSONB NOT NULL,
    detected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'acknowledged', 'resolved', 'false_positive')),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by UUID REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Attendance notifications log
CREATE TABLE attendance_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL CHECK (notification_type IN ('daily_absence', 'consecutive_absence', 'weekly_summary')),
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('whatsapp', 'sms', 'both')),
    message_content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'delivered', 'failed')),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Attendance configuration table
CREATE TABLE attendance_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    marking_method VARCHAR(50) DEFAULT 'dropdown' CHECK (marking_method IN ('dropdown', 'swipe', 'qr_code')),
    require_reason_for_absence BOOLEAN DEFAULT TRUE,
    require_symptoms_for_sick BOOLEAN DEFAULT TRUE,
    edit_window_hours INTEGER DEFAULT 24,
    notification_delay_minutes INTEGER DEFAULT 30,
    consecutive_absence_alert_days INTEGER DEFAULT 3,
    chronic_absence_threshold_percent DECIMAL(5, 2) DEFAULT 20.0,
    notification_enabled BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id)
);
```

### 3.2 Views for Attendance Reporting
```sql
-- Daily attendance summary view
CREATE VIEW daily_attendance_summary AS
SELECT 
    school_id,
    class_id,
    date,
    COUNT(*) as total_students,
    COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
    COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count,
    COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
    COUNT(CASE WHEN status = 'excused' THEN 1 END) as excused_count,
    ROUND(
        COUNT(CASE WHEN status = 'present' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) as attendance_rate
FROM attendance_records
WHERE deleted_at IS NULL
GROUP BY school_id, class_id, date;

-- Student attendance summary view
CREATE VIEW student_attendance_summary AS
SELECT 
    ar.student_id,
    ar.school_id,
    DATE_TRUNC('month', ar.date) as month,
    COUNT(*) as total_days,
    COUNT(CASE WHEN ar.status = 'present' THEN 1 END) as present_days,
    COUNT(CASE WHEN ar.status = 'absent' THEN 1 END) as absent_days,
    COUNT(CASE WHEN ar.status = 'absent' AND ar.reason_code = 'sick' THEN 1 END) as sick_days,
    COUNT(CASE WHEN ar.status = 'late' THEN 1 END) as late_days,
    ROUND(
        COUNT(CASE WHEN ar.status = 'present' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) as attendance_percentage
FROM attendance_records ar
WHERE ar.deleted_at IS NULL
GROUP BY ar.student_id, ar.school_id, DATE_TRUNC('month', ar.date);

-- Illness pattern view (for Sentinel)
CREATE VIEW illness_pattern_view AS
SELECT 
    ar.school_id,
    ar.date,
    ar.reason_code,
    UNNEST(ar.symptom_codes) as symptom_code,
    COUNT(DISTINCT ar.student_id) as affected_students,
    COUNT(DISTINCT ar.class_id) as affected_classes,
    ROUND(
        COUNT(DISTINCT ar.student_id) * 100.0 / s.total_students,
        2
    ) as percentage_affected
FROM attendance_records ar
JOIN (
    SELECT school_id, COUNT(*) as total_students 
    FROM students 
    WHERE status = 'active' 
    GROUP BY school_id
) s ON ar.school_id = s.school_id
WHERE ar.deleted_at IS NULL
    AND ar.status = 'absent'
    AND ar.reason_code = 'sick'
    AND ar.symptom_codes IS NOT NULL
GROUP BY ar.school_id, ar.date, ar.reason_code, UNNEST(ar.symptom_codes), s.total_students;

-- Chronic absence view
CREATE VIEW chronic_absence_view AS
SELECT 
    ar.student_id,
    ar.school_id,
    ar.class_id,
    COUNT(*) as total_days,
    COUNT(CASE WHEN ar.status = 'absent' THEN 1 END) as absent_days,
    ROUND(
        COUNT(CASE WHEN ar.status = 'absent' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) as absence_rate,
    MIN(ar.date) as first_absence,
    MAX(ar.date) as last_absence
FROM attendance_records ar
WHERE ar.deleted_at IS NULL
    AND ar.date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY ar.student_id, ar.school_id, ar.class_id
HAVING COUNT(CASE WHEN ar.status = 'absent' THEN 1 END) * 100.0 / COUNT(*) > 20;
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Attendance Marking Endpoints
```yaml
Endpoints:
  POST /api/v1/attendance/mark:
    - Description: Mark attendance for a class
    - Request Body: AttendanceMarking schema
    - Response: AttendanceMarkingResult schema
    - Auth: Required (teacher)
    - Business Rules:
      - Teacher must be assigned to class
      - Cannot mark for future dates
      - Validate student enrollment
      - Symptom codes required when reason is 'sick'
    - Side Effects:
      - Create attendance records
      - Queue parent notifications
      - Feed data to Sentinel Engine
      - Log audit trail
    - Offline Support: Yes, queues for sync

  POST /api/v1/attendance/mark/bulk:
    - Description: Bulk mark attendance (mark all present, then mark exceptions)
    - Request Body: BulkAttendanceMarking schema
    - Response: BulkMarkingResult schema
    - Auth: Required (teacher)
    - Business Rules:
      - Default status for unmarked students
      - Individual exceptions override default

  PATCH /api/v1/attendance/{attendance_id}:
    - Description: Update attendance record
    - Request Body: AttendanceUpdate schema
    - Response: Updated AttendanceResponse
    - Auth: Required (teacher, school_admin)
    - Business Rules:
      - Check edit window (24 hours)
      - Require reason for edit
      - Log all changes

  GET /api/v1/attendance:
    - Description: Get attendance records
    - Query Parameters: student_id, class_id, school_id, date, start_date, end_date, status
    - Response: Paginated list of AttendanceResponse
    - Auth: Required

  GET /api/v1/attendance/summary:
    - Description: Get attendance summary
    - Query Parameters: class_id, school_id, month, term_id
    - Response: AttendanceSummary schema
    - Includes:
      - Daily attendance rates
      - Student attendance percentages
      - Absence reason breakdown
      - Illness statistics
```

#### 4.1.2 Absence Reason Endpoints
```yaml
Endpoints:
  POST /api/v1/attendance/absence/reason:
    - Description: Record absence reason and symptoms
    - Request Body: AbsenceReason schema
    - Response: AbsenceReasonResponse schema
    - Auth: Required (teacher)
    - Business Rules:
      - Required for all absences
      - Symptoms required for 'sick' reason
      - Can be updated within edit window

  GET /api/v1/attendance/absence/reasons:
    - Description: Get configured absence reasons
    - Response: List of AbsenceReasonConfig
    - Auth: Required

  GET /api/v1/attendance/absence/symptoms:
    - Description: Get available symptom codes
    - Response: List of SymptomCode
    - Auth: Required
```

#### 4.1.3 Attendance Patterns Endpoints
```yaml
Endpoints:
  GET /api/v1/attendance/patterns:
    - Description: Get detected attendance patterns
    - Query Parameters: school_id, class_id, pattern_type, severity, status
    - Response: List of AttendancePatternResponse
    - Auth: Required (school_admin, nurse)
    - Business Rules:
      - School admin sees all patterns
      - Nurse sees health-related patterns only

  POST /api/v1/attendance/patterns/detect:
    - Description: Trigger pattern detection for school/class
    - Request Body: { "school_id": "...", "class_id": "..." }
    - Response: DetectionResult schema
    - Auth: Required (school_admin, system)
    - Business Rules:
      - Can be triggered manually or scheduled
      - Runs pattern detection algorithms
      - Generates new patterns if found

  PATCH /api/v1/attendance/patterns/{pattern_id}/acknowledge:
    - Description: Acknowledge detected pattern
    - Request Body: { "action": "acknowledge", "notes": "..." }
    - Response: Updated pattern
    - Auth: Required (school_admin)
```

#### 4.1.4 Notification Endpoints
```yaml
Endpoints:
  POST /api/v1/attendance/notifications/send:
    - Description: Manually trigger attendance notifications
    - Request Body: { "date": "...", "school_id": "..." }
    - Response: NotificationResult schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Normally triggered automatically
      - Manual trigger for missed notifications

  GET /api/v1/attendance/notifications:
    - Description: Get notification history
    - Query Parameters: student_id, guardian_id, type, status, date
    - Response: List of AttendanceNotificationResponse
    - Auth: Required

  GET /api/v1/attendance/notifications/stats:
    - Description: Get notification statistics
    - Query Parameters: school_id, date_range
    - Response: NotificationStats schema
    - Includes:
      - Delivery rates
      - Failure reasons
      - Channel effectiveness
```

#### 4.1.5 EMIS Export Endpoints
```yaml
Endpoints:
  GET /api/v1/attendance/export/emis:
    - Description: Export attendance data in EMIS format
    - Query Parameters: school_id, term_id, format (csv, json)
    - Response: EMIS export file
    - Auth: Required (school_admin, lga_education)
    - Business Rules:
      - EMIS-compatible format
      - Includes school code, class, gender split
      - Termly attendance rates

  GET /api/v1/attendance/export/emis/state:
    - Description: Export state-level EMIS data
    - Query Parameters: state, term_id
    - Response: State EMIS export
    - Auth: Required (state_education)
```

#### 4.1.6 Attendance Analytics Endpoints
```yaml
Endpoints:
  GET /api/v1/attendance/analytics/dashboard:
    - Description: Get attendance analytics dashboard
    - Query Parameters: school_id, term_id
    - Response: AttendanceDashboard schema
    - Includes:
      - Daily attendance trends
      - Class comparison
      - Absence reason breakdown
      - Illness patterns
      - Chronic absence alerts

  GET /api/v1/attendance/analytics/student/{student_id}:
    - Description: Get student attendance analytics
    - Query Parameters: term_id, academic_year_id
    - Response: StudentAttendanceAnalytics schema
    - Includes:
      - Attendance history
      - Pattern analysis
      - Correlation with academic performance
      - Health correlation

  GET /api/v1/attendance/analytics/illness-heatmap:
    - Description: Get illness absence heatmap
    - Query Parameters: school_id, start_date, end_date
    - Response: IllnessHeatmap schema
    - Includes:
      - Geographic distribution
      - Symptom clusters
      - Timeline view
```

## 5. Sentinel Integration Implementation

### 5.1 Sentinel Data Feeding
```python
class SentinelIntegrationService:
    async def process_attendance_for_sentinel(
        self,
        attendance_record: AttendanceRecord
    ):
        """Process attendance record for Sentinel surveillance."""
        
        # 1. Check if record is relevant for Sentinel
        if not self.is_sentinel_relevant(attendance_record):
            return
        
        # 2. Extract symptom data
        symptom_data = self.extract_symptom_data(attendance_record)
        
        # 3. Check for immediate alerts (real-time thresholds)
        if await self.check_immediate_alert(attendance_record, symptom_data):
            await self.generate_immediate_alert(attendance_record, symptom_data)
        
        # 4. Queue for batch analysis
        await self.queue_for_batch_analysis(attendance_record, symptom_data)
        
        # 5. Update school absence rate metrics
        await self.update_school_metrics(attendance_record)
    
    def is_sentinel_relevant(self, record: AttendanceRecord) -> bool:
        """Check if attendance record is relevant for Sentinel."""
        return (
            record.status == 'absent' and 
            record.reason_code == 'sick' and 
            record.symptom_codes and 
            len(record.symptom_codes) > 0
        )
    
    def extract_symptom_data(self, record: AttendanceRecord) -> dict:
        """Extract symptom data for Sentinel analysis."""
        return {
            'student_id': str(record.student_id),
            'school_id': str(record.school_id),
            'class_id': str(record.class_id),
            'date': record.date.isoformat(),
            'symptoms': record.symptom_codes,
            'student_count': 1
        }
    
    async def check_immediate_alert(
        self, 
        record: AttendanceRecord, 
        symptom_data: dict
    ) -> bool:
        """Check for immediate alert thresholds."""
        # Get school configuration
        config = await self.get_sentinel_config(record.school_id)
        
        # Check same-day illness cluster
        same_day_illness = await self.get_same_day_illness_count(
            record.school_id,
            record.date,
            record.symptom_codes
        )
        
        # Threshold: >10% of students with same symptoms
        total_students = await self.get_school_student_count(record.school_id)
        threshold = total_students * 0.1
        
        return same_day_illness >= threshold
```

### 5.2 Batch Analysis for Sentinel
```python
class SentinelBatchAnalysis:
    async def analyze_attendance_patterns(self, school_id: UUID, date: date):
        """Batch analyze attendance patterns for Sentinel."""
        
        # 1. Get all illness absences for date range (48-96 hours window)
        illness_records = await self.get_illness_absences(
            school_id, 
            date, 
            window_hours=48
        )
        
        # 2. Group by symptom profile
        symptom_groups = self.group_by_symptoms(illness_records)
        
        # 3. Analyze each symptom group
        for symptom_profile, records in symptom_groups.items():
            # Check threshold
            if len(records) >= self.get_threshold(symptom_profile):
                # Generate Sentinel signal
                signal = await self.create_sentinel_signal(
                    school_id=school_id,
                    symptom_profile=symptom_profile,
                    affected_students=[r.student_id for r in records],
                    date_range=(records[0].date, records[-1].date)
                )
                
                # Trigger alerts based on signal tier
                await self.trigger_alerts(signal)
    
    def group_by_symptoms(self, records: List[AttendanceRecord]) -> dict:
        """Group records by symptom profile."""
        groups = {}
        for record in records:
            # Create normalized symptom signature
            symptom_signature = tuple(sorted(record.symptom_codes))
            if symptom_signature not in groups:
                groups[symptom_signature] = []
            groups[symptom_signature].append(record)
        return groups
    
    async def create_sentinel_signal(
        self,
        school_id: UUID,
        symptom_profile: tuple,
        affected_students: List[UUID],
        date_range: tuple
    ) -> SentinelSignal:
        """Create Sentinel signal for cluster."""
        
        # Determine alert tier based on scope
        school_count = 1  # Single school
        lga = await self.get_school_lga(school_id)
        
        # Check if other schools in same LGA affected
        lga_affected = await self.get_lga_affected_schools(
            lga, 
            symptom_profile, 
            date_range
        )
        
        if len(lga_affected) >= 2:
            alert_tier = 'lga'
        else:
            alert_tier = 'school'
        
        # Create signal
        signal = SentinelSignal(
            school_ids=[school_id] + lga_affected,
            lga=lga,
            state=await self.get_school_state(school_id),
            date_generated=datetime.utcnow(),
            symptom_profile={
                'primary_symptoms': list(symptom_profile),
                'affected_count': len(affected_students),
                'time_window_hours': 48
            },
            students_affected=len(affected_students),
            threshold_type='symptom_cluster',
            alert_tier=alert_tier,
            status='open'
        )
        
        self.session.add(signal)
        await self.session.commit()
        
        return signal
```

## 6. UI Component Specifications

### 6.1 Attendance Marking Component
```typescript
interface AttendanceMarkingProps {
  classId: string;
  date: Date;
  period?: number;
  onAttendanceMarked: (result: AttendanceMarkingResult) => void;
}

// Component Requirements:
// 1. Display student list with attendance status toggle
// 2. Quick mark buttons (All Present, All Absent)
// 3. Individual student marking with reason selection
// 4. Symptom checklist (appears when 'Sick' selected)
// 5. Offline indicator and sync status
// 6. Timer for marking deadline
// 7. Summary statistics (present/absent counts)
// 8. Submit button with validation

// Student Marking Card:
interface StudentMarkingCardProps {
  student: Student;
  marking: AttendanceMarking;
  onStatusChange: (status: AttendanceStatus) => void;
  onReasonChange: (reason: AbsenceReason) => void;
  onSymptomToggle: (symptom: SymptomCode) => void;
  isLocked: boolean;
}
```

### 6.2 Attendance Dashboard Component
```typescript
interface AttendanceDashboardProps {
  schoolId: string;
  termId: string;
  dateRange?: DateRange;
}

// Dashboard Components:
// 1. Daily attendance rate chart
// 2. Class comparison table
// 3. Absence reason breakdown pie chart
// 4. Illness symptom heatmap
// 5. Chronic absence alerts list
// 6. Sentinel alerts panel
// 7. Export buttons (EMIS, CSV)
// 8. Date range selector
```

### 6.3 Parent Notification Preview Component
```typescript
interface NotificationPreviewProps {
  studentId: string;
  date: Date;
  onSend: () => void;
  onCustomize: (message: string) => void;
}

// Preview Sections:
// 1. Student and class information
// 2. Absence reason and symptoms (if provided)
// 3. Message template preview
// 4. WhatsApp preview
// 5. SMS preview
// 6. Custom message option
// 7. Send button
// 8. Schedule option
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for AttendanceService
class TestAttendanceService:
    async def test_mark_attendance_success(self):
        """Test successful attendance marking."""
        pass
    
    async def test_mark_attendance_with_symptoms(self):
        """Test attendance marking with symptoms."""
        pass
    
    async def test_validate_teacher_access(self):
        """Test teacher access validation."""
        pass
    
    async def test_edit_window_enforcement(self):
        """Test edit window enforcement."""
        pass
    
    async def test_duplicate_attendance_prevention(self):
        """Test prevention of duplicate attendance records."""
        pass

# Test cases for SentinelIntegrationService
class TestSentinelIntegrationService:
    async def test_sentinel_relevant_detection(self):
        """Test detection of Sentinel-relevant records."""
        pass
    
    async def test_immediate_alert_generation(self):
        """Test immediate alert generation."""
        pass
    
    async def test_symptom_grouping(self):
        """Test symptom grouping for batch analysis."""
        pass
    
    async def test_sentinel_signal_creation(self):
        """Test Sentinel signal creation."""
        pass
```

### 7.2 Integration Tests
```python
class TestAttendanceAPI:
    async def test_attendance_marking_endpoint(self):
        """Test POST /api/v1/attendance/mark endpoint."""
        pass
    
    async def test_attendance_summary_endpoint(self):
        """Test GET /api/v1/attendance/summary endpoint."""
        pass
    
    async def test_emis_export_endpoint(self):
        """Test GET /api/v1/attendance/export/emis endpoint."""
        pass
    
    async def test_offline_sync_endpoint(self):
        """Test offline attendance sync."""
        pass
```

### 7.3 Offline Tests
```python
class TestOfflineAttendance:
    async def test_offline_marking(self):
        """Test attendance marking while offline."""
        pass
    
    async def test_offline_to_online_sync(self):
        """Test sync from offline to online."""
        pass
    
    async def test_conflict_resolution(self):
        """Test conflict resolution during sync."""
        pass
    
    async def test_data_integrity_after_sync(self):
        """Test data integrity after sync."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Attendance module
ATTENDANCE_PERMISSIONS = {
    "school_admin": [
        "attendance:create",
        "attendance:read",
        "attendance:update",
        "attendance:delete",
        "attendance:export",
        "attendance:view_patterns",
        "attendance:manage_notifications"
    ],
    "teacher": [
        "attendance:create:class_only",
        "attendance:read:class_only",
        "attendance:update:own_marking",
        "attendance:read:own_class_summary"
    ],
    "nurse": [
        "attendance:read:health_patterns",
        "attendance:read:illness_stats"
    ],
    "bursar": [
        "attendance:read:summary"
    ],
    "parent": [
        "attendance:read:own_child",
        "attendance:create:excusal"
    ],
    "student": [
        "attendance:read:own"
    ],
    "lga_education": [
        "attendance:read:aggregate",
        "attendance:export:emis"
    ],
    "lga_health": [
        "attendance:read:health_aggregate",
        "attendance:read:sentinel_alerts"
    ]
}
```

### 8.2 Data Privacy
```python
# Sensitive attendance data handling
SENSITIVE_ATTENDANCE_DATA = [
    "illness_symptoms",     # Health-related absence reasons
    "chronic_absence_patterns", # Patterns indicating health issues
    "disciplinary_absences"     # Suspension records
]

# Access logging for sensitive data
ATTENDANCE_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Attendance Marking:
    - Target: < 5 minutes for class of 45 students (mobile)
    - Target: < 3 minutes with bulk marking
    - Validation: Real-time (< 100ms)
  
  Attendance Sync:
    - Target: < 10 minutes for full day sync (500-student school)
    - Incremental sync: Only unsynced records
    - Conflict resolution: < 5 seconds per conflict
  
  Pattern Detection:
    - Target: < 30 seconds for daily batch analysis
    - Target: < 5 minutes for weekly pattern analysis
    - Alert generation: < 15 minutes from threshold crossing
  
  EMIS Export:
    - Target: < 2 minutes for school term export
    - Target: < 10 minutes for state-level export
    - Format: EMIS-compatible CSV
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed attendance data
ATTENDANCE_CACHE_CONFIG = {
    "daily_summary": {
        "ttl": 300,  # 5 minutes
        "key": "school:{school_id}:date:{date}:summary"
    },
    "student_attendance": {
        "ttl": 600,  # 10 minutes
        "key": "student:{student_id}:term:{term_id}:attendance"
    },
    "class_attendance": {
        "ttl": 300,  # 5 minutes
        "key": "class:{class_id}:date:{date}:attendance"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
ATTENDANCE_INTEGRATIONS = {
    "sis": {
        "student_data": "student enrollment, class assignment",
        "validation": "student must be active and enrolled"
    },
    "academics": {
        "absence_flags": "flag INC for absent students during exams",
        "performance_correlation": "correlate attendance with grades"
    },
    "finance": {
        "attendance_fees": "some schools charge for absence",
        "suspension_tracking": "track suspensions for fee waivers"
    },
    "health": {
        "sick_bay_integration": "correlate attendance with sick bay visits",
        "referral_tracking": "track students sent home from attendance"
    },
    "sentinel": {
        "real_time_data": "feed absence and symptom data",
        "alert_generation": "receive Sentinel alerts for clusters"
    },
    "parent_portal": {
        "attendance_view": "show child attendance to parents",
        "excusal_submission": "receive parent excusal requests"
    },
    "intelligence": {
        "attendance_analytics": "provide data for dashboards",
        "trend_analysis": "support historical analysis"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_ATTENDANCE_INTEGRATIONS = {
    "whatsapp": {
        "purpose": "Send absence notifications to parents",
        "templates": [
            "daily_absence_notification",
            "consecutive_absence_alert",
            "weekly_summary"
        ],
        "rate_limiting": "respect WhatsApp business limits"
    },
    "termii": {
        "purpose": "SMS backup for WhatsApp failures",
        "templates": ["absence_sms", "consecutive_absence_sms"],
        "fallback": "used when WhatsApp delivery fails"
    },
    "emis": {
        "purpose": "Export attendance data for government reporting",
        "format": "CSV with EMIS standard columns",
        "frequency": "termly export"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create AttendanceRecord model and schema
- [ ] Create AttendancePattern model and schema
- [ ] Create AttendanceNotification model and schema
- [ ] Create AttendanceConfiguration model and schema
- [ ] Implement AttendanceService
- [ ] Implement SentinelIntegrationService
- [ ] Implement NotificationService
- [ ] Create attendance API endpoints
- [ ] Implement attendance marking logic
- [ ] Implement absence reason capture
- [ ] Implement symptom capture
- [ ] Implement pattern detection
- [ ] Implement parent notifications
- [ ] Implement EMIS export
- [ ] Implement offline sync support
- [ ] Add Sentinel data feeding
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create AttendanceMarking component
- [ ] Create AttendanceDashboard component
- [ ] Create NotificationPreview component
- [ ] Create PatternAlerts component
- [ ] Create EMISExport component
- [ ] Implement offline attendance marking
- [ ] Implement sync status indicator
- [ ] Implement bulk marking interface
- [ ] Implement symptom checklist
- [ ] Implement real-time validation
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Sentinel Integration Tasks
- [ ] Implement symptom data extraction
- [ ] Implement immediate alert checking
- [ ] Implement batch pattern analysis
- [ ] Implement signal creation
- [ ] Implement alert tier determination
- [ ] Implement geospatial mapping
- [ ] Test with sample outbreak data
- [ ] Calibrate thresholds with epidemiologists

### 11.4 Testing Tasks
- [ ] Unit tests for AttendanceService
- [ ] Unit tests for SentinelIntegrationService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for attendance workflow
- [ ] Offline functionality testing
- [ ] Sync conflict testing
- [ ] Performance testing
- [ ] Security testing

---

*This module specification provides a comprehensive guide for implementing the Attendance & Absence Tracking system. The module is critical for both school operations and the LafiyaSentinel surveillance engine, providing real-time data for disease outbreak detection.*

---

**End of Attendance & Absence Tracking (M3) Specification**