# EduLafia Platform - Module Specification: Fee & Finance Management (M4)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M4 - Fee & Finance Management
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
The Fee & Finance Management module handles all financial operations including fee scheduling, payment collection, receipt generation, financial reporting, and reconciliation. This module provides schools with comprehensive financial management capabilities and supports multiple payment channels including online payments via Paystack, Flutterwave, and Remita.

### 1.2 Scope
- Fee schedule configuration
- Payment recording (cash, online, bank transfer)
- Receipt generation (printable, WhatsApp, email)
- Outstanding balance tracking
- Financial dashboards and reporting
- Audit trail for all transactions
- Scholarship and waiver management
- Debt reporting and collection
- Revenue analytics
- Multi-payment gateway integration

### 1.3 Dependencies
- **Required Modules:** M1 (Student Information System)
- **Dependent Modules:** M7 (Parent Portal - for payments), M8 (Intelligence - for analytics)
- **External Dependencies:** Paystack, Flutterwave, Remita (for government schools), Termii (for SMS receipts)

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 Fee Schedule Configuration
```yaml
Feature: Fee Schedule Configuration
Description: Configure fee categories and amounts per class
Acceptance Criteria:
  - Create fee schedules per academic year
  - Configure fee categories (tuition, PTA, exam, uniform, lab, IT, sports, etc.)
  - Set amounts per class level
  - Support mandatory vs optional fees
  - Support special categories (scholarship, bursary, sponsored)
  - Copy fee schedules between academic years
  - Lock fee schedules once term begins (admin override with reason)
  - Support different fee structures for different student categories
```

#### 2.1.2 Payment Recording
```yaml
Feature: Payment Recording
Description: Record payments from various channels
Acceptance Criteria:
  - Cash payment recording with receipt generation
  - Online payment via Paystack/Flutterwave webhooks
  - Remita integration for government schools
  - Bank transfer recording with reference validation
  - Cheque recording with clearing status
  - Payment reversal with mandatory reason
  - Support partial payments
  - Real-time balance updates
  - Payment method tracking
```

#### 2.1.3 Receipt Generation
```yaml
Feature: Receipt Generation
Description: Generate payment receipts in multiple formats
Acceptance Criteria:
  - Printable A5 receipt with school branding
  - WhatsApp PDF receipt delivery
  - Email PDF receipt delivery
  - Unique receipt numbers (sequential per school)
  - Include student name, class, amount, date, payment method
  - Include outstanding balance after payment
  - School stamp/seal on printed receipts
  - Receipt reprint capability
  - Bulk receipt generation for batch payments
```

#### 2.1.4 Outstanding Balance Tracking
```yaml
Feature: Outstanding Balance Tracking
Description: Track and manage student fee balances
Acceptance Criteria:
  - Real-time balance calculation per student
  - Live ledger with all transactions
  - Filter by class, amount owed, payment status
  - Highlight students with overdue payments
  - Support for payment plans
  - Automated reminders for overdue payments
  - Debt report generation
  - Balance carry-forward between terms
```

#### 2.1.5 Financial Dashboard
```yaml
Feature: Financial Dashboard
Description: Comprehensive financial analytics and reporting
Acceptance Criteria:
  - Termly revenue summary
  - Outstanding balance overview
  - Collection rate by class
  - Comparison across terms and academic years
  - Revenue breakdown by fee category
  - Payment method analysis
  - Top debtors list
  - Collection trends and forecasts
  - Export capabilities (CSV, PDF)
```

#### 2.1.6 Scholarship and Waiver Management
```yaml
Feature: Scholarship and Waiver Management
Description: Manage scholarships, bursaries, and fee waivers
Acceptance Criteria:
  - Create scholarship programs
  - Define waiver criteria (full waiver, partial waiver)
  - Track sponsored students
  - Exclude waivers from revenue distortion
  - Generate scholarship reports
  - Track scholarship utilization
  - Support donor reporting
  - Integration with student records
```

### 2.2 Business Rules

#### 2.2.1 Fee Configuration Business Rules
1. **Lock Period:** Fee schedules locked once term begins
2. **Admin Override:** Changes after lock require admin override with reason
3. **Mandatory Fees:** Tuition always mandatory, others configurable
4. **Class Level:** Fees configured per class level, not per individual student
5. **Special Categories:** Scholarships/waivers tracked separately
6. **Annual Configuration:** Fee schedules configured per academic year
7. **Copy Functionality:** Ability to copy previous year's schedule with adjustments

#### 2.2.2 Payment Business Rules
1. **Bursar Only:** Only users with 'Bursar' role can record payments
2. **Separation of Duties:** School admin can view but not record transactions
3. **Maximum Transaction:** Configurable maximum transaction amount (default ₦500,000)
4. **No Deletion:** Financial records cannot be deleted, only reversed
5. **Reversal Process:** Reversals create new offsetting record with mandatory reason
6. **Webhook Validation:** Online payments validated via payment gateway webhooks
7. **Duplicate Prevention:** Prevent duplicate payments for same invoice
8. **Receipt Required:** Receipt automatically generated for every payment

#### 2.2.3 Receipt Business Rules
1. **Sequential Numbering:** Receipt numbers sequential per school per year
2. **School Branding:** All receipts include school logo and details
3. **Digital Delivery:** WhatsApp delivery preferred, email optional
4. **Print Format:** A5 format for printing, PDF for digital
5. **Reprint History:** Track all receipt reprints
6. **Void Receipts:** Ability to void receipts with audit trail
7. **Tax Compliance:** Include tax information where applicable

#### 2.2.4 Audit Business Rules
1. **Immutable Log:** Every transaction timestamped and user-attributed
2. **No Deletions:** Records marked as reversed, not deleted
3. **Change Tracking:** All changes logged with before/after values
4. **User Attribution:** Every action linked to specific user
5. **IP Logging:** Record IP address for online transactions
6. **Session Tracking:** Link transactions to user sessions
7. **Retention Period:** Financial records retained for 7 years minimum

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Fee schedules table
CREATE TABLE fee_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    academic_year_id UUID NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    locked_at TIMESTAMP WITH TIME ZONE,
    locked_by UUID REFERENCES users(id),
    -- Audit fields
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
    class_level VARCHAR(20) NOT NULL,  -- JSS1, JSS2, SS1, etc.
    fee_category VARCHAR(100) NOT NULL,  -- tuition, pta, exam, etc.
    amount DECIMAL(12, 2) NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Fee ledger (transaction log) - partitioned by date
CREATE TABLE fee_ledger (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
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
    -- Webhook fields for online payments
    gateway_reference VARCHAR(255),
    gateway_response JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    PRIMARY KEY (id, transaction_date)
) PARTITION BY RANGE (transaction_date);

-- Create monthly partitions
CREATE TABLE fee_ledger_2026_01 
    PARTITION OF fee_ledger
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Indexes for performance
CREATE INDEX idx_fee_ledger_student_date ON fee_ledger(student_id, transaction_date);
CREATE INDEX idx_fee_ledger_school_date ON fee_ledger(school_id, transaction_date);
CREATE INDEX idx_fee_ledger_receipt ON fee_ledger(receipt_number);
CREATE INDEX idx_fee_ledger_reference ON fee_ledger(payment_reference);
CREATE INDEX idx_fee_ledger_gateway_ref ON fee_ledger(gateway_reference);
CREATE INDEX idx_fee_ledger_type_date ON fee_ledger(transaction_type, transaction_date);
CREATE INDEX idx_fee_ledger_category_date ON fee_ledger(fee_category, transaction_date);

-- Scholarships table
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
    donor_name VARCHAR(255),
    donor_contact VARCHAR(255),
    -- Audit fields
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
    notes TEXT,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(student_id, scholarship_id, academic_year_id)
);

-- Payment configurations
CREATE TABLE payment_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    payment_gateway VARCHAR(50) NOT NULL CHECK (payment_gateway IN ('paystack', 'flutterwave', 'remita')),
    is_active BOOLEAN DEFAULT TRUE,
    public_key VARCHAR(255),
    secret_key VARCHAR(255),  -- Encrypted
    merchant_id VARCHAR(255),
    webhook_secret VARCHAR(255),  -- Encrypted
    config JSONB,  -- Additional gateway-specific configuration
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1,
    UNIQUE(school_id, payment_gateway)
);

-- Financial reporting views
CREATE VIEW financial_summary AS
SELECT 
    fl.school_id,
    fl.academic_year_id,
    fl.term_id,
    fl.fee_category,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) as total_charges,
    SUM(CASE WHEN fl.transaction_type = 'payment' THEN fl.amount ELSE 0 END) as total_payments,
    SUM(CASE WHEN fl.transaction_type = 'waiver' THEN fl.amount ELSE 0 END) as total_waivers,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) 
        - SUM(CASE WHEN fl.transaction_type IN ('payment', 'waiver') THEN fl.amount ELSE 0 END) as balance
FROM fee_ledger fl
WHERE fl.deleted_at IS NULL
GROUP BY fl.school_id, fl.academic_year_id, fl.term_id, fl.fee_category;

CREATE VIEW student_balance_summary AS
SELECT 
    fl.student_id,
    fl.school_id,
    fl.academic_year_id,
    fl.term_id,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) as total_charges,
    SUM(CASE WHEN fl.transaction_type IN ('payment', 'waiver') THEN fl.amount ELSE 0 END) as total_credits,
    SUM(CASE WHEN fl.transaction_type = 'charge' THEN fl.amount ELSE 0 END) 
        - SUM(CASE WHEN fl.transaction_type IN ('payment', 'waiver') THEN fl.amount ELSE 0 END) as balance
FROM fee_ledger fl
WHERE fl.deleted_at IS NULL
GROUP BY fl.student_id, fl.school_id, fl.academic_year_id, fl.term_id;
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 Fee Schedule Endpoints
```yaml
Endpoints:
  POST /api/v1/finance/fee-schedules:
    - Description: Create fee schedule
    - Request Body: FeeScheduleCreate schema
    - Response: FeeScheduleResponse schema
    - Auth: Required (school_admin, bursar)
    - Business Rules:
      - Can only create for active academic year
      - Cannot duplicate fee categories for same class level
    - Side Effects: None

  GET /api/v1/finance/fee-schedules:
    - Description: List fee schedules for school
    - Query Parameters: school_id, academic_year_id, is_active
    - Response: List of FeeScheduleResponse
    - Auth: Required

  GET /api/v1/finance/fee-schedules/{schedule_id}:
    - Description: Get fee schedule details
    - Response: FeeScheduleDetailResponse
    - Auth: Required

  PATCH /api/v1/finance/fee-schedules/{schedule_id}:
    - Description: Update fee schedule
    - Request Body: FeeScheduleUpdate schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Check if schedule is locked
      - Require admin override if locked

  POST /api/v1/finance/fee-schedules/{schedule_id}/lock:
    - Description: Lock fee schedule
    - Auth: Required (school_admin)
    - Business Rules:
      - Cannot unlock once locked
      - Require override for changes after lock

  POST /api/v1/finance/fee-schedules/copy:
    - Description: Copy fee schedule from previous year
    - Request Body: { "source_schedule_id": "...", "academic_year_id": "..." }
    - Response: New FeeScheduleResponse
    - Auth: Required (school_admin)
```

#### 4.1.2 Payment Endpoints
```yaml
Endpoints:
  POST /api/v1/finance/payments:
    - Description: Record a payment
    - Request Body: PaymentCreate schema
    - Response: PaymentResponse schema
    - Auth: Required (bursar)
    - Business Rules:
      - Validate amount against maximum
      - Generate receipt number
      - Update student balance
    - Side Effects:
      - Create fee_ledger record
      - Generate receipt
      - Send notification to guardian
      - Log audit trail

  POST /api/v1/finance/payments/online:
    - Description: Initiate online payment
    - Request Body: OnlinePaymentRequest schema
    - Response: PaymentInitiationResponse schema
    - Auth: Required (parent, bursar)
    - Business Rules:
      - Generate payment link
      - Set expiration time
      - Include student and fee details
    - Returns: Payment URL for gateway

  GET /api/v1/finance/payments:
    - Description: List payments
    - Query Parameters: student_id, school_id, date_range, payment_method
    - Response: Paginated list of PaymentResponse
    - Auth: Required

  GET /api/v1/finance/payments/{payment_id}:
    - Description: Get payment details
    - Response: PaymentDetailResponse
    - Auth: Required

  POST /api/v1/finance/payments/{payment_id}/reverse:
    - Description: Reverse a payment
    - Request Body: { "reason": "..." }
    - Response: ReversalResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Cannot reverse online payments without gateway confirmation
      - Require detailed reason
      - Create offsetting transaction
```

#### 4.1.3 Receipt Endpoints
```yaml
Endpoints:
  GET /api/v1/finance/receipts/{receipt_number}:
    - Description: Get receipt details
    - Response: ReceiptResponse schema
    - Auth: Required

  GET /api/v1/finance/receipts/{receipt_number}/pdf:
    - Description: Download receipt PDF
    - Response: PDF file
    - Auth: Required
    - Business Rules:
      - A5 format with school branding
      - Include QR code for verification

  POST /api/v1/finance/receipts/{receipt_number}/send:
    - Description: Send receipt via WhatsApp/email
    - Request Body: { "channel": "whatsapp", "recipient": "..." }
    - Response: DeliveryResult schema
    - Auth: Required

  GET /api/v1/finance/receipts/{receipt_number}/verify:
    - Description: Verify receipt authenticity
    - Response: VerificationResult schema
    - Auth: Public (for verification portal)
```

#### 4.1.4 Balance and Reporting Endpoints
```yaml
Endpoints:
  GET /api/v1/finance/students/{student_id}/balance:
    - Description: Get student balance
    - Query Parameters: term_id, academic_year_id
    - Response: StudentBalanceResponse schema
    - Auth: Required

  GET /api/v1/finance/students/balances:
    - Description: List students with balances
    - Query Parameters: school_id, class_id, min_balance, term_id
    - Response: Paginated list of StudentBalanceResponse
    - Auth: Required (school_admin, bursar)
    - Business Rules:
      - Support filtering by balance amount
      - Include last payment date
      - Sort by balance amount

  GET /api/v1/finance/dashboard:
    - Description: Get financial dashboard
    - Query Parameters: school_id, term_id
    - Response: FinancialDashboardResponse schema
    - Includes:
      - Total revenue
      - Outstanding balance
      - Collection rate
      - By class breakdown
      - By category breakdown
      - Trends

  GET /api/v1/finance/reports/debtors:
    - Description: Generate debtors report
    - Query Parameters: school_id, term_id, min_balance
    - Response: DebtorsReport schema or CSV
    - Auth: Required (school_admin, bursar)

  GET /api/v1/finance/reports/revenue:
    - Description: Generate revenue report
    - Query Parameters: school_id, start_date, end_date, group_by
    - Response: RevenueReport schema or CSV
    - Auth: Required (school_admin, bursar)

  GET /api/v1/finance/reports/collection-rate:
    - Description: Get collection rate analysis
    - Query Parameters: school_id, term_id
    - Response: CollectionRateReport schema
```

#### 4.1.5 Scholarship Endpoints
```yaml
Endpoints:
  POST /api/v1/finance/scholarships:
    - Description: Create scholarship
    - Request Body: ScholarshipCreate schema
    - Response: ScholarshipResponse schema
    - Auth: Required (school_admin)

  GET /api/v1/finance/scholarships:
    - Description: List scholarships
    - Query Parameters: school_id, academic_year_id, is_active
    - Response: List of ScholarshipResponse
    - Auth: Required

  POST /api/v1/finance/scholarships/{scholarship_id}/award:
    - Description: Award scholarship to student
    - Request Body: ScholarshipAward schema
    - Response: AwardResponse schema
    - Auth: Required (school_admin)
    - Business Rules:
      - Check eligibility criteria
      - Cannot award if already awarded same scholarship
      - Generate waiver transaction

  GET /api/v1/finance/scholarships/{scholarship_id}/recipients:
    - Description: List scholarship recipients
    - Response: List of ScholarshipRecipientResponse
    - Auth: Required
```

#### 4.1.6 Webhook Endpoints
```yaml
Endpoints:
  POST /api/v1/webhooks/paystack:
    - Description: Paystack webhook handler
    - Headers: x-paystack-signature
    - Request Body: PaystackEvent schema
    - Response: { "status": "success" }
    - Auth: Webhook signature validation
    - Business Rules:
      - Validate signature
      - Process payment events
      - Idempotent processing
    - Events:
      - charge.success
      - charge.failed
      - transfer.success
      - transfer.failed

  POST /api/v1/webhooks/flutterwave:
    - Description: Flutterwave webhook handler
    - Headers: verif-hash
    - Request Body: FlutterwaveEvent schema
    - Response: { "status": "success" }
    - Auth: Webhook signature validation

  POST /api/v1/webhooks/remita:
    - Description: Remita webhook handler
    - Request Body: RemitaEvent schema
    - Response: { "status": "success" }
    - Auth: Webhook signature validation
```

## 5. Business Logic Implementation

### 5.1 Payment Processing Logic
```python
class PaymentService:
    async def record_payment(
        self,
        payment_data: PaymentCreate,
        recorded_by: UUID
    ) -> Payment:
        """Record a payment transaction."""
        
        # 1. Validate bursar role
        user = await self.user_service.get_user(recorded_by)
        if 'bursar' not in user.roles:
            raise PermissionError("Only bursars can record payments")
        
        # 2. Validate amount
        if payment_data.amount > self.get_max_transaction_amount():
            raise ValidationError(f"Amount exceeds maximum transaction limit")
        
        # 3. Get student and validate
        student = await self.student_service.get_student(payment_data.student_id)
        if student.status != 'active':
            raise ValidationError("Cannot record payment for inactive student")
        
        # 4. Calculate fee categories if not specified
        if not payment_data.fee_category:
            fee_category = await self.determine_fee_category(
                student, 
                payment_data.amount
            )
        else:
            fee_category = payment_data.fee_category
        
        # 5. Generate receipt number
        receipt_number = await self.generate_receipt_number(student.school_id)
        
        # 6. Create ledger entry
        ledger_entry = FeeLedger(
            student_id=payment_data.student_id,
            school_id=student.school_id,
            transaction_date=datetime.utcnow(),
            transaction_type='payment',
            fee_category=fee_category,
            amount=payment_data.amount,
            payment_method=payment_data.payment_method,
            payment_reference=payment_data.payment_reference,
            receipt_number=receipt_number,
            description=payment_data.description,
            term_id=await self.get_current_term_id(student.school_id),
            academic_year_id=await self.get_current_academic_year_id(student.school_id),
            recorded_by=recorded_by
        )
        
        self.session.add(ledger_entry)
        await self.session.flush()
        
        # 7. Generate receipt
        receipt = await self.generate_receipt(ledger_entry, student)
        
        # 8. Send notification to guardian
        await self.notify_guardian(student, ledger_entry)
        
        # 9. Log audit trail
        await self.audit_service.log(
            action="payment_recorded",
            resource_type="payment",
            resource_id=ledger_entry.id,
            details={
                "student_id": str(payment_data.student_id),
                "amount": str(payment_data.amount),
                "receipt_number": receipt_number,
                "payment_method": payment_data.payment_method
            }
        )
        
        await self.session.commit()
        return ledger_entry
    
    async def generate_receipt_number(self, school_id: UUID) -> str:
        """Generate unique receipt number for school."""
        # Format: {SCHOOL_CODE}-{YEAR}-{SEQUENCE}
        school = await self.school_service.get_school(school_id)
        year = datetime.now().year
        
        # Get max sequence for school and year
        result = await self.session.execute(
            select(FeeLedger.receipt_number)
            .where(
                FeeLedger.school_id == school_id,
                FeeLedger.receipt_number.like(f"{school.code}-{year}-%")
            )
            .order_by(FeeLedger.receipt_number.desc())
            .limit(1)
        )
        
        last_receipt = result.scalar()
        
        if last_receipt:
            # Extract sequence from last receipt
            sequence = int(last_receipt.split('-')[-1])
            next_sequence = sequence + 1
        else:
            next_sequence = 1
        
        return f"{school.code}-{year}-{next_sequence:06d}"
    
    async def determine_fee_category(
        self, 
        student: Student, 
        amount: Decimal
    ) -> str:
        """Determine fee category based on amount and student's outstanding."""
        # Get student's outstanding balance by category
        balances = await self.get_student_balances_by_category(student.id)
        
        # Find category with matching or closest amount
        for category, balance in balances.items():
            if balance == amount:
                return category
            # If amount is less than balance, assume partial payment
            if amount < balance:
                return category
        
        # Default to tuition if no match
        return 'tuition'
```

### 5.2 Online Payment Integration
```python
class OnlinePaymentService:
    async def initiate_payment(
        self,
        request: OnlinePaymentRequest
    ) -> PaymentInitiation:
        """Initiate online payment via gateway."""
        
        # 1. Get school's payment configuration
        config = await self.get_payment_config(
            request.school_id, 
            request.gateway
        )
        
        if not config.is_active:
            raise ValidationError("Payment gateway not configured")
        
        # 2. Get student and calculate amount
        student = await self.student_service.get_student(request.student_id)
        amount = await self.calculate_payment_amount(
            student, 
            request.fee_category
        )
        
        # 3. Generate reference
        reference = f"EDU-{uuid4().hex[:8].upper()}"
        
        # 4. Create pending ledger entry
        ledger_entry = FeeLedger(
            student_id=request.student_id,
            school_id=request.school_id,
            transaction_date=datetime.utcnow(),
            transaction_type='payment',
            fee_category=request.fee_category,
            amount=amount,
            payment_method=request.gateway,
            payment_reference=reference,
            gateway_reference=None,
            status='pending'
        )
        
        self.session.add(ledger_entry)
        await self.session.flush()
        
        # 5. Initialize gateway
        if request.gateway == 'paystack':
            payment_url = await self.initialize_paystack(
                config, 
                amount, 
                reference,
                student
            )
        elif request.gateway == 'flutterwave':
            payment_url = await self.initialize_flutterwave(
                config, 
                amount, 
                reference,
                student
            )
        
        # 6. Return payment initiation details
        return PaymentInitiation(
            reference=reference,
            payment_url=payment_url,
            amount=amount,
            ledger_entry_id=ledger_entry.id
        )
    
    async def process_webhook(
        self,
        gateway: str,
        event_data: dict,
        signature: str
    ) -> WebhookResult:
        """Process payment gateway webhook."""
        
        # 1. Validate signature
        if not await self.validate_webhook_signature(gateway, event_data, signature):
            raise ValidationError("Invalid webhook signature")
        
        # 2. Extract payment details
        if gateway == 'paystack':
            reference = event_data['data']['reference']
            status = event_data['data']['status']
            gateway_reference = event_data['data']['id']
        elif gateway == 'flutterwave':
            reference = event_data['data']['tx_ref']
            status = event_data['data']['status']
            gateway_reference = event_data['data']['id']
        
        # 3. Find ledger entry
        ledger_entry = await self.session.execute(
            select(FeeLedger)
            .where(FeeLedger.payment_reference == reference)
        )
        ledger_entry = ledger_entry.scalar()
        
        if not ledger_entry:
            raise NotFoundError(f"Payment reference {reference} not found")
        
        # 4. Check for duplicate processing
        if ledger_entry.gateway_reference:
            # Already processed
            return WebhookResult(
                success=True,
                message="Payment already processed",
                ledger_entry_id=ledger_entry.id
            )
        
        # 5. Update ledger entry
        if status == 'success':
            ledger_entry.status = 'completed'
            ledger_entry.gateway_reference = gateway_reference
            ledger_entry.gateway_response = event_data
            
            # Generate receipt
            receipt_number = await self.generate_receipt_number(ledger_entry.school_id)
            ledger_entry.receipt_number = receipt_number
            
            # Notify guardian
            student = await self.student_service.get_student(ledger_entry.student_id)
            await self.notify_guardian(student, ledger_entry)
            
            await self.session.commit()
            
            return WebhookResult(
                success=True,
                message="Payment processed successfully",
                ledger_entry_id=ledger_entry.id,
                receipt_number=receipt_number
            )
        else:
            ledger_entry.status = 'failed'
            ledger_entry.gateway_response = event_data
            await self.session.commit()
            
            return WebhookResult(
                success=False,
                message="Payment failed",
                ledger_entry_id=ledger_entry.id
            )
```

### 5.3 Financial Reporting Logic
```python
class FinancialReportingService:
    async def get_financial_dashboard(
        self,
        school_id: UUID,
        term_id: UUID
    ) -> FinancialDashboard:
        """Get financial dashboard data."""
        
        # 1. Get term charges and payments
        term_data = await self.get_term_financial_data(school_id, term_id)
        
        # 2. Get class-wise breakdown
        class_breakdown = await self.get_class_breakdown(school_id, term_id)
        
        # 3. Get category-wise breakdown
        category_breakdown = await self.get_category_breakdown(school_id, term_id)
        
        # 4. Get collection trends
        trends = await self.get_collection_trends(school_id, term_id)
        
        # 5. Calculate metrics
        total_charges = term_data['total_charges']
        total_payments = term_data['total_payments']
        total_waivers = term_data['total_waivers']
        outstanding = total_charges - total_payments - total_waivers
        collection_rate = (total_payments / total_charges * 100) if total_charges > 0 else 0
        
        return FinancialDashboard(
            total_charges=total_charges,
            total_payments=total_payments,
            total_waivers=total_waivers,
            outstanding_balance=outstanding,
            collection_rate=collection_rate,
            class_breakdown=class_breakdown,
            category_breakdown=category_breakdown,
            trends=trends
        )
    
    async def generate_debtors_report(
        self,
        school_id: UUID,
        term_id: UUID,
        min_balance: Optional[Decimal] = None
    ) -> List[DebtorRecord]:
        """Generate debtors report."""
        
        # Query students with outstanding balances
        query = select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.admission_number,
            Class.name.label('class_name'),
            func.sum(
                case(
                    (FeeLedger.transaction_type == 'charge', FeeLedger.amount),
                    else_=0
                )
            ).label('total_charges'),
            func.sum(
                case(
                    (FeeLedger.transaction_type.in_(['payment', 'waiver']), FeeLedger.amount),
                    else_=0
                )
            ).label('total_credits')
        ).join(
            Class, Student.class_id == Class.id
        ).join(
            FeeLedger, Student.id == FeeLedger.student_id
        ).where(
            Student.school_id == school_id,
            FeeLedger.term_id == term_id,
            Student.status == 'active'
        ).group_by(
            Student.id, Student.first_name, Student.last_name, 
            Student.admission_number, Class.name
        ).having(
            func.sum(
                case(
                    (FeeLedger.transaction_type == 'charge', FeeLedger.amount),
                    else_=0
                )
            ) - func.sum(
                case(
                    (FeeLedler.transaction_type.in_(['payment', 'waiver']), FeeLedger.amount),
                    else_=0
                )
            ) > 0
        )
        
        if min_balance:
            query = query.having(
                func.sum(
                    case(
                        (FeeLedger.transaction_type == 'charge', FeeLedger.amount),
                        else_=0
                    )
                ) - func.sum(
                    case(
                        (FeeLedger.transaction_type.in_(['payment', 'waiver']), FeeLedger.amount),
                        else_=0
                    )
                ) >= min_balance
            )
        
        result = await self.session.execute(query)
        debtors = []
        
        for row in result:
            balance = row.total_charges - row.total_credits
            debtors.append(DebtorRecord(
                student_id=row.id,
                student_name=f"{row.first_name} {row.last_name}",
                admission_number=row.admission_number,
                class_name=row.class_name,
                balance=balance
            ))
        
        return sorted(debtors, key=lambda x: x.balance, reverse=True)
```

## 6. UI Component Specifications

### 6.1 Payment Recording Component
```typescript
interface PaymentRecordingProps {
  schoolId: string;
  onPaymentRecorded: (payment: Payment) => void;
}

// Component Requirements:
// 1. Student search and selection
// 2. Fee category selection
// 3. Amount input with validation
// 4. Payment method selection
// 5. Reference number input
// 6. Receipt preview
// 7. Print receipt button
// 8. WhatsApp receipt button

// Student Search Component:
interface StudentSearchProps {
  schoolId: string;
  onSelect: (student: Student) => void;
  showBalance?: boolean;
}

// Payment Form:
interface PaymentFormProps {
  student: Student;
  onSubmit: (data: PaymentData) => void;
  onCancel: () => void;
}
```

### 6.2 Financial Dashboard Component
```typescript
interface FinancialDashboardProps {
  schoolId: string;
  termId: string;
}

// Dashboard Components:
// 1. Summary cards (revenue, outstanding, collection rate)
// 2. Revenue trend chart
// 3. Collection rate by class table
// 4. Outstanding balance pie chart
// 5. Top debtors list
// 6. Payment method breakdown
// 7. Export buttons
// 8. Date range selector

// Summary Card:
interface SummaryCardProps {
  title: string;
  value: number;
  trend?: number;
  format: 'currency' | 'percentage' | 'number';
}
```

### 6.3 Student Balance Component
```typescript
interface StudentBalanceProps {
  studentId: string;
}

// Balance View:
// 1. Current balance summary
// 2. Transaction history table
// 3. Fee breakdown by category
// 4. Payment history
// 5. Make payment button
// 6. Download statement button
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for PaymentService
class TestPaymentService:
    async def test_record_payment_success(self):
        """Test successful payment recording."""
        pass
    
    async def test_record_payment_exceeds_maximum(self):
        """Test payment exceeding maximum transaction limit."""
        pass
    
    async def test_receipt_number_generation(self):
        """Test receipt number generation."""
        pass
    
    async def test_payment_reversal(self):
        """Test payment reversal."""
        pass
    
    async def test_bursar_role_requirement(self):
        """Test that only bursars can record payments."""
        pass

# Test cases for OnlinePaymentService
class TestOnlinePaymentService:
    async def test_initiate_paystack_payment(self):
        """Test Paystack payment initiation."""
        pass
    
    async def test_process_webhook_success(self):
        """Test successful webhook processing."""
        pass
    
    async def test_webhook_signature_validation(self):
        """Test webhook signature validation."""
        pass
    
    async def test_duplicate_webhook_handling(self):
        """Test duplicate webhook handling."""
        pass
```

### 7.2 Integration Tests
```python
class TestFinanceAPI:
    async def test_payment_recording_endpoint(self):
        """Test POST /api/v1/finance/payments endpoint."""
        pass
    
    async def test_balance_endpoint(self):
        """Test GET /api/v1/finance/students/{student_id}/balance endpoint."""
        pass
    
    async def test_financial_dashboard_endpoint(self):
        """Test GET /api/v1/finance/dashboard endpoint."""
        pass
    
    async def test_debtors_report_endpoint(self):
        """Test GET /api/v1/finance/reports/debtors endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Finance module
FINANCE_PERMISSIONS = {
    "school_admin": [
        "finance:create",
        "finance:read",
        "finance:update",
        "finance:delete",
        "finance:export",
        "finance:configure_schedules",
        "finance:manage_scholarships",
        "finance:view_reports"
    ],
    "bursar": [
        "finance:create:payment",
        "finance:read",
        "finance:update:payment",
        "finance:read:reports",
        "finance:generate_receipts"
    ],
    "teacher": [
        "finance:read:summary"
    ],
    "parent": [
        "finance:read:own_child",
        "finance:create:online_payment",
        "finance:read:receipts"
    ],
    "student": [
        "finance:read:own_balance"
    ]
}
```

### 8.2 Data Security
```python
# Sensitive financial data handling
SENSITIVE_FINANCIAL_DATA = [
    "payment_amounts",     # Individual payment amounts
    "bank_details",        # Bank account information
    "gateway_credentials", # Payment gateway API keys
    "transaction_details"  # Detailed transaction records
]

# Encryption for sensitive fields
ENCRYPTED_FINANCIAL_FIELDS = [
    "gateway_secret_key",
    "webhook_secret",
    "merchant_id"
]

# Access logging for financial data
FINANCIAL_ACCESS_LOGGING = True
```

### 8.3 PCI Compliance
```python
# PCI DSS considerations for payment data
PCI_REQUIREMENTS = {
    "card_data": "Never store full card numbers",
    "cvv": "Never store CVV/CVC codes",
    "tokenization": "Use payment gateway tokenization",
    "encryption": "Encrypt all payment data in transit",
    "access_control": "Restrict access to payment data",
    "monitoring": "Monitor all payment transactions",
    "vulnerability": "Regular security scans"
}
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  Payment Recording:
    - Target: < 2 seconds for single payment
    - Target: < 5 seconds including receipt generation
    - Validation: Real-time (< 100ms)
  
  Online Payment:
    - Target: < 5 seconds for payment initiation
    - Target: < 10 seconds for webhook processing
    - Gateway response: Include in timing
  
  Financial Dashboard:
    - Target: < 3 seconds for school dashboard
    - Target: < 5 seconds for detailed reports
    - Caching: 5-minute cache for dashboard data
  
  Debtors Report:
    - Target: < 10 seconds for school of 500 students
    - Export: < 30 seconds for full export
    - Filtering: Real-time client-side filtering
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed financial data
FINANCE_CACHE_CONFIG = {
    "student_balance": {
        "ttl": 300,  # 5 minutes
        "key": "student:{student_id}:balance:term:{term_id}"
    },
    "financial_dashboard": {
        "ttl": 300,  # 5 minutes
        "key": "school:{school_id}:dashboard:term:{term_id}"
    },
    "fee_schedule": {
        "ttl": 3600,  # 1 hour
        "key": "school:{school_id}:fee_schedule:year:{year}"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
FINANCE_INTEGRATIONS = {
    "sis": {
        "student_data": "student enrollment, class assignment",
        "validation": "student must be active and enrolled"
    },
    "academics": {
        "fee_clearance": "check fee status before results release",
        "scholarship_eligibility": "academic performance for scholarships"
    },
    "attendance": {
        "attendance_fees": "some schools charge for absence",
        "suspension_tracking": "track suspensions for fee implications"
    },
    "health": {
        "medical_fees": "track medical fees and waivers",
        "screening_fees": "charge for health screenings"
    },
    "parent_portal": {
        "payment_view": "show balance and payment history",
        "online_payment": "enable online fee payment",
        "receipt_delivery": "deliver receipts via WhatsApp"
    },
    "sentinel": {
        "fee_waivers": "waivers for health-related absences"
    },
    "intelligence": {
        "financial_analytics": "revenue trends and forecasts",
        "collection_analysis": "payment pattern analysis"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_FINANCE_INTEGRATIONS = {
    "paystack": {
        "purpose": "Online payment processing",
        "features": ["card payments", "bank transfers", "USSD"],
        "webhooks": ["charge.success", "charge.failed"],
        "security": "signature validation"
    },
    "flutterwave": {
        "purpose": "Alternative payment gateway",
        "features": ["card payments", "bank transfers", "mobile money"],
        "webhooks": ["charge.completed", "charge.failed"],
        "security": "hash verification"
    },
    "remita": {
        "purpose": "Government payment integration",
        "features": ["government payment channels"],
        "webhooks": ["payment status updates"],
        "security": "API key authentication"
    },
    "termii": {
        "purpose": "SMS receipt delivery",
        "templates": ["payment_receipt", "payment_reminder"],
        "fallback": "used when WhatsApp delivery fails"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create FeeSchedule model and schema
- [ ] Create FeeScheduleItem model and schema
- [ ] Create FeeLedger model and schema
- [ ] Create Scholarship model and schema
- [ ] Create PaymentConfiguration model and schema
- [ ] Implement PaymentService
- [ ] Implement OnlinePaymentService
- [ ] Implement FinancialReportingService
- [ ] Create finance API endpoints
- [ ] Implement payment recording logic
- [ ] Implement online payment integration
- [ ] Implement receipt generation
- [ ] Implement financial reporting
- [ ] Implement webhook handlers
- [ ] Add scholarship management
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create PaymentRecording component
- [ ] Create FinancialDashboard component
- [ ] Create StudentBalance component
- [ ] Create OnlinePayment component
- [ ] Create ReceiptViewer component
- [ ] Create DebtorsReport component
- [ ] Implement payment form validation
- [ ] Implement receipt printing
- [ ] Implement WhatsApp receipt sending
- [ ] Implement financial charts
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Integration Tasks
- [ ] Implement Paystack integration
- [ ] Implement Flutterwave integration
- [ ] Implement Remita integration
- [ ] Implement webhook validation
- [ ] Test with payment gateways
- [ ] Handle payment failures
- [ ] Implement retry logic

### 11.4 Testing Tasks
- [ ] Unit tests for PaymentService
- [ ] Unit tests for OnlinePaymentService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for payment workflow
- [ ] Webhook processing tests
- [ ] Security testing
- [ ] Performance testing

---

*This module specification provides a comprehensive guide for implementing the Fee & Finance Management system. The module supports multiple payment channels and provides comprehensive financial management capabilities for Nigerian schools.*

---

**End of Fee & Finance Management (M4) Specification**