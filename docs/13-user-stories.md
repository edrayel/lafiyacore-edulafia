# EduLafia User Stories

> Format: **As a** [role], **I want** [feature], **so that** [benefit].
> Each story includes: ID, Priority (P0-P3), Module, Acceptance Criteria.

---

## User Roles

| Role                | Description                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| **Super Admin**     | Platform-level administrator managing all schools and system configuration |
| **State Admin**     | State-level administrator overseeing schools in their state                |
| **School Admin**    | School-level administrator (principal/VP) managing school operations       |
| **Teacher**         | Classroom teacher managing attendance, grades, and communications          |
| **School Nurse**    | Health professional managing sick bay, screenings, and sentinel alerts     |
| **Finance Officer** | Bursar managing fee schedules, payments, and financial reports             |
| **Parent/Guardian** | Parent or guardian monitoring their children's school activities           |
| **Researcher**      | External researcher accessing anonymized data with ethics approval         |

---

## M1: Student Information System

### US-001: Create Student Profile

**As a** School Admin, **I want** to register a new student with full profile details, **so that** the student is enrolled in the system.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Form captures: first name, last name, middle name, date of birth, gender, nationality, state of origin, LGA
  - [ ] Auto-generates admission number based on school code
  - [ ] Validates age is between 6-20 years
  - [ ] Validates NIN format (11 digits) if provided
  - [ ] Optional fields: address, medical conditions, special needs
  - [ ] On submit, student status defaults to "active"

### US-002: Link Guardians to Student

**As a** School Admin, **I want** to link up to 2 guardians to a student, **so that** the school knows who to contact.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Search existing guardians by name, phone, or NIN
  - [ ] Create new guardian inline if not found
  - [ ] Designate one guardian as primary contact
  - [ ] Mark guardian as emergency contact and/or pickup authorized
  - [ ] Prevent linking more than 2 guardians per student

### US-003: Search and Filter Students

**As a** School Admin, **I want** to search and filter students, **so that** I can quickly find specific records.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Full-text search by name, admission number, or NIN
  - [ ] Filter by class, gender, status (active/inactive/graduated/withdrawn)
  - [ ] Results displayed in paginated table (default 20 per page)
  - [ ] Export results to CSV

### US-004: Batch Import Students

**As a** School Admin, **I want** to import students via CSV, **so that** I can enroll many students at once.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Download CSV template with required/optional columns
  - [ ] Upload CSV with validation preview before import
  - [ ] Report errors per row (missing required fields, invalid data)
  - [ ] Skip duplicates based on NIN or admission number
  - [ ] Import up to 1000 students per batch

### US-005: Update Student Status

**As a** School Admin, **I want** to change a student's status, **so that** records reflect their current enrollment state.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Status options: active, inactive, graduated, withdrawn, transferred, deceased
  - [ ] Require reason for status change (free text)
  - [ ] Log status change in audit trail
  - [ ] Notify linked guardians via WhatsApp/SMS for withdrawal/transfer

### US-006: View Student Detail

**As a** School Admin, **I want** to view a complete student profile, **so that** I have all information in one place.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Display personal info, guardian links, academic history, attendance summary, health profile, fee balance
  - [ ] Edit student details inline
  - [ ] Upload supporting documents (birth certificate, transfer letter)
  - [ ] Print student ID card

---

## M2: Academic & Grading System

### US-007: Configure Subjects

**As a** School Admin, **I want** to set up subjects per class, **so that** teachers know what to teach and grade.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Add subject with name, code, and WAEC/NECO alignment
  - [ ] Assign subjects to specific classes
  - [ ] Mark subjects as core or elective
  - [ ] Bulk import subjects via CSV

### US-008: Enter CA Scores

**As a** Teacher, **I want** to enter continuous assessment scores for my class, **so that** student grades are calculated.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Select class and subject
  - [ ] Enter scores for each CA component (classwork, homework, assignment, mid-term)
  - [ ] CA total must not exceed configured maximum (default 40)
  - [ ] Validate score ranges (0-max)
  - [ ] Auto-save as draft, submit when complete

### US-009: Enter Exam Scores

**As a** Teacher, **I want** to enter exam scores, **so that** final grades can be computed.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Select class, subject, and term
  - [ ] Enter exam scores for each student (max 60)
  - [ ] Validate score ranges
  - [ ] Bulk entry via spreadsheet paste

### US-010: View Computed Grades

**As a** Teacher, **I want** to see automatically computed grades, **so that** I don't have to calculate them manually.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Total = CA + Exam (out of 100)
  - [ ] Grade mapped to WAEC scale: A1 (≥75), B2 (70-74), B3 (65-69), C4 (60-64), C5 (55-59), C6 (50-54), D7 (45-49), E8 (40-44), F9 (<40)
  - [ ] Class rank displayed per student
  - [ ] Lock scores after configurable period (prevents post-deadline changes)

### US-011: Generate Report Cards

**As a** School Admin, **I want** to generate report cards, **so that** parents receive student performance summaries.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Generate PDF report card per student (A4 printable)
  - [ ] Include all subjects, CA scores, exam scores, total, grade, rank
  - [ ] Include teacher's remark and principal's signature area
  - [ ] Batch generate for entire class
  - [ ] Send via WhatsApp as PDF

### US-012: View Performance Analytics

**As a** School Admin, **I want** to see class and school-level performance trends, **so that** I can identify areas needing improvement.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Bar chart showing grade distribution per subject
  - [ ] Line chart showing class average over terms
  - [ ] Identify bottom 10% students per class
  - [ ] Compare performance across classes

---

## M3: Attendance & Absence Tracking

### US-013: Mark Daily Attendance

**As a** Teacher, **I want** to mark attendance for my class, **so that** the school tracks student presence.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Select class and date
  - [ ] Mark each student as Present, Absent, Late, or Excused
  - [ ] Bulk action: "Mark All Present" as starting point
  - [ ] Save marks for entire class in one action
  - [ ] Complete marking for 45 students within 5 minutes

### US-014: Record Absence Reason

**As a** Teacher, **I want** to record why a student is absent, **so that** the school has context for follow-up.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] When marking Absent, require reason: sick, family, unknown, excused, suspended
  - [ ] If sick, show symptom checklist: fever, cough, headache, vomiting, diarrhea, rash, sore throat, fatigue
  - [ ] Optional notes field for additional context
  - [ ] Symptoms feed into LafiyaSentinel engine

### US-015: View Attendance Patterns

**As a** School Admin, **I want** to see attendance patterns and chronic absenteeism, **so that** I can intervene early.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Flag students with >20% absence rate (chronic absenteeism)
  - [ ] Alert for 3+ consecutive absences
  - [ ] Filter by date range, class, status
  - [ ] Export attendance report to CSV for EMIS

### US-016: Edit Attendance Records

**As a** School Admin, **I want** to correct attendance records within a time window, **so that** errors can be fixed.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Edit window configurable (default 24 hours)
  - [ ] Require edit reason
  - [ ] Log edit in audit trail (who, when, what changed)
  - [ ] Prevent editing after window expires

---

## M4: Fee & Finance Management

### US-017: Configure Fee Schedules

**As a** Finance Officer, **I want** to set up fee schedules per class, **so that** the school knows what to charge.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Create fee schedule: class, term, fee type (tuition, uniform, exam, transport), amount, due date
  - [ ] Mark fees as mandatory or optional
  - [ ] Duplicate fee schedule from previous term
  - [ ] View total expected revenue per class/term

### US-018: Record Payments

**As a** Finance Officer, **I want** to record student payments, **so that** balances are tracked accurately.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Search student by name or admission number
  - [ ] Select fee schedule to apply payment against
  - [ ] Enter amount paid, payment method (cash, transfer, POS, cheque)
  - [ ] Generate receipt number: {SCHOOL_CODE}-{YEAR}-{SEQUENCE:06d}
  - [ ] Support partial payments against a fee
  - [ ] Print A5 receipt or send via WhatsApp

### US-019: View Fee Balances

**As a** Finance Officer, **I want** to see outstanding balances, **so that** I can follow up on unpaid fees.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Dashboard showing total expected, collected, outstanding, collection rate
  - [ ] List students with outstanding balances
  - [ ] Filter by class, term, amount range
  - [ ] Export debtors list to CSV

### US-020: Manage Scholarships

**As a** School Admin, **I want** to assign scholarships and waivers, **so that** eligible students receive financial support.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create scholarship: name, type (academic, sports, need-based), discount percentage or fixed amount
  - [ ] Assign to specific students
  - [ ] Track scholarship utilization
  - [ ] Report on scholarship impact

### US-021: Process Online Payments

**As a** Parent, **I want** to pay school fees online, **so that** I don't have to visit the school.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] View outstanding fees in parent portal
  - [ ] Pay via Paystack, Flutterwave, or Remita
  - [ ] Payment methods: card, bank transfer, USSD, mobile money
  - [ ] Receive payment receipt via WhatsApp/email
  - [ ] Payment webhook updates balance automatically

---

## M5: School Health & Sentinel Engine

### US-022: Create Health Profile

**As a** School Nurse, **I want** to create health profiles for students, **so that** medical information is readily available.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Record: blood group, genotype, chronic conditions, allergies, current medications
  - [ ] Record disability status and special accommodations
  - [ ] Record vision (left/right), hearing (left/right)
  - [ ] Flag students with critical conditions (epilepsy, asthma, diabetes)
  - [ ] Require parental consent before storing health data

### US-023: Log Sick Bay Visits

**As a** School Nurse, **I want** to log sick bay visits, **so that** health incidents are tracked.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Search student, select complaint codes
  - [ ] Record vital signs: temperature, BP (systolic/diastolic), pulse rate
  - [ ] Record treatment given and outcome (returned to class, sent home, referred)
  - [ ] Auto-notify parent if student sent home or referred
  - [ ] Flag visits that may trigger Sentinel alerts

### US-024: Conduct Health Screenings

**As a** School Nurse, **I want** to conduct mass health screenings, **so that** I can identify health issues early.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Screening types: annual, pre-sports, special
  - [ ] Record: height, weight, BMI, MUAC, vision, hearing, BP, dental notes
  - [ ] Sickle cell test result
  - [ ] Auto-flag abnormal results (BMI <18.5 or >25, vision <6/12)
  - [ ] Generate screening summary report

### US-025: Manage Referrals

**As a** School Nurse, **I want** to create and track referrals, **so that** students get proper medical care.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Create referral: student, destination facility, reason, priority (low/medium/high/critical)
  - [ ] Set follow-up due date
  - [ ] Track referral status: pending, completed, overdue
  - [ ] Send reminder if follow-up is overdue

### US-026: View Sentinel Alerts

**As a** School Nurse, **I want** to see automated disease outbreak alerts, **so that** I can respond quickly.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Dashboard showing active alerts with tier (school/LGA/state)
  - [ ] Alert details: symptom profile, students affected, date range
  - [ ] Acknowledge alerts with response notes
  - [ ] Resolve alerts when situation is under control
  - [ ] Alert generated within 15 minutes of threshold crossing

### US-027: Track Vaccinations

**As a** School Nurse, **I want** to record student vaccinations, **so that** immunization records are maintained.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record: vaccine name, dose number, administration date, lot number, facility
  - [ ] View vaccination history per student
  - [ ] Flag students with missing or overdue vaccines
  - [ ] Export vaccination report for health authority

---

## M6: Teacher & Staff Management

### US-028: Manage Staff Profiles

**As a** School Admin, **I want** to maintain staff records, **so that** HR information is centralized.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Create staff: name, phone, email, role (teacher/nurse/bursar/admin), department
  - [ ] Record employment type: permanent, contract, NYSC, intern
  - [ ] Track qualifications and certifications
  - [ ] Soft delete (archive) staff who leave

### US-029: Assign Teachers to Classes

**As a** School Admin, **I want** to assign teachers to classes and subjects, **so that** responsibilities are clear.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Assign teacher to class + subject for academic year/term
  - [ ] Mark teacher as form teacher for a class
  - [ ] View all assignments per teacher
  - [ ] Prevent duplicate assignments for same class/subject/term

### US-030: Build Timetable

**As a** School Admin, **I want** to create and publish class timetables, **so that** everyone knows the schedule.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Add timetable entries: day, period, start/end time, subject, teacher, room
  - [ ] Detect teacher clashes (same teacher, same time, different class)
  - [ ] Detect class clashes (same class, same time, different subject)
  - [ ] Publish timetable (makes it visible to teachers and students)
  - [ ] Version control for timetable changes

### US-031: Track Teacher Attendance

**As a** School Admin, **I want** to track teacher attendance, **so that** I know who is present.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Check-in/check-out with timestamp
  - [ ] Method: QR code scan, geofencing, or manual
  - [ ] Calculate late minutes and early departure
  - [ ] Generate monthly attendance report per teacher

### US-032: Broadcast Announcements

**As a** School Admin, **I want** to send announcements to staff, **so that** everyone is informed.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Compose message with title and content
  - [ ] Target audience: all staff, by role, by department
  - [ ] Channels: in-app, WhatsApp, SMS
  - [ ] Require acknowledgement for urgent messages
  - [ ] Track read/unread status

---

## M7: Parent & Guardian Portal

### US-033: Login via OTP

**As a** Parent, **I want** to log in using an OTP sent to my phone, **so that** I don't need to remember a password.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Enter registered phone number
  - [ ] Receive 6-digit OTP via WhatsApp or SMS
  - [ ] OTP expires in 10 minutes
  - [ ] Max 3 attempts per OTP
  - [ ] Rate limit: 3 OTP requests per hour

### US-034: View Children's Profiles

**As a** Parent, **I want** to see my children's school information, **so that** I stay informed.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] View child's name, class, admission number, status
  - [ ] Switch between children if multiple linked
  - [ ] View attendance summary (present/absent/late counts, rate)
  - [ ] View fee balance and payment history
  - [ ] View health summary (recent sick bay visits, screenings)

### US-035: View Academic Results

**As a** Parent, **I want** to see my child's academic results, **so that** I know how they're performing.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] View results by term and subject
  - [ ] See CA score, exam score, total, grade, class rank
  - [ ] Download report card as PDF

### US-036: Submit Absence Excusal

**As a** Parent, **I want** to submit an excusal for my child's absence, **so that** the school knows it's authorized.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Select absence date and reason
  - [ ] Add details (optional)
  - [ ] Submit excusal request
  - [ ] View status: pending, approved, rejected

### US-037: Receive Notifications

**As a** Parent, **I want** to receive notifications about my child, **so that** I'm always informed.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Receive notifications for: absence, payment receipt, health alert, report card, school communication
  - [ ] View notification history in portal
  - [ ] Mark notifications as read
  - [ ] Configure notification preferences per channel (WhatsApp/SMS)

### US-038: Submit Correction Requests

**As a** Parent, **I want** to request corrections to my child's records, **so that** information is accurate.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Select field to correct (name, DOB, address, etc.)
  - [ ] Provide current value and requested value
  - [ ] Add reason for correction
  - [ ] Track request status: pending, approved, rejected

### US-039: Submit Feedback

**As a** Parent, **I want** to submit feedback to the school, **so that** I can share concerns or appreciation.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Select feedback type: complaint, suggestion, appreciation, question
  - [ ] Add subject and message
  - [ ] Option to submit anonymously
  - [ ] View school's response

---

## M8: Intelligence & Analytics

### US-040: View School Dashboard

**As a** School Admin, **I want** to see a dashboard of key metrics, **so that** I have a quick overview of school performance.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] KPI cards: total students, attendance rate, fee collection rate, active health alerts
  - [ ] Active alerts list with severity
  - [ ] Quick stats: total teachers, total classes
  - [ ] Trends: attendance rate over time, fee collection trend
  - [ ] Dashboard loads within 5 seconds

### US-041: View LGA Dashboard

**As a** State Admin, **I want** to see aggregated data for my LGA, **so that** I can compare schools.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Total schools, students, avg attendance, sick bay visits, collections, open alerts
  - [ ] School comparison table with key metrics
  - [ ] Filter by date
  - [ ] Data refreshed daily

### US-042: View Sentinel Surveillance

**As a** State Admin, **I want** to see the disease surveillance dashboard, **so that** I can monitor health threats.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Real-time illness heat map by geographic area
  - [ ] Active alerts list with tier and status
  - [ ] Trend data: signals over time
  - [ ] Filter by school, LGA, state, date range, tier, status
  - [ ] Signals grouped by symptom profile

### US-043: Generate Reports

**As a** School Admin, **I want** to generate custom reports, **so that** I can share data with stakeholders.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Report types: school, attendance, academic, finance, sentinel
  - [ ] Formats: PDF, CSV, XLSX
  - [ ] Track report generation status (pending, generating, completed, failed)
  - [ ] Download completed reports
  - [ ] Reports expire after 7 days

### US-044: Access Anonymized Data (Researcher)

**As a** Researcher, **I want** to access anonymized school data, **so that** I can conduct studies.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Submit data request with ethics approval reference
  - [ ] Specify data categories, date range, geographic scope
  - **State Admin reviews and approves/rejects request**
  - [ ] Download anonymized dataset (max 5 downloads)
  - [ ] Data file expires after 30 days

---

## M9: System Administration

### US-045: Provision New School

**As a** Super Admin, **I want** to onboard a new school, **so that** it can start using the platform.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] School details: name, type (private/public/government), state, LGA, phone, email
  - [ ] Principal details: name, email
  - [ ] Auto-generate school code: {STATE_CODE}-{RANDOM}-{SEQUENCE}
  - [ ] Create school admin user with temporary password
  - [ ] Generate onboarding checklist
  - [ ] Send welcome email/WhatsApp with login credentials

### US-046: Manage Users

**As a** Super Admin, **I want** to manage platform users, **so that** access is properly controlled.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Create user with email, phone, name, role
  - [ ] Reset user password
  - [ ] Deactivate user with reason
  - [ ] Search and filter users by role, school, status
  - [ ] View login history

### US-047: Monitor Sync Health

**As a** Super Admin, **I want** to monitor device sync status, **so that** I can identify connectivity issues.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Dashboard showing devices synced, pending syncs, failed syncs
  - [ ] Amber alert if school hasn't synced in 24 hours
  - [ ] Red alert if school hasn't synced in 48 hours
  - [ ] View sync history per school (start/end time, operations, conflicts)
  - [ ] Manually trigger sync for a school

### US-048: Configure Sentinel Thresholds

**As a** Super Admin, **I want** to configure disease detection thresholds, **so that** alerts are accurate.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Set thresholds per state/LGA/school
  - [ ] Configure: symptom category, time window (hours), cluster threshold, school threshold (%)
  - [ ] Test threshold against historical data
  - [ ] Track threshold changes with reason and effective date
  - [ ] Default: 10% of student population, 48-hour window, 3-student cluster

### US-049: Deploy System Updates

**As a** Super Admin, **I want** to deploy platform updates, **so that** all schools get improvements.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Create update with version, release notes, deployment type (global/school-specific)
  - [ ] Schedule deployment
  - **Monitor deployment progress**
  - [ ] Rollback with reason if issues detected
  - [ ] Zero-downtime deployment

### US-050: Manage Training Resources

**As a** Super Admin, **I want** to manage training materials, **so that** users know how to use the platform.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Upload training resources: video, guide, document, interactive
  - [ ] Categorize: onboarding, module-specific, advanced, troubleshooting
  - [ ] Multi-language support (English, Igbo, Hausa)
  - [ ] Assign resources to specific schools
  - [ ] Track completion: assigned, completed, overdue

---

## Cross-Cutting User Stories

### Offline-First

### US-051: Work Offline

**As a** Teacher, **I want** to mark attendance even without internet, **so that** I'm not blocked by connectivity issues.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] App detects offline state and shows offline banner
  - [ ] Attendance marks stored in IndexedDB
  - [ ] Sync automatically when connection restored
  - [ ] Show sync status indicator (syncing/synced/pending)
  - [ ] Resolve conflicts if same record modified on server

### US-052: Priority-Based Sync

**As a** School Nurse, **I want** health data to sync first, **so that** critical health information is available immediately.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Sync queue prioritizes: P0 (health), P1 (attendance), P2 (grades), P3 (fees), P4 (background)
  - [ ] Health records sync within 1 minute of reconnection
  - [ ] Show pending sync count

### Security & Compliance

### US-053: Data Subject Access Request

**As a** Parent, **I want** to request a copy of my child's data, **so that** I can exercise my rights under NDPA 2023.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Submit data access request through portal
  - [ ] Receive data export within 30 days
  - [ ] Export includes: student profile, attendance, grades, health, fees
  - [ ] Format: machine-readable (JSON/CSV)

### US-054: Consent Management

**As a** Parent, **I want** to manage consent for my child's data, **so that** I control what information is shared.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] View current consent status for: health data, research data, communications
  - [ ] Grant or revoke consent per category
  - **Consent changes logged with timestamp**
  - [ ] School notified of consent changes

### UI/UX

### US-055: Mobile-First Experience

**As a** Parent, **I want** to use the platform on my phone, **so that** I can check on my child anywhere.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] All pages responsive down to 320px width
  - [ ] Touch targets minimum 44px
  - [ ] Forms optimized for mobile input (numeric keyboards, date pickers)
  - [ ] PWA installable on home screen

### US-056: Multi-Language Support

**As a** Parent, **I want** to use the platform in my preferred language, **so that** I can understand the interface.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Language switcher in header (English, Igbo, Hausa)
  - [ ] All UI strings translated
  - [ ] Language preference persisted
  - [ ] Default language based on browser/locale

### US-057: Accessibility

**As a** user with visual impairment, **I want** the platform to be accessible, **so that** I can use it independently.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] WCAG 2.1 AA compliance
  - [ ] Keyboard navigation for all interactive elements
  - [ ] Screen reader compatible (ARIA labels, live regions)
  - [ ] Sufficient color contrast (4.5:1 minimum)
  - [ ] Skip-to-content link
  - [ ] Focus visible indicators

---

## Story Summary

| Module                  | Stories | P0     | P1     | P2     |
| ----------------------- | ------- | ------ | ------ | ------ |
| M1: Student Information | 6       | 3      | 2      | 1      |
| M2: Academic & Grading  | 6       | 3      | 2      | 1      |
| M3: Attendance          | 4       | 2      | 1      | 1      |
| M4: Fee & Finance       | 5       | 3      | 1      | 1      |
| M5: Health & Sentinel   | 6       | 3      | 2      | 1      |
| M6: Teacher & Staff     | 5       | 2      | 2      | 1      |
| M7: Parent Portal       | 7       | 4      | 2      | 1      |
| M8: Intelligence        | 5       | 2      | 2      | 1      |
| M9: System Admin        | 6       | 3      | 2      | 1      |
| Cross-Cutting           | 7       | 3      | 3      | 1      |
| **Total**               | **57**  | **28** | **19** | **10** |

---

## Addendum: Nigerian Context User Stories

> These stories address gaps specific to the Nigerian education context, including language diversity, payment patterns, government compliance, boarding schools, and rural connectivity.

### US-058: Yoruba Language Support

**As a** Parent in Southwest Nigeria, **I want** to use the platform in Yoruba, **so that** I can understand the interface in my native language.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Add Yoruba to language switcher (English, Igbo, Hausa, Yoruba)
  - [ ] All 200+ UI strings translated to Yoruba
  - [ ] Language preference persisted per user
  - [ ] Default language based on school's state (Lagos/Oyo/Ogun → Yoruba)

### US-059: USSD Parent Access

**As a** Parent without a smartphone, **I want** to check my child's information via USSD, **so that** I can stay informed without internet.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Dial short code (e.g., \*347\*EDU#)
  - [ ] Menu: 1=Attendance, 2=Results, 3=Fees, 4=Health
  - [ ] Authenticate with phone number + PIN
  - [ ] Display key info via USSD text response
  - [ ] Works on any feature phone (no internet required)

### US-060: Voice Call Notifications

**As a** Parent who cannot read, **I want** to receive voice call notifications, **so that** I'm informed about my child even if I'm illiterate.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Auto-dial parent's phone for critical alerts (absence, health emergency)
  - [ ] Play pre-recorded message in parent's preferred language
  - [ ] Options: "Press 1 to acknowledge, Press 2 to call school"
  - [ ] Log call delivery status (answered, missed, busy)
  - [ ] Fallback to SMS if voice call fails

### US-061: Boarding School Management

**As a** Boarding House Master, **I want** to manage dormitory assignments and exeat requests, **so that** boarding students are properly supervised.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Assign students to dormitories/houses
  - [ ] Track boarding attendance (night roll call)
  - [ ] Process exeat requests (permission to leave campus)
  - [ ] Log exeat: departure time, return time, destination, guardian pickup
  - [ ] Alert if student doesn't return by curfew
  - [ ] Weekend exeat summary report

### US-062: Class Promotion Workflow

**As a** School Admin, **I want** to bulk-promote students at end of session, **so that** I don't have to update each student individually.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Select academic year to close
  - [ ] Preview promotion: JSS1→JSS2, JSS2→JSS3, JSS3→SS1, SS1→SS2, SS2→SS3, SS3→Graduated
  - [ ] Override individual promotions (hold back, skip grade)
  - [ ] Require reason for held-back students
  - [ ] Execute promotion: update class, archive old records, generate promotion letters
  - [ ] Notify parents of promotion/hold-back via WhatsApp

### US-063: BECE/SSCE Exam Tracking

**As a** School Admin, **I want** to track WAEC/NECO/JAMB registrations and results, **so that** I can monitor exam performance.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Register students for BECE (JSS3) and SSCE (SS3)
  - [ ] Track exam center, candidate number, subjects registered
  - [ ] Import WAEC/NECO/JAMB results via CSV
  - [ ] Compare school results vs national average
  - [ ] Generate exam performance report
  - [ ] Flag students at risk of failing

### US-064: Multi-Installment Fee Payment

**As a** Parent, **I want** to pay school fees in installments, **so that** I can manage my finances across the term.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] School configures installment plan: 2 or 3 payments per term
  - [ ] Each installment has its own due date and amount
  - [ ] Track payment status per installment (paid, partial, overdue)
  - [ ] Send reminder 7 days before each installment due date
  - [ ] Block report card if any installment is overdue by 30+ days
  - [ ] Apply late fee for overdue installments (configurable)

### US-065: NYSC Corps Member Management

**As a** School Admin, **I want** to manage NYSC corps members as staff, **so that** I can track their service year.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Employment type: NYSC Corps Member
  - [ ] Track: state code, call-up number, PPA (Place of Primary Assignment)
  - [ ] Alert 3 months before service year ends
  - [ ] Auto-archive staff when service year completes
  - [ ] Generate corps member handover report

### US-066: TRCN Teacher Verification

**As a** School Admin, **I want** to verify teacher TRCN registration, **so that** I comply with teaching regulations.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record TRCN registration number per teacher
  - [ ] Validate format: TRCN/XXXXX/XX
  - **Flag teachers without TRCN or expired registration**
  - [ ] Alert 60 days before TRCN renewal due
  - [ ] Export TRCN compliance report for Ministry of Education

### US-067: EMIS/UBEC/SUBEB Reporting

**As a** School Admin, **I want** to generate government reports, **so that** I comply with education authority requirements.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] EMIS Annual School Census report (enrolment, staffing, infrastructure)
  - [ ] UBEC intervention report (capitation grant utilization)
  - [ ] SUBEB teacher deployment report
  - [ ] Export in required CSV/Excel format
  - [ ] Pre-populate from existing data (no manual entry)
  - [ ] Validate against government data dictionary

### US-068: NCDC Disease Reporting

**As a** School Nurse, **I want** to report disease outbreaks to NCDC, **so that** public health authorities can respond.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Auto-generate NCDC-compatible report from Sentinel alerts
  - [ ] Include: disease type, cases, deaths, date range, location
  - [ ] Export in IDSR (Integrated Disease Surveillance and Response) format
  - [ ] Submit via API to NCDC dashboard
  - [ ] Log submission status and NCDC acknowledgment

### US-069: Fee Refund Processing

**As a** Finance Officer, **I want** to process fee refunds for withdrawn students, **so that** parents receive their money back.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Calculate refund: total paid - (daily rate × days attended) - admin fee
  - [ ] Require approval from School Admin for refunds above threshold
  - [ ] Generate refund receipt
  - [ ] Track refund status: pending, approved, processed
  - [ ] Log refund in audit trail

### US-070: End-of-Term Processing

**As a** School Admin, **I want** to process end-of-term activities in bulk, **so that** I can close the term efficiently.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Lock all grades for the term (prevent further changes)
  - [ ] Generate report cards for entire school
  - [ ] Send report cards to parents via WhatsApp
  - [ ] Generate term summary: attendance rate, fee collection, pass rate
  - [ ] Archive term data for historical reference
  - [ ] Open next term automatically

### US-071: SMS Credit Management

**As a** School Admin, **I want** to monitor SMS credit balance, **so that** notifications don't fail due to insufficient credit.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Display current Termii SMS credit balance on dashboard
  - **Alert when credit drops below 500 messages**
  - [ ] Show SMS usage per day/week/month
  - [ ] Link to Termii top-up portal
  - [ ] Estimate credit needed for next week's scheduled notifications

### US-072: Low-Bandwidth Optimization

**As a** Teacher in a rural school, **I want** the app to work on slow internet, **so that** I can use it despite poor connectivity.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Page load <3 seconds on 2G connection (50kbps)
  - [ ] Compress images to <50KB
  - [ ] Lazy-load non-critical content
  - [ ] Offline mode for attendance marking and grade entry
  - [ ] Sync queue with retry on connection failure
  - [ ] Show connection quality indicator

### US-073: NIN Verification

**As a** School Admin, **I want** to verify student and guardian NINs against the NIMC database, **so that** I ensure data accuracy.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Submit NIN to NIMC API for verification
  - [ ] Validate: name, date of birth, photo match
  - [ ] Flag mismatches for manual review
  - [ ] Cache verification result (valid for 30 days)
  - [ ] Log verification attempts for audit

### US-074: Religious School Calendar

**As a** School Admin of a faith-based school, **I want** to configure a custom academic calendar, **so that** it reflects our religious holidays.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Configure term dates independently of government calendar
  - [ ] Add religious holidays (Eid, Christmas, Easter, etc.)
  - [ ] Exclude religious holidays from attendance calculations
  - [ ] Template: Islamic, Christian, Secular
  - [ ] Sync with government calendar for exam dates

### US-075: Girl-Child Education Tracking

**As a** State Admin, **I want** to monitor girl-child enrollment and retention, **so that** I can address dropout issues.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Dashboard showing girl-child enrollment by LGA
  - [ ] Track dropout rate: girls vs boys
  - [ ] Flag schools with >15% girl dropout rate
  - [ ] Generate girl-child education report for SUBEC
  - [ ] Track scholarship recipients (girl-child specific)

### US-076: Discipline and Behavioral Records

**As a** School Admin, **I want** to record student disciplinary actions, **so that** there's a formal record of behavior issues.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record: student, date, offense type (truancy, fighting, bullying, exam malpractice, insubordination), action taken (verbal warning, written warning, suspension, expulsion)
  - [ ] Notify parent for serious offenses
  - [ ] Track repeat offenses
  - [ ] Generate discipline summary report
  - [ ] Include in student transfer records

### US-077: Exam Malpractice Reporting

**As a** Teacher, **I want** to report exam malpractice, **so that** the school can take appropriate action.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record: student, exam, malpractice type (cheating, impersonation, smuggling materials, collusion)
  - [ ] Attach evidence (photo, witness statement)
  - [ ] Route to School Admin for review
  - [ ] Track investigation status and outcome
  - [ ] Generate malpractice report for WAEC/NECO

### US-078: Alumni Management

**As a** School Admin, **I want** to maintain alumni records, **so that** Old Students Associations can support the school.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Auto-graduate students when they complete SS3
  - [ ] Maintain alumni contact information
  - [ ] Track alumni donations and projects funded
  - [ ] Send reunion invitations via WhatsApp/SMS
  - [ ] Generate alumni directory

### US-079: School Inspection Tracking

**As a** School Admin, **I want** to record government inspection findings, **so that** I can address compliance issues.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record: inspection date, inspector name, ministry, findings, recommendations, deadline
  - [ ] Track compliance status: open, in progress, resolved
  - [ ] Upload inspection report document
  - [ ] Alert if deadline approaching
  - [ ] Generate inspection compliance report

### US-080: Transport/Bus Management

**As a** School Admin, **I want** to manage school bus routes and student assignments, **so that** transportation is organized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create bus routes with stops and schedule
  - [ ] Assign students to bus routes
  - [ ] Track bus attendance (boarded/alighted)
  - [ ] Notify parent when child boards/alights
  - [ ] Alert if student misses bus
  - [ ] Generate transport fee invoice

### US-081: PTA Management

**As a** School Admin, **I want** to manage PTA dues and meetings, **so that** parent-teacher association activities are organized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Configure PTA levy per term
  - [ ] Track PTA payment status per parent
  - [ ] Schedule PTA meetings with agenda
  - [ ] Send meeting invitations via WhatsApp/SMS
  - [ ] Record meeting minutes and action items
  - [ ] Generate PTA financial report

### US-082: Emergency Broadcast

**As a** School Admin, **I want** to send emergency broadcasts to all parents, **so that** everyone is informed during crises.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Compose emergency message (max 160 chars for SMS)
  - **Send to all parents immediately (bypass notification preferences)**
  - [ ] Channels: WhatsApp, SMS, voice call
  - [ ] Track delivery status per parent
  - [ ] Retry failed deliveries every 5 minutes
  - [ ] Log emergency broadcast in audit trail

---

## Updated Summary

| Module                  | Stories | P0     | P1     | P2     | P3    |
| ----------------------- | ------- | ------ | ------ | ------ | ----- |
| M1: Student Information | 6       | 3      | 2      | 1      | 0     |
| M2: Academic & Grading  | 8       | 4      | 3      | 1      | 0     |
| M3: Attendance          | 5       | 2      | 1      | 2      | 0     |
| M4: Fee & Finance       | 8       | 4      | 2      | 2      | 0     |
| M5: Health & Sentinel   | 8       | 3      | 3      | 1      | 1     |
| M6: Teacher & Staff     | 8       | 2      | 3      | 3      | 0     |
| M7: Parent Portal       | 10      | 5      | 3      | 2      | 0     |
| M8: Intelligence        | 7       | 3      | 2      | 2      | 0     |
| M9: System Admin        | 9       | 4      | 3      | 2      | 0     |
| Cross-Cutting           | 12      | 4      | 4      | 3      | 1     |
| **Total**               | **81**  | **34** | **26** | **19** | **2** |

---

## Addendum 2: Additional Nigerian Context & Operational Stories

> These 40 stories cover school operations, financial workflows, edge cases, platform features, and Nigerian-specific requirements not captured in the first two sections.

### US-083: Process Student Admission

**As a** School Admin, **I want** to manage the admission process from application to enrollment, **so that** new students are properly onboarded.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Create admission form with required fields
  - [ ] Accept applications online or walk-in
  - [ ] Schedule entrance exam and interview
  - [ ] Record exam score and interview result
  - [ ] Approve/reject application with reason
  - [ ] Convert approved application to student profile automatically

### US-084: Manage School Inventory

**As a** School Admin, **I want** to track school assets and inventory, **so that** I can account for all property.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Register assets: category (furniture, lab equipment, computer, vehicle), description, quantity, value, location
  - [ ] Assign assets to staff or rooms
  - [ ] Record asset condition: new, good, fair, damaged, disposed
  - [ ] Generate asset register report for government audit
  - [ ] Alert when asset needs replacement

### US-085: Manage Library

**As a** Librarian, **I want** to manage the school library, **so that** books are properly tracked.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Catalog books: title, author, ISBN, category, quantity
  - [ ] Lend books to students/staff with due date
  - [ ] Track overdue books and send reminders
  - [ ] Record lost/damaged books
  - [ ] Generate library usage report

### US-086: Manage Cafeteria

**As a** School Admin, **I want** to manage the school cafeteria, **so that** student meals are organized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Configure meal plans: breakfast, lunch, dinner (boarding), snacks
  - [ ] Track daily meal attendance (who ate what)
  - [ ] Record daily sales and expenses
  - [ ] Generate cafeteria financial report
  - [ ] Track dietary restrictions per student

### US-087: Manage Extracurricular Activities

**As a** Teacher, **I want** to manage clubs and extracurricular activities, **so that** students develop holistically.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Create clubs: sports, debate, JETS, press, drama, music
  - [ ] Register students for clubs
  - [ ] Record attendance and achievements
  - [ ] Generate club participation report
  - [ ] Include in student report card

### US-088: Generate Exam Timetable

**As a** School Admin, **I want** to create exam timetables without clashes, **so that** exams run smoothly.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Select exam type: mid-term, terminal, WAEC, NECO, mock
  - [ ] Assign subjects to dates, times, and venues
  - [ ] Detect clashes: same student has two exams at same time
  - [ ] Detect invigilator clashes: same teacher assigned to two venues
  - [ ] Publish timetable to teachers and students
  - [ ] Print exam timetable (A4)

### US-089: Assign Substitute Teachers

**As a** School Admin, **I want** to assign substitute teachers when a teacher is absent, **so that** classes aren't disrupted.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] View absent teacher's timetable for the day
  - [ ] Assign available teacher to each period
  - [ ] Notify substitute teacher via WhatsApp/SMS
  - [ ] Log substitution in attendance record
  - [ ] Prevent assigning teacher who already has a class at that time

### US-090: Track School Bus Location

**As a** Parent, **I want** to track my child's school bus in real-time, **so that** I know when to expect them.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] View bus location on map
  - [ ] See estimated arrival time at next stop
  - [ ] Receive notification when bus is 5 minutes away
  - [ ] View bus route and all stops
  - [ ] Works on low-bandwidth connection

### US-091: Biometric/QR Attendance

**As a** School Admin, **I want** biometric or QR code attendance for staff and students, **so that** proxy attendance is prevented.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Staff check-in via fingerprint or QR code scan
  - [ ] Student check-in via QR code at school gate
  - [ ] Log timestamp and location
  - [ ] Flag suspicious patterns (same device for multiple people)
  - [ ] Generate daily attendance summary

### US-092: Sibling Discount

**As a** School Admin, **I want** to automatically apply discounts for siblings, **so that** families with multiple children pay less.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Configure discount: 2nd child (10%), 3rd child (15%), etc.
  - [ ] Auto-apply discount when generating fee schedule
  - [ ] Show discount breakdown on invoice
  - [ ] Include discount in financial reports
  - [ ] Notify parent of sibling discount applied

### US-093: Staff Discount

**As a** School Admin, **I want** to apply fee discounts for staff children, **so that** staff receive their employment benefit.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Configure staff discount percentage (default 50%)
  - [ ] Link staff member to their children in the system
  - [ ] Auto-apply discount on fee schedule
  - [ ] Remove discount when staff leaves employment
  - [ ] Report on staff discount utilization

### US-094: Debt Recovery Workflow

**As a** Finance Officer, **I want** an automated debt recovery process, **so that** outstanding fees are collected efficiently.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Stage 1: SMS reminder 7 days before due date
  - [ ] Stage 2: WhatsApp reminder on due date
  - [ ] Stage 3: Warning letter at 14 days overdue
  - [ ] Stage 4: Suspend student from class at 30 days overdue
  - [ ] Stage 5: Escalate to School Admin at 60 days overdue
  - [ ] Track recovery progress per debtor

### US-095: Fee Cap Compliance

**As a** School Admin, **I want** to ensure fees comply with state government caps, **so that** the school avoids penalties.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Configure maximum fee per class level (state-specific)
  - [ ] Validate fee schedule against cap before saving
  - [ ] Alert if total fees (tuition + extras) exceed cap
  - [ ] Generate compliance report for Ministry of Education
  - [ ] Track fee cap changes over time

### US-096: Mid-Session Student Transfer

**As a** School Admin, **I want** to process mid-session transfers, **so that** students joining or leaving mid-term are handled properly.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Incoming transfer: create profile, prorate fees, assign class
  - [ ] Outgoing transfer: calculate refund, generate transfer letter
  - [ ] Include academic records to date in transfer letter
  - [ ] Notify all relevant staff of transfer
  - [ ] Update enrollment counts for government reporting

### US-097: Student Name Change

**As a** School Admin, **I want** to process legal name changes, **so that** records are accurate.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Submit name change request with supporting document (court order, affidavit)
  - [ ] Require School Admin approval
  - [ ] Update all records: profile, grades, attendance, fees
  - [ ] Log name change in audit trail
  - [ ] Generate updated student ID card

### US-098: Duplicate Record Detection

**As a** School Admin, **I want** the system to detect duplicate student records, **so that** data quality is maintained.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Flag potential duplicates on student creation (same name + DOB, same NIN, same phone)
  - [ ] Show possible duplicates for review
  - [ ] Merge duplicate records with conflict resolution
  - [ ] Log merge action in audit trail
  - [ ] Run duplicate scan on demand

### US-099: Custody Dispute Handling

**As a** School Admin, **I want** to manage custody disputes, **so that** the school avoids legal liability.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record custody order: which parent has legal custody
  - [ ] Restrict non-custodial parent access to student info
  - [ ] Block non-custodial parent from picking up student
  - [ ] Log all custody-related actions
  - [ ] Alert staff when custody dispute is active

### US-100: Data Retention Policy

**As a** Super Admin, **I want** to configure data retention policies, **so that** the school complies with NDPA 2023.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Configure retention period per data type: student records (7 years after graduation), health records (10 years), financial records (7 years)
  - [ ] Auto-archive records after retention period
  - [ ] Auto-delete archived records after extended period
  - [ ] Generate data retention compliance report
  - [ ] Allow manual override with approval

### US-101: School Closure Workflow

**As a** Super Admin, **I want** to manage school closure, **so that** data is properly archived.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Initiate closure with reason and effective date
  - [ ] Export all school data for archival
  - [ ] Notify all users of closure
  - [ ] Deactivate all user accounts
  - [ ] Archive data with configurable retention period
  - [ ] Generate closure report

### US-102: Teacher Misconduct Tracking

**As a** School Admin, **I want** to record and investigate teacher misconduct, **so that** the school handles issues properly.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record allegation: type (harassment, negligence, fraud, abuse), description, evidence, reporter
  - [ ] Assign investigator
  - [ ] Track investigation status: pending, investigating, resolved
  - [ ] Record outcome: cleared, warning, suspension, termination
  - [ ] Generate misconduct report for Ministry of Education

### US-103: Pandemic/Emergency Mode

**As a** School Admin, **I want** to activate emergency mode, **so that** the school can operate during crises.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Activate emergency mode with reason and start date
  - [ ] Switch to remote learning mode (attendance via online check-in)
  - [ ] Enable daily health screening at gate (temperature, symptoms)
  - [ ] Send daily health status to parents
  - [ ] Generate emergency mode report for government

### US-104: Special Needs Accommodation

**As a** School Admin, **I want** to track special needs accommodations, **so that** disabled students receive proper support.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record disability type: visual, hearing, mobility, cognitive, autism
  - [ ] Create Individual Education Plan (IEP) with goals and accommodations
  - [ ] Track IEP progress and reviews
  - [ ] Assign support staff (special education teacher, aide)
  - [ ] Generate special needs report for SUBEB

### US-105: Certificate Verification Portal

**As a** University Admissions Officer, **I want** to verify student certificates, **so that** I can detect forged certificates.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Public verification page (no login required)
  - [ ] Enter: student name, admission number, graduation year
  - [ ] Display: verified/unverified, school name, graduation date
  - [ ] Include QR code on printed certificates linking to verification
  - [ ] Log all verification attempts

### US-106: School Branding/White-Labeling

**As a** School Admin, **I want** to customize the platform with my school's branding, **so that** it reflects our identity.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Upload school logo (appears in header, report cards, receipts)
  - [ ] Set primary and secondary colors
  - [ ] Customize login page with school name and motto
  - [ ] Customize report card template with school header
  - [ ] Preview branding changes before publishing

### US-107: Data Backup and Restore

**As a** Super Admin, **I want** to backup and restore school data, **so that** data is protected against loss.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Automated daily backup of all school data
  - [ ] Manual backup on demand
  - [ ] Download backup file (encrypted)
  - [ ] Restore from backup with confirmation
  - [ ] Verify backup integrity after creation

### US-108: API Webhook Configuration

**As a** Super Admin, **I want** to configure webhooks for third-party integrations, **so that** external systems receive real-time updates.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Register webhook URL and events (student.created, payment.received, attendance.marked)
  - [ ] Set webhook secret for signature verification
  - [ ] View webhook delivery history and retry failed deliveries
  - [ ] Test webhook with sample payload
  - [ ] Enable/disable webhook per event type

### US-109: WhatsApp Bot

**As a** Parent, **I want** to interact with a WhatsApp chatbot, **so that** I can get information without logging into a portal.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Send "Hi" to school WhatsApp number to start
  - [ ] Menu: 1=Attendance, 2=Results, 3=Fees, 4=Health, 5=Notifications
  - [ ] Authenticate with phone number + PIN on first use
  - [ ] Return formatted text response for each query
  - [ ] Support natural language: "How is my child doing today?"

### US-110: Bulk SMS Scheduling

**As a** School Admin, **I want** to schedule SMS messages in advance, **so that** I can plan communications ahead.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Compose message and select recipient group
  - [ ] Set send date and time
  - [ ] Preview message and recipient count
  - [ ] Edit or cancel scheduled messages
  - [ ] View delivery report after sending

### US-111: Staff Performance Evaluation

**As a** School Admin, **I want** to conduct annual staff evaluations, **so that** I can assess teacher performance.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create evaluation form: punctuality, lesson delivery, student engagement, professionalism
  - [ ] Score each criterion (1-5 scale)
  - [ ] Add comments and recommendations
  - [ ] Generate evaluation report
  - [ ] Track evaluation history over years

### US-112: Report Card Template Designer

**As a** School Admin, **I want** to design custom report card templates, **so that** they match our school's format.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Drag-and-drop template builder
  - [ ] Add school logo, name, address, motto
  - [ ] Configure sections: personal info, academic results, attendance, teacher's remark, principal's signature
  - [ ] Preview template with sample data
  - [ ] Save multiple templates (different for JSS and SS)

### US-113: Audit Log Export

**As a** Super Admin, **I want** to export audit logs, **so that** I can provide evidence for compliance audits.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Filter audit logs by date range, user, action type, school
  - [ ] Export to CSV/Excel
  - [ ] Include: timestamp, user, action, resource, old value, new value, IP address
  - [ ] Generate audit summary report
  - [ ] Retain audit logs for 7 years minimum

### US-114: Push Notifications

**As a** Parent, **I want** to receive push notifications on my phone, **so that** I'm informed even without opening the app.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Opt-in to push notifications during onboarding
  - [ ] Configure notification types: absence, payment, health, academic
  - [ ] Receive notification even when app is closed
  - [ ] Tap notification to open relevant screen
  - [ ] Fallback to SMS if push notification fails

### US-115: School Policy Management

**As a** School Admin, **I want** to store and distribute school policies, **so that** everyone knows the rules.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Upload policy documents (PDF): code of conduct, dress code, anti-bullying, health policy
  - [ ] Categorize policies: student, staff, parent
  - [ ] Notify users when new policy is published
  - [ ] Track policy acknowledgment (who has read)
  - [ ] Generate policy compliance report

### US-116: Almajiri Integration Tracking

**As a** State Admin, **I want** to track Almajiri student integration into formal education, **so that** the government can monitor the program.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Flag students as Almajiri program participants
  - [ ] Track enrollment, attendance, and academic progress
  - [ ] Generate Almajiri integration report for SUBEB
  - [ ] Monitor dropout rate and intervention effectiveness
  - [ ] Compare with non-Almajiri student outcomes

### US-117: Free Education Program Tracking

**As a** State Admin, **I want** to track free education program beneficiaries, **so that** government funds are properly allocated.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Flag students as free education beneficiaries
  - [ ] Track capitation grant received and utilized
  - [ ] Generate utilization report for SUBEB/UBEC
  - [ ] Alert if grant is insufficient for enrolled students
  - [ ] Compare per-student allocation vs actual spending

### US-118: School Feeding Program Tracking

**As a** School Admin, **I want** to track the school feeding program, **so that** I can report meals served to the government.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record daily meal count (students fed)
  - [ ] Track menu and nutritional content
  - [ ] Generate monthly feeding report for N-Power/State program
  - [ ] Alert if meal count drops below enrollment threshold
  - [ ] Include feeding data in EMIS report

### US-119: WAEC/NECO Bulk Registration

**As a** School Admin, **I want** to register entire classes for WAEC/NECO exams at once, **so that** I don't have to register students individually.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Select class and exam type (WAEC SSCE, NECO, BECE)
  - [ ] Preview eligible students (completed required subjects)
  - [ ] Bulk register selected students
  - [ ] Generate registration summary for payment
  - [ ] Track registration status: pending, paid, confirmed

### US-120: JAMB CAPS Integration

**As a** School Admin, **I want** to track JAMB CAPS admission status for SS3 graduates, **so that** I can support university applications.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record JAMB registration number per SS3 student
  - [ ] Track university choices and admission status
  - [ ] Generate JAMB admission summary report
  - [ ] Alert students of admission updates
  - [ ] Include in school's university placement rate report

### US-121: State Ministry Quarterly Reporting

**As a** School Admin, **I want** to generate quarterly reports for the State Ministry of Education, **so that** I comply with government requirements.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Generate quarterly enrolment report (by class, gender, age)
  - [ ] Generate quarterly staffing report (by qualification, employment type)
  - [ ] Generate quarterly financial report (fees collected, expenditures)
  - [ ] Generate quarterly academic performance report
  - [ ] Export in Ministry-required format (Excel/CSV)

---

## Final Updated Summary

| Module                  | Stories | P0     | P1     | P2     | P3    |
| ----------------------- | ------- | ------ | ------ | ------ | ----- |
| M1: Student Information | 10      | 4      | 3      | 3      | 0     |
| M2: Academic & Grading  | 10      | 4      | 4      | 2      | 0     |
| M3: Attendance          | 7       | 2      | 2      | 3      | 0     |
| M4: Fee & Finance       | 12      | 5      | 4      | 3      | 0     |
| M5: Health & Sentinel   | 10      | 3      | 4      | 2      | 1     |
| M6: Teacher & Staff     | 11      | 2      | 4      | 5      | 0     |
| M7: Parent Portal       | 13      | 6      | 4      | 3      | 0     |
| M8: Intelligence        | 10      | 4      | 3      | 3      | 0     |
| M9: System Admin        | 14      | 5      | 5      | 4      | 0     |
| Cross-Cutting           | 24      | 5      | 6      | 9      | 4     |
| **Total**               | **121** | **40** | **39** | **37** | **5** |

---

## Addendum 3: Remaining Operational Gaps

> These 50 stories cover HR/payroll, facilities management, student welfare, safety/security, and school governance — areas not captured in the first three sections.

### HR & Payroll

### US-122: Staff Payroll Processing

**As a** Finance Officer, **I want** to process monthly staff payroll, **so that** salaries are paid on time.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Auto-calculate salary from employment contract
  - [ ] Apply deductions: tax (PAYE), pension (8%), NHF (2.5%), union dues
  - [ ] Apply allowances: housing, transport, teaching, hazard
  - [ ] Generate payslip per staff member
  - [ ] Export payroll summary for bank payment
  - [ ] Generate monthly payroll report

### US-123: Staff Leave Management

**As a** Teacher, **I want** to request leave, **so that** I can take time off with proper approval.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Leave types: annual (20 days), sick (10 days), maternity (12 weeks), paternity (2 weeks), study, compassionate
  - [ ] Submit leave request with start/end dates and reason
  - [ ] School Admin approves/rejects
  - [ ] Track leave balance remaining
  - [ ] Auto-assign substitute teacher during leave period
  - [ ] Alert if leave overlaps with exam period

### US-124: Staff Performance Review

**As a** School Admin, **I want** to conduct periodic staff reviews, **so that** I can assess and improve performance.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Review criteria: punctuality, lesson preparation, student engagement, professionalism, teamwork
  - [ ] Score each criterion (1-5 scale)
  - [ ] Add strengths, weaknesses, and development recommendations
  - [ ] Staff acknowledges review
  - [ ] Track review history and improvement trends
  - [ ] Link review outcomes to contract renewal

### US-125: Staff Contract Management

**As a** School Admin, **I want** to manage staff contracts, **so that** employment terms are clear and renewed on time.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record contract: start date, end date, salary, benefits, probation period
  - [ ] Alert 60 days before contract expiry
  - [ ] Process contract renewal with new terms
  - [ ] Confirm staff after probation period
  - [ ] Generate contract termination letter with reason
  - [ ] Calculate and process gratuity/severance on exit

### US-126: Staff Professional Development

**As a** School Admin, **I want** to track staff training and development, **so that** teachers maintain professional standards.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record training attended: workshop, seminar, conference, certification
  - [ ] Track TRCN continuing professional development (CPD) points
  - [ ] Alert when CPD points are below threshold
  - [ ] Generate professional development report
  - [ ] Link training to performance improvement

### Facilities & Operations

### US-127: Facility Maintenance Tracking

**As a** School Admin, **I want** to track facility maintenance requests, **so that** the school environment is safe and functional.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Log maintenance request: facility (classroom, lab, toilet, office), issue description, priority, reported by
  - [ ] Assign to maintenance staff or external vendor
  - [ ] Track status: open, in progress, completed, cancelled
  - [ ] Record cost of repair and completion date
  - [ ] Generate maintenance summary report

### US-128: Generator/Fuel Management

**As a** School Admin, **I want** to track generator usage and fuel consumption, **so that** I can manage power costs.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Log fuel purchase: date, quantity (litres), cost, supplier
  - [ ] Track generator running hours per day
  - [ ] Calculate fuel consumption rate (litres/hour)
  - [ ] Alert when fuel level is low
  - [ ] Schedule generator servicing
  - [ ] Generate fuel cost report per month

### US-129: Utility Management

**As a** Finance Officer, **I want** to track utility bills, **so that** I can budget for electricity, water, and internet.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record utility bills: electricity (PHCN/prepaid), water, internet, waste disposal
  - [ ] Track payment status: pending, paid, overdue
  - [ ] Alert when bill is due
  - [ ] Compare monthly utility costs
  - [ ] Generate utility expenditure report

### US-130: Procurement Management

**As a** School Admin, **I want** to manage procurement of goods and services, **so that** purchases are properly authorized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create purchase request: item, quantity, estimated cost, justification
  - [ ] Require approval based on cost threshold
  - [ ] Record vendor, purchase order, delivery date
  - [ ] Track delivery and quality inspection
  - [ ] Generate procurement report

### US-131: Vendor Management

**As a** School Admin, **I want** to maintain a vendor database, **so that** I can source goods and services efficiently.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Register vendor: name, contact, services/products, payment terms
  - [ ] Rate vendor performance: quality, timeliness, pricing
  - [ ] Track payment history per vendor
  - [ ] Flag vendors with poor performance
  - [ ] Generate vendor summary report

### US-132: Cleaning & Sanitation Schedule

**As a** School Admin, **I want** to manage cleaning and sanitation, **so that** the school environment is hygienic.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create cleaning schedule: area, frequency, responsible person
  - [ ] Track cleaning completion
  - [ ] Schedule fumigation/pest control
  - [ ] Record waste disposal
  - [ ] Generate sanitation compliance report

### US-133: Insurance Management

**As a** School Admin, **I want** to manage school insurance policies, **so that** the school is protected against risks.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record insurance policies: building, vehicle, liability, staff, student
  - [ ] Track premium, coverage, expiry date
  - [ ] Alert 30 days before policy renewal
  - [ ] Log insurance claims and settlement
  - [ ] Generate insurance summary report

### Student Welfare & Safety

### US-134: Student Counseling Records

**As a** Guidance Counselor, **I want** to record counseling sessions, **so that** I can track student wellbeing.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record session: student, date, counselor, issue type (academic, behavioral, emotional, social, family)
  - [ ] Add confidential notes and action plan
  - [ ] Schedule follow-up sessions
  - [ ] Track counseling progress over time
  - [ ] Generate counseling summary (anonymized for reports)

### US-135: Career Guidance

**As a** Guidance Counselor, **I want** to provide career guidance to SS students, **so that** they make informed subject and university choices.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record student's career interests and aptitude
  - [ ] Recommend subject combinations based on career goal
  - [ ] Track university course preferences
  - [ ] Generate career guidance report per student
  - [ ] Include in student's final year profile

### US-136: School Excursion/Trip Management

**As a** School Admin, **I want** to organize school trips, **so that** students have experiential learning opportunities.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create trip: destination, date, purpose, cost, participating classes
  - [ ] Collect parental consent (digital signature)
  - [ ] Track payment status per student
  - [ ] Generate trip manifest and emergency contact list
  - [ ] Post-trip: generate report with photos

### US-137: Prize-Giving/Speech Day Management

**As a** School Admin, **I want** to manage prize-giving ceremonies, **so that** student achievements are recognized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Define award categories: academic, sports, leadership, improvement, attendance
  - [ ] Auto-nominate eligible students based on criteria
  - [ ] Generate award list and certificates
  - [ ] Print invitation list for parents/guests
  - [ ] Generate event program

### US-138: Graduation Management

**As a** School Admin, **I want** to manage SS3 graduation, **so that** the ceremony is well-organized.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Identify graduating students (completed all requirements)
  - [ ] Generate graduation list
  - [ ] Calculate final GPA/class rank
  - [ ] Generate certificates and transcripts
  - [ ] Send graduation invitations to parents
  - [ ] Archive graduating student records

### US-139: Student Safety Incident Reporting

**As a** Teacher, **I want** to report safety incidents, **so that** the school can respond appropriately.

- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Record incident: type (accident, injury, bullying, fight, cultism, drug abuse, abduction attempt), location, time, students involved, witnesses
  - [ ] Severity level: minor, moderate, severe, critical
  - [ ] Auto-notify School Admin and parents
  - [ ] Track investigation and resolution
  - [ ] Generate incident report for authorities if required

### US-140: Emergency Evacuation Plan

**As a** School Admin, **I want** to manage emergency evacuation procedures, **so that** everyone is safe during crises.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Document evacuation routes per building
  - [ ] Assign assembly points
  - [ ] Record evacuation drill results
  - [ ] Track drill frequency (minimum once per term)
  - [ ] Generate evacuation readiness report

### US-141: Fire Safety Management

**As a** School Admin, **I want** to track fire safety equipment and procedures, **so that** the school is prepared for fire emergencies.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Inventory fire extinguishers: location, type, last service date, expiry
  - [ ] Alert when extinguisher needs servicing
  - [ ] Record fire drill results
  - [ ] Track fire safety training for staff
  - [ ] Generate fire safety compliance report

### US-142: Teenage Pregnancy Management

**As a** School Nurse, **I want** to manage cases of teenage pregnancy, **so that** the student receives proper support.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record pregnancy: student, date confirmed, expected due date
  - [ ] Confidential counseling referral
  - [ ] Track attendance during pregnancy
  - [ ] Arrange maternity leave from school
  - [ ] Plan for return to school after delivery
  - [ ] Strict confidentiality — access limited to nurse and counselor

### US-143: Drug Abuse Prevention

**As a** School Admin, **I want** to track and prevent drug abuse, **so that** students are protected.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record suspected drug abuse incident
  - [ ] Confidential counseling referral
  - [ ] Track intervention progress
  - [ ] Notify parents (with sensitivity)
  - [ ] Generate drug abuse prevention report (anonymized)
  - [ ] Coordinate with NDLEA if required

### US-144: Mental Health Monitoring

**As a** School Counselor, **I want** to monitor student mental health, **so that** at-risk students receive help.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Conduct mental health screening (PHQ-A, SDQ frameworks)
  - [ ] Flag students showing signs of depression, anxiety, self-harm
  - [ ] Refer to professional help when needed
  - [ ] Track intervention and progress
  - [ ] Generate mental health summary (anonymized for government)
  - [ ] Strict confidentiality controls

### US-145: Vulnerable Student Tracking

**As a** School Admin, **I want** to identify and support vulnerable students, **so that** no child is left behind.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Flag vulnerability: orphan, IDP, refugee, abuse victim, extreme poverty, disability
  - [ ] Assign support plan: scholarship, counseling, mentoring, material support
  - [ ] Track support delivery and outcomes
  - [ ] Generate vulnerable student report for NGOs/government
  - [ ] Strict confidentiality — access controlled

### US-146: Special Learning Needs (ADHD, Dyslexia, Autism)

**As a** Teacher, **I want** to know about students' special learning needs, **so that** I can adapt my teaching.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record diagnosis: ADHD, dyslexia, autism, cerebral palsy, Down syndrome
  - [ ] Document recommended accommodations
  - [ ] Share with relevant teachers (with parent consent)
  - [ ] Track academic progress with accommodations
  - [ ] Generate special needs education report

### US-147: Disease-Specific Health Tracking

**As a** School Nurse, **I want** to track disease-specific health data, **so that** I can manage endemic diseases.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Track: malaria, typhoid, cholera, meningitis, Lassa fever, tuberculosis, hepatitis
  - [ ] Record cases per term with symptoms and treatment
  - [ ] Generate disease prevalence report
  - [ ] Alert NCDC for notifiable diseases
  - [ ] Track vaccination coverage for preventable diseases

### US-148: Nutritional Status Monitoring

**As a** School Nurse, **I want** to monitor student nutritional status, **so that** I can identify malnutrition and obesity.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record height, weight, MUAC per screening
  - [ ] Auto-calculate BMI and nutritional status
  - [ ] Flag underweight, stunted, wasted, obese students
  - [ ] Refer to nutritionist or health facility
  - [ ] Generate nutritional status report for SUBEB

### Governance & Compliance

### US-149: School Proprietor/Board Dashboard

**As a** School Proprietor, **I want** a high-level dashboard, **so that** I can oversee school operations without daily involvement.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] View: total students, revenue, expenses, profit/loss, attendance rate, pass rate
  - [ ] Compare performance across terms/years
  - [ ] View pending issues requiring attention
  - [ ] Approve major expenditures above threshold
  - [ ] Download executive summary report

### US-150: SMC/SBG Reporting

**As a** School Admin, **I want** to generate reports for the School-Based Management Committee, **so that** governance requirements are met.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Generate SBMC report: enrolment, staffing, infrastructure, finances, challenges
  - [ ] Prepare SBMC meeting agenda and minutes
  - [ ] Track action items from previous meetings
  - [ ] Generate community engagement report
  - [ ] Export in SUBEB-required format

### US-151: School Accreditation Readiness

**As a** School Admin, **I want** to track accreditation requirements, **so that** the school maintains its license.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Checklist: teacher qualifications, student-teacher ratio, facilities, curriculum compliance, financial records
  - [ ] Track compliance status per requirement
  - [ ] Alert when requirement is at risk
  - [ ] Generate accreditation readiness report
  - [ ] Document inspection findings and corrective actions

### US-152: Fundraising & Donation Tracking

**As a** School Admin, **I want** to track fundraising and donations, **so that** I can account for all funds received.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record donation: donor, amount, purpose, date, receipt number
  - [ ] Track fundraising campaign progress
  - [ ] Allocate funds to specific projects
  - [ ] Generate donor acknowledgment letter
  - [ ] Generate fundraising report for auditors

### US-153: Building & Renovation Project Tracking

**As a** School Admin, **I want** to track construction and renovation projects, **so that** projects are completed on time and budget.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record project: type (new building, renovation, repair), budget, timeline, contractor
  - [ ] Track milestones and payments
  - [ ] Log progress photos and inspection notes
  - [ ] Alert when project is behind schedule
  - [ ] Generate project completion report

### US-154: Alumni Engagement

**As a** School Admin, **I want** to engage alumni, **so that** they support the school.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Maintain alumni database with contact information
  - [ ] Track alumni achievements and career progression
  - [ ] Send reunion invitations
  - [ ] Record alumni donations and projects funded
  - [ ] Generate alumni engagement report

### US-155: School Budget Management

**As a** Finance Officer, **I want** to create and track the school budget, **so that** spending is controlled.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Create annual budget by category: salaries, operations, maintenance, development
  - [ ] Track actual spending vs budget
  - [ ] Alert when spending exceeds budget line
  - [ ] Generate budget variance report
  - [ ] Forecast remaining budget for the year

### US-156: Bank Reconciliation

**As a** Finance Officer, **I want** to reconcile bank statements with school records, **so that** financial records are accurate.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Import bank statement (CSV/Excel)
  - [ ] Match transactions with school records
  - [ ] Flag unmatched transactions for investigation
  - [ ] Generate reconciliation report
  - [ ] Track outstanding items from previous periods

### US-157: Petty Cash Management

**As a** Finance Officer, **I want** to manage petty cash, **so that** small expenses are properly recorded.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record petty cash float amount
  - [ ] Log each expense: date, amount, purpose, requester, approver
  - [ ] Track remaining balance
  - [ ] Alert when float needs replenishment
  - [ ] Generate petty cash report

### US-158: Multi-School Management

**As a** Super Admin, **I want** to manage multiple schools from one dashboard, **so that** I can oversee a school chain.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] View all schools with key metrics side by side
  - [ ] Compare performance across schools
  - [ ] Transfer students and staff between schools
  - [ ] Generate group-wide reports
  - [ ] Set group-wide policies and configurations

### US-159: Parent Complaint Escalation

**As a** School Admin, **I want** to manage parent complaints through an escalation process, **so that** issues are resolved professionally.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Record complaint: parent, student, category (academic, discipline, fee, health, safety, staff behavior), description
  - [ ] Assign priority and responsible person
  - [ ] Track resolution status and timeline
  - [ ] Escalate to proprietor if unresolved after 7 days
  - [ ] Generate complaint resolution report

### US-160: Data Breach Response

**As a** Super Admin, **I want** to respond to data breaches, **so that** I comply with NDPA 2023 requirements.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Log breach: type, scope, affected records, discovery date
  - [ ] Assess severity and impact
  - [ ] Notify NDPC within 72 hours if required
  - [ ] Notify affected data subjects
  - [ ] Document remediation actions
  - [ ] Generate breach report for audit

### US-161: Inter-School Competition Management

**As a** Teacher, **I want** to manage inter-school competitions, **so that** students can participate in external events.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Register students for competitions: sports, debate, quiz, science, arts
  - [ ] Track competition schedule and results
  - [ ] Record student achievements and awards
  - [ ] Include achievements in student profile
  - [ ] Generate competition participation report

### US-162: Morning Assembly Management

**As a** School Admin, **I want** to manage morning assembly schedules, **so that** daily assembly runs smoothly.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Create weekly assembly schedule: day, leader, theme, prayers, announcements
  - [ ] Assign student roles: prayer leader, news reader, pledge leader
  - [ ] Track assembly attendance
  - [ ] Generate assembly attendance report
  - [ ] Include assembly participation in student profile

### US-163: Inter-House Sports Competition

**As a** Teacher, **I want** to manage inter-house sports, **so that** house competitions are organized.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Assign students to houses
  - [ ] Create sports events and schedule
  - [ ] Record results and points per house
  - [ ] Generate house standings
  - [ ] Award house cup to winning house

### US-164: School Calendar Management

**As a** School Admin, **I want** to manage the school calendar, **so that** everyone knows important dates.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Create academic calendar: term dates, holidays, exam periods, events
  - [ ] Sync with government calendar for exam dates
  - [ ] Share calendar with parents via WhatsApp/SMS
  - [ ] Alert users of upcoming events
  - [ ] Export calendar as PDF/ICS

### US-165: WhatsApp Group Management

**As a** School Admin, **I want** to manage WhatsApp groups for different audiences, **so that** communications are organized.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Create groups: all parents, per class, staff, PTA, management
  - [ ] Auto-add/remove members based on enrollment
  - [ ] Send broadcast messages to groups
  - **Track message delivery and read status**
  - [ ] Generate communication report

### US-166: Student ID Card Generation

**As a** School Admin, **I want** to generate student ID cards, **so that** students can be identified.

- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Auto-generate ID card with: photo, name, admission number, class, blood group, emergency contact
  - [ ] Include QR code linking to student profile
  - [ ] Print-ready format (CR80 standard)
  - [ ] Batch generate for entire class
  - [ ] Reprint for lost/damaged cards

### US-167: Staff ID Card Generation

**As a** School Admin, **I want** to generate staff ID cards, **so that** staff can be identified on campus.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Auto-generate ID card with: photo, name, staff ID, role, department
  - [ ] Include QR code for attendance scanning
  - [ ] Print-ready format (CR80 standard)
  - [ ] Reprint for lost/damaged cards
  - [ ] Deactivate card when staff leaves

### US-168: Security Guard Management

**As a** School Admin, **I want** to manage security guards, **so that** the school is properly guarded.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Record guard details: name, phone, shift, post location
  - [ ] Track guard attendance (check-in/check-out)
  - [ ] Log security incidents
  - [ ] Generate security duty roster
  - [ ] Generate security report

### US-169: Visitor Management

**As a** School Admin, **I want** to log visitors to the school, **so that** campus security is maintained.

- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Log visitor: name, phone, purpose, person visiting, time in
  - [ ] Issue visitor badge
  - [ ] Record time out
  - [ ] Flag unauthorized visitors
  - [ ] Generate visitor log report

### US-170: School Bus Route Optimization

**As a** School Admin, **I want** to optimize bus routes, **so that** transportation is efficient.

- **Priority:** P3
- **Acceptance Criteria:**
  - [ ] Map student home locations
  - [ ] Suggest optimal routes and stops
  - [ ] Calculate estimated travel time
  - [ ] Assign students to routes
  - [ ] Generate route map and schedule

---

## Final Complete Summary

| Module                  | Stories | P0     | P1     | P2     | P3    |
| ----------------------- | ------- | ------ | ------ | ------ | ----- |
| M1: Student Information | 13      | 5      | 4      | 4      | 0     |
| M2: Academic & Grading  | 13      | 5      | 5      | 3      | 0     |
| M3: Attendance          | 9       | 3      | 3      | 3      | 0     |
| M4: Fee & Finance       | 16      | 6      | 6      | 4      | 0     |
| M5: Health & Sentinel   | 15      | 4      | 6      | 4      | 1     |
| M6: Teacher & Staff     | 17      | 3      | 7      | 7      | 0     |
| M7: Parent Portal       | 15      | 7      | 5      | 3      | 0     |
| M8: Intelligence        | 13      | 5      | 4      | 4      | 0     |
| M9: System Admin        | 18      | 6      | 6      | 6      | 0     |
| Cross-Cutting           | 42      | 6      | 9      | 20     | 7     |
| **Total**               | **171** | **50** | **55** | **58** | **8** |
