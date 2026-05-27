# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-18

### Added

**Module 1: Student Information System (SIS)**
- Foundational DB models and APIs for `Student` and `StudentGuardian`.
- Frontend UI for digital student profiles (create, edit, archive, list).
- Guardian linking view and basic student search functionality.
- Document storage (uploading admission letters, birth certificates, etc.).
- Batch import via CSV for onboarding entire classes.
- Transfer-out export package generation.
- NIN linkage and validation logic.

**Module 2: Academics (Academic & Grading System)**
- DB models for subjects, continuous assessments, and exam scores.
- Frontend subject management (create, edit, archive).
- Full backend integration for the grade entry grid.
- Automated class rank computation and grade computation logic.
- PDF report card generation and WhatsApp/SMS delivery endpoints.
- Automated alerts for students whose performance drops by >20%.
- WAEC/NECO alignment configurations.

**Module 3: Attendance (Attendance & Absence Tracking)**
- DB models for attendance records.
- Frontend daily attendance marking (bulk actions and grid view).
- LafiyaSentinel symptom capture integration (dropdowns for symptoms).
- 3-day consecutive absence automated alerts.
- EMIS-compatible termly export functionality.

**Module 4: Finance (Fee & Finance Management)**
- DB models for fee schedules, ledgers, and scholarships.
- Frontend fee schedule management (add, copy, lock).
- Manual payment recording and receipt generation.
- Financial dashboard.
- Online payment gateway integration (Paystack/Flutterwave/Remita).
- Debt report export for end-of-term collection drives.
- Reversal audit trail UI (reversing transactions with mandatory reasons).

**Module 5: Health (School Health & Sentinel Engine)**
- DB models for health profiles, sick bay visits, referrals, and vaccinations.
- LafiyaSentinel core engine logic (symptom clustering and alerts).
- Basic UI for logging individual visits and managing profiles.
- Termly Mental Health & Wellbeing Screening (PHQ-A, SDQ).
- Batch screening mode UI for rapid class-wide assessments.
- Offline-first sync capabilities for health data using local storage and event listeners.

**Module 6: Staff (HR & Teacher Management)**
- DB models for staff profiles and employment data.
- Frontend UI for adding/editing staff members.
- Role-based filtering.
- Full HR document upload support (CVs, credentials).
- Class assignments interface (mapping teachers to specific classes/subjects).
- Basic staff attendance view.

**Module 7: Parent (Parent & Guardian Portal)**
- Guardian portal dashboard.
- Notifications panel.
- Absence excusal reporting form.
- Feedback submission dialog.
- Direct online fee payment interface.
- Downloadable PDF report cards.
- Direct messaging interface with teachers/admin.

**Module 8: Intelligence (Intelligence & Analytics Dashboard)**
- School and LGA dashboard APIs.
- Custom report generation models.
- Core anonymisation logic.
- Real-time EMIS push/sync API.
- Geographic heatmap visualizations for illness signals.
- Anonymised data portal workflow for donors and researchers.

**Module 9: Admin (System Administration & Onboarding)**
- DB models and APIs for user and school provisioning.
- Frontend school management and user role assignment panels.
- Sentinel threshold configuration UI.
- Functional offline sync monitoring UI.
- Automated system backup and restore interface.
- System updates deployment module.
- Training resource library for school onboarding.

### Fixed
- Pydantic schema validation errors across API payloads.
- Test coverage across all 9 modules (achieved 500+ passing unit tests).
- Type checking across the React/Vite frontend mono-repo environment.
