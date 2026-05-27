# EduLafia Marketing Website - Secondary Pages Design

## Overview
This document specifies the architecture and design for the secondary pages of the EduLafia marketing website (`website/`). These pages are critical for capturing leads, addressing specific buyer personas (Private Schools vs. Government), and establishing trust regarding health and financial data.

## 1. Page Architecture & Routing

The Next.js App Router will be expanded with the following routes:

### 1.1 Solutions Pages
- `/solutions/private-schools`
  - **Goal:** Highlight operational efficiency, fee collection automation, and parent satisfaction.
  - **Key Sections:** Pain points (spreadsheets, unpaid fees), EduLafia solutions, ROI calculator CTA.
- `/solutions/government`
  - **Goal:** Focus on scale, health data intelligence, and compliance for SUBEB/MOE deployments.
  - **Key Sections:** Multi-school dashboard, outbreak detection (Sentinel Engine), donor-funded pilot CTA.

### 1.2 Conversion & Trust Pages
- `/book-demo`
  - **Goal:** Primary lead capture form.
  - **Key Sections:** Interactive form (Name, School Name, Role, Student Count), social proof sidebar.
- `/about`
  - **Goal:** Humanize the brand and state the mission.
  - **Key Sections:** "Built for Nigeria" narrative, team overview, company timeline.
- `/security`
  - **Goal:** Overcome objections regarding sensitive student health and financial data.
  - **Key Sections:** Encryption standards, compliance (NDPR), data residency, infrastructure reliability.

### 1.3 Legal Pages
- `/legal/privacy` (Privacy Policy)
- `/legal/terms` (Terms of Service)

## 2. Shared UI Components

To maintain the premium, sleek aesthetic established on the homepage, we will build the following reusable components:

- `PageHeader.tsx`: A consistent hero component for secondary pages featuring a subtle gradient background and a bold title.
- `LeadForm.tsx`: A form component with floating labels and sleek focus states (Tailwind `focus-within:ring`), built to handle demo requests.
- `Accordion.tsx` (or Shadcn Accordion): For the FAQ section on the pricing page and detailed policies on the Security page.

## 3. Navigation Updates

The global `Navbar` and `Footer` will be updated to:
- Use `next/link` for client-side routing.
- Point "Sign In" to `app.edulafia.com` (external application URL).
- Link all "Book a Demo" and "Get Started" buttons to the `/book-demo` route.
- Populate the Footer with the new `/about`, `/security`, and `/legal/*` links.

## 4. Aesthetics & Motion
- All new pages will utilize the existing `bg-slate-950` dark theme.
- Framer Motion will be used for subtle page entrance animations (e.g., `initial={{ opacity: 0, y: 10 }}`).
- The `LeadForm` will feature interactive validation feedback without relying on standard browser tooltips.

## 5. Testing & Verification
- Ensure all internal links resolve correctly (no 404s).
- Verify responsive behavior of the `LeadForm` on mobile devices.
- Confirm accessibility (`aria-label` on form inputs, focus states on all interactive elements).