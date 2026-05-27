# EduLafia Platform - Data Model Specification

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. Data Model Overview

### 1.1 Design Principles
1. **Normalization**: Third Normal Form (3NF) for transactional data
2. **Denormalization**: Strategic denormalization for reporting and performance
3. **Audit Trail**: All tables include audit fields (created_at, updated_at, etc.)
4. **Soft Deletes**: Records are never deleted, only marked as inactive
5. **UUID Primary Keys**: All primary keys use UUID for distributed system compatibility
6. **JSON Flexibility**: JSONB columns for flexible, schema-less data where needed

### 1.2 Schema Organization
```sql
-- Database creation
CREATE DATABASE edulafia
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TEMPLATE = template0;
```

### 1.3 Common Table Structure
All tables include these common audit fields:
```sql
-- Common audit fields template
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
created_by UUID REFERENCES users(id),
updated_by UUID REFERENCES users(id),
deleted_at TIMESTAMP WITH TIME ZONE,
deleted_by UUID REFERENCES users(id),
version INTEGER DEFAULT 1
```

## 2. Core Tables

### 2.1 Users and Authentication
```sql
-- Users table (for all system users)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    must_change_password BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Roles table
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB NOT NULL DEFAULT '[]',
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- User roles (many-to-many)
CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    assigned_by UUID REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(user_id, role_id)
);

-- Refresh tokens for JWT
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    revoked_at TIMESTAMP WITH TIME ZONE,
    revoked_by UUID REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 2.2 Schools and Academic Structure
```sql
-- Schools table
CREATE TABLE schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('private', 'public', 'federal')),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100) NOT NULL,
    lga VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    principal_name VARCHAR(200),
    principal_phone VARCHAR(20),
    principal_email VARCHAR(255),
    subscription_tier VARCHAR(20) CHECK (subscription_tier IN ('starter', 'standard', 'premium')),
    subscription_start_date DATE,
    subscription_end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    logo_url VARCHAR(500),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Academic years
CREATE TABLE academic_years (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, name)
);

-- Terms (semesters)
CREATE TABLE terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    term_number INTEGER NOT NULL CHECK (term_number BETWEEN 1 AND 3),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(academic_year_id, term_number)
);

-- Classes (e.g., JSS1A, SS2B)
CREATE TABLE classes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL CHECK (level IN ('JSS1', 'JSS2', 'JSS3', 'SS1', 'SS2', 'SS3')),
    arm VARCHAR(10) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 45,
    form_teacher_id UUID REFERENCES staff(id),
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, name, academic_year_id)
);

-- Subjects
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL,
    description TEXT,
    is_core BOOLEAN DEFAULT TRUE,
    waec_code VARCHAR(20),
    neco_code VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, code)
);

-- Staff (teachers and non-teaching staff)
CREATE TABLE staff (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    staff_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    whatsapp_phone VARCHAR(20),
    role VARCHAR(50) NOT NULL CHECK (role IN ('teacher', 'nurse', 'bursar', 'admin', 'accountant', 'librarian', 'lab_attendant', 'security', 'cleaner', 'other')),
    department VARCHAR(100),
    qualifications TEXT,
    subjects UUID[] DEFAULT '{}',
    employment_type VARCHAR(20) DEFAULT 'permanent' CHECK (employment_type IN ('permanent', 'contract', 'nysc', 'intern')),
    employment_date DATE,
    salary DECIMAL(12, 2),
    is_active BOOLEAN DEFAULT TRUE,
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
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(staff_id, class_id, subject_id, academic_year_id)
);
```

### 2.3 Students and Guardians
```sql
-- Students table
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, admission_number)
);

-- Guardians/Parents
CREATE TABLE guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    whatsapp_phone VARCHAR(20),
    relationship VARCHAR(50) NOT NULL CHECK (relationship IN ('father', 'mother', 'uncle', 'aunt', 'brother', 'sister', 'grandparent', 'guardian', 'other')),
    occupation VARCHAR(100),
    address TEXT,
    is_primary_contact BOOLEAN DEFAULT FALSE,
    portal_access_token VARCHAR(500),
    portal_access_expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Student-Guardian relationship (many-to-many)
CREATE TABLE student_guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    is_emergency_contact BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, guardian_id)
);

-- Student documents (admission letters, birth certificates, etc.)
CREATE TABLE student_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL CHECK (document_type IN ('admission_letter', 'birth_certificate', 'transfer_letter', 'medical_record', 'report_card', 'other')),
    document_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 2.4 Attendance and Health
```sql
-- Attendance records (partitioned by date)
CREATE TABLE attendance_records (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    period INTEGER,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'absent', 'late', 'excused')),
    reason_code VARCHAR(50) CHECK (reason_code IN ('sick', 'family', 'unknown', 'excused', 'suspended')),
    symptom_codes TEXT[],
    notes TEXT,
    recorded_by UUID NOT NULL REFERENCES users(id),
    edited_at TIMESTAMP WITH TIME ZONE,
    edited_by UUID REFERENCES users(id),
    edit_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    PRIMARY KEY (id, date)
) PARTITION BY RANGE (date);

-- Create monthly partitions for 2026
CREATE TABLE attendance_records_2026_01 
    PARTITION OF attendance_records
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE attendance_records_2026_02 
    PARTITION OF attendance_records
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Continue for all months of 2026, 2027, etc.

-- Indexes for attendance
CREATE INDEX idx_attendance_student_date ON attendance_records(student_id, date);
CREATE INDEX idx_attendance_class_date ON attendance_records(class_id, date);
CREATE INDEX idx_attendance_school_date ON attendance_records(school_id, date);
CREATE INDEX idx_attendance_status_date ON attendance_records(status, date);
CREATE INDEX idx_attendance_reason_date ON attendance_records(reason_code, date);

-- Sick bay visits
CREATE TABLE sick_bay_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    visit_date TIMESTAMP WITH TIME ZONE NOT NULL,
    presenting_complaint_codes TEXT[] NOT NULL,
    presenting_complaint_notes TEXT,
    temperature DECIMAL(4, 1),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    pulse_rate INTEGER,
    treatment_given TEXT,
    outcome VARCHAR(50) NOT NULL CHECK (outcome IN ('returned_to_class', 'sent_home', 'referred', 'hospitalized')),
    referred_to VARCHAR(255),
    referred_by UUID REFERENCES staff(id),
    recorded_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Health screenings
CREATE TABLE health_screenings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    screening_date DATE NOT NULL,
    screening_type VARCHAR(50) NOT NULL CHECK (screening_type IN ('annual', 'termly', 'ad_hoc')),
    height DECIMAL(5, 2),
    weight DECIMAL(5, 2),
    bmi DECIMAL(5, 2),
    muac DECIMAL(5, 2),
    vision_left DECIMAL(3, 1),
    vision_right DECIMAL(3, 1),
    hearing_left VARCHAR(20),
    hearing_right VARCHAR(20),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    dental_notes TEXT,
    flags TEXT[],
    conducted_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Mental health assessments
CREATE TABLE mental_health_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    assessment_date DATE NOT NULL,
    term_id UUID NOT NULL REFERENCES terms(id),
    responses JSONB NOT NULL,
    total_score INTEGER,
    flag_level VARCHAR(20) CHECK (flag_level IN ('none', 'watch', 'refer')),
    counsellor_assigned_id UUID REFERENCES staff(id),
    conducted_by UUID NOT NULL REFERENCES users(id),
    is_confidential BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 2.5 Academic Records
```sql
-- Academic results (CA and exam scores)
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, subject_id, term_id)
);

-- Grading scales (school-specific)
CREATE TABLE grading_scales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Report cards
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, term_id)
);
```

### 2.6 Finance and Fees
```sql
-- Fee schedules
CREATE TABLE fee_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Fee schedule items
CREATE TABLE fee_schedule_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fee_schedule_id UUID NOT NULL REFERENCES fee_schedules(id) ON DELETE CASCADE,
    class_level VARCHAR(20) NOT NULL,
    fee_category VARCHAR(100) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Fee ledger (transaction log)
CREATE TABLE fee_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('charge', 'payment', 'waiver', 'refund', 'adjustment')),
    fee_category VARCHAR(100) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50) CHECK (payment_method IN ('cash', 'bank_transfer', 'paystack', 'flutterwave', 'remita', 'cheque')),
    payment_reference VARCHAR(255),
    receipt_number VARCHAR(100),
    description TEXT,
    term_id UUID REFERENCES terms(id),
    academic_year_id UUID REFERENCES academic_years(id),
    recorded_by UUID NOT NULL REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Scholarships and waivers
CREATE TABLE scholarships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    amount DECIMAL(12, 2),
    percentage DECIMAL(5, 2),
    criteria JSONB,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Student scholarships
CREATE TABLE student_scholarships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    scholarship_id UUID NOT NULL REFERENCES scholarships(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    amount_awarded DECIMAL(12, 2) NOT NULL,
    awarded_date DATE NOT NULL,
    awarded_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, scholarship_id, academic_year_id)
);
```

### 2.7 Sentinel Surveillance
```sql
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Sentinel configuration
CREATE TABLE sentinel_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state VARCHAR(100),
    lga VARCHAR(100),
    symptom_category VARCHAR(100) NOT NULL,
    time_window_hours INTEGER NOT NULL DEFAULT 48,
    cluster_threshold INTEGER NOT NULL DEFAULT 3,
    school_threshold_percent DECIMAL(5, 2) NOT NULL DEFAULT 10.0,
    baseline_illness_rate DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

### 2.8 Timetable and Scheduling
```sql
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Timetable entries
CREATE TABLE timetable_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timetable_id UUID NOT NULL REFERENCES timetables(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    period_number INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    room_number VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(timetable_id, day_of_week, period_number)
);
```

### 2.9 Notifications and Audit
```sql
-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient_type VARCHAR(20) NOT NULL CHECK (recipient_type IN ('user', 'guardian', 'staff', 'school', 'lga', 'state')),
    recipient_id UUID NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('in_app', 'sms', 'whatsapp', 'email')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'delivered', 'failed', 'read')),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Audit logs (immutable, no updated_at)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- No updated_at, deleted_at, or version for audit logs
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions for audit logs
CREATE TABLE audit_logs_2026_01 
    PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Sync status for offline devices
CREATE TABLE sync_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    school_id UUID NOT NULL REFERENCES schools(id),
    last_sync_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'synced' CHECK (sync_status IN ('synced', 'pending', 'failed', 'conflict')),
    pending_operations INTEGER DEFAULT 0,
    last_operation_timestamp TIMESTAMP WITH TIME ZONE,
    device_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);
```

## 3. Indexes and Performance

### 3.1 Performance Indexes
```sql
-- Student performance indexes
CREATE INDEX idx_students_school_status ON students(school_id, status);
CREATE INDEX idx_students_class_status ON students(class_id, status);
CREATE INDEX idx_students_admission_number ON students(admission_number);
CREATE INDEX idx_students_nin ON students(nin);

-- Attendance performance indexes
CREATE INDEX idx_attendance_student_date_range ON attendance_records(student_id, date);
CREATE INDEX idx_attendance_class_date_range ON attendance_records(class_id, date);
CREATE INDEX idx_attendance_school_date_range ON attendance_records(school_id, date);
CREATE INDEX idx_attendance_status_date ON attendance_records(status, date);
CREATE INDEX idx_attendance_reason_date ON attendance_records(reason_code, date);

-- Academic performance indexes
CREATE INDEX idx_academic_results_student_term ON academic_results(student_id, term_id);
CREATE INDEX idx_academic_results_subject_term ON academic_results(subject_id, term_id);
CREATE INDEX idx_academic_results_class_term ON academic_results(class_id, term_id);

-- Finance performance indexes
CREATE INDEX idx_fee_ledger_student_date ON fee_ledger(student_id, transaction_date);
CREATE INDEX idx_fee_ledger_school_date ON fee_ledger(school_id, transaction_date);
CREATE INDEX idx_fee_ledger_type_date ON fee_ledger(transaction_type, transaction_date);

-- Health performance indexes
CREATE INDEX idx_sick_bay_student_date ON sick_bay_visits(student_id, visit_date);
CREATE INDEX idx_sick_bay_school_date ON sick_bay_visits(school_id, visit_date);
CREATE INDEX idx_health_screenings_student_date ON health_screenings(student_id, screening_date);
CREATE INDEX idx_vaccination_student_date ON vaccination_records(student_id, administration_date);

-- Sentinel performance indexes
CREATE INDEX idx_sentinel_signals_date ON sentinel_signals(date_generated);
CREATE INDEX idx_sentinel_signals_status ON sentinel_signals(status);
CREATE INDEX idx_sentinel_signals_alert_tier ON sentinel_signals(alert_tier);
```

### 3.2 Unique Constraints
```sql
-- Ensure one attendance record per student per day
CREATE UNIQUE INDEX idx_attendance_unique_student_date 
    ON attendance_records(student_id, date) 
    WHERE deleted_at IS NULL;

-- Ensure one result per student per subject per term
CREATE UNIQUE INDEX idx_academic_results_unique 
    ON academic_results(student_id, subject_id, term_id) 
    WHERE deleted_at IS NULL;

-- Ensure one report card per student per term
CREATE UNIQUE INDEX idx_report_cards_unique 
    ON report_cards(student_id, term_id) 
    WHERE deleted_at IS NULL;
```

## 4. Views and Functions

### 4.1 Common Views
```sql
-- View for student summary
CREATE VIEW student_summary AS
SELECT 
    s.id,
    s.school_id,
    s.admission_number,
    s.first_name || ' ' || s.last_name AS full_name,
    s.class_id,
    c.name AS class_name,
    s.status,
    s.date_of_birth,
    EXTRACT(YEAR FROM AGE(s.date_of_birth)) AS age,
    g.first_name AS guardian_first_name,
    g.last_name AS guardian_last_name,
    g.phone AS guardian_phone,
    g.whatsapp_phone AS guardian_whatsapp
FROM students s
LEFT JOIN classes c ON s.class_id = c.id
LEFT JOIN student_guardians sg ON s.id = sg.student_id AND sg.is_emergency_contact = TRUE
LEFT JOIN guardians g ON sg.guardian_id = g.id
WHERE s.deleted_at IS NULL;

-- View for attendance summary
CREATE VIEW attendance_summary AS
SELECT 
    a.student_id,
    a.class_id,
    a.school_id,
    DATE_TRUNC('month', a.date) AS month,
    COUNT(*) AS total_days,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) AS present_days,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) AS absent_days,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) AS late_days,
    ROUND(
        COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) AS attendance_percentage
FROM attendance_records a
WHERE a.deleted_at IS NULL
GROUP BY a.student_id, a.class_id, a.school_id, DATE_TRUNC('month', a.date);

-- View for academic performance
CREATE VIEW academic_performance AS
SELECT 
    ar.student_id,
    ar.term_id,
    ar.school_id,
    ROUND(AVG(ar.total_score), 2) AS average_score,
    COUNT(*) AS subjects_count,
    RANK() OVER (PARTITION BY ar.class_id, ar.term_id ORDER BY AVG(ar.total_score) DESC) AS class_rank
FROM academic_results ar
WHERE ar.deleted_at IS NULL AND ar.flag IS NULL
GROUP BY ar.student_id, ar.term_id, ar.class_id, ar.school_id;

-- View for financial summary
CREATE VIEW financial_summary AS
SELECT 
    fl.student_id,
    fl.school_id,
    fl.academic_year_id,
    fl.term_id,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) AS total_charges,
    SUM(CASE WHEN fl.transaction_type = 'payment' THEN fl.amount ELSE 0 END) AS total_payments,
    SUM(CASE WHEN fl.transaction_type = 'waiver' THEN fl.amount ELSE 0 END) AS total_waivers,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) 
        - SUM(CASE WHEN fl.transaction_type IN ('payment', 'waiver') THEN fl.amount ELSE 0 END) AS balance
FROM fee_ledger fl
WHERE fl.deleted_at IS NULL
GROUP BY fl.student_id, fl.school_id, fl.academic_year_id, fl.term_id;

-- View for health alerts
CREATE VIEW health_alerts AS
SELECT 
    sbv.student_id,
    sbv.school_id,
    sbv.visit_date,
    sbv.presenting_complaint_codes,
    sbv.outcome,
    s.first_name || ' ' || s.last_name AS student_name,
    s.class_id,
    c.name AS class_name
FROM sick_bay_visits sbv
JOIN students s ON sbv.student_id = s.id
LEFT JOIN classes c ON s.class_id = c.id
WHERE sbv.deleted_at IS NULL 
    AND sbv.visit_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY sbv.visit_date DESC;
```

### 4.2 Utility Functions
```sql
-- Function to calculate age
CREATE OR REPLACE FUNCTION calculate_age(birth_date DATE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(birth_date));
END;
$$ LANGUAGE plpgsql;

-- Function to generate student admission number
CREATE OR REPLACE FUNCTION generate_admission_number(school_id UUID)
RETURNS VARCHAR AS $$
DECLARE
    school_code VARCHAR;
    next_number INTEGER;
    admission_number VARCHAR;
BEGIN
    SELECT code INTO school_code FROM schools WHERE id = school_id;
    
    SELECT COALESCE(MAX(
        CAST(SUBSTRING(admission_number FROM '[0-9]+$') AS INTEGER)
    ), 0) + 1 INTO next_number
    FROM students 
    WHERE students.school_id = school_id;
    
    admission_number := school_code || '-' || LPAD(next_number::TEXT, 4, '0');
    RETURN admission_number;
END;
$$ LANGUAGE plpgsql;

-- Function to check for sentinel alerts
CREATE OR REPLACE FUNCTION check_sentinel_alerts(
    p_school_id UUID,
    p_symptom_codes TEXT[],
    p_time_window_hours INTEGER DEFAULT 48
)
RETURNS BOOLEAN AS $$
DECLARE
    affected_count INTEGER;
    school_total_students INTEGER;
    threshold_percent DECIMAL;
BEGIN
    -- Count students with similar symptoms in time window
    SELECT COUNT(DISTINCT student_id) INTO affected_count
    FROM attendance_records
    WHERE school_id = p_school_id
        AND status = 'absent'
        AND reason_code = 'sick'
        AND symptom_codes && p_symptom_codes
        AND date >= CURRENT_DATE - (p_time_window_hours || ' hours')::INTERVAL;
    
    -- Get school total students
    SELECT COUNT(*) INTO school_total_students
    FROM students
    WHERE school_id = p_school_id AND status = 'active';
    
    -- Calculate threshold percent
    threshold_percent := (affected_count::DECIMAL / school_total_students::DECIMAL) * 100;
    
    -- Return true if threshold exceeded
    RETURN threshold_percent >= 10.0; -- Default 10% threshold
END;
$$ LANGUAGE plpgsql;
```

## 5. Data Migration Scripts

### 5.1 Initial Data Setup
```sql
-- Insert default roles
INSERT INTO roles (id, name, description, permissions, is_system_role) VALUES
    (gen_random_uuid(), 'super_admin', 'Super Administrator', '["*"]', TRUE),
    (gen_random_uuid(), 'school_admin', 'School Administrator', '["school:*", "student:*", "attendance:*", "academic:*", "finance:*", "health:*"]', TRUE),
    (gen_random_uuid(), 'teacher', 'Teacher', '["attendance:mark", "academic:grade", "student:read"]', TRUE),
    (gen_random_uuid(), 'nurse', 'School Nurse', '["health:*", "student:read", "attendance:read"]', TRUE),
    (gen_random_uuid(), 'bursar', 'Bursar', '["finance:*", "student:read"]', TRUE),
    (gen_random_uuid(), 'parent', 'Parent/Guardian', '["student:read:own", "attendance:read:own", "academic:read:own"]', TRUE),
    (gen_random_uuid(), 'student', 'Student', '["student:read:own", "academic:read:own"]', TRUE),
    (gen_random_uuid(), 'lga_education', 'LGA Education Officer', '["school:read:aggregate", "student:read:aggregate"]', TRUE),
    (gen_random_uuid(), 'lga_health', 'LGA Health Officer', '["sentinel:read", "health:read:aggregate"]', TRUE),
    (gen_random_uuid(), 'state_education', 'State MOE Official', '["school:read:state", "student:read:state"]', TRUE),
    (gen_random_uuid(), 'state_health', 'State MOH Official', '["sentinel:read:state", "health:read:state"]', TRUE),
    (gen_random_uuid(), 'system_admin', 'System Administrator', '["*"]', TRUE);

-- Insert default grading scale (WAEC/NECO)
INSERT INTO grading_scales (id, school_id, name, description, is_default) VALUES
    (gen_random_uuid(), NULL, 'WAEC/NECO Standard', 'Standard WAEC/NECO grading scale', TRUE);

INSERT INTO grading_scale_details (grading_scale_id, grade, min_score, max_score, remark, position)
SELECT 
    gs.id,
    g.grade,
    g.min_score,
    g.max_score,
    g.remark,
    g.position
FROM grading_scales gs,
(VALUES 
    ('A1', 75.00, 100.00, 'Excellent', 1),
    ('B2', 70.00, 74.99, 'Very Good', 2),
    ('B3', 65.00, 69.99, 'Good', 3),
    ('C4', 60.00, 64.99, 'Credit', 4),
    ('C5', 55.00, 59.99, 'Credit', 5),
    ('C6', 50.00, 54.99, 'Credit', 6),
    ('D7', 45.00, 49.99, 'Pass', 7),
    ('E8', 40.00, 44.99, 'Pass', 8),
    ('F9', 0.00, 39.99, 'Fail', 9)
) AS g(grade, min_score, max_score, remark, position)
WHERE gs.name = 'WAEC/NECO Standard';

-- Insert default sentinel configurations
INSERT INTO sentinel_configurations (id, symptom_category, time_window_hours, cluster_threshold, school_threshold_percent) VALUES
    (gen_random_uuid(), 'respiratory', 48, 3, 10.0),
    (gen_random_uuid(), 'gastrointestinal', 48, 3, 10.0),
    (gen_random_uuid(), 'fever', 48, 3, 10.0),
    (gen_random_uuid(), 'rash', 72, 5, 15.0),
    (gen_random_uuid(), 'neurological', 24, 2, 5.0);
```

## 6. Backup and Recovery

### 6.1 Backup Strategy
```sql
-- Full backup command (run daily)
-- pg_dump -h localhost -U edulafia edulafia > backup_$(date +%Y%m%d).sql

-- Incremental backup (using WAL archiving)
-- archive_mode = on
-- archive_command = 'cp %p /path/to/archive/%f'

-- Point-in-time recovery
-- restore_command = 'cp /path/to/archive/%f %p'
-- recovery_target_time = '2026-03-26 14:30:00'
```

### 6.2 Maintenance Scripts
```sql
-- Vacuum and analyze (run weekly)
VACUUM ANALYZE;

-- Reindex (run monthly)
REINDEX DATABASE edulafia;

-- Check for bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

*This data model specification provides the complete database schema for the EduLafia platform. All tables include proper relationships, constraints, and indexes for optimal performance.*

---

**End of Data Model Specification**