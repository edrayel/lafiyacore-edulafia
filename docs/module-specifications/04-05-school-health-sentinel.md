# EduLafia Platform - Module Specification: School Health & Sentinel Engine (M5)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M5 - School Health & Sentinel Engine
- **Priority:** High (Core Module)
- **Sentinel Layer:** YES — Core Sentinel module

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Data Model Implementation](#3-data-model-implementation)
4. [Sentinel Engine Implementation](#4-sentinel-engine-implementation)
5. [UI Component Specifications](#5-ui-component-specifications)
6. [Testing Requirements](#6-testing-requirements)
7. [Security Considerations](#7-security-considerations)
8. [Performance Requirements](#8-performance-requirements)
9. [Integration Points](#10-integration-points)
10. [Implementation Checklist](#11-implementation-checklist)

## 1. Module Overview

### 1.1 Purpose
The School Health & Sentinel Engine module manages all school health operations including student health profiles, sick bay visits, health screenings, mental health assessments, referrals, immunizations, and the embedded LafiyaSentinel disease surveillance engine. This module transforms schools into public health early-warning nodes while providing comprehensive school health services.

### 1.2 Scope
- Student health profile management
- Sick bay visit logging and tracking
- Mass health screening module
- Mental health screening and wellbeing
- Referral management and tracking
- Vaccination/immunization records
- LafiyaSentinel automated outbreak detection
- Population health dashboards
- Health analytics and reporting
- Integration with attendance and Sentinel systems

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information System), M3 (Attendance - for Sentinel)
- **Dependent Modules:** M7 (Parent Portal), M8 (Intelligence), M9 (Admin - for Sentinel config)
- **External Dependencies:** WhatsApp/SMS for alerts, geospatial mapping services

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Student Health Profile
```yaml
Feature: Student Health Profile
Description: Comprehensive digital health profile for each student
Acceptance Criteria:
  - Blood group and genotype (sickle cell status: AA, AS, SS, SC)
  - Known chronic conditions (sickle cell, asthma, diabetes, etc.)
  - Allergies (food, medication, environmental)
  - Current medications
  - Disability status
  - Emergency health notes for first responders
  - Family health history (optional, guardian-provided)
  - Vision and hearing status (updated annually)
  - Profile visible to school nurse and authorized staff
  - Confidentiality controls for sensitive information
```

#### 2.1.2 Sick Bay Visit Log
```yaml
Feature: Sick Bay Visit Logging
Description: Log and track all sick bay visits
Acceptance Criteria:
  - Date and time of visit
  - Presenting complaint (structured + free text)
  - Observations (temperature, blood pressure, pulse if available)
  - Treatment given
  - Outcome (returned to class / sent home / referred)
  - Linked to student profile and attendance record
  - Searchable by complaint type, date, student, class
  - Repeat-visitor flag (>3 visits per term for same complaint)
  - Nurse attribution for each visit
  - Offline-capable for schools with limited connectivity
```

#### 2.1.3 Mass Screening Module
```yaml
Feature: Mass Health Screening
Description: Conduct and record annual/termly health screenings
Acceptance Criteria:
  - Annual or termly structured screening
  - BMI and nutritional status (height, weight, MUAC)
  - Vision screening (Snellen chart equivalent)
  - Hearing screening (basic assessment)
  - Blood pressure measurement
  - Dental observation
  - Sickle cell confirmatory test record
  - Batch screening mode for entire class
  - Abnormal result flags for follow-up
  - Screening coverage dashboard
  - Integration with student health profiles
```

#### 2.1.4 Mental Health & Wellbeing Screening
```yaml
Feature: Mental Health Screening
Description: Termly mental health and wellbeing assessment
Acceptance Criteria:
  - Termly structured screening
  - Culturally adapted, age-appropriate questions
  - Available in Igbo, Hausa, and English
  - Based on adapted PHQ-A (Adolescent) and SDQ frameworks
  - Reviewed by Nigerian child psychologists
  - Confidentiality controls (nurse + counsellor only)
  - Flag-and-refer system for at-risk students
  - Follow-up tracker for flagged students
  - Integration with school counselor workflow
  - Not visible to teachers or administrators without authorization
```

#### 2.1.5 Referral Management
```yaml
Feature: Referral Management
Description: Manage student referrals to external health facilities
Acceptance Criteria:
  - Structured referral from nurse to external clinic/hospital
  - Auto-generated referral letter with student health profile
  - Include presenting complaint and clinical notes
  - Referral status tracking (pending, attended, overdue, cancelled)
  - Follow-up tracker with outcome recording
  - 48-hour auto-reminder to nurse and family
  - Outcome recording when student returns
  - Integration with sick bay visit log
  - Referral completion rate analytics
```

#### 2.1.6 Vaccination/Immunization Records
```yaml
Feature: Vaccination Records
Description: Track student immunization status
Acceptance Criteria:
  - Vaccination record per student per vaccine
  - Administered date and lot number (optional)
  - Administering facility
  - Coverage dashboard by antigen
  - NPHCDA campaign tracking
  - Reminder system for due vaccines
  - Integration with national immunization schedule
  - Batch import of vaccination data
  - Export for NPHCDA reporting
```

#### 2.1.7 LafiyaSentinel Outbreak Detection
```yaml
Feature: LafiyaSentinel Automated Outbreak Detection
Description: Real-time disease surveillance and alert system
Acceptance Criteria:
  - Continuous analysis of sick bay visits and attendance data
  - Configurable triggers:
    - ≥3 students with same complaint in same class within 48 hours
    - ≥5 students with same complaint across school within 72 hours
    - Cross-school cluster: ≥2 schools in same LGA within 96 hours
  - All thresholds configurable by LafiyaCore admin
  - Alert content includes symptom profile, affected count, recommended action
  - Tiered alerts:
    - School-level: to headteacher and school nurse
    - LGA-level: to LGA Health Officer
    - State-level: to State Epidemiologist
  - Geospatial mapping of illness signals
  - Historical signal data retention
  - Calibration against baseline illness rates
  - Disease-specific detection logic (respiratory, gastrointestinal, vector-borne)
```

#### 2.1.8 Population Health Dashboard
```yaml
Feature: Population Health Dashboard
Description: School, LGA, and state health analytics
Acceptance Criteria:
  - School level: top complaints, chronic condition prevalence, referral rate, vaccination coverage
  - LGA level: illness signal heat map, cross-school comparison, alert history
  - State level: full Sentinel dashboard, time-series trends, geographic cluster analysis
  - IDSR-formatted export capabilities
  - Real-time updates
  - Filter by time period, school, LGA, symptom type
  - Drill-down capability from state to school level
  - Export for government reporting
```

### 2.2 Business Rules

#### 2.2.1 Health Profile Business Rules
1. **Confidentiality:** Sickle cell status, mental health data accessible only to nurse and designated staff
2. **Guardian Consent:** Family health history requires guardian consent
3. **Update Frequency:** Health profiles updated at least annually during screening
4. **Emergency Access:** Emergency notes accessible to all staff in emergency situations
5. **Data Retention:** Health records retained for 7 years after student leaves school
6. **Access Logging:** All health data access logged with user and timestamp
7. **NIN Integration:** Optional linkage to National Health Insurance records

#### 2.2.2 Sick Bay Business Rules
1. **Nurse Only:** Only school nurse or health officer can log sick bay visits
2. **Real-time Logging:** Visits logged immediately, not in arrears
3. **Outcome Required:** Must record outcome for each visit
4. **Referral Threshold:** Automatic referral suggestion for severe symptoms
5. **Parent Notification:** Guardian notified for visits with treatment or referral
6. **Attendance Correlation:** Sick bay visits automatically correlated with attendance records
7. **Chronic Flag:** Students with >3 visits for same complaint flagged for follow-up

#### 2.2.3 Screening Business Rules
1. **Annual Requirement:** At least one comprehensive screening per academic year
2. **Parental Consent:** Parental consent required for screenings
3. **Abnormal Results:** Flagged results require follow-up within 2 weeks
4. **Nurse Supervision:** Screenings conducted under nurse supervision
5. **Batch Efficiency:** Support for screening entire class in one session
6. **Data Integrity:** Screening results cannot be deleted, only updated with audit trail
7. **Coverage Target:** 95% screening coverage target per academic year

#### 2.2.4 Sentinel Business Rules
1. **Data Quality:** Sentinel analysis depends on quality of sick bay and attendance data
2. **Threshold Calibration:** Thresholds calibrated per school based on historical data
3. **False Positive Reduction:** Multiple data points required before alert generation
4. **Alert Escalation:** Alerts escalate based on severity and geographic scope
5. **Response Tracking:** All alerts must be acknowledged and resolved
6. **Model Validation:** Sentinel model validated against confirmed outbreaks
7. **Privacy:** Sentinel data aggregated; individual student data not exposed to government officials

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Student health profiles
CREATE TABLE student_health_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID UNIQUE NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    blood_group VARCHAR(5),
    genotype VARCHAR(5) CHECK (genotype IN ('AA', 'AS', 'SS', 'SC', 'AC')),
    chronic_conditions TEXT[],
    allergies TEXT[],
    current_medications TEXT[],
    emergency_notes TEXT,  -- Encrypted
    disability_status TEXT,
    family_health_history JSONB,  -- Guardian-provided, optional
    vision_left DECIMAL(3,1),
    vision_right DECIMAL(3,1),
    hearing_left VARCHAR(20),
    hearing_right VARCHAR(20),
    last_updated TIMESTAMP WITH TIME ZONE,
    updated_by UUID REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Sick bay visits
CREATE TABLE sick_bay_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    visit_date TIMESTAMP WITH TIME ZONE NOT NULL,
    presenting_complaint_codes TEXT[] NOT NULL,
    presenting_complaint_notes TEXT,
    temperature DECIMAL(4,1),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    pulse_rate INTEGER,
    treatment_given TEXT,
    outcome VARCHAR(50) NOT NULL CHECK (outcome IN ('returned_to_class', 'sent_home', 'referred', 'hospitalized')),
    referred_to VARCHAR(255),
    referred_by UUID REFERENCES staff(id),
    recorded_by UUID NOT NULL REFERENCES users(id),
    -- Offline sync fields
    device_id VARCHAR(255),
    sync_status VARCHAR(20) DEFAULT 'synced',
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Indexes for sick bay
CREATE INDEX idx_sick_bay_student_date ON sick_bay_visits(student_id, visit_date);
CREATE INDEX idx_sick_bay_school_date ON sick_bay_visits(school_id, visit_date);
CREATE INDEX idx_sick_bay_complaints ON sick_bay_visits USING GIN(presenting_complaint_codes);
CREATE INDEX idx_sick_bay_outcome ON sick_bay_visits(outcome, visit_date);

-- Health screenings
CREATE TABLE health_screenings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    screening_date DATE NOT NULL,
    screening_type VARCHAR(50) NOT NULL CHECK (screening_type IN ('annual', 'termly', 'ad_hoc')),
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    bmi DECIMAL(5,2),
    muac DECIMAL(5,2),  -- Mid-Upper Arm Circumference
    vision_left DECIMAL(3,1),
    vision_right DECIMAL(3,1),
    hearing_left VARCHAR(20),
    hearing_right VARCHAR(20),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    dental_notes TEXT,
    sickle_cell_test_result VARCHAR(10),
    flags TEXT[],  -- Abnormal result flags
    conducted_by UUID NOT NULL REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Mental health assessments
CREATE TABLE mental_health_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL,
    term_id UUID NOT NULL REFERENCES terms(id),
    assessment_type VARCHAR(50) CHECK (assessment_type IN ('phq_a', 'sdq', 'custom')),
    responses JSONB NOT NULL,
    total_score INTEGER,
    flag_level VARCHAR(20) CHECK (flag_level IN ('none', 'watch', 'refer')),
    counsellor_assigned_id UUID REFERENCES staff(id),
    follow_up_notes TEXT,
    conducted_by UUID NOT NULL REFERENCES users(id),
    is_confidential BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Referrals
CREATE TABLE referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    sick_bay_visit_id UUID REFERENCES sick_bay_visits(id),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    referral_date TIMESTAMP WITH TIME ZONE NOT NULL,
    destination_facility VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    clinical_notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'attended', 'attended_no_outcome', 'overdue', 'cancelled')),
    follow_up_due_date DATE,
    outcome_notes TEXT,
    outcome_date DATE,
    created_by UUID NOT NULL REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Vaccination records
CREATE TABLE vaccination_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    vaccine_name VARCHAR(100) NOT NULL,
    vaccine_code VARCHAR(50),
    dose_number INTEGER,
    administration_date DATE NOT NULL,
    lot_number VARCHAR(100),
    administering_facility VARCHAR(255),
    administered_by VARCHAR(255),
    recorded_by UUID NOT NULL REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Sentinel signals (outbreak alerts)
CREATE TABLE sentinel_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_ids UUID[] NOT NULL,
    lga VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    date_generated TIMESTAMP WITH TIME ZONE NOT NULL,
    symptom_profile JSONB NOT NULL,
    students_affected INTEGER NOT NULL,
    threshold_type VARCHAR(50) NOT NULL,
    alert_tier VARCHAR(20) NOT NULL CHECK (alert_tier IN ('school', 'lga', 'state')),
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'acknowledged', 'investigating', 'resolved', 'false_alarm')),
    response_notes TEXT,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved_by UUID REFERENCES users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Sentinel configurations
CREATE TABLE sentinel_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state VARCHAR(100),
    lga VARCHAR(100),
    school_id UUID REFERENCES schools(id),
    symptom_category VARCHAR(100) NOT NULL,
    time_window_hours INTEGER NOT NULL DEFAULT 48,
    cluster_threshold INTEGER NOT NULL DEFAULT 3,
    school_threshold_percent DECIMAL(5,2) NOT NULL DEFAULT 10.0,
    baseline_illness_rate DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Health alert configurations
CREATE TABLE health_alert_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('sick_bay', 'referral_overdue', 'screening_due', 'vaccination_due', 'mental_health')),
    notification_channels TEXT[] DEFAULT ARRAY['in_app'],
    recipients JSONB,  -- Who receives alerts
    is_active BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 3.2 Views for Health Reporting
```sql
-- Chronic condition prevalence view
CREATE VIEW chronic_condition_prevalence AS
SELECT 
    school_id,
    UNNEST(chronic_conditions) as condition,
    COUNT(DISTINCT student_id) as student_count,
    ROUND(
        COUNT(DISTINCT student_id) * 100.0 / (
            SELECT COUNT(*) FROM students 
            WHERE school_id = shp.school_id AND status = 'active'
        ),
        2
    ) as prevalence_percent
FROM student_health_profiles shp
WHERE chronic_conditions IS NOT NULL
GROUP BY school_id, UNNEST(chronic_conditions);

-- Top presenting complaints view
CREATE VIEW top_presenting_complaints AS
SELECT 
    school_id,
    UNNEST(presenting_complaint_codes) as complaint_code,
    COUNT(*) as visit_count,
    DATE_TRUNC('month', visit_date) as month
FROM sick_bay_visits
WHERE visit_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY school_id, UNNEST(presenting_complaint_codes), DATE_TRUNC('month', visit_date)
ORDER BY visit_count DESC;

-- Vaccination coverage view
CREATE VIEW vaccination_coverage AS
SELECT 
    school_id,
    vaccine_name,
    COUNT(DISTINCT student_id) as vaccinated_count,
    (
        SELECT COUNT(*) FROM students 
        WHERE school_id = vr.school_id AND status = 'active'
    ) as total_students,
    ROUND(
        COUNT(DISTINCT student_id) * 100.0 / (
            SELECT COUNT(*) FROM students 
            WHERE school_id = vr.school_id AND status = 'active'
        ),
        2
    ) as coverage_percent
FROM vaccination_records vr
GROUP BY school_id, vaccine_name;

-- Illness signal view (for Sentinel)
CREATE VIEW illness_signal_view AS
SELECT 
    sbv.school_id,
    DATE(sbv.visit_date) as date,
    UNNEST(sbv.presenting_complaint_codes) as symptom_code,
    COUNT(DISTINCT sbv.student_id) as affected_students,
    COUNT(DISTINCT s.class_id) as affected_classes,
    ROUND(
        COUNT(DISTINCT sbv.student_id) * 100.0 / (
            SELECT COUNT(*) FROM students 
            WHERE school_id = sbv.school_id AND status = 'active'
        ),
        2
    ) as percentage_affected
FROM sick_bay_visits sbv
JOIN students s ON sbv.student_id = s.id
WHERE sbv.visit_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY sbv.school_id, DATE(sbv.visit_date), UNNEST(sbv.presenting_complaint_codes);
```

## 4. Sentinel Engine Implementation

### 4.1 Core Sentinel Algorithms
```python
class SentinelEngine:
    """Core Sentinel surveillance engine for disease outbreak detection."""
    
    async def analyze_school_signals(
        self,
        school_id: UUID,
        time_window_hours: int = 48
    ) -> List[SentinelSignal]:
        """Analyze signals from a single school."""
        
        # 1. Get recent sick bay visits and absences
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=time_window_hours)
        
        sick_bay_visits = await self.get_sick_bay_visits(
            school_id, start_date, end_date
        )
        
        illness_absences = await self.get_illness_absences(
            school_id, start_date, end_date
        )
        
        # 2. Combine and analyze symptom patterns
        all_symptom_events = self.combine_symptom_events(
            sick_bay_visits, illness_absences
        )
        
        # 3. Group by symptom profile
        symptom_groups = self.group_by_symptom_profile(all_symptom_events)
        
        # 4. Check each group against thresholds
        signals = []
        for symptom_profile, events in symptom_groups.items():
            config = await self.get_sentinel_config(
                school_id, symptom_profile
            )
            
            if not config or not config.is_active:
                continue
            
            # Check school-level threshold
            if len(events) >= config.cluster_threshold:
                percentage_affected = self.calculate_percentage_affected(
                    events, school_id
                )
                
                if percentage_affected >= config.school_threshold_percent:
                    signal = await self.create_signal(
                        school_id=school_id,
                        symptom_profile=symptom_profile,
                        affected_students=[e.student_id for e in events],
                        threshold_type='school_cluster',
                        alert_tier='school'
                    )
                    signals.append(signal)
        
        return signals
    
    async def analyze_lga_signals(
        self,
        lga: str,
        state: str,
        time_window_hours: int = 96
    ) -> List[SentinelSignal]:
        """Analyze signals across LGA for cross-school clusters."""
        
        # 1. Get schools in LGA
        schools = await self.get_schools_in_lga(lga, state)
        
        # 2. Get recent signals from each school
        all_signals = []
        for school in schools:
            school_signals = await self.analyze_school_signals(
                school.id, time_window_hours
            )
            all_signals.extend(school_signals)
        
        # 3. Cluster similar signals across schools
        clustered_signals = self.cluster_cross_school_signals(all_signals)
        
        # 4. Generate LGA-level signals
        lga_signals = []
        for cluster in clustered_signals:
            if len(cluster.school_ids) >= 2:  # At least 2 schools
                signal = await self.create_signal(
                    school_ids=cluster.school_ids,
                    symptom_profile=cluster.symptom_profile,
                    affected_students=cluster.affected_students,
                    threshold_type='lga_cluster',
                    alert_tier='lga'
                )
                lga_signals.append(signal)
        
        return lga_signals
    
    def combine_symptom_events(
        self,
        sick_bay_visits: List[SickBayVisit],
        illness_absences: List[AttendanceRecord]
    ) -> List[SymptomEvent]:
        """Combine sick bay visits and illness absences into symptom events."""
        
        events = []
        
        # Add sick bay visits
        for visit in sick_bay_visits:
            for symptom in visit.presenting_complaint_codes:
                events.append(SymptomEvent(
                    student_id=visit.student_id,
                    symptom_code=symptom,
                    timestamp=visit.visit_date,
                    source='sick_bay'
                ))
        
        # Add illness absences
        for absence in illness_absences:
            if absence.symptom_codes:
                for symptom in absence.symptom_codes:
                    events.append(SymptomEvent(
                        student_id=absence.student_id,
                        symptom_code=symptom,
                        timestamp=absence.created_at,
                        source='attendance'
                    ))
        
        return events
    
    def group_by_symptom_profile(
        self,
        events: List[SymptomEvent]
    ) -> Dict[str, List[SymptomEvent]]:
        """Group events by normalized symptom profile."""
        
        # Create normalized symptom signature for each student
        student_symptoms = {}
        for event in events:
            if event.student_id not in student_symptoms:
                student_symptoms[event.student_id] = set()
            student_symptoms[event.student_id].add(event.symptom_code)
        
        # Group by symptom profile
        profile_groups = {}
        for student_id, symptoms in student_symptoms.items():
            # Normalize symptom set to sorted tuple for grouping
            profile_key = tuple(sorted(symptoms))
            if profile_key not in profile_groups:
                profile_groups[profile_key] = []
            
            # Find matching events for this student and profile
            matching_events = [
                e for e in events 
                if e.student_id == student_id and e.symptom_code in symptoms
            ]
            profile_groups[profile_key].extend(matching_events)
        
        return profile_groups
    
    async def create_signal(
        self,
        school_id: UUID = None,
        school_ids: List[UUID] = None,
        symptom_profile: tuple = None,
        affected_students: List[UUID] = None,
        threshold_type: str = None,
        alert_tier: str = None
    ) -> SentinelSignal:
        """Create a Sentinel signal for cluster detection."""
        
        # Get geographic information
        if school_id:
            school = await self.school_service.get_school(school_id)
            lga = school.lga
            state = school.state
            school_ids = [school_id]
        else:
            # Get LGA and state from first school
            first_school = await self.school_service.get_school(school_ids[0])
            lga = first_school.lga
            state = first_school.state
        
        # Create signal
        signal = SentinelSignal(
            school_ids=school_ids,
            lga=lga,
            state=state,
            date_generated=datetime.utcnow(),
            symptom_profile={
                'primary_symptoms': list(symptom_profile),
                'affected_count': len(affected_students),
                'time_window_hours': 48
            },
            students_affected=len(affected_students),
            threshold_type=threshold_type,
            alert_tier=alert_tier,
            status='open'
        )
        
        self.session.add(signal)
        await self.session.commit()
        
        # Trigger alerts based on tier
        await self.trigger_alerts(signal)
        
        return signal
    
    async def trigger_alerts(self, signal: SentinelSignal):
        """Trigger alerts based on Sentinel signal tier."""
        
        if signal.alert_tier == 'school':
            # Alert school nurse and headteacher
            await self.alert_school_administrators(signal)
        
        elif signal.alert_tier == 'lga':
            # Alert LGA Health Officer
            await self.alert_lga_health_officer(signal)
            # Also alert school administrators
            await self.alert_school_administrators(signal)
        
        elif signal.alert_tier == 'state':
            # Alert State Epidemiologist
            await self.alert_state_epidemiologist(signal)
            # Also alert LGA and school
            await self.alert_lga_health_officer(signal)
            await self.alert_school_administrators(signal)
```

### 4.2 Alert Generation Logic
```python
class AlertService:
    """Service for generating and managing health alerts."""
    
    async def alert_school_administrators(self, signal: SentinelSignal):
        """Alert school headteacher and nurse."""
        
        for school_id in signal.school_ids:
            school = await self.school_service.get_school(school_id)
            
            # Get school administrators
            admins = await self.get_school_administrators(school_id)
            
            # Create alert content
            alert_content = self.format_school_alert(signal, school)
            
            # Send alerts
            for admin in admins:
                # In-app notification
                await self.create_notification(
                    recipient_id=admin.id,
                    notification_type='sentinel_alert_school',
                    title='Unusual Illness Pattern Detected',
                    message=alert_content,
                    channel='in_app'
                )
                
                # WhatsApp/SMS for urgent alerts
                if signal.students_affected >= 5:
                    await self.send_whatsapp_alert(
                        phone=admin.phone,
                        message=alert_content
                    )
    
    async def alert_lga_health_officer(self, signal: SentinelSignal):
        """Alert LGA Health Officer."""
        
        # Get LGA Health Officer
        lga_officer = await self.get_lga_health_officer(
            signal.lga, signal.state
        )
        
        if lga_officer:
            alert_content = self.format_lga_alert(signal)
            
            # Create notification
            await self.create_notification(
                recipient_id=lga_officer.id,
                notification_type='sentinel_alert_lga',
                title=f'Cross-School Illness Cluster Detected in {signal.lga}',
                message=alert_content,
                channel='in_app'
            )
            
            # Send SMS for immediate attention
            await self.send_sms_alert(
                phone=lga_officer.phone,
                message=alert_content
            )
    
    def format_school_alert(self, signal: SentinelSignal, school: School) -> str:
        """Format alert message for school administrators."""
        
        symptoms = ', '.join(signal.symptom_profile['primary_symptoms'])
        
        return f"""
🚨 HEALTH ALERT - {school.name}

An unusual illness pattern has been detected:

• School: {school.name}
• Location: {school.lga}, {school.state}
• Students affected: {signal.students_affected}
• Symptoms: {symptoms}
• Detection time: {signal.date_generated.strftime('%Y-%m-%d %H:%M')}
• Alert tier: {signal.alert_tier.upper()}

RECOMMENDED ACTIONS:
1. Investigate school water supply and food handling
2. Consider temporary isolation of affected students
3. Contact LGA Health Office if symptoms worsen
4. Monitor attendance for additional cases

This alert was generated by the LafiyaSentinel surveillance system.
        """.strip()
```

## 5. UI Component Specifications

### 5.1 Health Profile Component
```typescript
interface HealthProfileProps {
  studentId: string;
  readOnly?: boolean;
  onUpdate?: (profile: HealthProfile) => void;
}

// Profile Sections:
// 1. Basic health information (blood group, genotype)
// 2. Chronic conditions list (editable)
// 3. Allergies list (editable)
// 4. Current medications (editable)
// 5. Emergency notes (encrypted, nurse-only)
// 6. Family health history (guardian-provided)
// 7. Vision and hearing status
// 8. Vaccination summary
// 9. Recent sick bay visits
// 10. Screening history

// Confidentiality Controls:
interface ConfidentialityControls {
  showToTeacher: boolean;
  showToAdmin: boolean;
  showToParent: boolean;
  restrictedFields: string[];
}
```

### 5.2 Sick Bay Visit Component
```typescript
interface SickBayVisitFormProps {
  studentId?: string;
  onVisitLogged: (visit: SickBayVisit) => void;
}

// Form Fields:
// 1. Student search/selection
// 2. Date and time (auto-populated)
// 3. Presenting complaints (checklist)
// 4. Complaint notes (free text)
// 5. Vital signs (temperature, BP, pulse)
// 6. Treatment given
// 7. Outcome selection
// 8. Referral details (if referred)

// Batch Screening Mode:
interface BatchScreeningProps {
  classId: string;
  screeningType: 'annual' | 'termly';
  onComplete: () => void;
}
```

### 5.3 Sentinel Dashboard Component
```typescript
interface SentinelDashboardProps {
  schoolId?: string;
  lga?: string;
  state?: string;
  viewLevel: 'school' | 'lga' | 'state';
}

// Dashboard Components:
// 1. Active alerts list
// 2. Geographic illness heatmap
// 3. Symptom trend charts
// 4. School comparison matrix
// 5. Alert history timeline
// 6. Threshold configuration panel
// 7. Export/report generation

// Alert Card:
interface AlertCardProps {
  signal: SentinelSignal;
  onAcknowledge: () => void;
  onResolve: () => void;
  onViewDetails: () => void;
}
```

## 6. Testing Requirements

### 6.1 Unit Tests
```python
# Test cases for SentinelEngine
class TestSentinelEngine:
    async def test_analyze_school_signals_cluster_detected(self):
        """Test cluster detection when threshold reached."""
        pass
    
    async def test_analyze_school_signals_below_threshold(self):
        """Test no alert when below threshold."""
        pass
    
    async def test_combine_symptom_events(self):
        """Test combining sick bay and attendance data."""
        pass
    
    async def test_group_by_symptom_profile(self):
        """Test symptom profile grouping."""
        pass
    
    async def test_cluster_cross_school_signals(self):
        """Test cross-school signal clustering."""
        pass

# Test cases for HealthService
class TestHealthService:
    async def test_log_sick_bay_visit(self):
        """Test sick bay visit logging."""
        pass
    
    async def test_conduct_screening(self):
        """Test health screening."""
        pass
    
    async def test_create_referral(self):
        """Test referral creation."""
        pass
    
    async def test_mental_health_screening(self):
        """Test mental health screening."""
        pass
```

### 6.2 Integration Tests
```python
class TestSentinelAPI:
    async def test_sentinel_alerts_endpoint(self):
        """Test GET /api/v1/sentinel/alerts endpoint."""
        pass
    
    async def test_acknowledge_alert_endpoint(self):
        """Test PATCH /api/v1/sentinel/alerts/{id}/acknowledge endpoint."""
        pass
    
    async def test_sentinel_dashboard_endpoint(self):
        """Test GET /api/v1/sentinel/dashboard endpoint."""
        pass

class TestHealthAPI:
    async def test_sick_bay_visit_endpoint(self):
        """Test POST /api/v1/health/sick-bay-visits endpoint."""
        pass
    
    async def test_health_profile_endpoint(self):
        """Test GET /api/v1/health/students/{id}/profile endpoint."""
        pass
    
    async def test_screening_endpoint(self):
        """Test POST /api/v1/health/screenings endpoint."""
        pass
```

## 7. Security Considerations

### 7.1 Access Control
```python
# Role-based access for Health module
HEALTH_PERMISSIONS = {
    "school_admin": [
        "health:read:aggregate",
        "health:read:sick_bay_summary",
        "health:read:screening_coverage",
        "health:read:vaccination_coverage",
        "health:manage_referrals"
    ],
    "nurse": [
        "health:create:sick_bay_visit",
        "health:read:student_profile",
        "health:update:student_profile",
        "health:create:screening",
        "health:create:referral",
        "health:read:mental_health",
        "health:create:mental_health_assessment",
        "health:read:sentinel_alerts"
    ],
    "teacher": [
        "health:read:emergency_notes",
        "health:read:student_alerts"
    ],
    "parent": [
        "health:read:own_child_summary",
        "health:read:own_child_vaccination",
        "health:read:referral_status"
    ],
    "student": [
        "health:read:own_profile"
    ],
    "lga_health": [
        "health:read:lga_aggregate",
        "health:read:sentinel_alerts",
        "health:read:outbreak_investigation"
    ],
    "state_health": [
        "health:read:state_aggregate",
        "health:read:sentinel_dashboard",
        "health:read:idsr_export"
    ]
}
```

### 7.2 Data Privacy
```python
# Sensitive health data handling
SENSITIVE_HEALTH_DATA = [
    "sickle_cell_status",     # Genotype information
    "mental_health_data",     # Mental health assessments
    "hiv_status",            # If collected
    "chronic_conditions",    # Chronic illness information
    "emergency_notes"        # Clinical notes
]

# Access logging for health data
HEALTH_ACCESS_LOGGING = True

# Encryption for sensitive fields
ENCRYPTED_HEALTH_FIELDS = [
    "emergency_notes",
    "family_health_history"
]
```

## 8. Performance Requirements

### 8.1 Performance Metrics
```yaml
Performance Requirements:
  Sick Bay Visit Logging:
    - Target: < 2 seconds for single visit
    - Target: < 1 minute for batch screening of class (45 students)
    - Validation: Real-time (< 100ms)
  
  Sentinel Analysis:
    - Target: < 5 minutes for daily batch analysis (per school)
    - Target: < 15 minutes for LGA-wide analysis
    - Alert generation: < 15 minutes from threshold crossing
  
  Health Dashboard:
    - Target: < 3 seconds for school health dashboard
    - Target: < 5 seconds for LGA health dashboard
    - Target: < 10 seconds for state health dashboard
    - Caching: 5-minute cache for dashboard data
  
  Referral Tracking:
    - Target: < 2 seconds for referral status update
    - Reminder generation: < 30 minutes for overdue referrals
    - Batch processing: < 5 minutes for daily referral reminders
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed health data
HEALTH_CACHE_CONFIG = {
    "student_health_profile": {
        "ttl": 300,  # 5 minutes
        "key": "student:{student_id}:health_profile"
    },
    "school_health_summary": {
        "ttl": 300,  # 5 minutes
        "key": "school:{school_id}:health_summary:term:{term_id}"
    },
    "sentinel_signals": {
        "ttl": 60,  # 1 minute for real-time alerts
        "key": "school:{school_id}:sentinel_signals:active"
    },
    "vaccination_coverage": {
        "ttl": 3600,  # 1 hour
        "key": "school:{school_id}:vaccination_coverage"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
HEALTH_INTEGRATIONS = {
    "sis": {
        "student_data": "student enrollment, demographic data",
        "validation": "student must be active and enrolled"
    },
    "attendance": {
        "illness_absences": "absence data with symptom codes",
        "attendance_correlation": "correlate health with attendance patterns"
    },
    "academics": {
        "health_impact": "correlate health with academic performance",
        "screening_scheduling": "coordinate screenings with academic calendar"
    },
    "finance": {
        "medical_fees": "track medical fees and waivers",
        "screening_fees": "charge for health screenings if applicable"
    },
    "parent_portal": {
        "health_notifications": "send sick bay visit notifications",
        "screening_results": "share screening results with parents",
        "referral_updates": "update parents on referral status"
    },
    "sentinel": {
        "real_time_data": "feed health and absence data for analysis",
        "alert_generation": "generate and manage Sentinel alerts"
    },
    "intelligence": {
        "health_analytics": "provide data for health dashboards",
        "outbreak_trends": "support disease trend analysis"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_HEALTH_INTEGRATIONS = {
    "whatsapp": {
        "purpose": "Send health notifications to parents",
        "templates": [
            "sick_bay_visit_notification",
            "referral_notification",
            "screening_results",
            "vaccination_reminder"
        ],
        "privacy": "minimal health information shared"
    },
    "termii": {
        "purpose": "SMS backup for urgent health alerts",
        "templates": ["urgent_health_alert", "referral_reminder"],
        "fallback": "used when WhatsApp delivery fails"
    },
    "nphcda": {
        "purpose": "Immunization data exchange",
        "format": "API or batch import/export",
        "frequency": "monthly sync"
    },
    "dhis2": {
        "purpose": "Health data export for national reporting",
        "format": "DHIS2 API",
        "frequency": "weekly export"
    },
    "idsr": {
        "purpose": "Integrated Disease Surveillance and Response reporting",
        "format": "IDSR-standard CSV",
        "frequency": "weekly and outbreak-triggered"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create StudentHealthProfile model and schema
- [ ] Create SickBayVisit model and schema
- [ ] Create HealthScreening model and schema
- [ ] Create MentalHealthAssessment model and schema
- [ ] Create Referral model and schema
- [ ] Create VaccinationRecord model and schema
- [ ] Create SentinelSignal model and schema
- [ ] Create SentinelConfiguration model and schema
- [ ] Implement HealthService
- [ ] Implement SentinelEngine
- [ ] Implement AlertService
- [ ] Create health API endpoints
- [ ] Create Sentinel API endpoints
- [ ] Implement sick bay visit logging
- [ ] Implement health screening
- [ ] Implement mental health screening
- [ ] Implement referral management
- [ ] Implement vaccination tracking
- [ ] Implement Sentinel analysis algorithms
- [ ] Implement alert generation
- [ ] Implement geospatial mapping
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create HealthProfile component
- [ ] Create SickBayVisitForm component
- [ ] Create HealthScreeningForm component
- [ ] Create MentalHealthScreening component
- [ ] Create ReferralTracker component
- [ ] Create VaccinationRecords component
- [ ] Create SentinelDashboard component
- [ ] Create AlertCard component
- [ ] Create BatchScreening component
- [ ] Implement health profile editing
- [ ] Implement sick bay workflow
- [ ] Implement screening workflow
- [ ] Implement referral workflow
- [ ] Implement Sentinel alerts UI
- [ ] Implement geospatial maps
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Sentinel Engine Tasks
- [ ] Implement symptom data aggregation
- [ ] Implement cluster detection algorithms
- [ ] Implement threshold calibration
- [ ] Implement baseline calculation
- [ ] Implement cross-school analysis
- [ ] Implement LGA-level analysis
- [ ] Implement state-level analysis
- [ ] Implement false positive reduction
- [ ] Implement alert tier determination
- [ ] Implement alert generation logic
- [ ] Test with historical outbreak data
- [ ] Calibrate with epidemiologists

### 11.4 Testing Tasks
- [ ] Unit tests for HealthService
- [ ] Unit tests for SentinelEngine
- [ ] Integration tests for API endpoints
- [ ] E2E tests for health workflows
- [ ] Sentinel accuracy testing
- [ ] Alert generation testing
- [ ] Performance testing
- [ ] Security testing (PHI protection)
- [ ] Privacy testing (confidentiality controls)

---

*This module specification provides a comprehensive guide for implementing the School Health & Sentinel Engine system. The module combines comprehensive school health management with automated disease surveillance, making schools into public health early-warning nodes while providing essential health services to students.*

---

**End of School Health & Sentinel Engine (M5) Specification**