

**PRODUCT REQUIREMENTS DOCUMENT**

**EduLafia**

*Integrated School Management & Adolescent Health Surveillance Platform*

by LafiyaCore Integrated Services Ltd  ·  RC 9347000

hello@lafiyacore.com  ·  www.lafiyacore.com

Document Version: 2.0  (Consolidated: EduLafia \+ LafiyaSentinel)

Prepared: March 2026  ·  Confidential — Internal Use & SEDC SEVCP Application

| Submitted in support of an application to the South East Venture Capital Program (SEVCP) — Incubation Track South East Development Commission (SEDC) · HealthTech Category |
| :---: |

# **1\. Document Control & Version History**

| Version | Date | Author | Description |
| :---- | :---- | :---- | :---- |
| 1.0 | Dec 2025 | Victoria Festus / LafiyaCore Team | Initial EduLafia concept document |
| 1.1 | Mar 2026 | LafiyaCore Team | LafiyaSentinel formalised as Exhibit B in Adamawa State MoU |
| 2.0 | Mar 2026 | LafiyaCore Product Team | EduLafia \+ LafiyaSentinel consolidated into unified PRD; beefed up for Nigeria 2026 context and SEDC SEVCP incubation application |

## **1.1 Intended Audience**

This document is intended for: LafiyaCore's founding team and technical lead; prospective investors and programme officers (including SEDC SEVCP review panel); grant-making partners (UNICEF, USAID, WHO AFRO, Gates Foundation); state government stakeholders (Ministries of Health and Education); and pilot school partners. It is not a software specification — it is a product requirements document that defines what EduLafia must do, for whom, and why.

## **1.2 Scope of This Document**

This PRD covers the full EduLafia platform version 2.0, which consolidates the original EduLafia school management concept and the LafiyaSentinel school-based disease surveillance system into a single, unified product. It defines all functional modules, all user actors, and all user stories. It also includes non-functional requirements, integration requirements, business model, and go-to-market strategy for South East Nigeria in 2026\.

# **2\. Executive Summary**

| EduLafia is Nigeria's most comprehensive school management and adolescent health surveillance platform. It combines five school management modules — student records, academics, attendance, finance, and health — with an embedded, automated disease surveillance engine (the LafiyaSentinel layer) that turns every enrolled school into a real-time public health early-warning node. It is offline-first, WhatsApp-native, NDPA-2023 compliant, and built for the operational realities of Nigerian schools, not Silicon Valley ones. |
| :---- |

Nigeria has over 13,000 public secondary schools and tens of thousands of private ones, serving more than 9 million students. Almost none of this system operates digitally. Paper registers, handwritten sick bay logs, manual fee books, and unofficial WhatsApp groups are the state of the art. The result is a generation of adolescents who are invisible in every data system that should be protecting them.

EduLafia changes this. It gives schools a platform they actually need and can afford — one that dramatically reduces administrative burden and impresses parents — while simultaneously generating the most valuable adolescent health dataset Nigeria has never had.

| Metric | Target (End 2026\) | Target (End 2027\) | Target (2028-2029) |
| :---- | :---- | :---- | :---- |
| Enrolled Schools | 30–50 (pilot) | 150–200 | 1,000+ |
| States Active | Enugu \+ Adamawa | 3–5 States | 10+ States |
| Students Covered | 15,000–25,000 | 75,000–100,000 | 500,000+ |
| Annual Recurring Revenue (₦) | ₦4.5M–₦9M | ₦22M–₦40M | ₦120M+ |
| Public Health Surveillance Nodes | 30–50 schools | 150+ schools | 1,000+ schools |

# **3\. Product Vision & Mission**

## **3.1 Vision Statement**

| A Nigeria where every secondary school student has a complete digital health and academic record from enrolment to graduation — and where no disease outbreak begins in a school without the health system knowing about it first. |
| :---- |

## **3.2 Mission Statement**

EduLafia exists to give Nigerian secondary schools the operational infrastructure they deserve and to give Nigeria's public health system the adolescent health surveillance capability it has never had — by making one product indispensable to schools and invaluable to governments.

## **3.3 Product Philosophy**

* Schools-first design: The school management features are not a Trojan horse — they are a genuinely great product that schools pay for and value on their own merits. The surveillance dimension is a consequence of good school data, not an imposition on schools.

* Offline-first, connectivity-second: EduLafia is designed for the school that has intermittent internet once a day, not the school with fibre broadband. Every feature must work offline.

* WhatsApp-native parent engagement: The majority of Nigerian parents communicate via WhatsApp. EduLafia meets them there — report cards, absence alerts, fee receipts, and health notifications are all WhatsApp-delivered.

* NDPA-2023 compliance by design: Data privacy is not a feature added later. Every data flow in EduLafia is designed with the Nigeria Data Protection Act 2023 as a first principle.

* Dignity and purpose: EduLafia serves a population — Nigeria's 9+ million secondary school students — who deserve the same quality of educational and health infrastructure as their counterparts in Accra, Nairobi, or Cape Town.

# **4\. Problem Statement**

## **4.1 The School Administration Crisis**

The average Nigerian secondary school headteacher manages hundreds of student records with no digital system. Fee collection is tracked in handwritten ledgers. Attendance registers are paper-based, often completed in arrears, and never analysed. Report cards are typed manually at the end of each term — a process that takes weeks. There is no audit trail for any financial transaction. Parents have no visibility into their child's school life between visiting the school in person.

## **4.2 The Adolescent Health Invisibility Problem**

Nigeria's adolescent population — roughly 11-to-18-year-olds in secondary school — is among the most data-invisible health populations in the country. The Demographic and Health Survey does not systematically cover this age group. Clinic and hospital data captures them only when they seek care — which they often do not. School health programmes have existed on paper since the National School Health Policy of 2006 but have almost no digital implementation anywhere in Nigeria.

The consequences are severe and well-documented:

* Sickle cell disease: Nigeria has the world's highest burden. Thousands of secondary school students have unmanaged sickle cell crises. Their absences are noted; their condition is not.

* Malnutrition: Adolescent malnutrition is significantly underreported because it is never screened for systematically in schools.

* Mental health: Depression, anxiety, and the effects of bullying among Nigerian secondary school students are almost entirely uncharted in the public health data.

* Disease outbreaks: By the time a cholera or typhoid cluster appears in health facility data, it has already moved through a school. The early signal was in the attendance register — but nobody was looking.

* Undiagnosed conditions: Poor vision, hypertension, and anaemia quietly undermine thousands of students' academic performance every term with no one connecting the dots.

## **4.3 The Data Gap for Government**

Nigeria's Federal Ministry of Health has no real-time adolescent health surveillance capability. The Federal Ministry of Education's EMIS (Education Management Information System) relies on annual paper returns from schools that are often incomplete, inaccurate, or submitted years late. State governments make decisions about school funding, teacher deployment, and health outreach with almost no reliable data.

| The EduLafia Thesis: If you give schools a product they genuinely need — one that saves time, impresses parents, and makes administration manageable — and if that product captures structured health and attendance data as a natural byproduct of daily school operations, you have built the most powerful adolescent health surveillance network Nigeria has ever had. Not by creating new work for schools. By making the work they already do count. |
| :---- |

# **5\. Strategic Context**

## **5.1 The LafiyaCore Product Ecosystem**

EduLafia is not a standalone product. It is the fourth pillar of LafiyaCore's integrated health technology platform, designed to create a data-connected thread across the Nigerian health and education continuum:

| Product | What It Does | Population Served | EduLafia Link |
| :---- | :---- | :---- | :---- |
| LafiyaFlow | Health commodity supply chain management — tracks ARVs, diagnostic kits, and medical supplies from warehouse to facility | Health facility staff, LGA/state programme managers, warehouse officers | Shared offline-first PWA infrastructure; shared HMIS reporting layer |
| MamaLafia | Maternal and child health companion — supports mothers through pregnancy and the first two years of the child's life | Pregnant women, nursing mothers, CHWs | MamaLafia's children become EduLafia's students at age 11 — longitudinal health thread from birth through secondary school |
| EduLafia | School management and adolescent health surveillance — the full platform described in this document | Secondary school students aged 11–18, teachers, school nurses, parents, government | Central node connecting education, adolescent health, and public health surveillance |
| MedConnect | Medical conference and event management — enables medical associations to run CME events and manage professional membership | Medical associations, doctors, conference organisers | Shared institutional client management architecture; shared role-based access control logic |

## **5.2 EduLafia \+ LafiyaSentinel: The Consolidation Rationale**

LafiyaSentinel was originally developed as a standalone school-based disease surveillance concept, formalised as Exhibit B in LafiyaCore's Memorandum of Understanding with the Adamawa State Ministry of Health (March 2026). In this PRD, LafiyaSentinel is fully integrated into EduLafia as the Sentinel Surveillance Engine — not a separate product, but the intelligence layer within EduLafia's health and attendance modules.

The rationale for consolidation is product and commercial clarity:

* One product, one subscription: Schools should not have to purchase a 'school management system' and a 'surveillance system' separately. The surveillance value is a consequence of the data they generate through normal school operations.

* One data model: Student, attendance, and health data flow through a single data model. Separating the products would have created unnecessary complexity and duplication.

* Stronger government proposition: When LafiyaCore approaches a Ministry of Health, it can offer both the school management infrastructure (at no extra cost to schools in partnership models) and the surveillance capability — as a unified, already-deployed system, not two separate tools to negotiate.

* The LafiyaSentinel brand is preserved: State government and partner communications continue to reference LafiyaSentinel as the surveillance capability within EduLafia. It remains a named, marketed capability with its own IP notice — just embedded in the platform rather than separate from it.

## **5.3 The South East Nigeria Strategic Focus (2026)**

EduLafia's 2026 pilot is anchored in South East Nigeria, specifically Enugu State, alongside LafiyaCore's existing Adamawa State base. This dual-state strategy is deliberate:

* Enugu as the South East anchor: Enugu is the administrative and commercial hub of the South East. It has a significant private secondary school market, active state government engagement with digital health and education, and a strong technology ecosystem (Enugu SME Center, Southeast innovation hubs). Enugu is where the SEDC SEVCP programme is centred.

* South East market size: The five South East states (Enugu, Anambra, Abia, Imo, Ebonyi) collectively have hundreds of private secondary schools and thousands of public ones — a very large addressable market with a growing middle class that invests in private secondary education.

* Political and economic alignment: The SEDC SEVCP and the Renewed Hope Agenda create an explicit policy environment that rewards HealthTech and EdTech solutions with South East focus — a strategic funding and visibility opportunity.

* Igbo language localisation: EduLafia's 2026 roadmap includes Igbo language support for the South East market, adding to its English and Hausa capability.

# **6\. Target Market & Addressable Opportunity**

## **6.1 Primary Market: Private Secondary Schools**

Private secondary schools are EduLafia's entry market and primary revenue source. They pay a subscription because EduLafia directly solves their most acute pain points: administrative burden, parent communication, fee collection, and compliance reporting. They are willing to pay because the value is immediate and visible.

| Segment | Estimated Number (Nigeria) | Price Point | Decision Maker |
| :---- | :---- | :---- | :---- |
| Budget private schools | \~25,000 | ₦60,000–₦90,000/year | Proprietor / Headteacher |
| Mid-tier private schools | \~8,000 | ₦90,000–₦150,000/year | Proprietor / School Board |
| Premium private schools | \~2,000 | ₦150,000–₦250,000/year | School Board / Governors |
| International-curriculum schools | \~500 | ₦250,000+/year (or USD pricing) | School Management / Board |

## **6.2 Scale Market: State Government Schools**

State government schools represent EduLafia's scale market — hundreds of schools in a single procurement contract, funded through SUBEB, State Ministry of Education budgets, or donor grants. The entry point is a pilot with state government endorsement, using the private school evidence base to de-risk the procurement decision.

## **6.3 Prestige Market: Federal Government Colleges**

Nigeria's 110 Federal Government Colleges (FGCs) are well-funded, politically visible, and nationally distributed. A federal tender for EduLafia across FGCs represents a landmark contract and a powerful proof point for regional and continental expansion. This is a Year 3–4 target.

## **6.4 Donor-Funded Deployment Market**

A substantial portion of EduLafia's scale in public schools will be donor-funded — deployed at no cost to schools with grant support from UNICEF, USAID, WHO, the Gates Foundation, or the World Bank. This is not charity; it is a legitimate revenue model where donors pay for deployment in underserved schools because EduLafia generates the population health data their programmes need.

# **7\. User Actors & Stakeholder Map**

EduLafia serves thirteen distinct actor types across three tiers: school-level actors, government and institutional actors, and platform actors. Each actor has a distinct role, set of permissions, and set of user stories.

| Actor | Tier | Primary Role on Platform | Module Access |
| :---- | :---- | :---- | :---- |
| School Administrator / Headteacher | School | Manages the full school; sees all dashboards; approves actions across modules | All modules (read \+ write \+ approve) |
| Class / Subject Teacher | School | Marks attendance; enters grades; views student profiles in their classes | Attendance, Academics, SIS (read), Health alerts (receive) |
| School Nurse / Health Officer | School | Manages health module: sick bay log, screenings, referrals, mental health, immunisation | Health module (full); SIS (read); Attendance (read) |
| Bursar / Finance Officer | School | Manages all financial transactions: fee collection, receipts, reporting, reconciliation | Finance module (full); SIS (read) |
| Student | School | Limited self-service portal: view own timetable, results, and announcements | Timetable, own academic results (read-only) |
| Parent / Guardian | School | Views child's academic, attendance, and health summary; makes payments; receives alerts | Guardian portal (read); Finance (payment); Notifications |
| LGA Education Officer | Government | Views LGA-level enrolment, attendance, and academic data for EMIS reporting | Aggregate LGA dashboards (read-only); EMIS export |
| LGA Health Officer | Government | Receives Sentinel surveillance alerts; views LGA illness signal map; initiates investigation | LGA health surveillance dashboard; alert feed; geospatial map |
| State Ministry of Education Official | Government | Views state-wide EMIS data; monitors education performance across all enrolled schools | State education dashboard (read-only); bulk export |
| State Ministry of Health Official / Epidemiologist | Government | Accesses state-level Sentinel surveillance data; manages outbreak response intelligence | State health surveillance dashboard; IDSR export; historical analysis |
| NPHCDA Representative | Government | Accesses immunisation coverage data by school, LGA, and state | Immunisation coverage dashboard (read-only); export for campaigns |
| LafiyaCore System Administrator | Platform | Provisions schools; monitors sync health; manages thresholds; deploys updates | Full system access across all schools; configuration panel; deployment tools |
| Donor / Researcher | Platform | Accesses anonymised, aggregated population health and education data via data portal | Anonymised data export portal (after MOU and ethics approval) |

| Role-Based Access Control (RBAC) Note: No actor can access data outside their defined scope. A teacher cannot see another class's data. A nurse cannot see financial records. A parent can only see their own child. A government official sees only anonymised aggregates unless specifically authorised. Every access event is logged in a tamper-resistant audit trail. |
| :---- |

# **8\. Product Architecture Overview**

## **8.1 Core Modules — Summary**

| Module | Module Name | Core Function | LafiyaSentinel Layer? |
| :---- | :---- | :---- | :---- |
| M1 | Student Information System (SIS) | Digital student profiles, guardian contacts, document storage, transfer management | No — foundation layer |
| M2 | Academic & Grading System | CA and exam score entry, WAEC/NECO-aligned grading, report cards, performance analytics | No — academic layer |
| M3 | Attendance & Absence Tracking | Daily attendance registers, pattern detection, EMIS export, parent alerts | YES — absence data feeds Sentinel Engine |
| M4 | Fee & Finance Management | Fee schedule, payment recording, receipts, reconciliation, financial reporting | No — financial layer |
| M5 | School Health & Sentinel Engine | Sick bay log, health profiles, screenings, referrals, mental health, immunisation, automated outbreak detection | YES — primary Sentinel module |
| M6 | Teacher & Staff Management | Staff profiles, timetabling, teacher attendance, communications | No — HR layer |
| M7 | Parent & Guardian Portal | Mobile-first parent access, payment, notifications, absence excusal, school communications | Partial — receives health and absence alerts |
| M8 | Intelligence & Analytics Dashboard | School, LGA, state, and national dashboards; KPI aggregation; EMIS/IDSR export | YES — surveillance analytics surface here |
| M9 | System Administration & Onboarding | School provisioning, user management, sync monitoring, threshold configuration, update deployment | YES — Sentinel thresholds configured here |

## **8.2 The LafiyaSentinel Surveillance Engine — How It Works**

The Sentinel Engine is not a separate module — it is an intelligence layer that runs across Modules 3 (Attendance), 5 (Health), and 8 (Intelligence). It operates as follows:

1. Data Collection: Teachers mark daily attendance (Module 3). When a student is absent, the teacher records a structured reason — sick, family, unknown — and optionally records reported symptoms from a standardised list (fever, vomiting, diarrhoea, cough, rash, headache, etc.). The school nurse logs sick bay visits with presenting complaints (Module 5). This data is structured, timestamped, and geographically tagged at the school level.

2. Pattern Analysis: The Sentinel Engine continuously analyses absence and illness data across enrolled schools. It looks for statistically significant clusters — unusual numbers of students with similar reported symptoms or conditions, from similar geographic areas (same school, same LGA, adjacent LGAs), within a defined rolling time window (configurable: 48, 72, or 96 hours). Baseline illness rates per season and per location are calculated from historical data to reduce false positives.

3. Alert Generation: When a pattern crosses a defined threshold, the engine generates a tiered alert: (a) School-level alert to the headteacher and school nurse — 'Unusual illness pattern detected among students. Consider investigating food, water, or environmental sources.'; (b) LGA-level alert to the LGA Health Officer — includes school name, symptom profile, number of students affected, and recommended investigation action; (c) State-level alert to the state epidemiologist if the cluster spans multiple schools or crosses a higher threshold — geographically mapped, prioritised for response.

4. Geospatial Mapping: All signals are mapped on the intelligence dashboard, allowing health officers to see where clusters are emerging in real time and correlate them with community health worker reports or facility-based case data from the same area.

5. Longitudinal Tracking: Historical signal data is retained, allowing retrospective analysis of disease seasonality, pattern correlation with confirmed outbreaks, and model accuracy review.

## **8.3 Technical Architecture Summary**

The following represents EduLafia's technical architecture approach, subject to detailed specification by the CTO during the architecture planning phase:

* Frontend: Progressive Web Application (PWA) — works on any modern browser, installable on Android (primary device in Nigerian schools), no app store required. Responsive design for tablet-first use in school offices and mobile-first use for teachers and parents.

* Offline-First Data Layer: IndexedDB (client-side) with a CouchDB/PouchDB sync protocol — all data writes locally first; syncs to the central server whenever connectivity is available. Conflict resolution logic handles concurrent edits. No data is lost due to network outages.

* Backend: Node.js / Python FastAPI REST API; PostgreSQL relational database for structured data; Redis for caching and session management. All hosted on Nigerian cloud infrastructure (AWS Lagos af-south-1 or equivalent) to meet NDPA data residency requirements.

* SMS/WhatsApp Integration: Termii gateway (shared with LafiyaFlow) for SMS delivery; WhatsApp Business API via a Nigerian-approved Business Solution Provider for WhatsApp message delivery.

* Payment Integration: Paystack and Flutterwave webhooks for online payment processing; Remita for government/public school contexts.

* Analytics: Apache Superset (open source) for dashboards; time-series data stored in a read-optimised analytics layer separate from transactional data.

* Security: AES-256 encryption at rest; TLS 1.3 in transit; RBAC with audit logging; Nigeria Data Protection Act 2023 (NDPA) compliant; data residency within Nigeria. Penetration testing before each major release.

* EMIS/DHIS2 Compatibility: Data exports formatted to Federal Ministry of Education EMIS standards and DHIS2 API where applicable for government integration.

# **9\. Functional Requirements — Module by Module**

  **MODULE 1: STUDENT INFORMATION SYSTEM**


### **9.1.1 Core Capabilities**

* Comprehensive digital student profile: full name, date of birth, gender, address, class, admission number, year of admission, stream/arm

* Guardian/parent information: up to two guardians; name, relationship, phone, WhatsApp number, email (optional), occupation

* Document storage: admission letter, birth certificate, transfer letter, medical records — scanned or photographed and attached to profile

* Academic history: class progression from admission; repeat years flagged; transfer records

* Student status management: active, inactive (graduated, withdrawn, transferred, deceased)

* Unique student ID generation: alphanumeric, school-prefixed, sequential

* NIN linkage: optional National Identification Number field; format-validated

* Biometric or student ID card support: QR-code card printable from student profile

* Batch import: CSV template for uploading a full class list in one operation; duplicate detection; validation report

* Transfer-out export: sealed student data package for transfer to receiving school

* Search: full-text search by name, ID, guardian phone; results within 2 seconds

### **9.1.2 Business Rules**

* A student cannot be enrolled without at least one active guardian contact (phone number required)

* A student ID is system-generated and cannot be manually edited after creation

* Deleting a student record is not permitted; only inactive flagging is available

* Guardian portal access is auto-provisioned when a student record is created and guardian WhatsApp number is provided

  **MODULE 2: ACADEMIC & GRADING SYSTEM**


### **9.2.1 Core Capabilities**

* Subject configuration: school sets subjects per class per term; aligned with WAEC/NECO subject lists for SS1–SS3

* CA score entry: classwork (10%), assignment (10%), mid-term (10%) — configurable by school to match their CA framework

* Exam score entry: end-of-term exam score entry per student per subject

* Grade computation: automatic application of configured grading scale (A1–F9 default; configurable); running total visible to teacher during entry

* Class rank computation: automatic ranking within class for each subject and overall

* Incomplete result flagging: 'ABS' or 'INC' flag for students who missed exams

* Performance alert: automated trigger when a student's average drops \>20% below prior term

* Report card generation: PDF per student, per term; includes all subjects, CA, exam, total, grade, rank, attendance summary, nurse remark, principal remark, school seal

* WhatsApp/SMS delivery of report card to guardian

* Historical transcript: full academic record from enrolment to current class; exportable PDF

* Class dashboard: subject mean scores, distribution, top/bottom 10% identification

* WAEC/NECO alignment: subject names and grading bands configurable to exactly match national exam formats for SS1–SS3

### **9.2.2 Business Rules**

* Teachers can only enter scores for subjects and classes they are assigned to

* Scores are locked for admin editing after a configurable period (default: 2 weeks after term end) to ensure auditability

* Report cards are generated only after all subject teachers have submitted their scores for the term

* Grade scale and CA weighting are locked once the term begins; changes require admin override with reason

  **MODULE 3: ATTENDANCE & ABSENCE TRACKING**


### **9.3.1 Core Capabilities**

* Daily attendance register: per-class, per-period (or per-day at form teacher level) attendance marking

* Absence reason capture: structured dropdown — Sick, Family Reason, Unknown, Excused (with guardian submission), Suspended; free-text notes optional

* Illness symptom capture (LafiyaSentinel input): when 'Sick' selected, optional symptom checklist — fever, cough, vomiting, diarrhoea, rash, headache, body ache, runny nose, conjunctivitis, other

* Edit window: 24-hour edit window; audit log for every change

* Attendance summary: weekly, termly, annual per student; class-level aggregate

* Pattern detection: absence every same weekday; correlation with sick bay visits; chronic absenteeism flag at \>20% term absence rate

* Parent alert: WhatsApp \+ SMS sent within 30 minutes of absence marking

* 3-day consecutive absence alert: to admin, class teacher, and parent

* EMIS export: termly attendance data in EMIS-compatible CSV; includes school code, class, gender split, termly rate

* Attendance-health correlation: flag when a student's absence pattern correlates with their sick bay visit history or recorded chronic condition

### **9.3.2 LafiyaSentinel Integration Points**

* Absence reason \= 'Sick' \+ symptom selection → data enters Sentinel Engine for pattern analysis

* Unusual same-day illness absence cluster at school level (configurable threshold, e.g. \>10% absent with illness reason) → Sentinel Engine evaluates against symptom profile and baseline

* Confirmed cluster → School alert \+ LGA Health Officer alert generated

  **MODULE 4: FEE & FINANCE MANAGEMENT**


### **9.4.1 Core Capabilities**

* Fee schedule: configurable fee categories (tuition, PTA, exam, uniform, lab, IT, sports, etc.) per class level; set annually

* Special categories: scholarship (full waiver), bursary (partial waiver), sponsored student — separately tracked and excluded from revenue distortion

* Cash payment recording: bursar selects student, records amount, payment method, date; receipt generated instantly

* Online payment: Paystack/Flutterwave integration; payment link generated per student; guardian pays from phone; webhook confirms payment; receipt auto-sent

* Remita integration: for government schools or schools that use government payment infrastructure

* Receipt formats: printable A5 slip; WhatsApp PDF; email PDF

* Outstanding balance: live ledger per student; bursar can see all students with balances at a glance

* Financial dashboard: termly revenue, outstanding, collection rate by class; comparable across terms and academic years

* Audit trail: every transaction timestamped, user-attributed, immutable; no delete, only reversal with reason

* Debt report: exportable list of all students with outstanding balances for end-of-term collection drives

* Revenue analytics: trend charts across terms; income breakdown by fee category

### **9.4.2 Business Rules**

* Financial records cannot be deleted; reversals create a new offsetting record with a mandatory reason

* Only users with the 'Bursar' role can record or reverse financial transactions

* School Administrator can view all financial records but cannot record transactions (separation of duties)

* The system enforces a maximum transaction amount to protect against data entry errors (configurable; default ₦500,000)

* All financial data is encrypted at rest; financial reports accessible only to Bursar and Administrator roles

  **MODULE 5: SCHOOL HEALTH & LAFIYASENTINEL ENGINE**


### **9.5.1 Student Health Profile**

* Blood group, genotype (sickle cell status: AA, AS, SS, SC), known chronic conditions, allergies, current medications, disability status

* Emergency health notes: important clinical information for emergency responders

* Vaccination record: per-vaccine, per-student; administered date, lot number (optional), administering facility; coverage dashboard

* Family health history: relevant hereditary conditions (optional; guardian-provided)

* Vision and hearing status: updated annually via screening module

### **9.5.2 Sick Bay Visit Log**

* Each visit record: date/time, presenting complaint (structured \+ free text), observations (temperature, BP if available), treatment given, outcome (returned to class / sent home / referred)

* Linked to student profile and attendance record for the same day

* Searchable by complaint type, date, student, and class

* Repeat-visitor flag: student who visits sick bay \>3 times per term for the same complaint is flagged for follow-up

### **9.5.3 Mass Screening Module**

* Annual or termly structured screening: BMI and nutritional status (height, weight, MUAC); vision (Snellen chart equivalent); hearing (basic assessment); blood pressure; dental (observation-based); sickle cell confirmatory test record

* Batch screening mode: nurse can screen an entire class in one session, entering data per student sequentially

* Abnormal result flags: system highlights values outside normal range for age/gender; flags for follow-up

* Screening coverage dashboard: which students/classes have been screened this academic year

### **9.5.4 Mental Health & Wellbeing Screening**

* Termly structured screening embedded in student check-in: culturally adapted, age-appropriate questions (Igbo/Hausa/English options) covering mood, social relationships, sleep, stress, and bullying exposure

* Based on adapted PHQ-A (Adolescent) and SDQ (Strengths and Difficulties Questionnaire) frameworks, reviewed by Nigerian child psychologists before deployment

* Confidentiality controls: results visible only to school nurse and designated counsellor; not visible to teacher or admin

* Flag-and-refer: flagged students auto-added to counsellor caseload; follow-up tracker

### **9.5.5 Referral Management**

* Structured referral: from nurse to external clinic/hospital; auto-generates referral letter with student health profile, presenting complaint, and nurse's clinical notes

* Follow-up tracker: referral status — pending, attended (outcome received), attended (no outcome received), overdue

* 48-hour auto-reminder to nurse and family if referral not confirmed

* Outcome recording: nurse records the clinical outcome when the student returns from the referred facility

### **9.5.6 LafiyaSentinel Outbreak Detection**

* Automated cluster detection: runs continuously across sick bay visits and attendance data

* Triggers: (a) ≥3 students with same complaint in same class within 48 hours; (b) ≥5 students with same complaint across the school within 72 hours; (c) Cross-school cluster: ≥2 schools in the same LGA with similar symptom profiles within 96 hours — all thresholds configurable by LafiyaCore admin

* Alert content: symptom profile, number of students affected, classes and school(s) involved, timeline, recommended action

* Alert recipients: tiered by severity — school nurse \+ admin (every trigger); LGA Health Officer (school-wide or multi-school); State Epidemiologist (multi-school or high-severity)

* Disease-specific detection logic: each communicable disease in the system's taxonomy (respiratory, gastrointestinal, vector-borne) has a specific symptom signature and threshold calibrated to its typical cluster characteristics

### **9.5.7 Population Health Dashboard**

* School level: top 5 presenting complaints this term; chronic condition prevalence (anonymised count); referral completion rate; vaccination coverage by antigen; mental health flag rate

* LGA level: illness signal heat map; same-period comparison across schools; alert history

* State level: full Sentinel surveillance dashboard; time-series charts; geographic cluster analysis; IDSR-formatted export

  **MODULE 6: TEACHER & STAFF MANAGEMENT**


### **9.6.1 Core Capabilities**

* Staff profile: full name, staff ID, qualifications, subjects qualified for, contact details, employment date, employment type (permanent, contract, NYSC)

* Class and subject assignment: teacher assigned to specific classes and subjects; drives access to attendance and grading modules

* Timetable builder: drag-and-drop timetable construction with clash detection (same teacher in two places; same class in two places)

* Timetable publication: published timetable visible to all staff and students in their portals; WhatsApp notification on publication or update

* Teacher attendance: daily teacher attendance register; configurable check-in method (manual, QR code)

* Staff broadcast: in-app \+ WhatsApp broadcast to all staff

  **MODULE 7: PARENT & GUARDIAN PORTAL**


### **9.7.1 Core Capabilities**

* Secure portal: accessible via unique URL sent by WhatsApp or SMS; no app download required; OTP authentication

* Child profile view: current class, photo (if uploaded), academic status, upcoming exams

* Academic results: current term CA scores, exam results, and class rank; prior term report card download

* Attendance summary: current term attendance rate; calendar view showing absent days and reasons; link to excusal submission

* Fee status: current balance, itemised payment history, payment link for outstanding balance

* Health summary: last sick bay visit (date and general reason — no detailed clinical data without nurse authorisation); referral status if applicable; vaccination status

* Notifications: all school alerts (absence, health, academic, fee) delivered via WhatsApp with link to portal for details

* Absence excusal submission: parent submits planned absence with reason; flows to teacher and admin for acknowledgement

* Correction request: parent can flag incorrect data (name spelling, contact number) for admin review

  **MODULE 8: INTELLIGENCE & ANALYTICS DASHBOARD**


### **9.8.1 School-Level Dashboard**

* Morning snapshot: attendance rate, health alerts, pending fees, academic alerts — in one screen, loading in under 5 seconds

* Term-end report: one-click generation of a full term report for school governance

* Health intelligence: top complaints, chronic condition prevalence, referral rate, screening coverage

### **9.8.2 LGA-Level Dashboard**

* Education: enrolment by school; attendance rates; academic performance comparison; EMIS export

* Health: illness signal map; alert history; outbreak investigation status; vaccination coverage

### **9.8.3 State-Level Dashboard**

* Education: EMIS-compatible aggregate; performance benchmarking by LGA and school

* Health: Sentinel surveillance overview; time-series disease trends; geospatial cluster analysis; IDSR-formatted export

### **9.8.4 Anonymised Data Portal (Donors & Researchers)**

* Self-service data request application: organisation, intended use, ethics approval reference, data set required, date range

* LafiyaCore review workflow: application reviewed within 5 business days; approved data delivered as encrypted CSV download

* Granularity controls: minimum population size requirement before any aggregate is exported (prevents re-identification)

  **MODULE 9: SYSTEM ADMINISTRATION & ONBOARDING**


### **9.9.1 School Provisioning**

* Provisioning wizard: school name, LGA, state, type (private/public/federal), contact details, logo upload, module bundle selection

* Default admin user created; welcome email/WhatsApp sent with login credentials and onboarding checklist

* Training resource library: built-in video tutorials (English, Igbo, Hausa) for each module; downloadable quick-reference guides

### **9.9.2 Platform Monitoring**

* Deployment health dashboard: sync status per school; last sync timestamp; data completeness score

* Alert: amber at 24 hours without sync; red at 48 hours; LafiyaCore support notified

* Usage analytics: module engagement per school; feature adoption rate; inactive school identification

### **9.9.3 Sentinel Engine Configuration**

* Threshold management: per-state and per-LGA configuration of outbreak alert thresholds by disease category

* Baseline calibration: historical absence and illness data used to set rolling baselines per school; prevents chronic absenteeism from inflating alert sensitivity

* Alert channel management: configure who receives which tier of alert; override for specific events

# **10\. User Stories**

User stories are organised by actor. Each story follows the format: As a \[actor\], I want to \[action\], so that \[outcome\]. Acceptance criteria are summarised inline. Stories are tagged with a module reference for traceability.

## **10.1 School Administrator / Headteacher**

### **Student Information System**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| SIS-001 | School Administrator | register a new student by entering their full profile including personal details, guardian contacts, class, and admission date | the student has a complete, permanent digital record from day one | Student record created; unique ID generated; guardian notified via WhatsApp/SMS |
| SIS-002 | School Administrator | upload scanned admission letters, birth certificates, and transfer documents directly to a student's profile | all official paperwork is permanently attached to the record and retrievable on demand | Document uploaded, indexed, and searchable; original file retained |
| SIS-003 | School Administrator | process a student transfer out by generating a sealed, exportable record package | the receiving school can import the student's complete history without data loss | Export package includes full academic, health, and attendance history in standard format |
| SIS-004 | School Administrator | batch-import a full class list from a CSV or spreadsheet at term start | the school does not have to enter hundreds of records manually | Import validates format, flags duplicates, creates all records in one operation |
| SIS-005 | School Administrator | search the student database by name, class, admission number, or guardian phone number | any record can be located in under 10 seconds | Search returns results in real time; partial name matching supported |
| SIS-006 | School Administrator | flag a student as inactive (graduated, withdrawn, deceased) without deleting their record | historical data is preserved while active rosters stay clean | Inactive flag applied; record hidden from active lists but fully searchable in archives |
| SIS-007 | School Administrator | link a student's NIN (National Identification Number) to their school record | the student's identity is verifiable against a national database in future | NIN field present; optional at entry; validated format enforced |

### **Academic & Grading**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| ACA-004 | School Administrator | generate a PDF report card for every student at end of term with one action | the school saves the weeks of manual typing that report cards currently require | PDF generated per student; includes results, attendance summary, nurse comment, principal's remark; school letterhead applied |
| ACA-005 | School Administrator | set up the grading scale and maximum scores per subject at the start of the academic year | the system correctly interprets all teacher entries throughout the year | Configurable grade bands and CA/exam weighting per school; locked once term begins |
| ACA-006 | School Administrator | view a class performance dashboard showing subject averages, top and bottom performers, and class rank | I can identify struggling students and underperforming subjects before the term ends | Dashboard shows subject mean scores and ranking; filterable by class and term |
| ACA-007 | School Administrator | receive an automated alert when a student's term average drops more than 20% below their prior-term performance | academic decline is caught early and a welfare check can be initiated | Alert sent in-app and via SMS to admin and class teacher when threshold breached |
| ACA-008 | School Administrator | generate a full academic transcript for any student from JS1 to their current class | a single document can be issued for scholarship applications, transfers, and records | Transcript PDF includes all terms on record; watermarked with school seal and EduLafia authentication code |

### **Attendance**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| ATT-004 | School Administrator | view a real-time dashboard of today's attendance across all classes by 8:30 AM | I know immediately if an entire class or unusual number of students are absent | Dashboard shows attendance % per class; highlights classes below 85% in amber; below 70% in red |
| ATT-005 | School Administrator | receive an alert when a student has been absent for three or more consecutive days | the school can proactively contact the family and check on the student's welfare | Alert generated after day 3; sent to admin and class teacher; parent also notified via SMS/WhatsApp |
| ATT-006 | School Administrator | generate EMIS-compliant attendance returns for the term with a single export action | statutory reporting obligations are met without manual data compilation | Export produces CSV in EMIS format; includes school ID, class, gender breakdown, and termly rates |

### **Finance**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| FIN-006 | School Administrator | view a termly revenue summary showing total collected, total outstanding, and collection rate by class | the school's financial health is always visible and annual planning is evidence-based | Financial dashboard shows term-to-date income, outstanding, and % collected; comparable across terms |
| FIN-007 | School Administrator | run an audit trail report showing every financial transaction, who recorded it, and when | any disputed payment or potential fraud can be investigated with a complete record | Immutable log of all transactions; every entry user-attributed and timestamped; no deletions permitted |

### **Health & Sentinel**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| HLT-009 | School Administrator | view a school-level health intelligence dashboard showing the top presenting complaints, chronic condition prevalence, referral rates, and immunisation coverage | health management is as visible and actionable as academic performance | Dashboard updated in real time; data from sick bay log, screening, and referral modules aggregated |
| HLT-010 | School Administrator | receive an automated alert when the system detects that absence patterns among students are statistically consistent with a communicable disease cluster | the school can act before an outbreak becomes a public health crisis | Alert generated by Sentinel Engine when absence \+ symptom data exceeds threshold; includes LGA health officer notification |

### **Staff, Intelligence & Other**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| STF-001 | School Administrator | create and manage digital staff profiles for all teachers and non-teaching staff including qualifications, subjects assigned, and contact details | HR and timetabling functions have a reliable staff data foundation | Staff profile created; linked to subject and class assignments; role-based access controlled from profile |
| STF-002 | School Administrator | build and publish the school timetable by assigning teachers to subjects, classes, and periods | all teachers and students see a consistent, published timetable from the start of term | Timetable builder with clash detection; published view accessible to teachers and visible to students in their portal |
| STF-003 | School Administrator | track teacher attendance and generate monthly summaries of teacher presence and absences | accountability for teacher attendance is as rigorous as for student attendance | Teacher attendance register; monthly summary generated; pattern alerts for chronic absenteeism |
| STF-005 | School Administrator | send a school-wide announcement to all staff via in-app message and WhatsApp broadcast | important communications reach every staff member without relying on phone trees or notice boards | Broadcast function sends to all active staff profiles; delivery confirmed; recipients can acknowledge |
| INT-001 | School Administrator | see a single-screen management dashboard every morning showing today's attendance, pending health alerts, fee collection status, and any system-generated flags | I can manage the school proactively with full situational awareness before the first class bell rings | Dashboard loads in under 5 seconds; shows attendance, health, finance, and academic KPIs; alert feed prioritised by urgency |
| INT-002 | School Administrator | generate a single-click end-of-term report covering all five operational modules for submission to the proprietor or school board | reporting to governance structures is automated and consistent, not a manual exercise | Report generated as PDF with school branding; covers academic, attendance, financial, and health performance for the term |
| SYS-004 | School Administrator | create user accounts for all teachers, nurses, and bursars and assign them role-appropriate access levels | every staff member can access exactly what their role requires and nothing more | Role-based access control with pre-defined role templates; admin cannot escalate own privileges; audit log of all access changes |
| SYS-005 | School Administrator | export all school data in a standard open format (CSV/JSON) at any time | the school is never locked into the platform and retains ownership of its own records | Full data export available to school admin at any time; export includes all modules; format documented and importable into standard tools |

## **10.2 Class / Subject Teacher**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| SIS-008 | Teacher | view a read-only profile of any student in my class | I have immediate access to their emergency contacts, chronic conditions, and class history | Teacher role sees all personal and health fields; cannot edit non-academic fields |
| ACA-001 | Teacher | enter continuous assessment scores (classwork, assignment, mid-term) for each student in my subject | scores accumulate automatically into the final CA total without manual arithmetic | CA scores entered per student; running total updated in real time; max scores enforced |
| ACA-002 | Teacher | enter end-of-term exam scores per student and have the system compute the combined result | I do not have to manually calculate grades or risk arithmetic errors | System applies WAEC/NECO grading formula; grade and position computed automatically |
| ACA-003 | Teacher | flag a student's result as 'incomplete' if they missed the exam due to a documented absence | the system distinguishes genuine scores of zero from missed examinations | Incomplete flag applied; report card shows 'ABS' not '0'; admin alerted for follow-up |
| ATT-001 | Teacher | mark attendance for my class each morning on my phone or tablet with a single tap per student | the daily register is completed digitally in under three minutes without paper | Attendance recorded per student per period; timestamped; offline-capable |
| ATT-002 | Teacher | mark a student absent and select a reason (sick, family, unknown) from a structured dropdown | absence data is structured and usable for surveillance rather than just a tally | Reason captured at point of marking; reason codes align with LafiyaSentinel surveillance taxonomy |
| ATT-003 | Teacher | update attendance records for up to 24 hours after the school day in case of an entry error | honest corrections are possible without enabling backdating of records | 24-hour edit window; edits logged with reason; no edit possible after 24 hours without admin override |
| STF-004 | Teacher | view my full teaching timetable, assigned classes, and subject list from my EduLafia dashboard | I have all the information I need to plan my lessons and locate my attendance registers | Teacher dashboard shows timetable, assigned classes, pending assessments, and recent health alerts for my students |

## **10.3 School Nurse / Health Officer**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| HLT-001 | School Nurse | access a complete digital health profile for any student before a sick bay consultation | I know their blood group, known conditions, allergies, and medications before I begin | Health profile visible to nurse role; includes all fields set during enrolment and updated over time |
| HLT-002 | School Nurse | log every sick bay visit with presenting complaint, observations, treatment given, and outcome (sent to class / referred / sent home) | there is a complete clinical record of every health event involving every student | Sick bay log created per visit; linked to student profile; timestamped; searchable by date and complaint |
| HLT-003 | School Nurse | initiate a referral from EduLafia to a clinic or hospital, with the referral letter generated automatically from the student's health record | referrals are complete, professional, and contain the clinical information the receiving facility needs | Referral letter PDF generated with student history, presenting complaint, and school contact; sent to nurse and family |
| HLT-004 | School Nurse | track the status of every open referral (pending, attended, outcome received) | no student falls through the cracks between the school referral and the clinical visit | Referral tracker shows open, closed, and overdue referrals; auto-reminder sent at 48 hours if no update |
| HLT-005 | School Nurse | conduct and record a structured annual health screening for each student (BMI, vision, hearing, BP, dental, sickle cell) | every student has a documented health baseline that is reviewed and updated yearly | Screening form built into system; results stored per student; flags raised for abnormal values |
| HLT-006 | School Nurse | receive an automated alert when three or more students present to the sick bay with similar symptoms within 48 hours | a potential outbreak is surfaced immediately before it spreads further within the school | Alert generated when threshold met; includes symptoms, students affected, classes; sent to nurse and admin |
| HLT-007 | School Nurse | record each student's immunisation status and update it when new vaccines are administered | vaccine coverage gaps are visible and the school can participate in NPHCDA immunisation campaigns | Vaccine registry per student; coverage dashboard for nurse and admin; NPHCDA-linked campaign tracking |
| HLT-008 | School Nurse | conduct a termly mental health screening using age-appropriate, culturally adapted questions and flag students who need counsellor follow-up | students experiencing anxiety, depression, or bullying are identified before their academic performance collapses | Screening tool embedded; PHQ-A adapted questions; flagged students added to counsellor caseload with confidentiality controls |

## **10.4 Bursar / Finance Officer**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| FIN-001 | Bursar | set up the school's full fee schedule (tuition, PTA, exam, uniform) at the start of each academic year | the system automatically knows what each student owes based on their class and status | Fee schedule configured per class level; special categories (scholarship, bursary) defined with zero or partial amounts |
| FIN-002 | Bursar | record a cash fee payment from a parent and print or send a receipt in under 60 seconds | the bursary queue moves quickly and every payment is immediately documented | Receipt generated with school logo, date, amount, balance; printable and SMS/WhatsApp deliverable |
| FIN-003 | Bursar | record online payments made via Paystack or Flutterwave automatically without manual entry | digital payments are reconciled instantly without waiting for end-of-day bank statements | Payment gateway webhook integration; payments posted to student ledger within 5 minutes of confirmation |
| FIN-004 | Bursar | view a live list of all students with outstanding balances, filterable by class and amount owed | the school can follow up on arrears before end-of-term registration | Debtor report shows student name, class, amount owed, last payment date; sortable; exportable |
| FIN-005 | Bursar | record a full or partial fee waiver for a scholarship student without distorting the school's income report | bursary records are accurate and donor-funded waivers are separately accounted | Waiver recorded with reason and authorising officer; excluded from revenue in financial statements |

## **10.5 Parent / Guardian**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| SIS-009 | Parent / Guardian | view my child's digital profile, including personal data currently on record | I can verify accuracy and request corrections if needed | Guardian portal shows profile; correction request button sends notification to admin |
| ACA-009 | Parent / Guardian | receive my child's report card via WhatsApp at end of term without coming to school | I am informed of academic performance regardless of my distance or work schedule | Report card PDF sent via WhatsApp API; delivery confirmed; option to download from portal |
| ATT-007 | Parent / Guardian | receive a WhatsApp or SMS message each time my child is marked absent | I am immediately aware and can contact the school or explain the absence | Message sent within 30 minutes of absence marking; includes child name, class, date; reply link included |
| FIN-008 | Parent / Guardian | pay my child's school fees online via a secure payment link sent to my phone | I do not have to take time off work to come to the school bursary | Paystack/Flutterwave payment link generated and sent via WhatsApp; receipt auto-sent upon payment |
| FIN-009 | Parent / Guardian | check my child's current fee balance and payment history at any time from the parent portal | I always know what is outstanding before collection exercises at school | Balance and itemised payment history visible in guardian portal; updated in real time |
| HLT-017 | Parent / Guardian | receive a notification when my child visits the sick bay, including the reason for the visit and what action was taken | I am always informed of health events at school and can follow up with care at home | WhatsApp notification sent on sick bay visit completion; includes complaint, treatment, and whether referral was issued |
| PAR-001 | Parent / Guardian | access a secure portal on my phone via a unique login link (no app download required) to view my child's academic, attendance, and health summary | I can stay informed about my child's progress and wellbeing without visiting the school | Portal accessible via WhatsApp link or SMS URL; works on all browsers; no app download required; secured with OTP |
| PAR-002 | Parent / Guardian | receive an automated end-of-term summary of my child's academic performance, attendance rate, and health visits | I have a holistic picture of my child's school year in a single, readable message | Summary generated at end of each term; delivered via WhatsApp; includes trends vs. prior term; PDF attachment included |
| PAR-003 | Parent / Guardian | submit a formal notification of my child's upcoming planned absence (e.g., family travel, illness) through the portal | the school has advance notice and the absence is pre-categorised correctly | Absence notification submitted via portal; pushed to class teacher and admin; absence auto-categorised as 'excused' |
| PAR-004 | Parent / Guardian | view and respond to requests from the school nurse or admin regarding follow-up care or documentation | school health and administrative processes are completed without requiring my physical presence | Notification and response thread visible in portal; school can mark request as resolved once parent responds |

## **10.6 LGA Education Officer**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| SIS-010 | LGA Education Officer | see aggregate enrolment statistics by gender, class, and age band for all schools in my LGA | I can meet EMIS reporting obligations without manual data collection | Dashboard shows live enrolment counts; exportable in EMIS-compatible CSV format |
| ACA-010 | LGA Education Officer | compare subject-level pass rates across all schools in the LGA | I can identify schools that need targeted intervention or teacher redeployment | Comparative dashboard by subject, class level, and school; exportable for reporting |
| ATT-009 | LGA Education Officer | view termly attendance rates per school and identify schools with chronic absenteeism problems | I can direct pastoral support or investigate systemic issues at the school level | Attendance analytics by school, class, gender; downloadable for LGEA submission |

## **10.7 LGA Health Officer**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| ATT-008 | LGA Health Officer | receive an automated alert when absence rates at a school in my LGA exceed 15% on a given day | I am prompted to investigate whether a disease cluster may explain the pattern | Alert generated when daily absence rate breaches threshold; includes school name, class, reported symptoms |
| HLT-011 | LGA Health Officer | receive real-time alerts when school-based absence and illness patterns in my LGA cross surveillance thresholds | I can dispatch a community health team to investigate before the outbreak is confirmed in facility data | Alert sent in-app, SMS, and email; includes school name, location, number affected, symptom profile, and recommended action |
| HLT-012 | LGA Health Officer | view a geographically mapped display of active illness signals across all schools in my LGA | I can correlate school-based signals with community health worker and facility reports for triangulation | Map view with colour-coded school pins (green/amber/red) based on illness signal intensity; clickable for detail |

## **10.8 State Ministry of Education Official**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| ACA-011 | State MOE Official | see statewide academic performance benchmarks aggregated across all EduLafia-enrolled schools | evidence-based education policy decisions are possible without conducting separate surveys | State-level analytics dashboard; anonymised at school level unless authorised; updated termly |
| INT-003 | State MOE Official | view a state-level EMIS dashboard with enrolment, attendance, and academic performance data from all EduLafia-enrolled schools in real time | state EMIS returns can be generated automatically, eliminating annual paper data collection exercises | State dashboard live; EMIS-formatted export available; updated at least weekly from enrolled schools |

## **10.9 State Ministry of Health Official / Epidemiologist**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| ATT-010 | State Epidemiologist | access absence rate trends across all enrolled schools over the past 12 months | seasonal disease patterns and year-on-year comparisons are visible in one view | Time-series chart available in state health dashboard; filterable by LGA, school, symptom category |
| HLT-013 | State Epidemiologist | access a state-level surveillance dashboard showing illness signal trends, geographic clusters, and seasonal disease patterns across all enrolled schools | early warning intelligence from school populations supplements formal IDSR reporting | Dashboard with time-series charts, heat map, outbreak timeline; data exportable for IDSR submission |
| HLT-014 | State Epidemiologist | run retrospective analyses of disease signals against known outbreak events to validate the surveillance model's sensitivity | confidence in the Sentinel Engine's early warning accuracy is evidence-based | Historical data archive accessible; comparison tools for signal vs. confirmed outbreak timelines |
| HLT-015 | State MOH Official | generate an annual school health surveillance report suitable for inclusion in epidemic preparedness documentation and IDSR reporting obligations | LafiyaSentinel data contributes formally to national disease surveillance infrastructure | Annual report generated automatically; includes outbreak signals, response actions, and coverage statistics; formatted for IDSR |

## **10.10 NPHCDA Representative**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| HLT-016 | NPHCDA Representative | view immunisation coverage rates by school, LGA, and state for adolescent vaccine-preventable diseases | outreach campaigns can be targeted at schools and areas with the lowest coverage | Coverage dashboard by geography and vaccine type; gap analysis available; exportable for programme planning |

## **10.11 LafiyaCore System Administrator**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| SYS-001 | LafiyaCore Admin | provision a new school on the platform by configuring their profile, user accounts, and module access in under 30 minutes | school onboarding is fast, repeatable, and does not require engineering involvement | School provisioning wizard creates school record, default admin user, and activates selected module bundle in one flow |
| SYS-002 | LafiyaCore Admin | monitor the sync health of all offline-capable school deployments and receive alerts when a school has not synced in more than 48 hours | data gaps are identified and resolved before they become irrecoverable | Sync health dashboard shows last sync time per school; amber alert at 24 hours; red alert at 48 hours; LafiyaCore support notified |
| SYS-003 | LafiyaCore Admin | push platform updates to all enrolled schools with zero downtime during school hours | product improvements are deployed safely without disrupting school operations | Update staged during off-hours (before 7 AM or after 6 PM); rollback capability available within 1 hour of deployment |
| SYS-006 | LafiyaCore Admin | configure LafiyaSentinel surveillance thresholds per state and LGA based on baseline illness rates | alert sensitivity is calibrated to local epidemiological context rather than a single national default | Threshold configuration panel allows setting of alert triggers by symptom category, time window, and geographic level |

## **10.12 Donor / Researcher**

| Story ID | As a... | I want to... | So that... | Acceptance Criteria (Summary) |
| :---- | :---- | :---- | :---- | :---- |
| INT-005 | Donor / Researcher | access a data request portal to apply for access to anonymised datasets for research purposes | evidence generation about adolescent health and education in Nigeria is supported by a structured, ethical process | Data request form with intended use, ethics approval reference, and organisation details; reviewed by LafiyaCore; access controlled by dataset and date range |
| HLT-018 | Donor / Researcher | access anonymised, aggregated population health data reports for enrolled schools covering nutritional status, chronic condition prevalence, and mental health indicators | research and programme evaluation are grounded in real adolescent health data from Nigeria | Data portal with anonymised exports; access requires MOU and ethics approval workflow; individual data never exposed |

# **11\. Non-Functional Requirements**

## **11.1 Performance**

| Metric | Requirement |
| :---- | :---- |
| Page load time (connected) | Under 3 seconds for any dashboard view on a 3G connection |
| Page load time (offline) | Under 1 second for any cached page — all core screens must be available offline |
| Attendance marking | A teacher must be able to mark a class of 45 students' attendance in under 5 minutes |
| Report card generation | A full class of 45 report cards must generate in under 60 seconds |
| Sync time | Full daily sync of a school's data (when connectivity resumes) in under 10 minutes for a 500-student school |
| Database response | 95th percentile query response time under 200ms for school-level queries |
| Alert delivery | Sentinel outbreak alert delivered to LGA Health Officer within 15 minutes of threshold crossing |
| WhatsApp delivery | Absence notifications delivered within 30 minutes of absence marking; receipt delivery within 2 minutes of payment |

## **11.2 Offline-First Architecture Requirements**

* Every core function — attendance marking, grade entry, sick bay logging, fee recording — must be operable with zero internet connectivity

* Data written offline must queue locally and sync automatically when connectivity is restored

* Sync must be incremental (only unsynchronised records), not full data re-download

* Conflict resolution: last-write-wins for non-critical fields; admin notification for high-stakes conflicts (financial records, health records)

* Offline mode must be invisible to the user — no degraded interface or warning screens required for normal operation

## **11.3 Security & Data Governance**

* Encryption at rest: AES-256 for all stored data; applies to both server-side storage and local device storage

* Encryption in transit: TLS 1.3 minimum for all API communications

* Authentication: OTP-based authentication for first login and guardian portal; username \+ password for staff; session timeout after 30 minutes of inactivity

* Role-Based Access Control (RBAC): pre-defined role templates; principle of least privilege; no user can escalate their own privileges

* Audit logging: every data create, update, delete, and access event logged with user ID, timestamp, and IP address; logs are immutable and retained for minimum 7 years

* Data residency: all data stored within Nigeria (AWS Lagos af-south-1 or equivalent Nigerian-certified cloud); no cross-border data transfer without Ministry approval

* NDPA 2023 compliance: data processing registrations; consent management; data subject rights (access, correction, deletion); data breach notification within 72 hours

* NITDA compliance: platform registered with NITDA; data protection officer designated

## **11.4 Accessibility & Device Support**

* Device support: Android smartphones (primary); feature phone web browsers (basic view); tablets (optimised); desktop browsers (admin dashboards)

* Android version: Android 8.0 (Oreo) and above — covers the vast majority of Nigerian school devices

* Browser support: Chrome 80+, Firefox 75+, Samsung Internet 12+

* Screen reader compatibility: WCAG 2.1 AA compliance for core admin interfaces

* Low-bandwidth mode: automatic image compression and text-only fallback on connections below 2G

## **11.5 Localisation**

* Language support: English (default); Igbo (South East deployment — 2026); Hausa (North Nigeria deployment — 2027); additional languages per state contract

* Number formatting: Nigerian number conventions (₦ currency; DDMMYYYY date format)

* Calendar system: Gregorian calendar with Nigerian public holiday awareness (affects attendance flags)

* Phone number format: Nigerian mobile number validation (+234 prefix and local format)

# **12\. Integration Requirements**

| Integration | Purpose | Direction | Priority |
| :---- | :---- | :---- | :---- |
| Termii (SMS gateway) | SMS delivery of absence alerts, fee receipts, OTP authentication, and general school notifications | EduLafia → Termii → Parent/Staff | Critical — P1 |
| WhatsApp Business API (via approved BSP) | WhatsApp delivery of absence alerts, report cards, fee receipts, health notifications — primary parent communication channel | EduLafia → WhatsApp API → Parent/Staff | Critical — P1 |
| Paystack | Online fee payment processing for private schools; webhook for payment confirmation and ledger update | Parent → Paystack → EduLafia webhook | High — P1 |
| Flutterwave | Alternative online payment gateway; same function as Paystack; provides redundancy | Parent → Flutterwave → EduLafia webhook | High — P2 |
| Remita | Payment gateway for government schools and public sector deployments where Remita is the mandated channel | Parent/SUBEB → Remita → EduLafia | Medium — P2 |
| Federal Ministry of Education EMIS | Export attendance, enrolment, and academic data in EMIS-compatible format for annual state returns | EduLafia → EMIS CSV export | High — P1 |
| DHIS2 (Nigeria NHMIS) | Export school health and Sentinel surveillance data in DHIS2 format for integration with the National Health Management Information System | EduLafia → DHIS2 API (school health module) | Medium — P2 |
| NPHCDA Immunisation Registry | Bidirectional link to NPHCDA's school immunisation campaign data; EduLafia reports coverage; NPHCDA pushes campaign schedules | Bidirectional API (phase 2\) | Medium — P3 |
| WAEC/NECO Result APIs | Import external exam results when available to complete student academic records at SS3 level | WAEC/NECO API → EduLafia (read-only) | Low — P3 |
| OpenHIE Framework | Align EduLafia's health data standards with the OpenHIE health information exchange framework for interoperability with national health systems | Standards alignment; not a live integration initially | Medium — P3 |

# **13\. Business Model & Revenue Architecture**

## **13.1 Revenue Streams**

| Revenue Stream | Payer | Price Range | Target Timeline | Annual Revenue Potential |
| :---- | :---- | :---- | :---- | :---- |
| School SaaS Subscription (Private) | Private secondary schools | ₦60,000–₦250,000/year (tiered by school size and module bundle) | 2026 Q3 — pilot; 2027 scale | ₦120M+ at 500 schools |
| State Government Licensing | State MOE / SUBEB | ₦30,000–₦80,000/school/year at bulk rate | 2027–2028 first state contract | ₦480M+ at one state (1,000 public schools) |
| Parent Portal Premium | Parents of enrolled students | ₦500–₦1,500/term per family for enhanced notifications and portal features | 2026 Q4 alongside school pilots | ₦10M+ at 10,000 families |
| Federal Government College Tender | FMOE — FGCs | National tender rate (negotiated); 110 FGCs | 2028–2029 | ₦200M+ contract value |
| Donor-Funded Public School Deployment | UNICEF, USAID, Gates Foundation, World Bank | Full grant coverage for underserved public school rollout; grant size $50,000–$500,000 per programme | 2027 pilot with first donor partner | $100,000–$500,000 per grant cycle |
| Health Data Intelligence Reports | State MOH, FMOH, academic researchers | ₦500,000–₦2,000,000 per annual report; per-dataset pricing for researchers | 2028 once data volume is sufficient | ₦50M+ per year at scale |
| Training & Onboarding Services | All school types; state agencies | ₦50,000–₦200,000 per school for onboarding engagement; train-the-trainer for state deployments | 2026 Q3 bundled with pilots | ₦3M–₦10M per year initially |

## **13.2 Pricing Philosophy**

EduLafia is priced to be within reach of the private schools that generate its initial revenue, while being compelling enough that schools prefer to pay for EduLafia over building manual workarounds. The pricing tiers are designed to accommodate the wide range of private school sizes and budgets in Nigeria:

* Starter (up to 200 students): ₦60,000/year — all 5 core modules; basic health module; WhatsApp notifications

* Standard (201–500 students): ₦120,000/year — all 9 modules including full Sentinel Engine; parent portal; Paystack integration

* Premium (501+ students): ₦200,000–₦250,000/year — all modules; custom branding; priority support; EMIS export; data intelligence dashboard

* Government/Public School: Negotiated bulk rate; funded through SUBEB, State MOE, or donor grant; minimum ₦30,000/school/year at scale

# **14\. Go-to-Market Strategy: South East Nigeria 2026**

## **14.1 Why South East Nigeria First**

* Enugu State is EduLafia's primary 2026 pilot state. It combines a significant private school market, active government digital health and education engagement, an established technology ecosystem (Enugu SME Center), and the SEDC SEVCP political and funding tailwinds.

* LafiyaCore already has a presence in Adamawa State (North East) through the MoU with the Adamawa State Ministry of Health. The South East expansion diversifies the geographic base and positions EduLafia for the national scale it needs.

* South East Nigeria has high secondary school enrolment driven by strong cultural emphasis on education, a large Igbo diaspora that remits money specifically for school fees, and a growing middle class that invests in private secondary schooling.

* The five South East states (Enugu, Anambra, Abia, Imo, Ebonyi) collectively represent thousands of private secondary schools — a very large immediate addressable market.

## **14.2 2026 Pilot Plan**

| Phase | Timeline | Actions | Success Metrics |
| :---- | :---- | :---- | :---- |
| Discovery | Q2 2026 (Apr–Jun) | Conduct 15–20 structured interviews with headteachers, bursars, and school nurses at private secondary schools in Enugu and Adamawa. Map pain points by module. Identify 5–8 willing pilot schools. | Discovery interviews completed; pilot schools confirmed; primary pain points validated |
| Build & Configure | Q2–Q3 2026 (Jun–Aug) | Complete MVP of Modules 1–5 (SIS, Academics, Attendance, Finance, Health). Igbo language support for South East pilot. WhatsApp integration live. Offline-first architecture validated. | MVP functional; offline tested in 3G/2G conditions; Igbo UI QA passed |
| Pilot Launch | Q3 2026 (Sep) | Deploy in 10–15 pilot schools across Enugu State for a full academic term (Sep–Dec 2026). Dedicate LafiyaCore staff member to on-site support in Enugu. Weekly check-in with pilot schools. | 10+ schools onboarded; attendance digitised in all pilot schools; at least 1 Sentinel alert generated and validated |
| Evidence & Iteration | Q4 2026 (Oct–Dec) | Collect quantitative and qualitative feedback. Generate first case studies (time saved per week; fee collection improvement; parent satisfaction). Publish early findings. | Case studies published; NPS \>60 from pilot schools; measurable operational improvement documented |
| Expansion | Q1–Q2 2027 | Use pilot evidence to approach state government and first donor conversations. Expand to 50–100 schools across South East. Pursue SEDC partnership for state government procurement. | 50+ schools signed; first government conversation commenced; first donor proposal submitted |

## **14.3 Channels**

* Direct sales: LafiyaCore's South East-based team (to be recruited/based in Enugu Q2 2026\) conducts school visits and demonstrations. A single 60-minute demo at the school leads to a decision in most cases — the pain points are obvious and the product solves them visibly.

* Referral programme: Pilot schools that refer new schools receive one term of free subscription. Headteachers talk to each other — referral is the most trusted channel in the Nigerian school market.

* State government endorsement: An official letter from the Enugu State Ministry of Education or Enugu SME Center endorsing EduLafia reduces procurement anxiety for public and semi-private schools.

* Enugu SME Center partnership: The Enugu SME Center (which co-signed the SEDC competition notice) is a natural distribution partner for reaching the startup and SME ecosystem that operates private schools.

* Digital marketing: WhatsApp broadcast to headteacher groups; Facebook ads targeting school proprietors and headteachers in South East states; LinkedIn for government and donor audience.

# **15\. SEDC SEVCP Competition Alignment — Incubation Track**

| This section is intentionally brief. EduLafia is a product document first. The competition is an opportunity that EduLafia fits, not a purpose EduLafia was built around. Everything in this PRD would exist and be true regardless of the SEDC SEVCP. |
| :---- |

## **15.1 Why EduLafia Qualifies for the Incubation Track**

| SEDC Incubation Track Criterion | EduLafia's Position |
| :---- | :---- |
| Validated idea and minimum viable product | EduLafia's concept has been validated through the EduLafia Concept Document (Dec 2025\) and the LafiyaSentinel MoU with Adamawa State Ministry of Health (Mar 2026). An MVP is in architecture planning, targeted for Q3 2026\. |
| Based in, operating in, or delivering clear impact in the South East | LafiyaCore's 2026 pilot is anchored in Enugu State, South East Nigeria. The company has founder connections to the South East and the pilot school recruitment targets Enugu private schools. |
| Meaningful technology component | EduLafia is a full-stack technology product: offline-first PWA, automated disease surveillance engine, WhatsApp-native parent platform, real-time government dashboards, and structured health/education data infrastructure. |
| HealthTech sector (priority sector) | EduLafia is a HealthTech product. Its health surveillance layer turns Nigerian schools into public health early-warning nodes — one of the most innovative and highest-impact applications of HealthTech in Nigeria. |
| Job creation and economic development | EduLafia directly creates employment in South East Nigeria: the Enugu-based sales, support, and customer success team, and indirect employment in the schools it digitises. The platform also improves school financial management, increasing fee collection efficiency — a direct economic benefit to school operators. |
| Alignment with Renewed Hope Agenda | EduLafia directly supports the Renewed Hope Agenda's pillars of education quality improvement, digital infrastructure, and inclusive health — specifically for the underserved adolescent population in South East Nigeria. |

## **15.2 What the $5,000 SEDC SEVCP Investment Enables**

If selected for the Incubation Track, the $5,000 SAFE investment (alongside the structured incubation program and ecosystem access) will be applied specifically to:

* South East-specific product localisation: Igbo language UI development for the South East pilot; ₦\~800,000

* Enugu State pilot school recruitment and onboarding: travel, demonstrations, onboarding visits, and school support for 10–15 pilot schools; ₦\~1,500,000

* WhatsApp Business API setup and first-year messaging credits for pilot schools; ₦\~600,000

* LafiyaCore's first South East-based hire: a part-time customer success and sales associate based in Enugu for the pilot period; ₦\~1,200,000

* NDPA 2023 compliance review and data protection registration: ₦\~500,000

The mentorship, investor access, and ecosystem connections available through the SEDC SEVCP programme are, frankly, worth more than the $5,000 capital — and LafiyaCore recognises this. The programme provides a structured pathway to the institutional partnerships (state government, SUBEB, state MOH) that represent EduLafia's largest revenue opportunity.

# **16\. Data Model Overview**

The following describes the core entities in EduLafia's data model. This is not a full schema specification — it is an entity-relationship overview to inform architecture planning.

| Entity | Key Attributes | Relationships |
| :---- | :---- | :---- |
| School | school\_id, name, type, LGA, state, subscription\_tier, active | Has many: Students, Staff, Classes, Fee Schedules, Health Events |
| Student | student\_id, school\_id, name, DOB, gender, class\_id, guardian\_ids, NIN, status, admission\_date | Belongs to: School, Class; Has many: Attendance Records, Academic Results, Health Records, Fee Ledger Entries |
| Guardian | guardian\_id, student\_ids, name, relationship, phone, whatsapp, email, portal\_access\_token | Linked to: Students (many-to-many); receives: Notifications |
| Class | class\_id, school\_id, name, level (JSS1–SS3), arm, form\_teacher\_id, academic\_year | Belongs to: School; Has many: Students, Timetable Entries, Attendance Records |
| Staff | staff\_id, school\_id, name, role, subject\_ids, class\_ids, qualifications, employment\_type, contact | Belongs to: School; Assigned to: Classes, Subjects |
| Attendance Record | record\_id, student\_id, class\_id, date, period, status (present/absent/late), reason\_code, symptom\_codes, recorded\_by, edited\_by, edit\_reason | Belongs to: Student, Class; feeds: Sentinel Engine |
| Academic Result | result\_id, student\_id, subject\_id, term, academic\_year, CA\_scores\[\], exam\_score, total, grade, rank, flag (ABS/INC) | Belongs to: Student, Subject; used in: Report Card |
| Health Profile | profile\_id, student\_id, blood\_group, genotype, chronic\_conditions\[\], allergies\[\], medications\[\], emergency\_notes | Belongs to: Student; referenced by: Sick Bay Visit, Referral, Screening |
| Sick Bay Visit | visit\_id, student\_id, school\_id, date\_time, complaint\_codes\[\], complaint\_notes, observations, treatment, outcome, recorded\_by | Belongs to: Student; feeds: Sentinel Engine; may create: Referral |
| Referral | referral\_id, visit\_id, student\_id, destination\_facility, date\_issued, status (pending/attended/overdue), outcome\_notes, follow\_up\_due | Belongs to: Sick Bay Visit, Student |
| Health Screening | screening\_id, student\_id, date, type (annual/termly), height, weight, BMI, vision\_result, hearing\_result, BP, dental\_notes, flags\[\] | Belongs to: Student; contributes to: Population Health Dashboard |
| Mental Health Assessment | assessment\_id, student\_id, term, academic\_year, responses\[\], flag\_level (none/watch/refer), counsellor\_assigned\_id | Belongs to: Student; confidentiality: nurse \+ counsellor only |
| Fee Ledger Entry | entry\_id, student\_id, school\_id, date, type (charge/payment/waiver), amount, fee\_category, payment\_method, recorded\_by, receipt\_number | Belongs to: Student; generates: Receipt; contributes to: Financial Dashboard |
| Sentinel Signal | signal\_id, school\_ids\[\], LGA, date\_generated, symptom\_profile, students\_affected, threshold\_type, alert\_tier (school/LGA/state), status (open/acknowledged/closed), response\_notes | Generated by: Sentinel Engine from Attendance \+ Sick Bay data; resolved by: LGA/State Health Officer |

# **17\. Compliance & Regulatory Framework**

## **17.1 Nigeria Data Protection Act 2023 (NDPA)**

* LafiyaCore registers as a Data Controller and Data Processor with the Nigeria Data Protection Commission (NDPC)

* A Data Protection Officer (DPO) is designated — an identifiable person with a direct contact email published in EduLafia's privacy policy

* Data Processing Agreements (DPAs) are signed with all third-party processors — Termii, Paystack, Flutterwave, cloud hosting provider

* Consent management: guardians explicitly consent to data processing at student enrolment; consent is digitally recorded and timestamped

* Data subject rights: every student and guardian can request access, correction, or deletion of their personal data through the guardian portal; requests responded to within 72 hours

* Data breach notification: any breach affecting personal data must be notified to NDPC within 72 hours and to affected individuals without undue delay

* Data residency: all personal and health data stored exclusively within Nigeria

## **17.2 National School Health Policy (Federal Ministry of Education, 2006\)**

* EduLafia's School Health Module is designed to implement — not just comply with — Nigeria's National School Health Policy. It provides the digital infrastructure the policy has always lacked.

* Health record categories, screening types, and referral protocols are aligned with the policy's framework for comprehensive school health programmes.

## **17.3 Federal Ministry of Education EMIS Standards**

* All enrolment, attendance, and performance data exports are formatted to EMIS standards as specified by the FMOE/Universal Basic Education Commission (UBEC)

* School codes, LGA codes, and state codes in EduLafia align with the official EMIS geographic classification

## **17.4 National Health Management Information System (NHMIS)**

* Health data exports are formatted for DHIS2 compatibility where applicable, enabling integration with the Federal Ministry of Health's NHMIS platform

* Disease codes in the Sentinel Engine's surveillance taxonomy align with ICD-10 coding where applicable, facilitating cross-platform data exchange

## **17.5 Integrated Disease Surveillance and Response (IDSR)**

* LafiyaSentinel's outbreak alerts are designed to feed into — not replace — Nigeria's IDSR framework at the LGA and state levels

* Annual surveillance summary reports are formatted to meet IDSR reporting obligations at the state level

## **17.6 Children's Data Protection**

* All student data is treated as children's data — subject to heightened protection obligations under the NDPA and the Child Rights Act

* Mental health assessment data has additional confidentiality controls — it is inaccessible to parents without nurse/counsellor authorisation in cases where disclosure could harm the child

# **18\. Pilot School Requirements & Onboarding Plan**

## **18.1 Ideal Pilot School Profile**

* Private secondary school in Enugu State (for South East pilot) or Adamawa State (existing base)

* Enrolment: 100–600 students (optimal for pilot feedback quality without enterprise complexity)

* Has at least one device (smartphone or tablet) available for each of: administration office, bursary, and class teacher use

* Has a school nurse or designated health officer (for testing the full health module)

* Headteacher or proprietor is actively engaged with the digital transformation of their school — not just delegating to a junior staff member

* Located in an area with at least occasional 3G connectivity

## **18.2 Onboarding Process for Pilot Schools**

| Step | Owner | Duration | Output |
| :---- | :---- | :---- | :---- |
| 1\. Scoping visit | LafiyaCore Customer Success | 2 hours | Module selection confirmed; student count, class structure, and fee schedule documented; key staff identified |
| 2\. System configuration | LafiyaCore (remote) | 1–2 days | School provisioned; fee schedule entered; classes created; staff accounts set up |
| 3\. Data migration | LafiyaCore \+ School Admin | 1 day on-site | Existing student records entered or imported; historical fee data entered for current term |
| 4\. Staff training | LafiyaCore Customer Success | Half day (3–4 hours) | All teachers trained on attendance; bursar trained on finance module; nurse trained on health module; admin trained on all dashboards |
| 5\. Go-live | School Admin \+ LafiyaCore support | Day 1 of new term | Live attendance marking begins; fee collection begins; health module activated |
| 6\. First-week support | LafiyaCore (WhatsApp \+ calls) | 5 school days | Daily check-in with school admin; issues resolved within 24 hours |
| 7\. First-month review | LafiyaCore \+ Headteacher | 1 hour video call | Feedback captured; adjustments made; case study data collection begins |

# **19\. Assumptions & Constraints**

## **19.1 Key Assumptions**

* At least 80% of Nigerian private secondary school headteachers have a smartphone and use WhatsApp — assumption based on general smartphone penetration data for urban and semi-urban Nigeria. This underpins the WhatsApp-first design.

* Schools that express interest in EduLafia have at least one device capable of running a PWA — a basic Android smartphone with Chrome browser. LafiyaCore does not provide hardware.

* State government endorsement (even a courtesy letter) meaningfully accelerates private school adoption — this is based on LafiyaCore's experience with the Adamawa State MOH engagement.

* Donor funding for public school deployment is achievable within 24–36 months of building an evidence base from the private school pilot — based on standard grant timelines for Nigerian HealthTech/EdTech NGO and bilateral programmes.

* The NPHCDA, FMOH, and FMOE are willing to receive data from EduLafia in the medium term — this is a precondition for the government revenue streams and the surveillance mission. It is not guaranteed but is strongly supported by existing policy frameworks.

## **19.2 Key Constraints**

* Engineering capacity: LafiyaCore is an early-stage company. The MVP build is constrained by the founding team's engineering bandwidth. Module prioritisation (M1–M5 first; M6–M9 in parallel) is designed to deliver value quickly while managing this constraint.

* Internet connectivity: EduLafia cannot rely on constant connectivity in many Nigerian school contexts. The offline-first architecture is both a design requirement and a technical constraint that increases build complexity.

* Data quality: The Sentinel Engine's surveillance value depends on the quality and completeness of absence and illness data entered by teachers. Teacher training and engagement are critical success factors that are outside the system's direct control.

* Regulatory unpredictability: Nigerian regulatory frameworks for EdTech and HealthTech are evolving. New NDPC guidance, FMOE procurement regulations, or FMOH data governance requirements could affect the timeline or design of government-facing features.

* Procurement cycles: State government and federal government procurement in Nigeria is slow, politically influenced, and unpredictable. LafiyaCore's growth model is designed to not depend on government procurement in Years 1–2.

# **20\. Donor & Strategic Funding Alignment**

| Funder | Priority Area Alignment | EduLafia's Proposition | Potential Funding Use |
| :---- | :---- | :---- | :---- |
| UNICEF Nigeria | Education equity, child rights, school health and nutrition, girls' education | EduLafia deploys in underserved public schools — UNICEF pays for deployment; UNICEF gets health and education equity data for programme evaluation | Deployment grant for 50–200 public schools in low-income LGAs; ₦10M–₦50M |
| WHO / AFRO | Adolescent health, school health programmes, disease surveillance | Grant support for the Sentinel surveillance layer as Nigeria's first adolescent health surveillance infrastructure — a direct contribution to AFRO's surveillance mandate | Research and deployment grant for Sentinel Engine validation; $100,000–$500,000 |
| Global Fund | HIV/TB awareness and management among adolescents | Sickle cell and HIV/TB awareness components of the School Health Module in high-burden states; links to LafiyaCore's HIV Asset Platform | Integration grant connecting EduLafia School Health Module to Global Fund programme monitoring; $50,000–$200,000 |
| USAID / Feed the Future | Girls' education, reproductive health, school nutrition, SBCC | Enhanced girls' health and nutritional surveillance features; deployment in USAID education programme states | EdTech and HealthTech deployment grant; $200,000–$500,000 |
| World Bank / SABER | Education systems strengthening, EMIS development in Nigeria | EduLafia as the school-level EMIS node that feeds upward into state and national education data systems — directly supports World Bank's school management systems programme | Systems integration grant; $500,000+ |
| Gates Foundation | Adolescent nutrition, health systems strengthening, digital health, data for development | Research and evaluation grants to study the impact of school-based health surveillance on adolescent health outcomes — produces publishable evidence | Research grant; $250,000–$1,000,000 |
| SEDC SEVCP | South East Nigeria HealthTech, economic development, Renewed Hope Agenda | EduLafia as a flagship South East HealthTech startup anchored in Enugu — directly aligned with SEVCP's HealthTech and EdTech priority sectors | Incubation Track SAFE investment ($5,000) \+ structured incubation \+ ecosystem access |

# **21\. Glossary**

| Term | Definition |
| :---- | :---- |
| AFRO | WHO Regional Office for Africa |
| BMI | Body Mass Index — weight (kg) / height (m²); used in nutritional screening |
| CA | Continuous Assessment — ongoing in-class evaluation contributing to a student's final grade alongside the end-of-term examination |
| DHIS2 | District Health Information Software 2 — open-source health management information system used by Nigeria's FMOH and 80+ countries |
| EMIS | Education Management Information System — Nigeria's national system for collecting and reporting school-level education data |
| EduLafia | LafiyaCore's integrated school management and adolescent health surveillance platform |
| FGC | Federal Government College — one of Nigeria's 110 nationally administered boarding secondary schools |
| FMOE | Federal Ministry of Education, Nigeria |
| FMOH | Federal Ministry of Health, Nigeria |
| IDSR | Integrated Disease Surveillance and Response — Nigeria's national communicable disease surveillance and response framework |
| Lafia | Hausa word for health, peace, and wellbeing — the anchor of LafiyaCore's brand family |
| LafiyaSentinel | LafiyaCore's branded school-based disease surveillance capability, embedded within EduLafia as the Sentinel Surveillance Engine from version 2.0 |
| LGEA / LGA | Local Government Education Authority / Local Government Area |
| MoU | Memorandum of Understanding — the formal partnership agreement between LafiyaCore and the Adamawa State Ministry of Health (March 2026\) |
| MUAC | Mid-Upper Arm Circumference — a nutritional assessment indicator particularly relevant for adolescents |
| MVP | Minimum Viable Product — the earliest version of EduLafia that delivers core value to a pilot school |
| NDPA | Nigeria Data Protection Act 2023 — Nigeria's primary data protection legislation |
| NDPC | Nigeria Data Protection Commission — the regulatory body for data protection under the NDPA |
| NECO | National Examinations Council — conducts the Senior Secondary Certificate Examination (SSCE) for Nigerian secondary school graduates |
| NIN | National Identification Number — Nigeria's biometric national identity system |
| NITDA | National Information Technology Development Agency — Nigeria's IT regulatory authority |
| NPHCDA | National Primary Health Care Development Agency — responsible for immunisation and primary healthcare delivery in Nigeria |
| NHMIS | National Health Management Information System — Nigeria's national health data platform |
| PHQ-A | Patient Health Questionnaire — Adolescent version; a validated mental health screening tool adapted for use in EduLafia |
| PRD | Product Requirements Document — this document |
| PWA | Progressive Web Application — a web application that can be installed on a smartphone and used offline |
| RBAC | Role-Based Access Control — a security model that restricts system access based on the user's role |
| SAFE | Simple Agreement for Future Equity — the investment instrument used by the SEDC SEVCP |
| SDQ | Strengths and Difficulties Questionnaire — a child mental health screening instrument adapted for use in EduLafia |
| SEDC | South East Development Commission — the Nigerian federal agency that launched the SEVCP |
| Sentinel Engine | The automated disease surveillance intelligence layer within EduLafia, derived from the LafiyaSentinel product concept |
| SEVCP | South East Venture Capital Program — the SEDC's HealthTech and startup funding programme |
| SIS | Student Information System — Module 1 of EduLafia |
| SUBEB | State Universal Basic Education Board — state-level body responsible for funding and managing public primary and junior secondary schools |
| WAEC | West African Examinations Council — conducts the WASSCE (West African Senior School Certificate Examination) in Nigeria |

*EduLafia — where education and health finally meet.*

A LafiyaCore Product  ·  RC 9347000  ·  hello@lafiyacore.com  ·  www.lafiyacore.com

Adamawa State & Enugu State, Nigeria  ·  March 2026