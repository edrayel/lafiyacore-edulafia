# EduLafia Codebase Audit & Tracker

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the remaining features across the 9 core modules to achieve 100% alignment with EduLafia_PRD_v2.0.md.

**Architecture:** Frontend is React/Vite (PWA) using Material-UI. Backend is FastAPI with SQLAlchemy.

**Tech Stack:** React, TypeScript, Material-UI, Vite, Python, FastAPI, SQLAlchemy.

---

## 1. SIS (Student Information System)

**Done:**
- Foundational DB models and APIs for `Student` and `StudentGuardian`.
- Frontend UI for digital student profiles (create, edit, archive, list).
- Guardian linking view and basic student search functionality.

**Left:**
- [x] Task 1.1: Document storage (uploading admission letters, birth certificates, etc.).
- [x] Task 1.2: Batch import via CSV for onboarding entire classes.
- [x] Task 1.3: Transfer-out export package generation.
- [x] Task 1.4: NIN linkage and validation logic.

## 2. Academics (Academic & Grading System)

**Done:**
- DB models for subjects, continuous assessments, and exam scores.
- Frontend subject management (create, edit, archive).
- Basic grading scale and report card preview views.

**Left:**
- [x] Task 2.1: Full backend integration for the grade entry grid.
- [x] Task 2.2: Automated class rank computation and grade computation logic.
- [x] Task 2.3: PDF report card generation and WhatsApp/SMS delivery.
- [x] Task 2.4: Automated alerts for students whose performance drops by >20%.
- [x] Task 2.5: WAEC/NECO alignment configurations.

## 3. Attendance (Attendance & Absence Tracking)

**Done:**
- DB models for attendance records.
- Frontend daily attendance marking (bulk actions and grid view).
- Basic attendance statistics and summary views.

**Left:**
- [x] Task 3.1: LafiyaSentinel symptom capture integration (dropdowns for symptoms).
- [x] Task 3.2: 3-day consecutive absence automated alerts.
- [x] Task 3.3: EMIS-compatible termly export functionality.

## 4. Finance (Fee & Finance Management)

**Done:**
- DB models for fee schedules, ledgers, and scholarships.
- Frontend fee schedule management (add, copy, lock).
- Manual payment recording and receipt generation.
- Financial dashboard.

**Left:**
- [x] Task 4.1: Online payment gateway integration (Paystack/Flutterwave/Remita).
- [x] Task 4.2: Debt report export for end-of-term collection drives.
- [x] Task 4.3: Reversal audit trail UI (reversing transactions with mandatory reasons).

## 5. Health (School Health & Sentinel Engine)

**Done:**
- DB models for health profiles, screenings, and sentinel signals.
- Frontend sick bay visit logging and referral tracking.
- Annual health screenings and vaccination records UI.
- Active sentinel alerts display panel.

**Left:**
- [x] Task 5.1: Termly Mental Health & Wellbeing Screening (PHQ-A, SDQ).
- [x] Task 5.2: Batch screening mode UI for rapid class-wide assessments.
- [x] Task 5.3: Offline-first sync capabilities for health data.

## 6. Staff (Teacher & Staff Management)

**Done:**
- DB models for staff, assignments, and timetables.
- Frontend staff directory.

**Left:**
- [x] Task 6.1: Timetable builder UI with conflict detection.
- [x] Task 6.2: Daily teacher attendance register.
- [x] Task 6.3: Staff broadcast system (in-app and WhatsApp messaging).

## 7. Parent (Parent & Guardian Portal)

**Done:**
- Guardian portal dashboard.
- Notifications panel.
- Absence excusal reporting form.
- Feedback submission dialog.

**Left:**
- [x] Task 7.1: Direct online fee payment interface.
- [x] Task 7.2: Downloadable PDF report cards.
- [x] Task 7.3: Direct messaging interface with teachers/admin.

## 8. Intelligence (Intelligence & Analytics Dashboard)

**Done:**
- Backend KPI aggregation service.
- Frontend dashboards for School KPIs and Sentinel summaries.
- Certificate verification page.

**Left:**
- [x] Task 8.1: Real-time EMIS push/sync API.
- [x] Task 8.2: Geographic heatmap visualizations for illness signals.
- [x] Task 8.3: Anonymised data portal workflow for donors and researchers.

## 9. Admin (System Administration & Onboarding)

**Done:**
- DB models and APIs for user and school provisioning.
- Frontend school management and user role assignment panels.
- Sentinel threshold configuration UI.

**Left:**
- [x] Task 9.1: Functional offline sync monitoring UI.
- [x] Task 9.2: Automated system backup and restore interface.
- [x] Task 9.3: System updates deployment module.
- [x] Task 9.4: Training resource library for school onboarding.
