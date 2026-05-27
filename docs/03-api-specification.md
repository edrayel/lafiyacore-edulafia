# EduLafia Platform - API Specification

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. API Overview

### 1.1 Base Information
- **Base URL:** `https://api.edulafia.ng/api/v1`
- **Content-Type:** `application/json`
- **Authentication:** Bearer Token (JWT)
- **Rate Limiting:** 100 requests per minute per user
- **Pagination:** Default 20 items per page, max 100 items

### 1.2 Authentication Flow
```
POST /auth/login
POST /auth/refresh
POST /auth/logout
POST /auth/forgot-password
POST /auth/reset-password
```

### 1.3 Standard Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2026-03-26T10:30:00Z",
  "request_id": "req_1234567890"
}
```

### 1.4 Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "timestamp": "2026-03-26T10:30:00Z",
  "request_id": "req_1234567890"
}
```

## 2. Authentication API

### 2.1 Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "device_id": "optional_device_id"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 900,
    "token_type": "Bearer",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "roles": ["school_admin"],
      "school_id": "uuid"
    }
  }
}
```

### 2.2 Refresh Token
```http
POST /auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 900,
    "token_type": "Bearer"
  }
}
```

### 2.3 OTP Login (for Parents)
```http
POST /auth/otp/send
```

**Request Body:**
```json
{
  "phone": "+2348012345678",
  "purpose": "login"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "OTP sent successfully"
}
```

```http
POST /auth/otp/verify
```

**Request Body:**
```json
{
  "phone": "+2348012345678",
  "otp": "123456",
  "purpose": "login"
}
```

## 3. School Management API

### 3.1 Create School
```http
POST /schools
```

**Request Body:**
```json
{
  "name": "Example Secondary School",
  "code": "ESS001",
  "type": "private",
  "address": "123 School Road",
  "city": "Enugu",
  "state": "Enugu",
  "lga": "Enugu East",
  "phone": "+2348012345678",
  "email": "info@school.com",
  "principal_name": "Dr. John Doe",
  "principal_phone": "+2348012345679",
  "principal_email": "principal@school.com",
  "subscription_tier": "standard"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Example Secondary School",
    "code": "ESS001",
    "type": "private",
    "subscription_tier": "standard",
    "created_at": "2026-03-26T10:30:00Z"
  }
}
```

### 3.2 Get School
```http
GET /schools/{school_id}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Example Secondary School",
    "code": "ESS001",
    "type": "private",
    "address": "123 School Road",
    "city": "Enugu",
    "state": "Enugu",
    "lga": "Enugu East",
    "phone": "+2348012345678",
    "email": "info@school.com",
    "principal_name": "Dr. John Doe",
    "principal_phone": "+2348012345679",
    "principal_email": "principal@school.com",
    "subscription_tier": "standard",
    "is_active": true,
    "settings": {},
    "created_at": "2026-03-26T10:30:00Z",
    "updated_at": "2026-03-26T10:30:00Z"
  }
}
```

### 3.3 Update School
```http
PATCH /schools/{school_id}
```

**Request Body:**
```json
{
  "name": "Updated School Name",
  "principal_name": "New Principal Name"
}
```

### 3.4 List Schools
```http
GET /schools?state=Enugu&type=private&page=1&limit=20
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

## 4. Student Management API

### 4.1 Create Student
```http
POST /students
```

**Request Body:**
```json
{
  "school_id": "uuid",
  "class_id": "uuid",
  "first_name": "John",
  "last_name": "Doe",
  "middle_name": "Michael",
  "date_of_birth": "2010-01-15",
  "gender": "male",
  "nationality": "Nigerian",
  "state_of_origin": "Enugu",
  "lga": "Enugu East",
  "address": "456 Student Road",
  "blood_group": "O+",
  "genotype": "AA",
  "admission_date": "2026-01-15",
  "guardians": [
    {
      "first_name": "James",
      "last_name": "Doe",
      "phone": "+2348012345678",
      "whatsapp_phone": "+2348012345678",
      "relationship": "father",
      "is_primary_contact": true
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "admission_number": "ESS001-0001",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael",
    "date_of_birth": "2010-01-15",
    "gender": "male",
    "class_id": "uuid",
    "class_name": "JSS1A",
    "status": "active",
    "admission_date": "2026-01-15",
    "guardians": [
      {
        "id": "uuid",
        "first_name": "James",
        "last_name": "Doe",
        "phone": "+2348012345678",
        "relationship": "father",
        "is_primary_contact": true
      }
    ],
    "created_at": "2026-03-26T10:30:00Z"
  }
}
```

### 4.2 Get Student
```http
GET /students/{student_id}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "admission_number": "ESS001-0001",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael",
    "date_of_birth": "2010-01-15",
    "age": 16,
    "gender": "male",
    "class_id": "uuid",
    "class_name": "JSS1A",
    "status": "active",
    "photo_url": "https://...",
    "blood_group": "O+",
    "genotype": "AA",
    "chronic_conditions": [],
    "allergies": [],
    "current_medications": [],
    "guardians": [],
    "attendance_summary": {
      "total_days": 100,
      "present_days": 95,
      "absent_days": 5,
      "attendance_percentage": 95.0
    },
    "academic_summary": {
      "current_average": 78.5,
      "class_rank": 5,
      "total_students": 30
    },
    "created_at": "2026-03-26T10:30:00Z",
    "updated_at": "2026-03-26T10:30:00Z"
  }
}
```

### 4.3 Update Student
```http
PATCH /students/{student_id}
```

**Request Body:**
```json
{
  "first_name": "Updated John",
  "address": "New Address"
}
```

### 4.4 List Students
```http
GET /students?school_id=uuid&class_id=uuid&status=active&page=1&limit=20
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "admission_number": "ESS001-0001",
        "first_name": "John",
        "last_name": "Doe",
        "class_id": "uuid",
        "class_name": "JSS1A",
        "status": "active"
      }
    ],
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

### 4.5 Batch Import Students
```http
POST /students/batch-import
```

**Request Body (multipart/form-data):**
- `file`: CSV file
- `school_id`: School UUID
- `class_id`: Class UUID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_processed": 100,
    "successful": 95,
    "failed": 5,
    "errors": [
      {
        "row": 10,
        "error": "Invalid date format"
      }
    ],
    "imported_ids": ["uuid1", "uuid2"]
  }
}
```

### 4.6 Export Student
```http
GET /students/{student_id}/export
```

**Response (200 OK):**
- Returns a downloadable ZIP file containing:
  - Student profile PDF
  - Academic transcript
  - Health records
  - Attendance records

## 5. Attendance API

### 5.1 Mark Attendance
```http
POST /attendance/mark
```

**Request Body:**
```json
{
  "class_id": "uuid",
  "date": "2026-03-26",
  "period": 1,
  "records": [
    {
      "student_id": "uuid",
      "status": "present"
    },
    {
      "student_id": "uuid",
      "status": "absent",
      "reason_code": "sick",
      "symptom_codes": ["fever", "cough"],
      "notes": "Student reported fever"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "marked_count": 30,
    "class_id": "uuid",
    "date": "2026-03-26",
    "period": 1
  }
}
```

### 5.2 Get Attendance Records
```http
GET /attendance?student_id=uuid&start_date=2026-03-01&end_date=2026-03-31&page=1&limit=20
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "student_id": "uuid",
        "student_name": "John Doe",
        "date": "2026-03-26",
        "status": "present",
        "period": 1,
        "recorded_by": "uuid"
      }
    ],
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

### 5.3 Get Attendance Summary
```http
GET /attendance/summary?class_id=uuid&month=2026-03
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "class_id": "uuid",
    "class_name": "JSS1A",
    "month": "2026-03",
    "total_days": 20,
    "summary": {
      "present": 18,
      "absent": 2,
      "late": 0,
      "excused": 0
    },
    "attendance_rate": 90.0,
    "students": [
      {
        "student_id": "uuid",
        "student_name": "John Doe",
        "present": 18,
        "absent": 2,
        "attendance_rate": 90.0
      }
    ]
  }
}
```

### 5.4 Export Attendance (EMIS Format)
```http
GET /attendance/export/emis?school_id=uuid&term_id=uuid
```

**Response (200 OK):**
- Returns a CSV file in EMIS format

## 6. Academic API

### 6.1 Enter CA Scores
```http
POST /academics/ca-scores
```

**Request Body:**
```json
{
  "subject_id": "uuid",
  "class_id": "uuid",
  "term_id": "uuid",
  "scores": [
    {
      "student_id": "uuid",
      "ca_scores": {
        "classwork": 8,
        "assignment": 9,
        "mid_term": 7
      }
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "saved_count": 30,
    "subject_id": "uuid",
    "class_id": "uuid",
    "term_id": "uuid"
  }
}
```

### 6.2 Enter Exam Scores
```http
POST /academics/exam-scores
```

**Request Body:**
```json
{
  "subject_id": "uuid",
  "class_id": "uuid",
  "term_id": "uuid",
  "scores": [
    {
      "student_id": "uuid",
      "exam_score": 65
    }
  ]
}
```

### 6.3 Get Academic Results
```http
GET /academics/results?student_id=uuid&term_id=uuid
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "student_id": "uuid",
    "student_name": "John Doe",
    "term_id": "uuid",
    "term_name": "First Term 2026",
    "results": [
      {
        "subject_id": "uuid",
        "subject_name": "Mathematics",
        "ca_total": 24,
        "exam_score": 65,
        "total_score": 89,
        "grade": "B2",
        "class_rank": 3
      }
    ],
    "overall_average": 78.5,
    "class_rank": 5,
    "total_students": 30
  }
}
```

### 6.4 Generate Report Card
```http
POST /academics/report-cards/generate
```

**Request Body:**
```json
{
  "student_id": "uuid",
  "term_id": "uuid",
  "principal_remark": "Good performance",
  "nurse_remark": "Healthy"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "report_card_id": "uuid",
    "pdf_url": "https://...",
    "generated_at": "2026-03-26T10:30:00Z"
  }
}
```

### 6.5 Generate Transcript
```http
GET /academics/transcripts/{student_id}
```

**Response (200 OK):**
- Returns a PDF transcript file

## 7. Finance API

### 7.1 Create Fee Schedule
```http
POST /finance/fee-schedules
```

**Request Body:**
```json
{
  "school_id": "uuid",
  "academic_year_id": "uuid",
  "name": "2026/2027 Fee Schedule",
  "items": [
    {
      "class_level": "JSS1",
      "fee_category": "tuition",
      "amount": 50000,
      "is_mandatory": true
    },
    {
      "class_level": "JSS1",
      "fee_category": "exam_fee",
      "amount": 5000,
      "is_mandatory": true
    }
  ]
}
```

### 7.2 Record Payment
```http
POST /finance/payments
```

**Request Body:**
```json
{
  "student_id": "uuid",
  "amount": 50000,
  "fee_category": "tuition",
  "payment_method": "cash",
  "payment_reference": "PAY-2026-001",
  "description": "First term tuition payment"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "transaction_id": "uuid",
    "receipt_number": "ESS001-RCPT-001",
    "amount": 50000,
    "student_id": "uuid",
    "student_name": "John Doe",
    "balance": 0,
    "receipt_url": "https://...",
    "created_at": "2026-03-26T10:30:00Z"
  }
}
```

### 7.3 Get Student Balance
```http
GET /finance/students/{student_id}/balance
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "student_id": "uuid",
    "student_name": "John Doe",
    "academic_year_id": "uuid",
    "term_id": "uuid",
    "total_charges": 150000,
    "total_payments": 100000,
    "total_waivers": 0,
    "balance": 50000,
    "items": [
      {
        "category": "tuition",
        "charged": 100000,
        "paid": 50000,
        "balance": 50000
      }
    ]
  }
}
```

### 7.4 Get Financial Dashboard
```http
GET /finance/dashboard?school_id=uuid&term_id=uuid
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "school_id": "uuid",
    "term_id": "uuid",
    "total_students": 500,
    "total_charges": 75000000,
    "total_collections": 60000000,
    "collection_rate": 80.0,
    "outstanding_balance": 15000000,
    "by_class": [
      {
        "class_id": "uuid",
        "class_name": "JSS1",
        "total_charges": 10000000,
        "collections": 8000000,
        "collection_rate": 80.0
      }
    ],
    "by_category": [
      {
        "category": "tuition",
        "charged": 50000000,
        "collected": 40000000
      }
    ]
  }
}
```

### 7.5 Generate Receipt
```http
GET /finance/receipts/{transaction_id}
```

**Response (200 OK):**
- Returns a PDF receipt

## 8. Health API

### 8.1 Log Sick Bay Visit
```http
POST /health/sick-bay-visits
```

**Request Body:**
```json
{
  "student_id": "uuid",
  "visit_date": "2026-03-26T10:30:00Z",
  "presenting_complaint_codes": ["fever", "cough"],
  "presenting_complaint_notes": "Student complains of fever and cough for 2 days",
  "temperature": 38.5,
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "pulse_rate": 90,
  "treatment_given": "Paracetamol 500mg",
  "outcome": "returned_to_class"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "visit_id": "uuid",
    "student_id": "uuid",
    "student_name": "John Doe",
    "visit_date": "2026-03-26T10:30:00Z",
    "outcome": "returned_to_class",
    "created_at": "2026-03-26T10:30:00Z"
  }
}
```

### 8.2 Create Referral
```http
POST /health/referrals
```

**Request Body:**
```json
{
  "student_id": "uuid",
  "sick_bay_visit_id": "uuid",
  "destination_facility": "Enugu State University Teaching Hospital",
  "reason": "Persistent high fever not responding to treatment",
  "clinical_notes": "Student has been on paracetamol for 3 days with no improvement",
  "follow_up_due_date": "2026-03-28"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "referral_id": "uuid",
    "student_id": "uuid",
    "student_name": "John Doe",
    "destination_facility": "Enugu State University Teaching Hospital",
    "status": "pending",
    "follow_up_due_date": "2026-03-28",
    "referral_letter_url": "https://...",
    "created_at": "2026-03-26T10:30:00Z"
  }
}
```

### 8.3 Conduct Health Screening
```http
POST /health/screenings
```

**Request Body:**
```json
{
  "student_id": "uuid",
  "screening_date": "2026-03-26",
  "screening_type": "annual",
  "height": 1.65,
  "weight": 55.5,
  "vision_left": 6/6,
  "vision_right": 6/6,
  "hearing_left": "normal",
  "hearing_right": "normal",
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "dental_notes": "Good oral hygiene"
}
```

### 8.4 Get Student Health Profile
```http
GET /health/students/{student_id}/profile
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "student_id": "uuid",
    "student_name": "John Doe",
    "blood_group": "O+",
    "genotype": "AA",
    "chronic_conditions": [],
    "allergies": ["Penicillin"],
    "current_medications": [],
    "emergency_notes": "Allergic to penicillin",
    "vaccination_status": {
      "total_vaccines": 10,
      "administered": 8,
      "pending": 2
    },
    "recent_screenings": [],
    "recent_visits": []
  }
}
```

## 9. Sentinel API

### 9.1 Get Sentinel Alerts
```http
GET /sentinel/alerts?school_id=uuid&status=open&page=1&limit=20
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "school_ids": ["uuid"],
        "school_names": ["Example Secondary School"],
        "lga": "Enugu East",
        "state": "Enugu",
        "date_generated": "2026-03-26T10:30:00Z",
        "symptom_profile": {
          "primary_symptoms": ["fever", "cough"],
          "affected_count": 8,
          "time_window": "48 hours"
        },
        "alert_tier": "school",
        "status": "open",
        "recommended_action": "Investigate school water supply and food handling"
      }
    ],
    "total": 10,
    "page": 1,
    "limit": 20,
    "pages": 1
  }
}
```

### 9.2 Acknowledge Alert
```http
PATCH /sentinel/alerts/{alert_id}/acknowledge
```

**Request Body:**
```json
{
  "response_notes": "Team dispatched to school for investigation"
}
```

### 9.3 Get Sentinel Dashboard
```http
GET /sentinel/dashboard?state=Enugu&period=30days
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "state": "Enugu",
    "period": "30 days",
    "total_alerts": 15,
    "open_alerts": 5,
    "acknowledged_alerts": 8,
    "resolved_alerts": 2,
    "by_tier": {
      "school": 12,
      "lga": 2,
      "state": 1
    },
    "by_symptom": {
      "respiratory": 8,
      "gastrointestinal": 5,
      "fever": 2
    },
    "geographic_clusters": [
      {
        "lga": "Enugu East",
        "alert_count": 8,
        "schools_affected": 3
      }
    ],
    "timeline": []
  }
}
```

## 10. Reports API

### 10.1 Generate School Report
```http
POST /reports/school
```

**Request Body:**
```json
{
  "school_id": "uuid",
  "term_id": "uuid",
  "report_type": "term_end"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "report_id": "uuid",
    "pdf_url": "https://...",
    "generated_at": "2026-03-26T10:30:00Z"
  }
}
```

### 10.2 Generate EMIS Report
```http
GET /reports/emis?school_id=uuid&term_id=uuid
```

**Response (200 OK):**
- Returns a CSV file in EMIS format

### 10.3 Generate IDSR Report
```http
GET /reports/idsr?state=Enugu&start_date=2026-01-01&end_date=2026-03-31
```

**Response (200 OK):**
- Returns a PDF/CSV file in IDSR format

## 11. Notification API

### 11.1 Send Notification
```http
POST /notifications/send
```

**Request Body:**
```json
{
  "recipient_type": "guardian",
  "recipient_id": "uuid",
  "notification_type": "absence_alert",
  "title": "Student Absent",
  "message": "Your child John Doe was marked absent today",
  "channel": "whatsapp"
}
```

### 11.2 Get Notifications
```http
GET /notifications?user_id=uuid&type=absence_alert&page=1&limit=20
```

### 11.3 Mark as Read
```http
PATCH /notifications/{notification_id}/read
```

## 12. Webhook Endpoints

### 12.1 Paystack Webhook
```http
POST /webhooks/paystack
```

**Headers:**
- `x-paystack-signature`: Webhook signature

**Request Body:**
```json
{
  "event": "charge.success",
  "data": {
    "id": 1234567890,
    "reference": "ESS001-RCPT-001",
    "amount": 5000000,
    "status": "success",
    "metadata": {
      "student_id": "uuid",
      "school_id": "uuid"
    }
  }
}
```

### 12.2 Flutterwave Webhook
```http
POST /webhooks/flutterwave
```

## 13. Sync API (for Offline Clients)

### 13.1 Get Sync Status
```http
GET /sync/status?device_id=uuid
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "device_id": "uuid",
    "last_sync_at": "2026-03-26T10:30:00Z",
    "sync_status": "synced",
    "pending_operations": 0,
    "last_operation_timestamp": "2026-03-26T10:25:00Z"
  }
}
```

### 13.2 Sync Data
```http
POST /sync/data
```

**Request Body:**
```json
{
  "device_id": "uuid",
  "last_sync_timestamp": "2026-03-26T10:25:00Z",
  "operations": [
    {
      "operation_id": "uuid",
      "operation_type": "create",
      "resource_type": "attendance",
      "data": {},
      "timestamp": "2026-03-26T10:28:00Z"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "sync_timestamp": "2026-03-26T10:30:00Z",
    "conflicts": [],
    "pending_operations": 0
  }
}
```

### 13.3 Resolve Conflict
```http
POST /sync/conflicts/{conflict_id}/resolve
```

**Request Body:**
```json
{
  "resolution": "client_wins",
  "reason": "Client data is more recent"
}
```

## 14. Data Export API

### 14.1 Request Data Access
```http
POST /data-access/requests
```

**Request Body:**
```json
{
  "organization": "University of Nigeria",
  "intended_use": "Research on adolescent health outcomes",
  "ethics_approval_reference": "UNN-ETHICS-2026-001",
  "data_set_required": "anonymized_health_data",
  "date_range": {
    "start": "2026-01-01",
    "end": "2026-12-31"
  },
  "contact_email": "researcher@unn.edu.ng"
}
```

### 14.2 Get Data Access Request Status
```http
GET /data-access/requests/{request_id}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "request_id": "uuid",
    "status": "pending",
    "organization": "University of Nigeria",
    "submitted_at": "2026-03-26T10:30:00Z",
    "reviewed_at": null,
    "reviewer_notes": null
  }
}
```

### 14.3 Download Approved Data
```http
GET /data-access/exports/{export_id}
```

**Response (200 OK):**
- Returns an encrypted CSV file

## 15. Admin API

### 15.1 Provision School
```http
POST /admin/schools/provision
```

**Request Body:**
```json
{
  "name": "Example Secondary School",
  "code": "ESS001",
  "type": "private",
  "state": "Enugu",
  "lga": "Enugu East",
  "subscription_tier": "standard",
  "admin_email": "admin@school.com",
  "admin_phone": "+2348012345678"
}
```

### 15.2 Get System Health
```http
GET /admin/health
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-03-26T10:30:00Z",
    "services": {
      "database": "healthy",
      "redis": "healthy",
      "celery": "healthy",
      "termii": "healthy",
      "paystack": "healthy"
    },
    "metrics": {
      "total_schools": 50,
      "total_students": 15000,
      "active_users": 500
    }
  }
}
```

### 15.3 Get Sync Health
```http
GET /admin/sync-health
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_devices": 200,
    "synced_devices": 180,
    "pending_devices": 15,
    "failed_devices": 5,
    "devices": [
      {
        "device_id": "uuid",
        "school_id": "uuid",
        "school_name": "Example Secondary School",
        "last_sync_at": "2026-03-26T10:30:00Z",
        "sync_status": "synced"
      }
    ]
  }
}
```

## 16. Error Codes

### 16.1 Authentication Errors
```json
{
  "INVALID_CREDENTIALS": "Invalid email or password",
  "ACCOUNT_LOCKED": "Account locked due to multiple failed attempts",
  "TOKEN_EXPIRED": "Token has expired",
  "TOKEN_INVALID": "Token is invalid",
  "UNAUTHORIZED": "Unauthorized access"
}
```

### 16.2 Validation Errors
```json
{
  "VALIDATION_ERROR": "Validation failed",
  "REQUIRED_FIELD": "Required field missing",
  "INVALID_FORMAT": "Invalid format",
  "INVALID_VALUE": "Invalid value",
  "DUPLICATE_ENTRY": "Duplicate entry"
}
```

### 16.3 Resource Errors
```json
{
  "NOT_FOUND": "Resource not found",
  "FORBIDDEN": "Access forbidden",
  "CONFLICT": "Resource conflict",
  "RATE_LIMIT_EXCEEDED": "Rate limit exceeded"
}
```

### 16.4 System Errors
```json
{
  "INTERNAL_SERVER_ERROR": "Internal server error",
  "SERVICE_UNAVAILABLE": "Service temporarily unavailable",
  "DATABASE_ERROR": "Database error",
  "EXTERNAL_SERVICE_ERROR": "External service error"
}
```

## 17. Rate Limiting

### 17.1 Default Limits
- **Authentication endpoints**: 5 requests per minute
- **Data creation endpoints**: 30 requests per minute
- **Data read endpoints**: 100 requests per minute
- **Report generation**: 10 requests per minute
- **File exports**: 5 requests per minute

### 17.2 Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1616791800
```

---

*This API specification provides all endpoints needed to implement the EduLafia platform. All endpoints follow RESTful conventions and include proper error handling.*

---

**End of API Specification**