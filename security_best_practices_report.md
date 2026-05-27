# Security Best Practices Report

## Executive Summary
This report outlines the security posture of the frontend React application (`apps/frontend/src/features/`). The application generally follows good practices by leveraging Material-UI and React's built-in escaping mechanisms, which effectively mitigates common Cross-Site Scripting (XSS) risks. No hardcoded secrets or instances of `dangerouslySetInnerHTML` were detected. However, several vulnerabilities related to session handling, client-side validation, and state management require attention to meet enterprise-grade security standards and NDPA 2023 compliance.

## Findings

### 1. High Severity: Poor Auth/Session Checks & Insecure Data Handling (IDOR Risk)
- **Impact:** An attacker could manipulate the `schoolId` in Local Storage to view sensitive dashboard data of other schools if backend authorization is insufficient.
- **Location:** `apps/frontend/src/features/dashboard/DashboardPage.tsx` (Lines 9–15)
- **Description:** The application directly retrieves a `schoolId` from `localStorage` (`localStorage.getItem('schoolId')`) without any validation or cryptographic verification. A developer comment explicitly notes: `// Get school id from local storage or context (in a real app, this would come from auth context)`.
- **Recommendation:** Migrate state retrieval to a secure Authentication/Authorization Context. Ensure the backend strictly validates that the requesting user has permissions for the requested `schoolId`.

### 2. Medium Severity: Missing Client-Side Form Validation
- **Impact:** Submitting malformed or incomplete data can result in unhandled application exceptions, excessive load on the backend, and poor user experience.
- **Locations:** 
  - `apps/frontend/src/features/students/StudentsPage.tsx` (Lines 107–109)
  - `apps/frontend/src/features/auth/ResetPasswordPage.tsx` (Lines 25–45)
  - `apps/frontend/src/features/health/HealthPage.tsx` (Lines 478–488)
- **Description:** The application relies almost entirely on basic HTML5 validation and backend validation. Form payloads are frequently typecast directly without verifying that required fields are populated or that data matches expected formats.
- **Recommendation:** Implement a client-side schema validation library (such as Zod or Yup) coupled with your form state to strictly enforce payload shapes before executing mutations.

### 3. Low Severity: Information Disclosure via Direct Error Reflection
- **Impact:** Reflecting backend errors to the frontend can result in Information Disclosure if the backend accidentally returns stack traces or database schema details.
- **Location:** `apps/frontend/src/features/auth/ResetPasswordPage.tsx` (Lines 42–43)
- **Description:** In the catch block of the password reset handler, the application sets the error state directly from the backend response: `setError(e?.response?.data?.detail || 'Failed to reset password');`. 
- **Recommendation:** Map known backend error codes to safe, predefined user-facing error messages on the frontend rather than directly rendering the raw API response.

### 4. Low Severity: Insecure Routing Practices
- **Impact:** Bypasses the Single Page Application (SPA) router, causing full page reloads which drop all active frontend state, including potentially critical security contexts or tokens held in memory.
- **Locations:** 
  - `apps/frontend/src/features/auth/LoginPage.tsx` (Lines 69–71)
  - `apps/frontend/src/features/auth/ResetPasswordPage.tsx` (Lines 69, 102, 169)
  - `apps/frontend/src/features/auth/ForgotPasswordPage.tsx` (Line 91)
- **Description:** The authentication pages use standard `<a>` tags with hardcoded `href` attributes instead of the application's dedicated router components (`<Link>` from `@tanstack/react-router`).
- **Recommendation:** Replace standard anchor tags with the `@tanstack/react-router` `<Link>` component.

## Clean Findings
- **XSS & Unescaped HTML:** No instances of `dangerouslySetInnerHTML`, `eval()`, `javascript:` URIs, or unescaped HTML were detected.
- **Hardcoded Secrets:** No hardcoded API keys, JWTs, or passwords were found in the scanned files.