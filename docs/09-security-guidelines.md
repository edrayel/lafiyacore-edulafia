# EduLafia Security Guidelines

## Document Information

- **Version**: 1.0.0
- **Last Updated**: 2026-03-26
- **Status**: Draft
- **Purpose**: Define security implementation requirements for EduLafia, ensuring NDPA 2023 compliance and protection of sensitive student, health, and financial data

---

## Table of Contents

1. [Security Overview](#1-security-overview)
2. [NDPA 2023 Compliance](#2-ndpa-2023-compliance)
3. [Authentication](#3-authentication)
4. [Authorization (RBAC)](#4-authorization-rbac)
5. [Data Encryption](#5-data-encryption)
6. [Input Validation and Sanitization](#6-input-validation-and-sanitization)
7. [API Security](#7-api-security)
8. [Audit Logging](#8-audit-logging)
9. [Data Protection Officer (DPO) Responsibilities](#9-data-protection-officer-dpo-responsibilities)
10. [Incident Response](#10-incident-response)
11. [Infrastructure Security](#11-infrastructure-security)
12. [Security Testing Requirements](#12-security-testing-requirements)
13. [Implementation Checklists](#13-implementation-checklists)

---

## 1. Security Overview

### 1.1 Security Principles

| Principle | Description |
|-----------|-------------|
| Defense in Depth | Multiple layers of security controls |
| Least Privilege | Users receive minimum necessary access |
| Data Minimization | Collect only required personal data |
| Privacy by Design | Security built into architecture from start |
| Fail Secure | System denies access on failure |
| Complete Mediation | Every access request is checked |

### 1.2 Data Classification

| Classification | Examples | Controls |
|---------------|----------|----------|
| **Restricted** | Health records, sentinel alerts, payment data | Encryption at rest + transit, access logging, DPO approval |
| **Confidential** | Student PII, grades, parent contact info | Encryption at transit, role-based access |
| **Internal** | School settings, class lists, timetables | Authentication required |
| **Public** | School name, address, general announcements | No special controls |

### 1.3 Threat Model

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| Unauthorized data access | High | Medium | RBAC, encryption, audit logging |
| Data breach via API | High | Medium | Rate limiting, input validation, WAF |
| Man-in-the-middle | High | Low | TLS 1.3, certificate pinning |
| SQL injection | High | Low | Parameterized queries, ORM |
| XSS attacks | Medium | Medium | Content Security Policy, output encoding |
| Session hijacking | High | Low | Secure cookies, token rotation |
| Insider threat | High | Medium | Audit logging, DPO oversight |
| Physical device theft | Medium | Medium | Local encryption, remote wipe |

---

## 2. NDPA 2023 Compliance

### 2.1 Nigeria Data Protection Act 2023 Requirements

| NDPA Requirement | Implementation |
|------------------|----------------|
| Lawful basis for processing | Consent management system with parental consent for minors |
| Data minimization | Collect only fields defined in data model |
| Purpose limitation | Enforce data access per module purpose |
| Storage limitation | Automated data retention policies |
| Data accuracy | Regular data quality checks, user correction rights |
| Data subject rights | Self-service portal for access, correction, deletion requests |
| Data breach notification | Incident response plan with 72-hour notification |
| Data Protection Impact Assessment | Required for health data processing |
| Cross-border transfer controls | Data residency in Nigeria (AWS Lagos region) |
| DPO appointment | Mandatory for educational institutions processing minors' data |

### 2.2 Consent Management

```sql
CREATE TABLE consent_records (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL REFERENCES students(id),
    parent_id UUID NOT NULL REFERENCES parents(id),
    consent_type VARCHAR(50) NOT NULL,
    -- consent_type values: 'data_processing', 'health_monitoring', 
    -- 'whatsapp_communication', 'photo_usage', 'analytics'
    status VARCHAR(20) NOT NULL DEFAULT 'granted',
    -- status values: 'granted', 'revoked', 'expired'
    granted_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    purpose TEXT NOT NULL,
    legal_basis VARCHAR(50) NOT NULL,
    -- legal_basis values: 'consent', 'legitimate_interest', 'legal_obligation', 'vital_interests'
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.3 Data Subject Rights Implementation

| Right | Implementation |
|-------|----------------|
| Right of Access | Export student data as JSON/PDF via parent portal |
| Right to Rectification | In-app correction workflow with admin approval |
| Right to Erasure | Soft delete with 90-day hold, then hard delete |
| Right to Restrict Processing | Flag record as restricted, exclude from analytics |
| Right to Data Portability | Export in machine-readable format (JSON, CSV) |
| Right to Object | Opt-out mechanism for non-essential processing |

### 2.4 Data Retention Policy

| Data Type | Retention Period | Action After Expiry |
|-----------|------------------|---------------------|
| Student records | 7 years after graduation | Archive, then anonymize |
| Health visit records | 10 years | Archive, restrict access |
| Attendance records | 5 years | Anonymize |
| Grade records | Permanent | Retain indefinitely |
| Fee/payment records | 7 years | Archive |
| Audit logs | 3 years | Archive, then delete |
| Consent records | Duration of processing + 2 years | Archive |
| Sentinel alerts | 10 years | Archive, restrict access |

---

## 3. Authentication

### 3.1 Authentication Methods

| Role | Primary Method | Secondary Method |
|------|---------------|------------------|
| School Admin | Email + Password | TOTP (Google Authenticator) |
| Teacher | Email + Password | SMS OTP |
| School Nurse | Email + Password | SMS OTP |
| Parent/Guardian | Phone + WhatsApp OTP | SMS OTP |
| State Admin | Email + Password | Hardware token / TOTP |
| Super Admin | Email + Password | Hardware token |

### 3.2 Password Policy

```
Requirements:
- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character
- Not similar to email or username
- Not in breached password list (check against HaveIBeenPwned API hash prefix)
- Maximum age: 90 days (admins), 180 days (teachers)
- Password history: Last 5 passwords cannot be reused
- Lockout after 5 failed attempts (15-minute lockout)
```

### 3.3 Token Management

```yaml
Access Token (JWT):
  Algorithm: RS256
  Expiration: 15 minutes
  Claims:
    - sub: user_id
    - role: user_role
    - school_id: school_context
    - permissions: [list]
    - iss: edulafia-api
    - aud: edulafia-client
    - iat: issued_at
    - exp: expires_at

Refresh Token:
  Storage: HttpOnly secure cookie
  Expiration: 7 days
  Rotation: On every use
  Revocation: Immediate on logout
  One-time use: Old token invalidated on refresh

Session:
  Max concurrent sessions: 3
  Idle timeout: 30 minutes
  Absolute timeout: 12 hours
```

### 3.4 Multi-Factor Authentication (MFA)

```
TOTP Configuration:
  Algorithm: SHA-1
  Digits: 6
  Period: 30 seconds
  Secret length: 20 bytes (Base32 encoded)
  
SMS OTP Configuration:
  Length: 6 digits
  Expiration: 5 minutes
  Max attempts: 3
  Rate limit: 3 per 15 minutes
  
WhatsApp OTP:
  Via Termii API
  Template: Pre-approved verification template
  Expiration: 5 minutes
```

---

## 4. Authorization (RBAC)

### 4.1 Role Definitions

| Role | ID | Description |
|------|----|-------------|
| Super Admin | `super_admin` | Platform-level administration |
| State Admin | `state_admin` | State-level oversight and analytics |
| School Admin | `school_admin` | Full school management access |
| Teacher | `teacher` | Classroom and academic operations |
| School Nurse | `school_nurse` | Health records and sentinel engine |
| Finance Officer | `finance_officer` | Fee management and payments |
| Parent/Guardian | `parent` | View-only access to child's data |
| Student | `student` | Limited self-service access |

### 4.2 Permission Matrix

| Resource | Super Admin | State Admin | School Admin | Teacher | School Nurse | Finance Officer | Parent | Student |
|----------|:-----------:|:-----------:|:------------:|:-------:|:------------:|:---------------:|:------:|:-------:|
| Students | CRUD | R | CRUD | R | R | R | R (own) | R (own) |
| Attendance | R | R | CRUD | CRUD | R | - | R (own) | R (own) |
| Grades | R | R | CRUD | CRUD | - | - | R (own) | R (own) |
| Health Visits | R | R | - | - | CRUD | - | R (own) | - |
| Fee Payments | R | R | R | - | - | CRUD | R (own) | R (own) |
| Teachers | CRUD | R | CRUD | R (own) | - | - | R | - |
| Reports | CRUD | R | CRUD | R | R | R | R (own) | - |
| School Settings | CRUD | R | CRUD | - | - | - | - | - |
| State Analytics | R | R | - | - | - | - | - | - |
| Audit Logs | R | R | R | - | - | - | - | - |
| Sentinel Alerts | R | R | R | - | R | - | - | - |
| User Management | CRUD | CRUD | CRUD (school) | - | - | - | - | - |

Legend: C=Create, R=Read, U=Update, D=Delete

### 4.3 Permission Enforcement

```python
# Permission check decorator
def require_permission(resource: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not has_permission(current_user, resource, action):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Row-level security: Ensure users only access their school's data
def apply_school_filter(query, user: User):
    if user.role not in ['super_admin', 'state_admin']:
        query = query.filter_by(school_id=user.school_id)
    return query
```

### 4.4 Resource-Level Access Control

```sql
-- Row-level security policies
ALTER TABLE students ENABLE ROW LEVEL SECURITY;

CREATE POLICY school_isolation ON students
    USING (school_id = current_setting('app.current_school_id')::UUID);

CREATE POLICY admin_override ON students
    USING (current_setting('app.current_user_role') IN ('super_admin', 'state_admin'));
```

---

## 5. Data Encryption

### 5.1 Encryption at Rest

| Data Type | Encryption Method | Key Management |
|-----------|------------------|----------------|
| Database (PostgreSQL) | AES-256 (TDE) | AWS KMS |
| File storage (S3) | SSE-KMS (AES-256) | AWS KMS |
| Local storage (IndexedDB) | AES-256-GCM | Derived from user key |
| Backups | AES-256 | AWS KMS |
| Logs | AES-256 | AWS KMS |

### 5.2 Encryption in Transit

| Component | Protocol | Certificate |
|-----------|----------|-------------|
| Client ↔ API | TLS 1.3 | Let's Encrypt / AWS ACM |
| API ↔ Database | TLS 1.2+ | AWS RDS certificate |
| API ↔ Redis | TLS 1.2 | AWS ElastiCache certificate |
| API ↔ S3 | TLS 1.2+ | AWS managed |
| Sync Gateway ↔ CouchDB | TLS 1.2+ | Self-signed (internal) |
| WhatsApp API | TLS 1.2+ | Facebook managed |

### 5.3 Field-Level Encryption

Sensitive fields are encrypted at the application level before storage:

```python
# Fields requiring application-level encryption
ENCRYPTED_FIELDS = {
    'students': ['nin', 'parent_nin', 'medical_history'],
    'health_visits': ['diagnosis', 'treatment', 'notes'],
    'fee_payments': ['card_number', 'bank_account'],
    'parents': ['nin', 'bank_details'],
    'teachers': ['nin', 'bank_account'],
}

# Encryption function
def encrypt_field(value: str, context: str) -> str:
    """
    Encrypt a field value using AES-256-GCM with context binding.
    The context (table.column) is included in the AAD to prevent 
    cross-context attacks.
    """
    key = derive_key(master_key, context)
    nonce = os.urandom(12)
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, value.encode(), context.encode())
    return base64.b64encode(nonce + ciphertext).decode()

def decrypt_field(encrypted_value: str, context: str) -> str:
    """Decrypt a field value."""
    data = base64.b64decode(encrypted_value)
    nonce = data[:12]
    ciphertext = data[12:]
    key = derive_key(master_key, context)
    cipher = AESGCM(key)
    return cipher.decrypt(nonce, ciphertext, context.encode()).decode()
```

### 5.4 Key Management

```
Key Hierarchy:
├── Master Key (AWS KMS)
│   ├── Database Encryption Key
│   ├── File Encryption Key
│   ├── Field Encryption Key
│   └── Token Signing Key (RS256 private key)

Key Rotation:
- Master Key: Annual rotation
- Database Key: Automatic with AWS RDS
- Field Encryption Key: Every 2 years
- Token Signing Key: Every 90 days
- JWT Secret: Every 30 days

Key Access:
- Master Key: Super Admin + DPO only
- Application Keys: Via AWS IAM roles (no direct access)
- Emergency Access: Break-glass procedure with audit logging
```

---

## 6. Input Validation and Sanitization

### 6.1 Validation Rules

```python
# Pydantic validation models
class StudentCreate(BaseModel):
    first_name: constr(min_length=1, max_length=100, regex=r'^[a-zA-Z\s\-\']+$')
    last_name: constr(min_length=1, max_length=100, regex=r'^[a-zA-Z\s\-\']+$')
    admission_number: constr(min_length=1, max_length=50)
    date_of_birth: date
    gender: Literal['male', 'female', 'other']
    class_id: UUID
    
    @validator('date_of_birth')
    def validate_age(cls, v):
        age = (date.today() - v).days / 365.25
        if age < 10 or age > 25:
            raise ValueError('Student age must be between 10 and 25')
        return v

class HealthVisitCreate(BaseModel):
    student_id: UUID
    symptoms: List[constr(max_length=200)]
    diagnosis: constr(max_length=500)
    treatment: constr(max_length=1000)
    severity: Literal['low', 'medium', 'high', 'critical']
    
    @validator('symptoms')
    def validate_symptoms(cls, v):
        if not v:
            raise ValueError('At least one symptom required')
        return [s.strip() for s in v]
```

### 6.2 Sanitization Rules

| Input Type | Sanitization |
|------------|-------------|
| Text fields | Strip HTML, limit length, encode special characters |
| Email | Validate format, lowercase, DNS MX check |
| Phone (Nigeria) | Validate format (+234XXXXXXXXXX) |
| NIN | Validate 11-digit format |
| Admission number | Alphanumeric, school-specific format |
| Date | Validate format, reasonable range |
| File uploads | Validate type, size, scan for malware |
| JSON fields | Schema validation, depth limit |

### 6.3 File Upload Security

```
Allowed file types:
- Images: .jpg, .jpeg, .png, .gif (max 5MB)
- Documents: .pdf, .doc, .docx (max 10MB)
- Spreadsheets: .csv, .xlsx (max 10MB)

Validation steps:
1. Check file extension against whitelist
2. Verify MIME type matches extension
3. Check file size against limit
4. Scan content for embedded scripts (images)
5. Generate unique filename (UUID-based)
6. Store in isolated S3 bucket with restricted access
7. Generate presigned URL for access (1-hour expiration)
```

---

## 7. API Security

### 7.1 Rate Limiting

```yaml
Rate Limits:
  General API:
    - 100 requests per minute per user
    - 1000 requests per hour per user
    
  Authentication:
    - Login: 5 attempts per 15 minutes per IP
    - OTP request: 3 per 15 minutes per phone
    - Password reset: 3 per hour per email
    
  Sensitive Operations:
    - Data export: 5 per day per user
    - Bulk operations: 10 per hour per user
    - Payment processing: 10 per minute per user
    
  Health Sentinel:
    - Alert creation: 50 per hour per nurse
    - Cluster alerts: 10 per day per school
```

### 7.2 Request Validation

```python
# Request validation middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Check request size
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_SIZE:
        return Response(status_code=413)
    
    # Validate content type for POST/PUT
    if request.method in ["POST", "PUT"]:
        content_type = request.headers.get("content-type", "")
        if not content_type.startswith("application/json"):
            return Response(status_code=415)
    
    # Add security headers
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response
```

### 7.3 CORS Configuration

```python
CORS_CONFIG = {
    "allow_origins": [
        "https://app.edulafia.com",
        "https://*.edulafia.com",
    ],
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
    "allow_headers": ["Authorization", "Content-Type", "X-School-ID"],
    "allow_credentials": True,
    "max_age": 3600,
}
```

### 7.4 Webhook Security

For incoming webhooks (Paystack, Flutterwave):

```python
# Paystack webhook verification
def verify_paystack_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        PAYSTACK_SECRET_KEY.encode(),
        payload,
        hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Flutterwave webhook verification
def verify_flutterwave_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        FLUTTERWAVE_SECRET_KEY.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## 8. Audit Logging

### 8.1 Audit Log Schema

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID REFERENCES users(id),
    user_role VARCHAR(50),
    school_id UUID REFERENCES schools(id),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    request_id UUID NOT NULL,
    session_id UUID,
    changes JSONB,
    -- { "before": {...}, "after": {...} } for updates
    status VARCHAR(20) NOT NULL,
    -- 'success', 'failure', 'denied'
    error_message TEXT,
    metadata JSONB
    -- Additional context (module, feature, etc.)
);

-- Partition by month for performance
CREATE INDEX idx_audit_timestamp ON audit_logs (timestamp);
CREATE INDEX idx_audit_user ON audit_logs (user_id, timestamp);
CREATE INDEX idx_audit_resource ON audit_logs (resource_type, resource_id);
CREATE INDEX idx_audit_action ON audit_logs (action, status);
CREATE INDEX idx_audit_school ON audit_logs (school_id, timestamp);
```

### 8.2 Events to Log

| Category | Events |
|----------|--------|
| Authentication | Login, logout, failed login, MFA setup, MFA verification, password change, password reset |
| User Management | User create, update, delete, role change, permission grant, permission revoke |
| Student Data | Create, read, update, delete student record, bulk import, data export |
| Attendance | Mark attendance, bulk mark, attendance correction |
| Grades | Enter grade, update grade, bulk enter, report generation |
| Health | Visit create, visit update, sentinel alert, health report |
| Finance | Payment create, payment process, refund, invoice generate |
| System | Settings change, integration config, backup create, backup restore |
| Compliance | Consent grant, consent revoke, data export (DPA request), data deletion |

### 8.3 Audit Log Retention

```
- Online storage: 90 days (hot storage)
- Archive storage: 3 years (S3 Glacier)
- Compliance copy: 7 years (S3 Glacier Deep Archive)
- Deletion: Secure delete after retention period
```

---

## 9. Data Protection Officer (DPO) Responsibilities

### 9.1 DPO Role Requirements

```
Responsibilities:
1. Monitor compliance with NDPA 2023
2. Conduct Data Protection Impact Assessments (DPIAs)
3. Manage data subject access requests (DSARs)
4. Liaise with Nigeria Data Protection Commission (NDPC)
5. Train staff on data protection
6. Investigate data breaches
7. Maintain records of processing activities
8. Review and approve data sharing agreements
9. Oversee consent management
10. Report to school board on compliance status
```

### 9.2 DPO Access Levels

| Access | Description |
|--------|-------------|
| Full audit log access | View all audit logs across all schools |
| Compliance dashboard | View compliance metrics and alerts |
| Data subject requests | Manage and respond to DSARs |
| Breach reports | Access breach investigation tools |
| Configuration | Modify privacy settings and retention policies |

### 9.3 DPIA Template

```
Data Protection Impact Assessment

1. Project/Feature Name:
2. Data Controller:
3. DPO Contact:
4. Description of Processing:
5. Purpose of Processing:
6. Lawful Basis:
7. Categories of Data Subjects:
8. Categories of Personal Data:
9. Data Recipients:
10. International Transfers:
11. Retention Period:
12. Technical Measures:
13. Organizational Measures:
14. Risk Assessment:
    - Likelihood: Low/Medium/High
    - Severity: Low/Medium/High
    - Overall Risk: Low/Medium/High
15. Mitigation Measures:
16. Consultation:
17. Approval:
```

---

## 10. Incident Response

### 10.1 Incident Classification

| Severity | Description | Response Time | Notification |
|----------|-------------|---------------|--------------|
| Critical | Data breach affecting >1000 records | 1 hour | NDPC + affected individuals within 72 hours |
| High | Unauthorized access, system compromise | 4 hours | NDPC within 72 hours if personal data involved |
| Medium | Failed attack, suspicious activity | 24 hours | Internal stakeholders |
| Low | Minor security event, policy violation | 48 hours | Security team |

### 10.2 Incident Response Procedure

```
Phase 1: Detection & Triage (0-1 hour)
├── Identify incident type and severity
├── Activate incident response team
├── Contain immediate threat
└── Document initial findings

Phase 2: Investigation (1-24 hours)
├── Collect and preserve evidence
├── Determine scope of breach
├── Identify affected data subjects
└── Assess impact

Phase 3: Remediation (24-72 hours)
├── Implement fixes
├── Patch vulnerabilities
├── Reset compromised credentials
└── Restore from clean backups if needed

Phase 4: Notification (as required)
├── Notify affected individuals
├── Notify NDPC within 72 hours
├── Notify school administrators
└── Issue public statement if needed

Phase 5: Post-Incident (1-2 weeks)
├── Conduct root cause analysis
├── Update security controls
├── Document lessons learned
└── Update incident response plan
```

### 10.3 NDPC Notification Template

```
To: Nigeria Data Protection Commission

RE: Data Breach Notification

1. Date and time of breach:
2. Date and time of discovery:
3. Nature of breach:
4. Categories of data affected:
5. Approximate number of data subjects:
6. Approximate number of records:
7. Description of likely consequences:
8. Measures taken or proposed:
9. Contact details of DPO:
10. Reference number:

Signature: ________________
Date: ________________
```

---

## 11. Infrastructure Security

### 11.1 AWS Security Configuration

```yaml
Network Security:
  VPC:
    - Private subnets for database and application
    - Public subnet only for load balancer
    - NACLs and Security Groups for access control
  
  WAF:
    - AWS Managed Rules for common attacks
    - Rate limiting rules
    - Geo-restriction (Nigeria + authorized regions)
  
  Shield:
    - AWS Shield Standard for DDoS protection
  
  CloudFront:
    - Origin access identity for S3
    - HTTPS only
    - Custom error responses

Compute Security:
  ECS/Fargate:
    - Task execution role with minimal permissions
    - No SSH access to containers
    - Secrets managed via AWS Secrets Manager
  
  RDS:
    - Private subnet only
    - Encryption at rest (AES-256)
    - Automated backups with encryption
    - Multi-AZ for high availability
  
  ElastiCache (Redis):
    - Private subnet only
    - Encryption at rest and in transit
    - AUTH token required
```

### 11.2 IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::edulafia-uploads-${school_id}/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:${region}:${account}:key/${key_id}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:${region}:${account}:secret:edulafia/*"
    }
  ]
}
```

### 11.3 Container Security

```
Security Practices:
- Use minimal base images (python:3.12-slim)
- Run as non-root user
- Scan images for vulnerabilities (Trivy)
- Sign images with Cosign
- Use read-only root filesystem where possible
- Drop all capabilities, add only required
- No privilege escalation
```

---

## 12. Security Testing Requirements

### 12.1 Testing Types

| Test Type | Frequency | Tool | Scope |
|-----------|-----------|------|-------|
| SAST | Every commit | Semgrep, Bandit | Source code |
| DAST | Weekly | OWASP ZAP | Running application |
| Dependency scan | Every build | Snyk, Dependabot | Dependencies |
| Container scan | Every build | Trivy | Docker images |
| Penetration test | Annual | External firm | Full application |
| API security test | Monthly | OWASP ZAP | API endpoints |

### 12.2 Security Test Checklist

```
Authentication Tests:
- [ ] Brute force protection (account lockout)
- [ ] Session fixation prevention
- [ ] Token expiration and rotation
- [ ] MFA bypass attempts
- [ ] Password policy enforcement

Authorization Tests:
- [ ] Horizontal privilege escalation (accessing other schools' data)
- [ ] Vertical privilege escalation (gaining admin access)
- [ ] IDOR (Insecure Direct Object Reference)
- [ ] Missing function level access control

Input Validation Tests:
- [ ] SQL injection (all input fields)
- [ ] XSS (stored and reflected)
- [ ] Command injection
- [ ] Path traversal
- [ ] File upload vulnerabilities
- [ ] XXE (XML External Entity)

API Security Tests:
- [ ] Rate limiting effectiveness
- [ ] CORS misconfiguration
- [ ] Mass assignment
- [ ] BOLA (Broken Object Level Authorization)
- [ ] Excessive data exposure

Data Protection Tests:
- [ ] Encryption verification (at rest and in transit)
- [ ] PII exposure in logs
- [ ] Data leakage in error messages
- [ ] Backup encryption
```

---

## 13. Implementation Checklists

### 13.1 Authentication Implementation

- [ ] Implement JWT token generation (RS256)
- [ ] Implement refresh token rotation
- [ ] Add password hashing (bcrypt, cost 12)
- [ ] Implement TOTP-based MFA
- [ ] Implement SMS OTP via Termii
- [ ] Implement WhatsApp OTP
- [ ] Add account lockout after failed attempts
- [ ] Add password strength validation
- [ ] Implement secure session management
- [ ] Add remember device functionality

### 13.2 Authorization Implementation

- [ ] Define all roles and permissions
- [ ] Implement RBAC middleware
- [ ] Add row-level security policies
- [ ] Implement permission decorators
- [ ] Add school-level data isolation
- [ ] Implement resource ownership checks
- [ ] Add permission caching (Redis)
- [ ] Test all permission combinations

### 13.3 Encryption Implementation

- [ ] Configure TLS 1.3 for all endpoints
- [ ] Implement field-level encryption for sensitive data
- [ ] Configure AWS KMS for key management
- [ ] Implement encryption for local storage
- [ ] Add encrypted backup configuration
- [ ] Implement key rotation procedures
- [ ] Test encryption/decryption performance
- [ ] Add encryption verification tests

### 13.4 Compliance Implementation

- [ ] Implement consent management system
- [ ] Add data subject access request workflow
- [ ] Implement data export functionality
- [ ] Add data deletion workflow
- [ ] Implement retention policy enforcement
- [ ] Add consent tracking and audit
- [ ] Create DPIA template and process
- [ ] Implement breach notification workflow

### 13.5 Audit Logging Implementation

- [ ] Implement audit log schema
- [ ] Add logging middleware for all API calls
- [ ] Log all authentication events
- [ ] Log all data modifications
- [ ] Log all administrative actions
- [ ] Add log retention and archival
- [ ] Implement log search and export
- [ ] Add compliance reporting

### 13.6 API Security Implementation

- [ ] Implement rate limiting
- [ ] Add request size validation
- [ ] Implement CORS configuration
- [ ] Add security headers middleware
- [ ] Implement input validation on all endpoints
- [ ] Add webhook signature verification
- [ ] Implement API versioning
- [ ] Add API documentation security

---

**End of Security Guidelines**
