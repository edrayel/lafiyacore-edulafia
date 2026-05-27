# Summary
Expand EduLafia to a comprehensive Learning Management System (LMS) and community platform by adding 6 major missing domains: Two-Way Communication/Chat, LMS & Homework Tracking, Hostel/Boarding Management, Automated Payment Webhooks, Centralized School Calendar, and Alumni Network.

# Current State Analysis
The system successfully handles administrative, financial, and health tracking workflows using a modular FastAPI backend and a React/MUI frontend. However, it lacks deeper community engagement (chat, alumni), learning management (homework submission, file uploads), centralized event planning (calendar), boarding management, and automated online payment reconciliation.

# Proposed Changes

## 1. Two-Way Communication / Chat
**Backend:**
- Create `apps/backend/src/edulafia/modules/messaging/` with standard module files (`models.py`, `schemas.py`, `repository.py`, `service.py`, `api/router.py`).
- Define a `messages` table storing `sender_id`, `receiver_id`, `content`, `read_at`, and `created_at`.
- Add endpoints: `GET /v1/messaging/conversations` and `POST /v1/messaging/send`.
- Register the router in `api/v1/router.py`.
**Frontend:**
- Create `apps/frontend/src/features/messaging/` with `MessagingPage.tsx` and `api.ts`.
- Implement a chat UI with a contact list (parents, teachers) and a message thread view.
- Add "Messages" to the `AppLayout.tsx` sidebar.

## 2. LMS & Homework Tracking
**Backend:**
- Create `apps/backend/src/edulafia/modules/lms/` with standard module files.
- Define `assignments` (title, description, due_date, class_id, subject_id, file_path) and `submissions` (assignment_id, student_id, file_path, grade, feedback) tables.
- Add an endpoint `POST /v1/lms/assignments/upload` to handle file uploads, saving files to `/app/uploads/assignments/` (Local File System).
**Frontend:**
- Create `apps/frontend/src/features/lms/` with `AssignmentsPage.tsx` and `api.ts`.
- Build UI for teachers to create assignments and for students/parents to view and upload submissions.
- Add "LMS" to the `AppLayout.tsx` sidebar.

## 3. Hostel / Boarding Management
**Backend:**
- Create `apps/backend/src/edulafia/modules/hostel/`.
- Define `hostels` (name, capacity, gender), `rooms` (hostel_id, room_number, capacity), and `bed_allocations` (room_id, student_id, academic_year_id) tables.
- Expose CRUD endpoints for hostel administration.
**Frontend:**
- Create `apps/frontend/src/features/hostel/HostelPage.tsx`.
- Implement a DataGrid to manage hostels, rooms, and student bed assignments.
- Add "Hostels" to the `AppLayout.tsx` sidebar.

## 4. Automated Payment Webhooks
**Backend:**
- Add `api/webhooks.py` inside `apps/backend/src/edulafia/modules/finance/`.
- Implement endpoints for all major gateways: `POST /v1/finance/webhooks/paystack`, `POST /v1/finance/webhooks/flutterwave`, and `POST /v1/finance/webhooks/remita`.
- Each endpoint will verify the webhook signature/hash from the respective gateway, locate the corresponding pending `payment` record using the reference, and mark it as `completed`.
- Update `api/v1/router.py` to include the webhook router without standard authentication middleware.
**Frontend:**
- Update `apps/frontend/src/features/finance/FinancePage.tsx` to display a real-time status of webhook-confirmed payments in the ledger.

## 5. Centralized School Calendar
**Backend:**
- Create `apps/backend/src/edulafia/modules/calendar/`.
- Define `events` table (title, description, start_date, end_date, event_type, school_id).
- Expose endpoints to list, create, update, and delete events.
**Frontend:**
- Create `apps/frontend/src/features/calendar/CalendarPage.tsx`.
- Implement a monthly/weekly calendar view to display school events.
- Add "Calendar" to the `AppLayout.tsx` sidebar.

## 6. Alumni Network
**Backend:**
- Create `apps/backend/src/edulafia/modules/alumni/`.
- Define `alumni_profiles` table (student_id, graduation_year, current_occupation, university, linkedin_url, contact_email).
- Expose endpoints to register and list alumni.
**Frontend:**
- Create `apps/frontend/src/features/alumni/AlumniPage.tsx`.
- Implement an alumni directory with search and filter capabilities.
- Add "Alumni" to the `AppLayout.tsx` sidebar.

# Assumptions & Decisions
- **Chat:** Messages will be stored in PostgreSQL to leverage existing infrastructure, avoiding the complexity of Redis for now. Basic polling or simple WebSocket connections will be used.
- **File Storage:** Uploaded files for the LMS will be stored locally in a Docker volume (`/app/uploads`). This is simpler than configuring AWS S3 but requires the server environment to persist the volume.
- **Webhooks:** The system will implement unified support for Paystack, Flutterwave, and Remita webhooks. It assumes the server will be publicly accessible to receive these POST requests.

# Verification
- Run `bun run type-check` and `bun run lint` in `apps/frontend/` to ensure no UI breakages.
- Write unit tests for the webhook signature verification logic in the backend.
- Start the application (`docker-compose up` or local dev servers) and verify all 6 new sidebar links render and route correctly.
- Test the file upload endpoint manually via Swagger UI to confirm files are saved to the local directory.
- Test the chat endpoint by sending a message and verifying it persists in the database.