# EduLafia Platform - Module Specification: System Administration & Onboarding (M9)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M9 - System Administration & Onboarding
- **Priority:** Medium (Extended Module)
- **LafiyaSentinel Layer:** YES — Sentinel thresholds configured here

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
The System Administration & Onboarding module provides comprehensive platform administration capabilities including school provisioning, user management, sync monitoring, Sentinel threshold configuration, system updates, and usage analytics. This module enables LafiyaCore administrators to efficiently manage the entire EduLafia platform and onboard new schools.

### 1.2 Scope
- School provisioning wizard
- User and role management
- Sync health monitoring
- Sentinel threshold configuration
- System update deployment
- Usage analytics
- Training resource management
- System configuration
- Audit log management
- Platform health monitoring

### 1.3 Dependencies
- **Required Modules:** All other modules depend on system administration
- **External Dependencies:** Monitoring services, email/SMS for notifications
- **System Access:** Super admin and LafiyaCore admin access only

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 School Provisioning Wizard
```yaml
Feature: School Provisioning Wizard
Description: Step-by-step school onboarding process
Acceptance Criteria:
  - School information capture (name, type, location, contact)
  - Module bundle selection (Starter, Standard, Premium)
  - Default admin user creation
  - Fee schedule template selection
  - Initial class structure setup
  - Welcome email/WhatsApp with credentials
  - Onboarding checklist generation
  - Training resource assignment
  - Provisioning completion within 30 minutes
  - Batch provisioning for multiple schools
```

#### 2.1.2 User and Role Management
```yaml
Feature: User and Role Management
Description: Manage platform users and permissions
Acceptance Criteria:
  - Create user accounts for school staff
  - Assign roles (school_admin, teacher, nurse, bursar, etc.)
  - Role-based permission templates
  - User activation/deactivation
  - Password reset functionality
  - Multi-factor authentication setup
  - User activity monitoring
  - Bulk user import
  - User search and filtering
  - Audit trail for all user changes
```

#### 2.1.3 Sync Health Monitoring
```yaml
Feature: Sync Health Monitoring
Description: Monitor offline sync status across schools
Acceptance Criteria:
  - Real-time sync status dashboard
  - Last sync timestamp per school
  - Sync failure alerts (amber at 24h, red at 48h)
  - Pending operations count
  - Conflict detection and resolution
  - Sync performance metrics
  - Device health monitoring
  - Automatic retry for failed syncs
  - Manual sync trigger capability
  - Sync history and logs
```

#### 2.1.4 Sentinel Threshold Configuration
```yaml
Feature: Sentinel Threshold Configuration
Description: Configure disease surveillance thresholds
Acceptance Criteria:
  - Per-state threshold configuration
  - Per-LGA threshold overrides
  - Symptom category thresholds
  - Time window configuration (48, 72, 96 hours)
  - Baseline illness rate calibration
  - Alert tier configuration
  - False positive reduction settings
  - Threshold testing and validation
  - Historical threshold performance review
  - Threshold change audit trail
```

#### 2.1.5 System Update Deployment
```yaml
Feature: System Update Deployment
Description: Deploy updates to platform and schools
Acceptance Criteria:
  - Staged deployment (dev → staging → production)
  - Zero-downtime deployments
  - School-specific or global updates
  - Update scheduling (off-school hours)
  - Rollback capability
  - Update notification to schools
  - Deployment status monitoring
  - Version management
  - Feature flag management
  - A/B testing support
```

#### 2.1.6 Usage Analytics
```yaml
Feature: Usage Analytics
Description: Monitor platform usage and adoption
Acceptance Criteria:
  - Module engagement per school
  - Feature adoption rates
  - User activity metrics
  - Inactive school identification
  - Usage trends over time
  - Comparative analytics
  - Export capabilities
  - Custom report generation
  - Alert for usage drops
  - ROI calculations
```

#### 2.1.7 Training Resource Management
```yaml
Feature: Training Resource Management
Description: Manage training materials and resources
Acceptance Criteria:
  - Video tutorial library
  - Quick reference guides
  - Multi-language support (English, Igbo, Hausa)
  - Role-specific resource bundles
  - Resource assignment to schools
  - Completion tracking
  - Certificate generation
  - Resource update notifications
  - Downloadable materials
  - Search and filtering
```

### 2.2 Business Rules

#### 2.2.1 School Provisioning Business Rules
1. **Unique School Code:** Auto-generated, must be unique across platform
2. **Subscription Validation:** Verify payment before provisioning completes
3. **Admin Contact Required:** At least one admin contact with email and phone
4. **Module Activation:** Selected modules activated immediately
5. **Trial Period:** Optional 30-day trial for evaluation
6. **Data Migration:** Support for importing existing data
7. **Regional Compliance:** Ensure data residency requirements met
8. **Onboarding SLA:** 48-hour completion target for standard provisioning

#### 2.2.2 User Management Business Rules
1. **Unique Email:** One user account per email address
2. **Role Hierarchy:** Super admin > School admin > Role-specific users
3. **Self-Service:** Users can update own profile, not role
4. **Password Policy:** Minimum 8 characters, complexity requirements
5. **Session Limits:** Maximum 3 concurrent sessions per user
6. **Account Lockout:** Lock after 5 failed login attempts
7. **Deactivation:** Soft delete, retain audit trail
8. **Bulk Operations:** Require confirmation for bulk user changes

#### 2.2.3 Sync Monitoring Business Rules
1. **Alert Thresholds:** 24-hour amber, 48-hour red alerts
2. **Conflict Resolution:** Last-write-wins for most data; admin review for financial/health
3. **Data Integrity:** Sync failures never result in data loss
4. **Retry Logic:** Automatic retry with exponential backoff
5. **Manual Override:** Admin can trigger manual sync
6. **Performance Monitoring:** Track sync duration and size
7. **Device Health:** Monitor device storage and connectivity
8. **Historical Data:** Retain sync logs for 90 days

#### 2.2.4 Sentinel Configuration Business Rules
1. **Calibration Required:** New thresholds must be calibrated against historical data
2. **Gradual Rollout:** New thresholds tested on subset of schools first
3. **Change Approval:** Threshold changes require super admin approval
4. **Impact Analysis:** Simulate threshold changes before applying
5. **Documentation:** All threshold changes documented with rationale
6. **Performance Review:** Monthly review of threshold accuracy
7. **Emergency Override:** State-level officials can request immediate threshold changes
8. **Audit Trail:** Complete history of all threshold modifications

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Platform schools (extends schools table with provisioning info)
ALTER TABLE schools ADD COLUMN IF NOT EXISTS provisioning_status VARCHAR(20) DEFAULT 'pending';
ALTER TABLE schools ADD COLUMN IF NOT EXISTS provisioning_completed_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS onboarding_checklist JSONB;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS training_resources_assigned UUID[];
ALTER TABLE schools ADD COLUMN IF NOT EXISTS last_sync_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS sync_status VARCHAR(20) DEFAULT 'unknown';
ALTER TABLE schools ADD COLUMN IF NOT EXISTS sync_device_count INTEGER DEFAULT 0;

-- Platform users (extends users table)
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_platform_admin BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP WITH TIME ZONE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_secret VARCHAR(255);

-- Sync status tracking
CREATE TABLE sync_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    device_info JSONB,
    user_id UUID REFERENCES users(id),
    last_sync_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'synced' CHECK (sync_status IN ('synced', 'pending', 'failed', 'conflict')),
    pending_operations INTEGER DEFAULT 0,
    last_operation_timestamp TIMESTAMP WITH TIME ZONE,
    sync_duration_ms INTEGER,
    data_size_bytes INTEGER,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    next_retry_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Indexes for sync status
CREATE INDEX idx_sync_status_school ON sync_status(school_id, last_sync_at);
CREATE INDEX idx_sync_status_status ON sync_status(sync_status, updated_at);
CREATE INDEX idx_sync_status_device ON sync_status(device_id, last_sync_at);

-- Sync history (for detailed logging)
CREATE TABLE sync_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    sync_start TIMESTAMP WITH TIME ZONE NOT NULL,
    sync_end TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('started', 'completed', 'failed', 'partial')),
    operations_sent INTEGER DEFAULT 0,
    operations_received INTEGER DEFAULT 0,
    conflicts_detected INTEGER DEFAULT 0,
    conflicts_resolved INTEGER DEFAULT 0,
    data_size_bytes INTEGER,
    error_details JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sentinel threshold configurations
CREATE TABLE sentinel_thresholds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state VARCHAR(100),
    lga VARCHAR(100),
    symptom_category VARCHAR(100) NOT NULL,
    time_window_hours INTEGER NOT NULL DEFAULT 48,
    cluster_threshold INTEGER NOT NULL DEFAULT 3,
    school_threshold_percent DECIMAL(5,2) NOT NULL DEFAULT 10.0,
    lga_threshold_percent DECIMAL(5,2) NOT NULL DEFAULT 5.0,
    baseline_illness_rate DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    effective_from DATE NOT NULL,
    effective_to DATE,
    change_reason TEXT,
    approved_by UUID REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Threshold change history
CREATE TABLE threshold_change_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threshold_id UUID NOT NULL REFERENCES sentinel_thresholds(id),
    change_type VARCHAR(20) NOT NULL CHECK (change_type IN ('create', 'update', 'deactivate')),
    previous_values JSONB,
    new_values JSONB,
    change_reason TEXT,
    changed_by UUID NOT NULL REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    impact_analysis JSONB,  -- Predicted impact of change
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System updates
CREATE TABLE system_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(50) NOT NULL,
    release_type VARCHAR(20) NOT NULL CHECK (release_type IN ('major', 'minor', 'patch', 'hotfix')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_notes TEXT,
    deployment_type VARCHAR(20) NOT NULL CHECK (deployment_type IN ('global', 'school_specific', 'regional')),
    target_schools UUID[],  -- NULL for global
    target_states TEXT[],
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'staging', 'deploying', 'deployed', 'rolled_back')),
    scheduled_for TIMESTAMP WITH TIME ZONE,
    deployed_at TIMESTAMP WITH TIME ZONE,
    rolled_back_at TIMESTAMP WITH TIME ZONE,
    deployed_by UUID REFERENCES users(id),
    rollback_reason TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Update deployment tracking
CREATE TABLE update_deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    update_id UUID NOT NULL REFERENCES system_updates(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'deploying', 'deployed', 'failed', 'rolled_back')),
    deployed_at TIMESTAMP WITH TIME ZONE,
    deployed_version VARCHAR(50),
    previous_version VARCHAR(50),
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Training resources
CREATE TABLE training_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL CHECK (resource_type IN ('video', 'guide', 'document', 'interactive')),
    category VARCHAR(50) NOT NULL CHECK (category IN ('onboarding', 'module_specific', 'advanced', 'troubleshooting')),
    target_role VARCHAR(50),  -- NULL for all roles
    target_module VARCHAR(50),  -- NULL for all modules
    language VARCHAR(20) NOT NULL DEFAULT 'en' CHECK (language IN ('en', 'ig', 'ha')),
    content_url VARCHAR(500),
    duration_minutes INTEGER,  -- For videos
    file_size_bytes INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    version VARCHAR(20),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- School training assignments
CREATE TABLE school_training_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    resource_id UUID NOT NULL REFERENCES training_resources(id) ON DELETE CASCADE,
    assigned_by UUID REFERENCES users(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    due_date DATE,
    status VARCHAR(20) DEFAULT 'assigned' CHECK (status IN ('assigned', 'in_progress', 'completed', 'overdue')),
    completed_at TIMESTAMP WITH TIME ZONE,
    completed_by UUID REFERENCES users(id),
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(school_id, resource_id)
);

-- Usage analytics
CREATE TABLE usage_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metadata JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(school_id, metric_date, metric_name)
);

-- Indexes for usage analytics
CREATE INDEX idx_usage_analytics_school_date ON usage_analytics(school_id, metric_date);
CREATE INDEX idx_usage_analytics_metric ON usage_analytics(metric_name, metric_date);

-- Platform audit logs
CREATE TABLE platform_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    school_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create monthly partitions for audit logs
CREATE TABLE platform_audit_logs_2026_01 
    PARTITION OF platform_audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 School Provisioning Endpoints
```yaml
Endpoints:
  POST /api/v1/admin/schools/provision:
    - Description: Provision a new school
    - Request Body: SchoolProvisioning schema
    - Response: SchoolProvisioningResponse schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Validate school doesn't already exist
      - Generate unique school code
      - Create default admin user
      - Activate selected modules
      - Send welcome notifications
    - Side Effects:
      - Create school record
      - Create admin user
      - Send welcome email/WhatsApp
      - Create onboarding checklist
      - Assign training resources

  GET /api/v1/admin/schools/provisioning:
    - Description: List schools being provisioned
    - Query Parameters: status, date_range
    - Response: List of SchoolProvisioningStatus
    - Auth: Required (super_admin)

  GET /api/v1/admin/schools/{school_id}/onboarding:
    - Description: Get school onboarding status
    - Response: OnboardingStatusResponse schema
    - Auth: Required (super_admin, school_admin)
    - Includes:
      - Checklist completion
      - Training progress
      - Data migration status
      - Activation status

  POST /api/v1/admin/schools/{school_id}/activate:
    - Description: Activate school after provisioning
    - Auth: Required (super_admin)
    - Business Rules:
      - Verify all provisioning steps complete
      - Activate subscription
      - Send activation confirmation

  POST /api/v1/admin/schools/batch-provision:
    - Description: Batch provision multiple schools
    - Request Body: BatchProvisioning schema
    - Response: BatchProvisioningResult schema
    - Auth: Required (super_admin)
```

#### 4.1.2 User Management Endpoints
```yaml
Endpoints:
  POST /api/v1/admin/users:
    - Description: Create a new user
    - Request Body: UserCreate schema
    - Response: UserResponse schema
    - Auth: Required (super_admin, school_admin)
    - Business Rules:
      - Validate email uniqueness
      - Assign default role permissions
      - Send welcome email with credentials
    - Side Effects:
      - Create user record
      - Send credentials via email
      - Log audit trail

  GET /api/v1/admin/users:
    - Description: List users
    - Query Parameters: role, school_id, status, search
    - Response: Paginated list of UserResponse
    - Auth: Required

  GET /api/v1/admin/users/{user_id}:
    - Description: Get user details
    - Response: UserDetailResponse schema
    - Auth: Required

  PATCH /api/v1/admin/users/{user_id}:
    - Description: Update user
    - Request Body: UserUpdate schema
    - Auth: Required (super_admin, self)
    - Business Rules:
      - Role changes require super admin
      - Users can update own profile

  POST /api/v1/admin/users/{user_id}/reset-password:
    - Description: Reset user password
    - Request Body: { "new_password": "..." }
    - Auth: Required (super_admin, self)
    - Side Effects:
      - Update password
      - Invalidate existing sessions
      - Send notification

  POST /api/v1/admin/users/{user_id}/deactivate:
    - Description: Deactivate user
    - Request Body: { "reason": "..." }
    - Auth: Required (super_admin)
    - Business Rules:
      - Cannot deactivate last admin for school
      - Reassign owned resources

  GET /api/v1/admin/roles:
    - Description: List available roles
    - Response: List of RoleResponse
    - Auth: Required

  POST /api/v1/admin/roles:
    - Description: Create custom role
    - Request Body: RoleCreate schema
    - Response: RoleResponse schema
    - Auth: Required (super_admin)
```

#### 4.1.3 Sync Monitoring Endpoints
```yaml
Endpoints:
  GET /api/v1/admin/sync/status:
    - Description: Get sync status dashboard
    - Query Parameters: school_id, status, state
    - Response: SyncDashboardResponse schema
    - Auth: Required (super_admin)
    - Includes:
      - Schools with sync issues
      - Overall sync health metrics
      - Pending operations count
      - Conflict summary

  GET /api/v1/admin/sync/schools/{school_id}:
    - Description: Get school sync details
    - Response: SchoolSyncDetailResponse schema
    - Auth: Required (super_admin, school_admin)
    - Includes:
      - Device sync status
      - Last sync times
      - Pending operations
      - Conflict list

  GET /api/v1/admin/sync/devices/{device_id}:
    - Description: Get device sync details
    - Response: DeviceSyncDetailResponse schema
    - Auth: Required (super_admin)

  POST /api/v1/admin/sync/schools/{school_id}/trigger:
    - Description: Trigger manual sync for school
    - Auth: Required (super_admin)
    - Business Rules:
      - Validate school connectivity
      - Queue sync operation

  GET /api/v1/admin/sync/history:
    - Description: Get sync history
    - Query Parameters: school_id, device_id, date_range
    - Response: List of SyncHistoryResponse
    - Auth: Required (super_admin)

  GET /api/v1/admin/sync/conflicts:
    - Description: Get unresolved sync conflicts
    - Query Parameters: school_id, date_range
    - Response: List of SyncConflictResponse
    - Auth: Required (super_admin)

  POST /api/v1/admin/sync/conflicts/{conflict_id}/resolve:
    - Description: Resolve sync conflict
    - Request Body: ConflictResolution schema
    - Auth: Required (super_admin)
```

#### 4.1.4 Sentinel Configuration Endpoints
```yaml
Endpoints:
  GET /api/v1/admin/sentinel/thresholds:
    - Description: Get Sentinel threshold configurations
    - Query Parameters: state, lga, symptom_category
    - Response: List of ThresholdResponse
    - Auth: Required (super_admin, state_health)

  POST /api/v1/admin/sentinel/thresholds:
    - Description: Create/update threshold configuration
    - Request Body: ThresholdCreate schema
    - Response: ThresholdResponse schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Require impact analysis
      - Require approval for production changes
      - Document change reason

  GET /api/v1/admin/sentinel/thresholds/{threshold_id}/history:
    - Description: Get threshold change history
    - Response: List of ThresholdChangeResponse
    - Auth: Required (super_admin)

  POST /api/v1/admin/sentinel/thresholds/{threshold_id}/test:
    - Description: Test threshold configuration
    - Request Body: { "test_period": "..." }
    - Response: ThresholdTestResult schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Run against historical data
      - Show predicted alert changes
      - Estimate false positive impact

  GET /api/v1/admin/sentinel/baselines:
    - Description: Get baseline illness rates
    - Query Parameters: state, lga, season
    - Response: List of BaselineResponse
    - Auth: Required (super_admin)

  POST /api/v1/admin/sentinel/baselines/calibrate:
    - Description: Recalibrate baseline rates
    - Request Body: BaselineCalibration schema
    - Auth: Required (super_admin)
```

#### 4.1.5 System Update Endpoints
```yaml
Endpoints:
  POST /api/v1/admin/updates:
    - Description: Create system update
    - Request Body: UpdateCreate schema
    - Response: UpdateResponse schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Semantic versioning required
      - Release notes mandatory
      - Target schools/states specified

  GET /api/v1/admin/updates:
    - Description: List system updates
    - Query Parameters: status, release_type
    - Response: List of UpdateResponse
    - Auth: Required (super_admin)

  GET /api/v1/admin/updates/{update_id}:
    - Description: Get update details
    - Response: UpdateDetailResponse schema
    - Auth: Required (super_admin)

  POST /api/v1/admin/updates/{update_id}/deploy:
    - Description: Deploy update
    - Request Body: { "scheduled_for": "...", "target_schools": [...] }
    - Response: DeploymentResult schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Validate update compatibility
      - Schedule for off-hours
      - Enable rollback

  POST /api/v1/admin/updates/{update_id}/rollback:
    - Description: Rollback update
    - Request Body: { "reason": "..." }
    - Auth: Required (super_admin)
    - Business Rules:
      - Can only rollback if not yet deployed to all schools
      - Document rollback reason

  GET /api/v1/admin/updates/{update_id}/deployments:
    - Description: Get deployment status per school
    - Response: List of DeploymentStatusResponse
    - Auth: Required (super_admin)
```

#### 4.1.6 Usage Analytics Endpoints
```yaml
Endpoints:
  GET /api/v1/admin/analytics/overview:
    - Description: Get platform usage overview
    - Query Parameters: date_range
    - Response: PlatformAnalyticsOverview schema
    - Auth: Required (super_admin)
    - Includes:
      - Total schools, users, students
      - Active schools percentage
      - Module adoption rates
      - Geographic distribution

  GET /api/v1/admin/analytics/schools/{school_id}:
    - Description: Get school usage analytics
    - Query Parameters: date_range
    - Response: SchoolUsageAnalytics schema
    - Auth: Required (super_admin, school_admin)
    - Includes:
      - Module engagement
      - Feature adoption
      - User activity
      - Data completeness

  GET /api/v1/admin/analytics/engagement:
    - Description: Get engagement analytics
    - Query Parameters: group_by, date_range
    - Response: EngagementAnalytics schema
    - Auth: Required (super_admin)
    - Includes:
      - Daily/weekly/monthly active users
      - Feature usage trends
      - Churn indicators

  GET /api/v1/admin/analytics/inactive-schools:
    - Description: Get list of inactive schools
    - Query Parameters: inactive_days
    - Response: List of InactiveSchoolResponse
    - Auth: Required (super_admin)

  GET /api/v1/admin/analytics/export:
    - Description: Export analytics data
    - Query Parameters: format, date_range
    - Response: Analytics export file
    - Auth: Required (super_admin)
```

#### 4.1.7 Training Resource Endpoints
```yaml
Endpoints:
  GET /api/v1/admin/training/resources:
    - Description: List training resources
    - Query Parameters: category, language, role, module
    - Response: List of TrainingResourceResponse
    - Auth: Required

  POST /api/v1/admin/training/resources:
    - Description: Create training resource
    - Request Body: TrainingResourceCreate schema
    - Response: TrainingResourceResponse schema
    - Auth: Required (super_admin)

  POST /api/v1/admin/training/assign:
    - Description: Assign training resources to school
    - Request Body: TrainingAssignment schema
    - Response: AssignmentResult schema
    - Auth: Required (super_admin)
    - Business Rules:
      - Assign based on school tier and modules
      - Set due dates
      - Send notifications

  GET /api/v1/admin/training/progress:
    - Description: Get training progress
    - Query Parameters: school_id
    - Response: TrainingProgressResponse schema
    - Auth: Required (super_admin, school_admin)

  GET /api/v1/admin/training/certificates/{school_id}:
    - Description: Get school training certificates
    - Response: List of CertificateResponse
    - Auth: Required (super_admin, school_admin)
```

## 5. Business Logic Implementation

### 5.1 School Provisioning Logic
```python
class SchoolProvisioningService:
    async def provision_school(
        self,
        provisioning_data: SchoolProvisioning,
        provisioned_by: UUID
    ) -> SchoolProvisioningResult:
        """Provision a new school on the platform."""
        
        # 1. Validate school doesn't already exist
        existing = await self.check_existing_school(provisioning_data)
        if existing:
            raise ValidationError("School already exists on platform")
        
        # 2. Generate unique school code
        school_code = await self.generate_school_code(
            provisioning_data.name,
            provisioning_data.state
        )
        
        # 3. Create school record
        school = School(
            name=provisioning_data.name,
            code=school_code,
            type=provisioning_data.type,
            address=provisioning_data.address,
            city=provisioning_data.city,
            state=provisioning_data.state,
            lga=provisioning_data.lga,
            phone=provisioning_data.phone,
            email=provisioning_data.email,
            principal_name=provisioning_data.principal_name,
            principal_phone=provisioning_data.principal_phone,
            principal_email=provisioning_data.principal_email,
            subscription_tier=provisioning_data.subscription_tier,
            provisioning_status='in_progress',
            is_active=False  # Activated after provisioning complete
        )
        
        self.session.add(school)
        await self.session.flush()
        
        # 4. Create default admin user
        admin_user = await self.create_admin_user(
            school.id,
            provisioning_data.admin_email,
            provisioning_data.admin_phone
        )
        
        # 5. Configure modules based on tier
        await self.configure_modules(school.id, provisioning_data.subscription_tier)
        
        # 6. Create default fee schedule template
        await self.create_fee_schedule_template(school.id, provisioning_data.subscription_tier)
        
        # 7. Generate onboarding checklist
        checklist = await self.generate_onboarding_checklist(school.id)
        school.onboarding_checklist = checklist
        
        # 8. Assign training resources
        training_resources = await self.assign_training_resources(
            school.id,
            provisioning_data.subscription_tier
        )
        school.training_resources_assigned = training_resources
        
        # 9. Send welcome notifications
        await self.send_welcome_notifications(school, admin_user)
        
        # 10. Log provisioning
        await self.audit_service.log(
            action="school_provisioned",
            resource_type="school",
            resource_id=school.id,
            user_id=provisioned_by,
            details={
                "school_code": school_code,
                "subscription_tier": provisioning_data.subscription_tier,
                "admin_email": provisioning_data.admin_email
            }
        )
        
        await self.session.commit()
        
        return SchoolProvisioningResult(
            school_id=school.id,
            school_code=school_code,
            admin_user_id=admin_user.id,
            onboarding_checklist=checklist,
            training_resources=training_resources,
            message="School provisioned successfully. Welcome email sent to admin."
        )
    
    async def generate_school_code(self, school_name: str, state: str) -> str:
        """Generate unique school code."""
        # Create code from school name and state
        # Format: {STATE_ABBR}{FIRST_LETTERS}{SEQUENCE}
        # Example: ENU-ESS-001
        
        state_abbr = self.get_state_abbreviation(state)
        name_parts = school_name.split()
        name_abbr = ''.join([p[0].upper() for p in name_parts[:3]])
        
        # Get next sequence for state
        result = await self.session.execute(
            select(func.count(School.id))
            .where(School.state == state)
        )
        count = result.scalar()
        sequence = count + 1
        
        return f"{state_abbr}-{name_abbr}-{sequence:03d}"
    
    async def create_admin_user(
        self,
        school_id: UUID,
        email: str,
        phone: str
    ) -> User:
        """Create default admin user for school."""
        
        # Generate temporary password
        temp_password = self.generate_secure_password()
        
        admin_user = User(
            email=email,
            phone=phone,
            password_hash=self.hash_password(temp_password),
            first_name="School",
            last_name="Administrator",
            is_active=True,
            must_change_password=True
        )
        
        self.session.add(admin_user)
        await self.session.flush()
        
        # Assign school_admin role
        await self.assign_role(admin_user.id, 'school_admin', school_id)
        
        # Store temp password for welcome email (encrypted)
        admin_user.metadata = {
            'temp_password': self.encrypt(temp_password),
            'password_set_at': None
        }
        
        return admin_user
    
    async def generate_onboarding_checklist(self, school_id: UUID) -> dict:
        """Generate onboarding checklist for school."""
        
        return {
            "steps": [
                {
                    "id": "profile_complete",
                    "title": "Complete School Profile",
                    "description": "Add school logo, complete contact information",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "admin_login",
                    "title": "Admin First Login",
                    "description": "School administrator logs in and changes password",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "class_structure",
                    "title": "Set Up Class Structure",
                    "description": "Create classes and assign form teachers",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "fee_schedule",
                    "title": "Configure Fee Schedule",
                    "description": "Review and customize fee categories and amounts",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "student_import",
                    "title": "Import Student Data",
                    "description": "Upload student records via CSV or manual entry",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "staff_setup",
                    "title": "Set Up Staff Accounts",
                    "description": "Create accounts for teachers, nurse, bursar",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "training_completion",
                    "title": "Complete Training",
                    "description": "Watch training videos and complete tutorials",
                    "required": True,
                    "completed": False
                },
                {
                    "id": "go_live",
                    "title": "Go Live",
                    "description": "Start using EduLafia for daily operations",
                    "required": True,
                    "completed": False
                }
            ],
            "progress": 0,
            "current_step": "profile_complete"
        }
```

### 5.2 Sync Monitoring Logic
```python
class SyncMonitoringService:
    async def get_sync_dashboard(self) -> SyncDashboard:
        """Get overall sync health dashboard."""
        
        # 1. Get schools with sync issues
        schools_with_issues = await self.get_schools_with_sync_issues()
        
        # 2. Get overall metrics
        total_schools = await self.get_total_active_schools()
        synced_schools = await self.get_synced_schools_count()
        pending_schools = await self.get_pending_schools_count()
        failed_schools = await self.get_failed_schools_count()
        
        # 3. Get pending operations
        total_pending = await self.get_total_pending_operations()
        
        # 4. Get unresolved conflicts
        unresolved_conflicts = await self.get_unresolved_conflicts_count()
        
        # 5. Get recent sync activity
        recent_syncs = await self.get_recent_sync_activity(hours=24)
        
        return SyncDashboard(
            total_schools=total_schools,
            synced_schools=synced_schools,
            pending_schools=pending_schools,
            failed_schools=failed_schools,
            sync_rate=synced_schools / total_schools * 100 if total_schools > 0 else 0,
            total_pending_operations=total_pending,
            unresolved_conflicts=unresolved_conflicts,
            schools_with_issues=schools_with_issues[:10],  # Top 10
            recent_syncs=recent_syncs,
            last_updated=datetime.utcnow()
        )
    
    async def check_sync_health(self):
        """Check sync health and generate alerts."""
        
        # 1. Get schools that haven't synced in 24 hours
        stale_schools = await self.get_stale_schools(hours=24)
        
        for school in stale_schools:
            # Check last sync time
            hours_since_sync = (datetime.utcnow() - school.last_sync_at).total_seconds() / 3600
            
            if hours_since_sync >= 48:
                # Red alert
                await self.create_alert(
                    school_id=school.id,
                    alert_type='sync_red',
                    severity='critical',
                    message=f"School {school.name} has not synced in {int(hours_since_sync)} hours"
                )
            elif hours_since_sync >= 24:
                # Amber alert
                await self.create_alert(
                    school_id=school.id,
                    alert_type='sync_amber',
                    severity='warning',
                    message=f"School {school.name} has not synced in {int(hours_since_sync)} hours"
                )
        
        # 2. Check for sync conflicts
        conflicts = await self.get_unresolved_conflicts()
        for conflict in conflicts:
            if conflict.created_at < datetime.utcnow() - timedelta(hours=48):
                await self.create_alert(
                    school_id=conflict.school_id,
                    alert_type='sync_conflict',
                    severity='high',
                    message=f"Unresolved sync conflict for {int((datetime.utcnow() - conflict.created_at).total_seconds() / 3600)} hours"
                )
    
    async def trigger_manual_sync(self, school_id: UUID) -> SyncTriggerResult:
        """Trigger manual sync for a school."""
        
        # 1. Get school's devices
        devices = await self.get_school_devices(school_id)
        
        if not devices:
            return SyncTriggerResult(
                success=False,
                message="No devices registered for this school"
            )
        
        # 2. Trigger sync for each device
        results = []
        for device in devices:
            try:
                result = await self.trigger_device_sync(device.device_id)
                results.append({
                    'device_id': device.device_id,
                    'status': 'triggered',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'device_id': device.device_id,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # 3. Log trigger
        await self.audit_service.log(
            action="manual_sync_triggered",
            resource_type="school",
            resource_id=school_id,
            details={
                "devices": len(devices),
                "results": results
            }
        )
        
        return SyncTriggerResult(
            success=True,
            message=f"Sync triggered for {len(devices)} devices",
            device_results=results
        )
```

### 5.3 Sentinel Configuration Logic
```python
class SentinelConfigService:
    async def create_threshold(
        self,
        threshold_data: ThresholdCreate,
        created_by: UUID
    ) -> SentinelThreshold:
        """Create or update Sentinel threshold."""
        
        # 1. Validate threshold configuration
        await self.validate_threshold(threshold_data)
        
        # 2. Check for existing active threshold
        existing = await self.session.execute(
            select(SentinelThreshold)
            .where(
                SentinelThreshold.state == threshold_data.state,
                SentinelThreshold.lga == threshold_data.lga,
                SentinelThreshold.symptom_category == threshold_data.symptom_category,
                SentinelThreshold.is_active == True
            )
        )
        
        existing_threshold = existing.scalar()
        
        # 3. Deactivate existing if updating
        if existing_threshold:
            existing_threshold.is_active = False
            existing_threshold.effective_to = datetime.utcnow().date()
            
            # Log change
            await self.log_threshold_change(
                threshold_id=existing_threshold.id,
                change_type='update',
                previous_values=existing_threshold.to_dict(),
                new_values=threshold_data.dict(),
                changed_by=created_by
            )
        
        # 4. Create new threshold
        new_threshold = SentinelThreshold(
            state=threshold_data.state,
            lga=threshold_data.lga,
            symptom_category=threshold_data.symptom_category,
            time_window_hours=threshold_data.time_window_hours,
            cluster_threshold=threshold_data.cluster_threshold,
            school_threshold_percent=threshold_data.school_threshold_percent,
            lga_threshold_percent=threshold_data.lga_threshold_percent,
            baseline_illness_rate=threshold_data.baseline_illness_rate,
            is_active=True,
            effective_from=datetime.utcnow().date(),
            change_reason=threshold_data.change_reason,
            created_by=created_by,
            approved_by=created_by  # In production, separate approver
        )
        
        self.session.add(new_threshold)
        await self.session.commit()
        
        return new_threshold
    
    async def test_threshold(
        self,
        threshold_id: UUID,
        test_period_days: int = 30
    ) -> ThresholdTestResult:
        """Test threshold configuration against historical data."""
        
        # 1. Get threshold
        threshold = await self.session.get(SentinelThreshold, threshold_id)
        if not threshold:
            raise NotFoundError("Threshold not found")
        
        # 2. Get historical data for test period
        start_date = datetime.utcnow().date() - timedelta(days=test_period_days)
        end_date = datetime.utcnow().date()
        
        historical_data = await self.get_historical_signals(
            threshold.state,
            threshold.lga,
            threshold.symptom_category,
            start_date,
            end_date
        )
        
        # 3. Simulate with new threshold
        simulated_alerts = self.simulate_alerts(
            historical_data,
            threshold
        )
        
        # 4. Compare with actual alerts (if any)
        actual_alerts = await self.get_actual_alerts(
            threshold.state,
            threshold.lga,
            threshold.symptom_category,
            start_date,
            end_date
        )
        
        # 5. Calculate metrics
        new_alert_count = len(simulated_alerts)
        current_alert_count = len(actual_alerts)
        alert_change_percent = (
            (new_alert_count - current_alert_count) / current_alert_count * 100
            if current_alert_count > 0 else 0
        )
        
        # 6. Estimate false positives
        false_positive_estimate = self.estimate_false_positives(
            simulated_alerts,
            historical_data
        )
        
        return ThresholdTestResult(
            threshold_id=threshold_id,
            test_period_days=test_period_days,
            new_alert_count=new_alert_count,
            current_alert_count=current_alert_count,
            alert_change_percent=alert_change_percent,
            false_positive_estimate=false_positive_estimate,
            new_alerts=simulated_alerts[:10],  # Sample
            recommendations=self.generate_recommendations(
                alert_change_percent,
                false_positive_estimate
            )
        )
    
    async def calibrate_baselines(
        self,
        state: str,
        lga: Optional[str] = None,
        historical_years: int = 2
    ) -> BaselineCalibrationResult:
        """Calibrate baseline illness rates from historical data."""
        
        # 1. Get historical illness data
        start_date = datetime.now().date() - timedelta(days=365 * historical_years)
        end_date = datetime.now().date()
        
        historical_data = await self.get_historical_illness_data(
            state, lga, start_date, end_date
        )
        
        # 2. Calculate seasonal baselines
        baselines = self.calculate_seasonal_baselines(historical_data)
        
        # 3. Update threshold configurations
        updated_thresholds = []
        for baseline in baselines:
            threshold = await self.get_threshold_for_baseline(
                baseline.state,
                baseline.lga,
                baseline.symptom_category
            )
            
            if threshold:
                threshold.baseline_illness_rate = baseline.average_rate
                updated_thresholds.append(threshold.id)
        
        # 4. Log calibration
        await self.audit_service.log(
            action="baselines_calibrated",
            resource_type="sentinel_config",
            details={
                "state": state,
                "lga": lga,
                "historical_years": historical_years,
                "updated_thresholds": len(updated_thresholds)
            }
        )
        
        await self.session.commit()
        
        return BaselineCalibrationResult(
            state=state,
            lga=lga,
            historical_years=historical_years,
            baselines_calculated=len(baselines),
            thresholds_updated=len(updated_thresholds),
            baselines=baselines
        )
```

## 6. UI Component Specifications

### 6.1 School Provisioning Wizard
```typescript
interface SchoolProvisioningWizardProps {
  onComplete: (result: SchoolProvisioningResult) => void;
  onCancel: () => void;
}

// Wizard Steps:
// 1. School Information
//    - Name, type, address
//    - Contact details
//    - Principal information
// 2. Subscription Selection
//    - Tier selection (Starter, Standard, Premium)
//    - Module bundle
//    - Pricing display
// 3. Admin User Setup
//    - Admin email and phone
//    - Role assignment
// 4. Class Structure
//    - Class levels
//    - Form teacher assignments
// 5. Fee Schedule
//    - Template selection
//    - Customization
// 6. Review & Confirm
//    - Summary of all settings
//    - Confirmation button

// Wizard Progress:
interface WizardProgressProps {
  currentStep: number;
  totalSteps: number;
  stepTitles: string[];
  onStepClick?: (step: number) => void;
}
```

### 6.2 Sync Monitoring Dashboard
```typescript
interface SyncMonitoringDashboardProps {
  onRefresh: () => void;
  onViewSchool: (schoolId: string) => void;
  onResolveConflict: (conflictId: string) => void;
}

// Dashboard Components:
// 1. Summary cards (synced, pending, failed schools)
// 2. Sync health chart (trend over time)
// 3. Schools with issues list
// 4. Unresolved conflicts list
// 5. Recent sync activity feed
// 6. Manual sync trigger

// School Sync Detail:
interface SchoolSyncDetailProps {
  schoolId: string;
  onTriggerSync: () => void;
  onViewConflict: (conflictId: string) => void;
}

// Device List:
interface DeviceListProps {
  devices: DeviceSyncStatus[];
  onDeviceClick: (deviceId: string) => void;
}
```

### 6.3 Sentinel Configuration Panel
```typescript
interface SentinelConfigPanelProps {
  state?: string;
  lga?: string;
  onSave: (config: ThresholdConfig) => void;
  onTest: (config: ThresholdConfig) => Promise<TestResult> => void;
}

// Configuration Form:
// 1. Geographic scope selection
// 2. Symptom category
// 3. Time window (hours)
// 4. Cluster threshold
// 5. School threshold (%)
// 6. LGA threshold (%)
// 7. Baseline rate
// 8. Change reason
// 9. Test button
// 10. Save button

// Threshold Test Results:
interface ThresholdTestResultsProps {
  result: ThresholdTestResult;
  onApply: () => void;
  onCancel: () => void;
}
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for SchoolProvisioningService
class TestSchoolProvisioningService:
    async def test_provision_school_success(self):
        """Test successful school provisioning."""
        pass
    
    async def test_generate_school_code_unique(self):
        """Test unique school code generation."""
        pass
    
    async def test_create_admin_user(self):
        """Test admin user creation."""
        pass
    
    async def test_generate_onboarding_checklist(self):
        """Test onboarding checklist generation."""
        pass

# Test cases for SyncMonitoringService
class TestSyncMonitoringService:
    async def test_get_sync_dashboard(self):
        """Test sync dashboard data retrieval."""
        pass
    
    async def test_check_sync_health(self):
        """Test sync health check."""
        pass
    
    async def test_trigger_manual_sync(self):
        """Test manual sync trigger."""
        pass

# Test cases for SentinelConfigService
class TestSentinelConfigService:
    async def test_create_threshold(self):
        """Test threshold creation."""
        pass
    
    async def test_test_threshold(self):
        """Test threshold testing."""
        pass
    
    async def test_calibrate_baselines(self):
        """Test baseline calibration."""
        pass
```

### 7.2 Integration Tests
```python
class TestAdminAPI:
    async def test_school_provisioning_endpoint(self):
        """Test POST /api/v1/admin/schools/provision endpoint."""
        pass
    
    async def test_user_management_endpoint(self):
        """Test POST /api/v1/admin/users endpoint."""
        pass
    
    async def test_sync_dashboard_endpoint(self):
        """Test GET /api/v1/admin/sync/status endpoint."""
        pass
    
    async def test_threshold_configuration_endpoint(self):
        """Test POST /api/v1/admin/sentinel/thresholds endpoint."""
        pass
    
    async def test_update_deployment_endpoint(self):
        """Test POST /api/v1/admin/updates/{update_id}/deploy endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Admin module
ADMIN_PERMISSIONS = {
    "super_admin": [
        "admin:school_provisioning",
        "admin:user_management",
        "admin:sync_monitoring",
        "admin:sentinel_config",
        "admin:system_updates",
        "admin:usage_analytics",
        "admin:training_management",
        "admin:platform_config",
        "admin:audit_logs"
    ],
    "school_admin": [
        "admin:user_management:school_only",
        "admin:sync_monitoring:school_only",
        "admin:training_progress:school_only",
        "admin:school_config"
    ]
}

# Multi-factor authentication for super admins
MFA_REQUIRED_FOR = [
    "admin:school_provisioning",
    "admin:sentinel_config",
    "admin:system_updates",
    "admin:audit_logs"
]
```

### 8.2 Data Security
```python
# Sensitive admin data handling
SENSITIVE_ADMIN_DATA = [
    "user_passwords",      # User credentials
    "system_config",       # System configuration
    "sentinel_thresholds", # Surveillance configuration
    "sync_credentials"     # Sync authentication
]

# Encryption for sensitive fields
ENCRYPTED_ADMIN_FIELDS = [
    "user_password_hash",
    "mfa_secret",
    "sync_credentials"
]

# Access logging for admin operations
ADMIN_ACCESS_LOGGING = True
HIGH_PRIVILEGE_OPERATIONS = [
    "school_provisioning",
    "threshold_changes",
    "system_updates",
    "user_role_changes"
]
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  School Provisioning:
    - Target: < 30 seconds for single school
    - Target: < 5 minutes for batch of 10 schools
    - Email delivery: < 60 seconds
  
  Sync Dashboard:
    - Target: < 5 seconds for dashboard load
    - Target: < 3 seconds for school sync details
    - Real-time updates: < 30 seconds
  
  Threshold Configuration:
    - Target: < 3 seconds for threshold save
    - Target: < 2 minutes for threshold testing
    - Target: < 1 hour for baseline calibration
  
  System Updates:
    - Target: < 5 seconds for update creation
    - Target: < 30 minutes for staged deployment
    - Target: < 10 minutes for rollback
  
  Usage Analytics:
    - Target: < 10 seconds for overview dashboard
    - Target: < 30 seconds for detailed analytics
    - Caching: 15-minute cache for analytics data
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed admin data
ADMIN_CACHE_CONFIG = {
    "sync_dashboard": {
        "ttl": 60,  # 1 minute for real-time monitoring
        "key": "admin:sync_dashboard"
    },
    "school_provisioning_status": {
        "ttl": 300,  # 5 minutes
        "key": "admin:schools:{school_id}:provisioning"
    },
    "sentinel_thresholds": {
        "ttl": 3600,  # 1 hour
        "key": "admin:sentinel:thresholds:{state}:{lga}"
    },
    "usage_analytics": {
        "ttl": 900,  # 15 minutes
        "key": "admin:analytics:{date_range}"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
ADMIN_INTEGRATIONS = {
    "all_modules": {
        "provisioning": "enable/disable modules during school setup",
        "user_management": "create users with appropriate module access",
        "sync": "monitor sync status across all modules"
    },
    "sentinel": {
        "configuration": "manage Sentinel thresholds and baselines",
        "monitoring": "monitor Sentinel performance and accuracy"
    },
    "intelligence": {
        "analytics": "access usage analytics and reports",
        "monitoring": "platform health monitoring"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_ADMIN_INTEGRATIONS = {
    "email": {
        "purpose": "Welcome emails, password resets, notifications",
        "provider": "SendGrid or AWS SES",
        "templates": ["welcome", "password_reset", "update_notification"]
    },
    "sms": {
        "purpose": "OTP, critical alerts, onboarding notifications",
        "provider": "Termii",
        "fallback": "SMS for non-email users"
    },
    "whatsapp": {
        "purpose": "Onboarding notifications, school communications",
        "provider": "WhatsApp Business API",
        "templates": ["welcome", "onboarding_reminder"]
    },
    "monitoring": {
        "purpose": "Platform health monitoring",
        "provider": "DataDog or New Relic",
        "metrics": ["uptime", "response_time", "error_rate"]
    },
    "logging": {
        "purpose": "Centralized logging and audit trail",
        "provider": "ELK Stack or CloudWatch",
        "retention": "1 year"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Extend School model with provisioning fields
- [ ] Extend User model with admin fields
- [ ] Create SyncStatus model and schema
- [ ] Create SyncHistory model and schema
- [ ] Create SentinelThreshold model and schema
- [ ] Create ThresholdChangeHistory model and schema
- [ ] Create SystemUpdate model and schema
- [ ] Create UpdateDeployment model and schema
- [ ] Create TrainingResource model and schema
- [ ] Create SchoolTrainingAssignment model and schema
- [ ] Create UsageAnalytics model and schema
- [ ] Create PlatformAuditLog model and schema
- [ ] Implement SchoolProvisioningService
- [ ] Implement SyncMonitoringService
- [ ] Implement SentinelConfigService
- [ ] Implement UpdateDeploymentService
- [ ] Implement UsageAnalyticsService
- [ ] Create admin API endpoints
- [ ] Implement provisioning wizard logic
- [ ] Implement sync health monitoring
- [ ] Implement threshold configuration
- [ ] Implement update deployment
- [ ] Implement usage analytics
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create SchoolProvisioningWizard component
- [ ] Create SyncMonitoringDashboard component
- [ ] Create SchoolSyncDetail component
- [ ] Create SentinelConfigPanel component
- [ ] Create UpdateManagement component
- [ ] Create UsageAnalyticsDashboard component
- [ ] Create TrainingResourceManager component
- [ ] Create UserManagement component
- [ ] Create AuditLogViewer component
- [ ] Implement wizard progress indicator
- [ ] Implement real-time sync updates
- [ ] Implement chart components for analytics
- [ ] Implement export functionality
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Testing Tasks
- [ ] Unit tests for SchoolProvisioningService
- [ ] Unit tests for SyncMonitoringService
- [ ] Unit tests for SentinelConfigService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for provisioning workflow
- [ ] E2E tests for sync monitoring
- [ ] E2E tests for threshold configuration
- [ ] Performance testing
- [ ] Security testing (admin access control)

---

*This module specification provides a comprehensive guide for implementing the System Administration & Onboarding system. The module is essential for platform operations, enabling efficient school onboarding, system monitoring, and Sentinel configuration management.*

---

**End of System Administration & Onboarding (M9) Specification**