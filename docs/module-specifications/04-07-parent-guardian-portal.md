# EduLafia Platform - Module Specification: Parent & Guardian Portal (M7)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M7 - Parent & Guardian Portal
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
The Parent & Guardian Portal provides mobile-first access for parents to view their child's academic results, attendance, health summaries, make payments, receive notifications, and communicate with the school. The portal is WhatsApp-native, accessible via unique login links, and designed for the smartphone-centric reality of Nigerian parents.

### 1.2 Scope
- Secure portal access (WhatsApp/SMS login)
- Child profile and academic results viewing
- Attendance summary and excusal submission
- Fee status and online payment
- Health summary and sick bay notifications
- WhatsApp/SMS notifications
- School communications
- Document download (report cards, receipts)
- Multi-child support

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information), M2 (Academics), M3 (Attendance), M4 (Finance), M5 (Health)
- **External Dependencies:** WhatsApp Business API, Termii SMS, Paystack/Flutterwave for payments
- **Integration Points:** All other modules provide data to parent portal

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Secure Portal Access
```yaml
Feature: Secure Portal Access
Description: Secure, app-less access for parents
Acceptance Criteria:
  - Unique URL sent via WhatsApp or SMS
  - No app download required
  - OTP-based authentication
  - Session timeout after 30 minutes inactivity
  - Multi-device support (phone, tablet)
  - Access revoked when student leaves school
  - Support for multiple guardians per student
  - Each guardian has separate login
  - Browser compatibility: Chrome, Safari, Firefox, Samsung Internet
```

#### 2.1.2 Child Profile and Academic Results
```yaml
Feature: Child Profile and Academic Results
Description: View child's profile and academic performance
Acceptance Criteria:
  - Current class and photo
  - Academic status and upcoming exams
  - Current term CA scores per subject
  - End-of-term exam results
  - Class rank and position
  - Performance trends (comparison with prior terms)
  - Subject-wise performance breakdown
  - Download previous term report cards
  - View academic transcript (full history)
  - Performance alerts (when average drops >20%)
```

#### 2.1.3 Attendance Summary and Excusal
```yaml
Feature: Attendance Summary and Excusal
Description: View attendance and submit excusals
Acceptance Criteria:
  - Current term attendance rate
  - Calendar view showing absent days
  - Reason for each absence (if provided)
  - Link to excusal submission form
  - Planned absence notification
  - Absence alert history
  - Compare attendance with class average
  - Chronic absence warnings
  - Export attendance history
```

#### 2.1.4 Fee Status and Online Payment
```yaml
Feature: Fee Status and Online Payment
Description: View fee balance and make payments
Acceptance Criteria:
  - Current fee balance
  - Itemized payment history
  - Fee breakdown by category (tuition, PTA, exam, etc.)
  - Outstanding balance per category
  - Payment link generation (Paystack/Flutterwave)
  - Payment receipt download
  - WhatsApp receipt delivery
  - Scholarship/waiver information
  - Payment reminder notifications
  - Installment payment options
```

#### 2.1.5 Health Summary and Notifications
```yaml
Feature: Health Summary and Notifications
Description: View child's health information and receive alerts
Acceptance Criteria:
  - Last sick bay visit date and general reason
  - Referral status if applicable
  - Vaccination status
  - Upcoming health screening notifications
  - Health alert notifications (urgent)
  - Detailed clinical data visible only with nurse authorization
  - Emergency contact information
  - Health profile update requests
  - Allergy and condition alerts to school
```

#### 2.1.6 WhatsApp/SMS Notifications
```yaml
Feature: WhatsApp/SMS Notifications
Description: Receive school communications via WhatsApp/SMS
Acceptance Criteria:
  - Absence notifications within 30 minutes
  - Report card delivery at term end
  - Fee payment receipts
  - Health notifications (sick bay visits, referrals)
  - School announcements
  - Exam schedule notifications
  - Event reminders
  - Opt-out option for non-critical notifications
  - Notification preferences management
  - Delivery confirmation tracking
```

#### 2.1.7 School Communications
```yaml
Feature: School Communications
Description: Two-way communication with school
Acceptance Criteria:
  - View school announcements
  - Receive messages from class teacher
  - Respond to school requests
  - Correction requests (name, contact info)
  - Feedback submission
  - Meeting scheduling
  - Document upload (medical records, etc.)
  - Communication history
  - Read receipts for important messages
```

### 2.2 Business Rules

#### 2.2.1 Access Business Rules
1. **Unique Login:** Each guardian receives unique portal access link
2. **OTP Authentication:** First login requires OTP verification
3. **Session Management:** 30-minute inactivity timeout
4. **Access Scope:** Guardian can only see their own child/children
5. **Multi-Child Support:** Single login shows all linked children
6. **Access Revocation:** Access revoked when student leaves school
7. **Security Questions:** Optional security questions for account recovery
8. **Device Limit:** Maximum 3 active devices per guardian

#### 2.2.2 Data Visibility Business Rules
1. **Academic Results:** Visible after teacher submission and admin approval
2. **Health Data:** Summary only; detailed data requires nurse authorization
3. **Financial Data:** Balance and payment history visible; internal school finances hidden
4. **Attendance Data:** Real-time updates; 24-hour delay for reason visibility
5. **Teacher Comments:** Visible after principal approval
6. **Other Students:** No visibility into other students' data
7. **Historical Data:** 3 years of historical data accessible
8. **Download Limits:** Report cards downloadable 5 times per term

#### 2.2.3 Notification Business Rules
1. **Absence Alerts:** Sent within 30 minutes of absence marking
2. **Health Alerts:** Sent immediately for sick bay visits and referrals
3. **Payment Receipts:** Sent within 2 minutes of payment confirmation
4. **Report Cards:** Sent at term end after generation
5. **Frequency Limits:** No more than 3 non-urgent notifications per day
6. **Opt-Out:** Parents can opt-out of non-critical notifications
7. **Urgent Alerts:** Cannot be opted-out (health emergencies, safety)
8. **Quiet Hours:** No notifications between 9 PM and 6 AM (except urgent)

#### 2.2.4 Payment Business Rules
1. **Payment Gateway:** Secure payment via Paystack/Flutterwave
2. **Receipt Generation:** Automatic receipt after successful payment
3. **WhatsApp Delivery:** Receipt sent via WhatsApp
4. **Payment Confirmation:** Webhook-based confirmation
5. **Duplicate Prevention:** Prevent double payment for same invoice
6. **Payment Plans:** Support for installment payments
7. **Payment History:** Complete history available
8. **Refund Process:** Refunds processed by school admin, not parent

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Guardian portal access (extends guardians table)
-- Portal access token is already in guardians table
-- Additional portal-specific fields

CREATE TABLE guardian_portal_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    session_token VARCHAR(500) NOT NULL,
    device_id VARCHAR(255),
    device_info JSONB,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- OTP verification records
CREATE TABLE otp_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(50) NOT NULL CHECK (purpose IN ('login', 'password_reset', 'transaction')),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    verified_at TIMESTAMP WITH TIME ZONE,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Parent notifications
CREATE TABLE parent_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL CHECK (notification_type IN ('absence', 'health', 'academic', 'fee', 'report_card', 'announcement', 'event')),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('whatsapp', 'sms', 'in_app', 'email')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'delivered', 'read', 'failed')),
    metadata JSONB,  -- Additional data (links, attachments, etc.)
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Parent notification preferences
CREATE TABLE parent_notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(guardian_id, notification_type, channel)
);

-- Absence excusals
CREATE TABLE absence_excusals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    absence_date DATE NOT NULL,
    reason VARCHAR(100) NOT NULL,
    details TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_notes TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Parent correction requests
CREATE TABLE parent_correction_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    field_name VARCHAR(100) NOT NULL,
    current_value TEXT,
    requested_value TEXT NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_notes TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Parent feedback
CREATE TABLE parent_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    feedback_type VARCHAR(50) NOT NULL CHECK (feedback_type IN ('general', 'complaint', 'suggestion', 'appreciation')),
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'reviewed', 'responded', 'resolved')),
    response TEXT,
    responded_by UUID REFERENCES users(id),
    responded_at TIMESTAMP WITH TIME ZONE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Indexes for parent portal
CREATE INDEX idx_parent_notifications_guardian ON parent_notifications(guardian_id, created_at);
CREATE INDEX idx_parent_notifications_student ON parent_notifications(student_id, notification_type);
CREATE INDEX idx_parent_notifications_status ON parent_notifications(status, created_at);
CREATE INDEX idx_otp_guardian_phone ON otp_verifications(guardian_id, phone, expires_at);
CREATE INDEX idx_guardian_sessions_token ON guardian_portal_sessions(session_token, expires_at);
```

### 3.2 Views for Parent Portal
```sql
-- Student summary view for parent portal
CREATE VIEW student_parent_summary AS
SELECT 
    s.id as student_id,
    s.first_name,
    s.last_name,
    s.photo_url,
    c.name as class_name,
    s.status,
    -- Latest attendance rate
    (
        SELECT ROUND(
            COUNT(CASE WHEN ar.status = 'present' THEN 1 END) * 100.0 / COUNT(*),
            2
        )
        FROM attendance_records ar
        WHERE ar.student_id = s.id 
            AND ar.date >= CURRENT_DATE - INTERVAL '30 days'
            AND ar.deleted_at IS NULL
    ) as attendance_rate_30_days,
    -- Current term balance
    (
        SELECT COALESCE(SUM(
            CASE 
                WHEN fl.transaction_type = 'charge' THEN fl.amount 
                ELSE -fl.amount 
            END
        ), 0)
        FROM fee_ledger fl
        WHERE fl.student_id = s.id 
            AND fl.term_id = (SELECT id FROM terms WHERE is_current = TRUE LIMIT 1)
            AND fl.deleted_at IS NULL
    ) as current_balance,
    -- Last sick bay visit
    (
        SELECT MAX(visit_date)
        FROM sick_bay_visits
        WHERE student_id = s.id AND deleted_at IS NULL
    ) as last_sick_bay_visit
FROM students s
JOIN classes c ON s.class_id = c.id
WHERE s.deleted_at IS NULL;

-- Parent notification summary view
CREATE VIEW parent_notification_summary AS
SELECT 
    pn.guardian_id,
    pn.student_id,
    DATE_TRUNC('day', pn.created_at) as date,
    COUNT(*) as total_notifications,
    COUNT(CASE WHEN pn.status = 'read' THEN 1 END) as read_count,
    COUNT(CASE WHEN pn.priority = 'urgent' THEN 1 END) as urgent_count,
    ARRAY_AGG(DISTINCT pn.notification_type) as notification_types
FROM parent_notifications pn
WHERE pn.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY pn.guardian_id, pn.student_id, DATE_TRUNC('day', pn.created_at);
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Authentication Endpoints
```yaml
Endpoints:
  POST /api/v1/parent/auth/request-otp:
    - Description: Request OTP for portal access
    - Request Body: { "phone": "+234..." }
    - Response: { "success": true, "message": "OTP sent" }
    - Auth: None (public)
    - Business Rules:
      - Validate phone number format
      - Check if guardian exists
      - Rate limit: 3 requests per hour per phone
      - OTP expires in 10 minutes
    - Side Effects:
      - Generate OTP
      - Send via SMS/WhatsApp
      - Log attempt

  POST /api/v1/parent/auth/verify-otp:
    - Description: Verify OTP and get access token
    - Request Body: { "phone": "+234...", "otp": "123456" }
    - Response: AuthResponse schema
    - Auth: None (public)
    - Business Rules:
      - OTP valid for 10 minutes
      - Maximum 3 attempts
      - Generate session token
      - Link to guardian record
    - Returns:
      - access_token (JWT)
      - refresh_token
      - guardian info
      - linked children

  POST /api/v1/parent/auth/refresh:
    - Description: Refresh access token
    - Request Body: { "refresh_token": "..." }
    - Response: New AuthResponse
    - Auth: None (uses refresh token)

  POST /api/v1/parent/auth/logout:
    - Description: Logout from portal
    - Auth: Required (parent)
    - Side Effects: Invalidate session
```

#### 4.1.2 Child Information Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/children:
    - Description: Get list of guardian's children
    - Response: List of ChildSummaryResponse
    - Auth: Required (parent)
    - Business Rules:
      - Only show children linked to guardian
      - Include current class and status

  GET /api/v1/parent/children/{student_id}/profile:
    - Description: Get child's detailed profile
    - Response: ChildProfileResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - Guardian must be linked to student
      - Include academic status, class info

  GET /api/v1/parent/children/{student_id}/academic:
    - Description: Get child's academic results
    - Query Parameters: term_id
    - Response: AcademicResultsResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - Only show results after teacher submission
      - Include CA, exam, total, grade, rank
      - Performance trends if available

  GET /api/v1/parent/children/{student_id}/report-card/{term_id}:
    - Description: Download report card PDF
    - Response: PDF file
    - Auth: Required (parent)
    - Business Rules:
      - Limit downloads per term
      - Include watermark

  GET /api/v1/parent/children/{student_id}/transcript:
    - Description: Download full academic transcript
    - Response: PDF file
    - Auth: Required (parent)
    - Business Rules:
      - Include all terms
      - School authentication
```

#### 4.1.3 Attendance Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/children/{student_id}/attendance:
    - Description: Get child's attendance summary
    - Query Parameters: term_id, month
    - Response: AttendanceSummaryResponse schema
    - Auth: Required (parent)
    - Includes:
      - Attendance rate
      - Absence calendar
      - Reasons for absences
      - Late arrivals

  POST /api/v1/parent/children/{student_id}/excusal:
    - Description: Submit absence excusal
    - Request Body: ExcusalRequest schema
    - Response: ExcusalResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - For planned absences
      - Requires reason and details
      - Notifies class teacher and admin
    - Side Effects:
      - Create excusal record
      - Send notification to teacher
      - Update attendance when day arrives

  GET /api/v1/parent/children/{student_id}/attendance/alerts:
    - Description: Get attendance alerts history
    - Response: List of AttendanceAlertResponse
    - Auth: Required (parent)
```

#### 4.1.4 Finance Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/children/{student_id}/finance:
    - Description: Get child's fee status
    - Query Parameters: term_id
    - Response: FinanceSummaryResponse schema
    - Auth: Required (parent)
    - Includes:
      - Current balance
      - Fee breakdown by category
      - Payment history
      - Outstanding amounts

  POST /api/v1/parent/children/{student_id}/payment/initiate:
    - Description: Initiate online payment
    - Request Body: PaymentInitiate schema
    - Response: PaymentInitiationResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - Generate payment link
      - Include fee details
      - Set expiration
    - Returns:
      - Payment URL for gateway
      - Reference number

  GET /api/v1/parent/children/{student_id}/payments:
    - Description: Get payment history
    - Query Parameters: term_id, date_range
    - Response: List of PaymentHistoryResponse
    - Auth: Required (parent)

  GET /api/v1/parent/children/{student_id}/receipts/{receipt_number}:
    - Description: Download payment receipt
    - Response: PDF file
    - Auth: Required (parent)
```

#### 4.1.5 Health Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/children/{student_id}/health:
    - Description: Get child's health summary
    - Response: HealthSummaryResponse schema
    - Auth: Required (parent)
    - Includes:
      - Last sick bay visit (date, general reason)
      - Referral status if active
      - Vaccination status summary
      - Upcoming screening notifications
    - Business Rules:
      - Summary only, not detailed clinical data
      - Nurse can authorize detailed view

  GET /api/v1/parent/children/{student_id}/health/sick-bay:
    - Description: Get sick bay visit history
    - Query Parameters: date_range
    - Response: List of SickBayVisitResponse
    - Auth: Required (parent)
    - Business Rules:
      - Limited to general information
      - Detailed notes require nurse authorization

  GET /api/v1/parent/children/{student_id}/health/referrals:
    - Description: Get referral status
    - Response: List of ReferralResponse
    - Auth: Required (parent)
```

#### 4.1.6 Notification Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/notifications:
    - Description: Get all notifications
    - Query Parameters: type, status, date_range, page, limit
    - Response: Paginated list of NotificationResponse
    - Auth: Required (parent)

  PATCH /api/v1/parent/notifications/{notification_id}/read:
    - Description: Mark notification as read
    - Auth: Required (parent)

  GET /api/v1/parent/notification-preferences:
    - Description: Get notification preferences
    - Response: NotificationPreferencesResponse
    - Auth: Required (parent)

  PUT /api/v1/parent/notification-preferences:
    - Description: Update notification preferences
    - Request Body: NotificationPreferencesUpdate schema
    - Auth: Required (parent)
    - Business Rules:
      - Cannot opt-out of urgent notifications
      - Changes take effect immediately
```

#### 4.1.7 Communication Endpoints
```yaml
Endpoints:
  GET /api/v1/parent/announcements:
    - Description: Get school announcements
    - Query Parameters: school_id, date_range
    - Response: List of AnnouncementResponse
    - Auth: Required (parent)

  POST /api/v1/parent/correction-requests:
    - Description: Submit correction request
    - Request Body: CorrectionRequest schema
    - Response: CorrectionRequestResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - Can request correction for own child's data
      - Requires justification
      - Admin reviews and approves/rejects

  POST /api/v1/parent/feedback:
    - Description: Submit feedback to school
    - Request Body: FeedbackSubmit schema
    - Response: FeedbackResponse schema
    - Auth: Required (parent)
    - Business Rules:
      - Can be anonymous
      - School admin notified
      - Response tracked
```

## 5. Business Logic Implementation

### 5.1 Authentication Logic
```python
class ParentAuthService:
    async def request_otp(self, phone: str) -> OTPRequestResult:
        """Request OTP for portal access."""
        
        # 1. Validate phone format
        if not self.validate_nigerian_phone(phone):
            raise ValidationError("Invalid phone number format")
        
        # 2. Find guardian by phone
        guardian = await self.find_guardian_by_phone(phone)
        if not guardian:
            # Don't reveal if guardian exists or not
            # Always return success to prevent enumeration
            return OTPRequestResult(
                success=True,
                message="If this phone number is registered, you will receive an OTP"
            )
        
        # 3. Check rate limit
        recent_otps = await self.get_recent_otps(guardian.id, minutes=60)
        if len(recent_otps) >= 3:
            raise RateLimitError("Too many OTP requests. Please try again later.")
        
        # 4. Generate OTP
        otp_code = self.generate_otp()
        
        # 5. Store OTP with expiration
        otp_record = OTPVerification(
            guardian_id=guardian.id,
            phone=phone,
            otp_code=otp_code,
            purpose='login',
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        
        self.session.add(otp_record)
        await self.session.commit()
        
        # 6. Send OTP via WhatsApp (preferred) or SMS
        await self.send_otp(guardian, otp_code)
        
        return OTPRequestResult(
            success=True,
            message="OTP sent successfully"
        )
    
    async def verify_otp(self, phone: str, otp_code: str) -> AuthResult:
        """Verify OTP and create session."""
        
        # 1. Find guardian
        guardian = await self.find_guardian_by_phone(phone)
        if not guardian:
            raise AuthenticationError("Invalid credentials")
        
        # 2. Find valid OTP
        otp_record = await self.session.execute(
            select(OTPVerification)
            .where(
                OTPVerification.guardian_id == guardian.id,
                OTPVerification.phone == phone,
                OTPVerification.otp_code == otp_code,
                OTPVerification.verified_at.is_(None),
                OTPVerification.expires_at > datetime.utcnow()
            )
            .order_by(OTPVerification.created_at.desc())
            .limit(1)
        )
        
        otp = otp_record.scalar()
        
        if not otp:
            # Increment attempt count
            await self.increment_failed_attempts(guardian.id)
            raise AuthenticationError("Invalid or expired OTP")
        
        # 3. Check max attempts
        if otp.attempts >= otp.max_attempts:
            raise AuthenticationError("OTP expired. Please request a new one.")
        
        # 4. Mark OTP as verified
        otp.verified_at = datetime.utcnow()
        
        # 5. Create session
        session = await self.create_session(guardian)
        
        # 6. Generate JWT tokens
        access_token = self.generate_access_token(guardian, session)
        refresh_token = self.generate_refresh_token(guardian, session)
        
        # 7. Get linked children
        children = await self.get_guardian_children(guardian.id)
        
        await self.session.commit()
        
        return AuthResult(
            access_token=access_token,
            refresh_token=refresh_token,
            guardian=GuardianResponse.from_orm(guardian),
            children=[ChildSummaryResponse.from_orm(child) for child in children]
        )
    
    async def create_session(self, guardian: Guardian) -> GuardianPortalSession:
        """Create portal session for guardian."""
        
        session_token = self.generate_session_token()
        
        session = GuardianPortalSession(
            guardian_id=guardian.id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(days=7)  # 7-day session
        )
        
        self.session.add(session)
        return session
```

### 5.2 Notification Logic
```python
class ParentNotificationService:
    async def send_absence_notification(
        self,
        student_id: UUID,
        attendance_record: AttendanceRecord
    ):
        """Send absence notification to guardians."""
        
        # 1. Get student and guardians
        student = await self.student_service.get_student(student_id)
        guardians = await self.get_student_guardians(student_id)
        
        # 2. Check notification time (quiet hours)
        if self.is_quiet_hours() and not self.is_urgent(attendance_record):
            # Schedule for later
            await self.schedule_notification(
                student, guardians, attendance_record, 
                send_at=self.get_next_available_time()
            )
            return
        
        # 3. Prepare notification content
        message = self.format_absence_message(student, attendance_record)
        
        # 4. Send to each guardian
        for guardian in guardians:
            # Check preferences
            preferences = await self.get_guardian_preferences(
                guardian.id, 'absence'
            )
            
            if not preferences.whatsapp_enabled and not preferences.sms_enabled:
                continue
            
            # Create notification record
            notification = ParentNotification(
                guardian_id=guardian.id,
                student_id=student_id,
                notification_type='absence',
                title=f"Absence Alert: {student.first_name} {student.last_name}",
                message=message,
                channel='whatsapp' if preferences.whatsapp_enabled else 'sms',
                priority='normal',
                metadata={
                    'attendance_id': str(attendance_record.id),
                    'date': attendance_record.date.isoformat(),
                    'reason': attendance_record.reason_code
                }
            )
            
            self.session.add(notification)
            
            # Send via WhatsApp
            if preferences.whatsapp_enabled:
                await self.send_whatsapp_notification(
                    guardian.whatsapp_phone or guardian.phone,
                    message,
                    notification
                )
            # Fallback to SMS
            elif preferences.sms_enabled:
                await self.send_sms_notification(
                    guardian.phone,
                    message,
                    notification
                )
        
        await self.session.commit()
    
    def format_absence_message(
        self, 
        student: Student, 
        attendance: AttendanceRecord
    ) -> str:
        """Format absence notification message."""
        
        reason_map = {
            'sick': 'reported sick',
            'family': 'absent for family reasons',
            'unknown': 'absent without explanation',
            'excused': 'excused absence',
            'suspended': 'suspended'
        }
        
        reason_text = reason_map.get(attendance.reason_code, 'absent')
        
        return f"""
📋 *Attendance Alert*

Your child *{student.first_name} {student.last_name}* has been marked *absent* today.

📅 Date: {attendance.date.strftime('%A, %d %B %Y')}
📝 Reason: {reason_text}

If this absence is planned or you need to provide more information, please click the link below to submit an excusal:

[Submit Excusal]

If you have any questions, please contact the school.

- EduLafia
        """.strip()
    
    async def send_report_card_notification(
        self,
        student_id: UUID,
        report_card: ReportCard
    ):
        """Send report card notification to guardians."""
        
        # 1. Get student and guardians
        student = await self.student_service.get_student(student_id)
        guardians = await self.get_student_guardians(student_id)
        
        # 2. Generate report card PDF
        pdf_url = report_card.pdf_url
        
        # 3. Prepare message
        message = self.format_report_card_message(student, report_card)
        
        # 4. Send to each guardian
        for guardian in guardians:
            # Create notification
            notification = ParentNotification(
                guardian_id=guardian.id,
                student_id=student_id,
                notification_type='report_card',
                title=f"Report Card Ready: {student.first_name} {student.last_name}",
                message=message,
                channel='whatsapp',
                priority='high',
                metadata={
                    'report_card_id': str(report_card.id),
                    'term_id': str(report_card.term_id),
                    'pdf_url': pdf_url,
                    'overall_average': str(report_card.overall_average)
                }
            )
            
            self.session.add(notification)
            
            # Send WhatsApp with PDF
            await self.send_whatsapp_with_pdf(
                guardian.whatsapp_phone or guardian.phone,
                message,
                pdf_url,
                notification
            )
        
        await self.session.commit()
    
    def format_report_card_message(
        self, 
        student: Student, 
        report_card: ReportCard
    ) -> str:
        """Format report card notification message."""
        
        return f"""
📊 *Report Card Available*

The report card for *{student.first_name} {student.last_name}* is now available.

📈 Overall Average: {report_card.overall_average}%
🏆 Class Position: {report_card.class_rank} out of {report_card.total_students}

Click the link below to view the full report card:

[View Report Card]

You can also download the PDF attached to this message.

- EduLafia
        """.strip()
```

### 5.3 Payment Integration Logic
```python
class ParentPaymentService:
    async def initiate_payment(
        self,
        student_id: UUID,
        guardian_id: UUID,
        fee_category: str,
        amount: Decimal
    ) -> PaymentInitiation:
        """Initiate online payment for parent."""
        
        # 1. Validate guardian has access to student
        if not await self.validate_guardian_access(guardian_id, student_id):
            raise PermissionError("Guardian not authorized for this student")
        
        # 2. Get student and school
        student = await self.student_service.get_student(student_id)
        school = await self.school_service.get_school(student.school_id)
        
        # 3. Get school's payment configuration
        config = await self.get_payment_config(school.id, 'paystack')
        
        if not config or not config.is_active:
            raise ValidationError("Online payments not available for this school")
        
        # 4. Generate reference
        reference = f"EDU-PAR-{uuid4().hex[:8].upper()}"
        
        # 5. Create pending ledger entry
        ledger_entry = FeeLedger(
            student_id=student_id,
            school_id=school.id,
            transaction_date=datetime.utcnow(),
            transaction_type='payment',
            fee_category=fee_category,
            amount=amount,
            payment_method='paystack',
            payment_reference=reference,
            status='pending',
            recorded_by=guardian_id  # Guardian initiated
        )
        
        self.session.add(ledger_entry)
        await self.session.flush()
        
        # 6. Initialize Paystack
        paystack = PaystackService(config)
        payment_data = await paystack.initialize_transaction(
            email=await self.get_guardian_email(guardian_id),
            amount=int(amount * 100),  # Convert to kobo
            reference=reference,
            metadata={
                'student_id': str(student_id),
                'student_name': f"{student.first_name} {student.last_name}",
                'fee_category': fee_category,
                'school_name': school.name,
                'ledger_entry_id': str(ledger_entry.id)
            }
        )
        
        # 7. Return payment initiation
        return PaymentInitiation(
            reference=reference,
            payment_url=payment_data['authorization_url'],
            amount=amount,
            ledger_entry_id=ledger_entry.id,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
    
    async def process_payment_webhook(
        self,
        event_data: dict
    ) -> WebhookResult:
        """Process Paystack payment webhook."""
        
        # 1. Extract payment details
        reference = event_data['data']['reference']
        status = event_data['data']['status']
        
        # 2. Find ledger entry
        ledger_entry = await self.session.execute(
            select(FeeLedger)
            .where(FeeLedger.payment_reference == reference)
        )
        ledger_entry = ledger_entry.scalar()
        
        if not ledger_entry:
            return WebhookResult(success=False, message="Reference not found")
        
        # 3. Check for duplicate processing
        if ledger_entry.status == 'completed':
            return WebhookResult(success=True, message="Already processed")
        
        # 4. Update ledger entry
        if status == 'success':
            ledger_entry.status = 'completed'
            ledger_entry.gateway_reference = event_data['data']['id']
            ledger_entry.gateway_response = event_data
            
            # Generate receipt number
            receipt_number = await self.generate_receipt_number(ledger_entry.school_id)
            ledger_entry.receipt_number = receipt_number
            
            # Get student and guardians
            student = await self.student_service.get_student(ledger_entry.student_id)
            guardians = await self.get_student_guardians(student.id)
            
            # Send receipt to guardians
            for guardian in guardians:
                await self.send_payment_receipt(
                    guardian, student, ledger_entry
                )
            
            await self.session.commit()
            
            return WebhookResult(
                success=True,
                message="Payment processed successfully",
                receipt_number=receipt_number
            )
        else:
            ledger_entry.status = 'failed'
            ledger_entry.gateway_response = event_data
            await self.session.commit()
            
            return WebhookResult(
                success=False,
                message="Payment failed"
            )
    
    async def send_payment_receipt(
        self,
        guardian: Guardian,
        student: Student,
        ledger_entry: FeeLedger
    ):
        """Send payment receipt to guardian via WhatsApp."""
        
        message = f"""
✅ *Payment Receipt*

Payment received for *{student.first_name} {student.last_name}*

💵 Amount: ₦{ledger_entry.amount:,.2f}
📋 Category: {ledger_entry.fee_category}
📅 Date: {ledger_entry.transaction_date.strftime('%d %B %Y')}
🧾 Receipt: {ledger_entry.receipt_number}

Thank you for your payment!

- EduLafia
        """.strip()
        
        # Create notification
        notification = ParentNotification(
            guardian_id=guardian.id,
            student_id=student.id,
            notification_type='fee',
            title="Payment Receipt",
            message=message,
            channel='whatsapp',
            priority='normal',
            metadata={
                'ledger_entry_id': str(ledger_entry.id),
                'receipt_number': ledger_entry.receipt_number,
                'amount': str(ledger_entry.amount)
            }
        )
        
        self.session.add(notification)
        
        # Send via WhatsApp
        await self.whatsapp_service.send_message(
            guardian.whatsapp_phone or guardian.phone,
            message
        )
        
        # Send receipt PDF if available
        if ledger_entry.receipt_number:
            pdf_url = await self.generate_receipt_pdf(ledger_entry)
            await self.whatsapp_service.send_document(
                guardian.whatsapp_phone or guardian.phone,
                pdf_url,
                f"Receipt_{ledger_entry.receipt_number}.pdf"
            )
```

## 6. UI Component Specifications

### 6.1 Login Component
```typescript
interface ParentLoginProps {
  onLoginSuccess: (auth: AuthResult) => void;
}

// Login Flow:
// 1. Phone number input
// 2. OTP request button
// 3. OTP input (6 digits)
// 4. Verify button
// 5. Resend OTP option
// 6. Error messages

// OTP Input:
interface OTPInputProps {
  length: number;
  onComplete: (otp: string) => void;
  onChange?: (otp: string) => void;
  autoFocus?: boolean;
}
```

### 6.2 Dashboard Component
```typescript
interface ParentDashboardProps {
  guardian: Guardian;
  children: ChildSummary[];
  onSelectChild: (child: ChildSummary) => void;
}

// Dashboard Components:
// 1. Child selector (for multi-child families)
// 2. Quick stats cards:
//    - Attendance rate
//    - Current balance
//    - Last sick bay visit
//    - Academic average
// 3. Recent notifications
// 4. Upcoming events
// 5. Quick actions:
//    - Make payment
//    - Submit excusal
//    - Contact school
// 6. Announcements feed
```

### 6.3 Academic Results Component
```typescript
interface AcademicResultsProps {
  studentId: string;
  termId?: string;
  onDownloadReportCard: () => void;
  onDownloadTranscript: () => void;
}

// Results View:
// 1. Term selector
// 2. Results table:
//    - Subject
//    - CA score
//    - Exam score
//    - Total
//    - Grade
//    - Class rank
// 3. Overall average and position
// 4. Performance chart (trend)
// 5. Download report card button
// 6. Download transcript button
```

### 6.4 Payment Component
```typescript
interface ParentPaymentProps {
  studentId: string;
  onPaymentInitiated: (payment: PaymentInitiation) => void;
}

// Payment Flow:
// 1. Balance summary
// 2. Fee breakdown table
// 3. Select fee category
// 4. Enter amount (or select full/partial)
// 5. Payment method selection
// 6. Pay button
// 7. Redirect to payment gateway
// 8. Payment confirmation screen
// 9. Receipt download

// Payment History:
interface PaymentHistoryProps {
  studentId: string;
  termId?: string;
}
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for ParentAuthService
class TestParentAuthService:
    async def test_request_otp_success(self):
        """Test successful OTP request."""
        pass
    
    async def test_request_otp_rate_limit(self):
        """Test OTP rate limiting."""
        pass
    
    async def test_verify_otp_success(self):
        """Test successful OTP verification."""
        pass
    
    async def test_verify_otp_expired(self):
        """Test expired OTP handling."""
        pass
    
    async def test_create_session(self):
        """Test session creation."""
        pass

# Test cases for ParentNotificationService
class TestParentNotificationService:
    async def test_send_absence_notification(self):
        """Test absence notification sending."""
        pass
    
    async def test_quiet_hours_handling(self):
        """Test quiet hours notification scheduling."""
        pass
    
    async def test_notification_preferences(self):
        """Test notification preference enforcement."""
        pass
    
    async def test_send_report_card_notification(self):
        """Test report card notification."""
        pass
```

### 7.2 Integration Tests
```python
class TestParentAPI:
    async def test_login_flow(self):
        """Test complete login flow."""
        pass
    
    async def test_child_profile_endpoint(self):
        """Test GET /api/v1/parent/children/{student_id}/profile endpoint."""
        pass
    
    async def test_payment_initiation_endpoint(self):
        """Test POST /api/v1/parent/children/{student_id}/payment/initiate endpoint."""
        pass
    
    async def test_excusal_submission_endpoint(self):
        """Test POST /api/v1/parent/children/{student_id}/excusal endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Parent Portal
PARENT_PERMISSIONS = {
    "parent": [
        "parent:read:own_children",
        "parent:read:child_profile",
        "parent:read:child_academic",
        "parent:read:child_attendance",
        "parent:read:child_finance",
        "parent:read:child_health_summary",
        "parent:create:excusal",
        "parent:create:payment",
        "parent:create:correction_request",
        "parent:create:feedback",
        "parent:read:notifications",
        "parent:update:notification_preferences"
    ]
}

# Access validation decorator
def validate_parent_access(student_id: UUID):
    """Validate parent has access to student data."""
    async def decorator(guardian_id: UUID = Depends(get_current_guardian)):
        has_access = await check_guardian_student_link(guardian_id, student_id)
        if not has_access:
            raise HTTPException(status_code=403, detail="Access denied")
        return guardian_id
    return decorator
```

### 8.2 Data Privacy
```python
# Data visibility rules for parent portal
PARENT_DATA_VISIBILITY = {
    "academic": {
        "visible": ["results", "grades", "rank", "attendance_summary"],
        "restricted": ["other_students", "internal_comments"],
        "delayed": ["teacher_remarks"]  # Visible after approval
    },
    "health": {
        "visible": ["last_visit_date", "general_reason", "referral_status", "vaccination_status"],
        "restricted": ["clinical_notes", "detailed_diagnosis"],
        "requires_authorization": ["mental_health_data", "detailed_screening"]
    },
    "finance": {
        "visible": ["balance", "payment_history", "fee_breakdown"],
        "restricted": ["school_revenue", "other_students"],
        "actions": ["make_payment", "download_receipt"]
    }
}

# Access logging for parent portal
PARENT_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Portal Login:
    - Target: < 3 seconds for OTP request
    - Target: < 2 seconds for OTP verification
    - OTP delivery: < 30 seconds via WhatsApp
  
  Dashboard Loading:
    - Target: < 3 seconds for dashboard with all children
    - Target: < 2 seconds for single child summary
    - Caching: 5-minute cache for child data
  
  Academic Results:
    - Target: < 3 seconds for term results
    - Target: < 5 seconds for full transcript
    - PDF Generation: < 30 seconds for report card
  
  Payment Processing:
    - Target: < 5 seconds for payment initiation
    - Target: < 10 seconds for receipt delivery
    - Gateway redirect: < 3 seconds
  
  Notifications:
    - Target: < 30 seconds for WhatsApp delivery
    - Target: < 60 seconds for SMS delivery
    - Batch processing: < 5 minutes for daily notifications
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed parent portal data
PARENT_PORTAL_CACHE_CONFIG = {
    "child_summary": {
        "ttl": 300,  # 5 minutes
        "key": "parent:{guardian_id}:child:{student_id}:summary"
    },
    "academic_results": {
        "ttl": 3600,  # 1 hour (results don't change frequently)
        "key": "student:{student_id}:results:term:{term_id}"
    },
    "fee_balance": {
        "ttl": 300,  # 5 minutes
        "key": "student:{student_id}:balance:term:{term_id}"
    },
    "notifications": {
        "ttl": 60,  # 1 minute for real-time updates
        "key": "parent:{guardian_id}:notifications:unread_count"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
PARENT_PORTAL_INTEGRATIONS = {
    "sis": {
        "student_data": "student profiles, guardian links",
        "validation": "guardian-student relationship"
    },
    "academics": {
        "results_data": "academic results, report cards",
        "performance_alerts": "academic decline notifications"
    },
    "attendance": {
        "attendance_data": "attendance records, summaries",
        "absence_alerts": "real-time absence notifications",
        "excusal_management": "excusal submission and tracking"
    },
    "finance": {
        "balance_data": "fee balances, payment history",
        "payment_processing": "online payment initiation",
        "receipt_generation": "payment receipts"
    },
    "health": {
        "health_summary": "sick bay visits, referrals",
        "health_alerts": "health notifications"
    },
    "sentinel": {
        "health_alerts": "urgent health notifications"
    },
    "teacher": {
        "class_teacher": "form teacher contact info",
        "communications": "teacher-parent messaging"
    },
    "intelligence": {
        "parent_analytics": "parent engagement metrics"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_PARENT_INTEGRATIONS = {
    "whatsapp": {
        "purpose": "Primary parent communication channel",
        "templates": [
            "absence_notification",
            "report_card_delivery",
            "payment_receipt",
            "health_notification",
            "announcement"
        ],
        "features": ["message", "document", "template"],
        "rate_limiting": "respect WhatsApp business limits"
    },
    "termii": {
        "purpose": "SMS for OTP and fallback notifications",
        "templates": ["otp", "absence_sms", "payment_confirmation"],
        "fallback": "used when WhatsApp fails"
    },
    "paystack": {
        "purpose": "Online fee payments",
        "features": ["initialize", "verify", "webhook"],
        "webhooks": ["charge.success", "charge.failed"]
    },
    "flutterwave": {
        "purpose": "Alternative payment gateway",
        "features": ["initialize", "verify", "webhook"],
        "webhooks": ["charge.completed", "charge.failed"]
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create GuardianPortalSession model and schema
- [ ] Create OTPVerification model and schema
- [ ] Create ParentNotification model and schema
- [ ] Create ParentNotificationPreference model and schema
- [ ] Create AbsenceExcusal model and schema
- [ ] Create ParentCorrectionRequest model and schema
- [ ] Create ParentFeedback model and schema
- [ ] Implement ParentAuthService
- [ ] Implement ParentNotificationService
- [ ] Implement ParentPaymentService
- [ ] Create parent API endpoints
- [ ] Implement OTP generation and verification
- [ ] Implement session management
- [ ] Implement notification sending
- [ ] Implement payment integration
- [ ] Implement WhatsApp integration
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create ParentLogin component
- [ ] Create ParentDashboard component
- [ ] Create ChildSelector component
- [ ] Create AcademicResults component
- [ ] Create AttendanceSummary component
- [ ] Create FinanceSummary component
- [ ] Create HealthSummary component
- [ ] Create PaymentForm component
- [ ] Create NotificationList component
- [ ] Create ExcusalForm component
- [ ] Implement WhatsApp-style UI
- [ ] Implement mobile-first design
- [ ] Implement offline indicators
- [ ] Implement push notifications
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Integration Tasks
- [ ] Implement Paystack integration
- [ ] Implement Flutterwave integration
- [ ] Implement WhatsApp Business API
- [ ] Implement Termii SMS integration
- [ ] Test webhook processing
- [ ] Test notification delivery
- [ ] Test payment flow end-to-end

### 11.4 Testing Tasks
- [ ] Unit tests for ParentAuthService
- [ ] Unit tests for ParentNotificationService
- [ ] Unit tests for ParentPaymentService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for parent portal workflow
- [ ] WhatsApp delivery testing
- [ ] Payment flow testing
- [ ] Security testing (access control)
- [ ] Performance testing
- [ ] Mobile responsiveness testing

---

*This module specification provides a comprehensive guide for implementing the Parent & Guardian Portal. The module is critical for parent engagement and provides a WhatsApp-native experience that meets Nigerian parents where they are.*

---

**End of Parent & Guardian Portal (M7) Specification**