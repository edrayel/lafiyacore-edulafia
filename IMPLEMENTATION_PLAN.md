# EduLafia Implementation Plan: 171 User Stories → Code Changes

**Generated:** 2026-04-05
**Target:** Full coverage of all 171 user stories
**Total Stories:** 171 (50 P0, 55 P1, 58 P2, 8 P3)
**Total Phases:** 12

---

## Current State Assessment

| Module           | Backend                               | Frontend                                    | Gap                                    |
| ---------------- | ------------------------------------- | ------------------------------------------- | -------------------------------------- |
| **Students**     | Full service/repo, NO API router      | Partial (list/detail, mock data, no create) | Wire API endpoints, fix mock data      |
| **Guardians**    | Full service/repo, NO API router      | Partial (list/detail, mock data, no create) | Wire API endpoints, fix mock data      |
| **Academics**    | FULL (endpoints + service)            | ZERO                                        | Build entire frontend                  |
| **Finance**      | FULL (endpoints + service)            | ZERO                                        | Build entire frontend                  |
| **Health**       | FULL (endpoints + service + Sentinel) | ZERO                                        | Build entire frontend                  |
| **Staff**        | FULL (endpoints + service)            | Partial (list only)                         | Add timetable, attendance UI           |
| **Attendance**   | FULL (endpoints + service + Sentinel) | Partial (mock student data)                 | Wire real student data                 |
| **Parent**       | FULL (except payment=501)             | Partial (login + children + notifications)  | Add excusal, feedback, correction      |
| **Intelligence** | FULL (endpoints + service)            | Partial (school dashboard only)             | Add LGA/state views                    |
| **Admin**        | FULL (endpoints + service)            | Partial (3 of 12 features)                  | Add sync, updates, training, analytics |
| **Auth**         | FULL (except forgot-password stub)    | FULL (login page)                           | Implement forgot-password              |
| **Dashboard**    | —                                     | STUB (all "--" placeholders)                | Wire real data                         |

### Key Insight

**Backend is ~70% complete** — most modules have full services and endpoints. The two biggest backend gaps are: Students/Guardians API routers (services exist, no routers) and 25 entirely new modules for Addendum 2/3 stories.

**Frontend is ~25% complete** — 3 modules have zero frontend, 6 are partial, only auth is complete.

---

## Phase 1: Wire Missing Student/Guardian API Endpoints

**Goal:** Connect existing Students and Guardians backend services to FastAPI routers.

**Stories Covered:** US-001, US-002, US-003, US-004, US-005, US-006

### Backend Changes

| File                                                           | Action | Contents                                                             |
| -------------------------------------------------------------- | ------ | -------------------------------------------------------------------- |
| `apps/backend/src/edulafia/modules/students/api/__init__.py`   | New    | Module init                                                          |
| `apps/backend/src/edulafia/modules/students/api/students.py`   | New    | Router: POST/GET/PATCH/DELETE /students, POST /students/batch-import |
| `apps/backend/src/edulafia/modules/guardians/api/__init__.py`  | New    | Module init                                                          |
| `apps/backend/src/edulafia/modules/guardians/api/guardians.py` | New    | Router: POST/GET/PATCH/DELETE /guardians, link/unlink endpoints      |
| `apps/backend/src/edulafia/api/v1/router.py`                   | Edit   | Import and mount new routers                                         |

### Frontend Changes

- None (existing frontend already calls these endpoints)

**Files:** 5 new, 1 modified
**Effort:** ~2 hours

---

## Phase 2: Build Finance Frontend

**Goal:** Build complete finance module UI wired to existing backend APIs.

**Stories Covered:** US-017, US-018, US-019, US-020, US-064, US-069, US-092, US-093, US-094, US-095, US-155, US-157

### Frontend Changes

| File                                                   | Action | Contents                                                 |
| ------------------------------------------------------ | ------ | -------------------------------------------------------- |
| `apps/frontend/src/features/finance/api.ts`            | New    | API client for all finance endpoints                     |
| `apps/frontend/src/features/finance/FinancePage.tsx`   | New    | Tabbed: Fee Schedules, Payments, Dashboard, Scholarships |
| `apps/frontend/src/features/finance/PaymentDialog.tsx` | New    | Payment recording dialog with student search             |
| `apps/frontend/src/features/finance/ReceiptView.tsx`   | New    | Printable A5 receipt                                     |
| `apps/frontend/src/app/router.tsx`                     | Edit   | Add /finance route                                       |

### Backend Changes

- None (all endpoints exist)

**Files:** 4 new, 1 modified
**Effort:** ~4 hours

---

## Phase 3: Build Health Frontend

**Goal:** Build complete health module UI wired to existing backend APIs.

**Stories Covered:** US-022, US-023, US-024, US-025, US-026, US-027, US-134, US-139, US-142, US-143, US-144, US-147, US-148

### Frontend Changes

| File                                                      | Action | Contents                                                        |
| --------------------------------------------------------- | ------ | --------------------------------------------------------------- |
| `apps/frontend/src/features/health/api.ts`                | New    | API client for all health endpoints                             |
| `apps/frontend/src/features/health/HealthPage.tsx`        | New    | Tabbed: Sick Bay, Profiles, Screenings, Referrals, Vaccinations |
| `apps/frontend/src/features/health/SentinelPage.tsx`      | New    | Sentinel surveillance dashboard                                 |
| `apps/frontend/src/features/health/SickBayVisitForm.tsx`  | New    | Sick bay visit logging form                                     |
| `apps/frontend/src/features/health/HealthProfileForm.tsx` | New    | Health profile form                                             |
| `apps/frontend/src/app/router.tsx`                        | Edit   | Add /health, /health/sentinel routes                            |

### Backend Changes

- None (all endpoints exist)

**Files:** 5 new, 1 modified
**Effort:** ~6 hours

---

## Phase 4: Build Academics Frontend

**Goal:** Build complete academics module UI wired to existing backend APIs.

**Stories Covered:** US-007, US-008, US-009, US-010, US-011, US-012, US-063, US-088, US-112, US-166

### Frontend Changes

| File                                                         | Action | Contents                                             |
| ------------------------------------------------------------ | ------ | ---------------------------------------------------- |
| `apps/frontend/src/features/academics/api.ts`                | New    | API client for subjects, scores, grades              |
| `apps/frontend/src/features/academics/AcademicsPage.tsx`     | New    | Tabbed: Subjects, Grade Entry, Results, Report Cards |
| `apps/frontend/src/features/academics/GradeEntryGrid.tsx`    | New    | Inline-editable grade entry grid                     |
| `apps/frontend/src/features/academics/ReportCardPreview.tsx` | New    | Printable report card                                |
| `apps/frontend/src/app/router.tsx`                           | Edit   | Add /academics route                                 |

### Backend Changes

- None (all endpoints exist)

**Files:** 4 new, 1 modified
**Effort:** ~4 hours

---

## Phase 5: Complete Student/Guardian Frontend

**Goal:** Fix mock data, add create functionality, wire real API calls.

**Stories Covered:** US-001, US-002, US-003, US-004, US-005, US-006, US-096, US-097, US-098, US-166

### Frontend Changes

| File                                                          | Action | Contents                                               |
| ------------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `apps/frontend/src/features/students/StudentsPage.tsx`        | Edit   | Wire create button, add batch import, fix class filter |
| `apps/frontend/src/features/students/StudentDetailPage.tsx`   | Edit   | Replace mock guardians with real API call              |
| `apps/frontend/src/features/guardians/GuardiansPage.tsx`      | Edit   | Wire create button, link student action                |
| `apps/frontend/src/features/guardians/GuardianDetailPage.tsx` | Edit   | Replace mock students with real API call               |

### Backend Changes

- None (Phase 1 creates the API endpoints)

**Files:** 4 modified
**Effort:** ~3 hours

---

## Phase 6: Complete Attendance Frontend

**Goal:** Wire real student data to attendance marking.

**Stories Covered:** US-013, US-014, US-015, US-016, US-089, US-091, US-162

### Frontend Changes

| File                                                       | Action | Contents                                               |
| ---------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `apps/frontend/src/features/attendance/AttendancePage.tsx` | Edit   | Replace mock data with real API, add reason/symptom UI |
| `apps/frontend/src/features/attendance/api.ts`             | Edit   | Add bulk mark, get students by class                   |

### Backend Changes

- None

**Files:** 2 modified
**Effort:** ~2 hours

---

## Phase 7: Complete Staff Frontend

**Goal:** Build timetable and attendance UI.

**Stories Covered:** US-028, US-029, US-030, US-031, US-032, US-065, US-066, US-111, US-125

### Frontend Changes

| File                                                         | Action | Contents                                       |
| ------------------------------------------------------------ | ------ | ---------------------------------------------- |
| `apps/frontend/src/features/staff/StaffPage.tsx`             | Edit   | Wire create button, add detail view            |
| `apps/frontend/src/features/staff/TimetablePage.tsx`         | New    | Timetable builder with clash detection         |
| `apps/frontend/src/features/staff/TeacherAttendancePage.tsx` | New    | Teacher attendance register                    |
| `apps/frontend/src/app/router.tsx`                           | Edit   | Add /staff/timetable, /staff/attendance routes |

### Backend Changes

- None

**Files:** 2 new, 2 modified
**Effort:** ~4 hours

---

## Phase 8: Complete Parent Portal

**Goal:** Build excusal, feedback, correction, and child profile UI.

**Stories Covered:** US-033, US-034, US-035, US-036, US-037, US-038, US-039, US-059

### Frontend Changes

| File                                                   | Action | Contents                                                        |
| ------------------------------------------------------ | ------ | --------------------------------------------------------------- |
| `apps/frontend/src/features/parent/ParentPage.tsx`     | Edit   | Add excusal, feedback, correction dialogs, child profile detail |
| `apps/frontend/src/features/parent/ExcusalDialog.tsx`  | New    | Absence excusal form                                            |
| `apps/frontend/src/features/parent/FeedbackDialog.tsx` | New    | Feedback submission form                                        |

### Backend Changes

| File                                                     | Action | Contents                                                       |
| -------------------------------------------------------- | ------ | -------------------------------------------------------------- |
| `apps/backend/src/edulafia/modules/parent/api/parent.py` | Edit   | Replace payment 501 stub with real integration or better error |

**Files:** 2 new, 2 modified
**Effort:** ~3 hours

---

## Phase 9: Complete Intelligence Frontend

**Goal:** Build LGA/state views and report download.

**Stories Covered:** US-040, US-041, US-042, US-043, US-044, US-105, US-120

### Frontend Changes

| File                                                           | Action | Contents                                |
| -------------------------------------------------------------- | ------ | --------------------------------------- |
| `apps/frontend/src/features/intelligence/IntelligencePage.tsx` | Edit   | Add LGA/state tabs, report download     |
| `apps/frontend/src/features/intelligence/LGADashboard.tsx`     | New    | LGA-level metrics and school comparison |
| `apps/frontend/src/features/intelligence/VerificationPage.tsx` | New    | Public certificate verification         |

### Backend Changes

- None

**Files:** 2 new, 1 modified
**Effort:** ~3 hours

---

## Phase 10: Complete Admin Frontend

**Goal:** Build sync monitoring, system updates, training, analytics UI.

**Stories Covered:** US-045, US-046, US-047, US-048, US-049, US-050, US-106, US-107, US-108, US-113, US-115, US-158

### Frontend Changes

| File                                                   | Action | Contents                           |
| ------------------------------------------------------ | ------ | ---------------------------------- |
| `apps/frontend/src/features/admin/AdminPage.tsx`       | Edit   | Add all missing tabs, wire buttons |
| `apps/frontend/src/features/admin/SyncMonitor.tsx`     | New    | Sync health dashboard              |
| `apps/frontend/src/features/admin/SystemUpdates.tsx`   | New    | Updates management UI              |
| `apps/frontend/src/features/admin/TrainingManager.tsx` | New    | Training resources UI              |
| `apps/frontend/src/features/admin/AnalyticsPage.tsx`   | New    | Platform analytics UI              |

### Backend Changes

- None

**Files:** 4 new, 1 modified
**Effort:** ~6 hours

---

## Phase 11: Build Missing Backend Features

**Goal:** Implement backend services and endpoints for 25 stories with no backend code.

**Stories Covered:** US-083, US-084, US-085, US-086, US-087, US-090, US-099, US-100, US-101, US-102, US-103, US-104, US-109, US-110, US-114, US-116, US-117, US-118, US-119, US-121, US-149, US-150, US-151, US-152, US-153

### Backend Changes

Each new feature requires: Model → Schema → Repository → Service → API Router

| Feature                         | Files | Priority |
| ------------------------------- | ----- | -------- |
| US-083: Admission processing    | 5     | P0       |
| US-103: Emergency mode          | 5     | P1       |
| US-104: Special needs (IEP)     | 5     | P2       |
| US-099: Custody disputes        | 5     | P1       |
| US-100: Data retention          | 5     | P1       |
| US-119: WAEC bulk registration  | 5     | P1       |
| US-121: Ministry reporting      | 5     | P1       |
| US-084-087, 090: Facilities/ops | 20    | P2       |
| US-109-110, 114: Communications | 15    | P2       |
| US-116-118, 149-153: Governance | 15    | P2       |

**Files:** ~75 new
**Effort:** ~30 hours

---

## Phase 12: Build Missing Frontend Features

**Goal:** Build frontend pages for all remaining 40 user stories.

**Stories Covered:** US-058, US-060, US-061, US-062, US-067, US-068, US-070, US-071, US-072, US-073, US-074, US-075, US-076, US-077, US-078, US-079, US-080, US-081, US-082, US-088, US-089, US-090, US-091, US-108, US-109, US-110, US-111, US-112, US-113, US-114, US-115, US-154, US-156, US-159, US-160, US-161, US-162, US-163, US-164, US-165, US-167, US-168, US-169, US-170

### Frontend Changes

| Feature                     | Files | Priority |
| --------------------------- | ----- | -------- |
| US-062: Class promotion     | 2     | P0       |
| US-070: End-of-term         | 2     | P0       |
| US-082: Emergency broadcast | 2     | P1       |
| US-067: EMIS reporting      | 2     | P0       |
| US-068: NCDC reporting      | 2     | P1       |
| US-075: Girl-child tracking | 2     | P1       |
| US-088: Exam timetable      | 2     | P1       |
| US-119: WAEC registration   | 2     | P1       |
| Remaining 36 stories        | ~24   | P2/P3    |

**Files:** ~40 new
**Effort:** ~25 hours

---

## Execution Summary

| Phase     | Name                          | New Files | Modified | Effort   | Cumulative |
| --------- | ----------------------------- | --------- | -------- | -------- | ---------- |
| P1        | Wire Students/Guardians API   | 5         | 1        | 2h       | 2h         |
| P2        | Finance Frontend              | 4         | 1        | 4h       | 6h         |
| P3        | Health Frontend               | 5         | 1        | 6h       | 12h        |
| P4        | Academics Frontend            | 4         | 1        | 4h       | 16h        |
| P5        | Complete Students/Guardians   | 0         | 4        | 3h       | 19h        |
| P6        | Complete Attendance           | 0         | 2        | 2h       | 21h        |
| P7        | Complete Staff                | 2         | 2        | 4h       | 25h        |
| P8        | Complete Parent Portal        | 2         | 2        | 3h       | 28h        |
| P9        | Complete Intelligence         | 2         | 1        | 3h       | 31h        |
| P10       | Complete Admin                | 4         | 1        | 6h       | 37h        |
| P11       | Missing Backend (25 stories)  | ~75       | ~5       | 30h      | 67h        |
| P12       | Missing Frontend (40 stories) | ~40       | ~5       | 25h      | 92h        |
| **Total** |                               | **~143**  | **~26**  | **~92h** |            |

### Dependencies Graph

```
P1 (Students/Guardians API) ──→ P5 (Complete Students/Guardians)
P2 (Finance) ─→ P8 (Parent Portal - payment)
P3 (Health) ──→ P9 (Intelligence - health data)
P4 (Academics) ─→ P9 (Intelligence - academic data)
P6 (Attendance) ──→ depends on P1 (student roster)
P7 (Staff) ──→ independent
P8 (Parent) ──→ depends on P2, P3, P4
P9 (Intelligence) ──→ depends on P3, P4
P10 (Admin) ──→ independent
P11 (Missing Backend) ──→ independent
P12 (Missing Frontend) ──→ depends on P11
```

### Success Criteria

- All 171 user stories have implementation
- All backend endpoints return real data (no stubs)
- All frontend pages wired to real APIs (no mock data)
- All tests pass (516 backend + frontend tests)
- Vite build succeeds
- Docker compose up works end-to-end
