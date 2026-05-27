# EduLafia Marketing Website Design & Strategy

## Overview
A premium, sleek, and professional standalone marketing website for EduLafia. This website serves as the primary funnel for converting school administrators, proprietors, and state governments into active users. It sits outside the core application (`apps/`) in a dedicated `website/` directory.

## Business Strategy & Positioning
As a strategic business asset, the website's primary objective is to build trust, demonstrate the tangible ROI of digitized school management and health records, and capture high-intent leads across different market segments in Nigeria.

### Target Audience
1. **Private School Proprietors (Decision Makers)**
2. **School Administrators / Headteachers (Influencers/Users)**
3. **State Governments / SUBEB (Scale Market)**
4. **Donors / NGOs (Scale Market)**

### Value Proposition (The "Hook")
"Transform your school's administration, improve student health outcomes, and increase parent engagement—all from one unified platform built for Nigeria."

## Architecture & Tech Stack
- **Framework:** Next.js (App Router) for optimal SEO and performance.
- **Styling:** Tailwind CSS + Framer Motion for sleek, premium animations that build credibility.
- **UI Components:** Shadcn/ui for accessible, consistent, and beautiful interactive elements.
- **Location:** `website/` directory at the repository root.

## Page Structure & Funnel Flow

### 1. Homepage (The Conversion Engine)
- **Hero Section:** High-contrast, premium aesthetic with a clear value proposition and dual CTAs ("Start Free Trial" & "Book a Demo").
- **Social Proof:** Logos of pilot schools, state partners, or donor organizations.
- **Problem vs. Solution:** Visual comparison of manual paper records vs. the EduLafia dashboard.
- **Core Pillars (Features):**
  - Smart Attendance & Administration
  - Sentinel Engine (Health & Immunization)
  - Parent Portal & Notifications
  - Financials & Fee Collection
- **Testimonials:** Quotes from proprietors highlighting time saved and increased parent satisfaction.

### 2. Pricing Page (Strategic 3-Tier Model + ROI)
A transparent, psychology-driven pricing page designed to anchor value.

- **Interactive ROI Calculator:** "How much time and money can EduLafia save your school?" (Inputs: # of students, current paper/SMS costs -> Output: Estimated savings).
- **The Tiers:**
  - **Starter (₦60,000/year):** Up to 200 students. Perfect for budget private schools. Includes 5 core modules + basic health.
  - **Standard (₦120,000/year):** 201–500 students. The sweet spot. Includes full Sentinel Engine, parent portal, and Paystack integration.
  - **Enterprise/Premium:** 500+ students or State Governments. Custom pricing. "Contact Sales" CTA.
- **FAQ Section:** Overcoming objections (e.g., "Do parents need smartphones?", "Is our data secure?").

### 3. Solutions Pages (Segment-Specific Landing Pages)
- `/solutions/private-schools`: Focused on fee collection, parent satisfaction, and operational efficiency.
- `/solutions/government`: Focused on scale, health data intelligence, and compliance.

### 4. About & Trust Center
- Company mission, team, and security/privacy commitments (crucial for health data).

## Design System & Aesthetics
- **Color Palette:** Deep navy/indigo (trust, professionalism) combined with vibrant teal/green accents (health, growth).
- **Typography:** Modern, clean sans-serif (e.g., Inter or Plus Jakarta Sans) for high legibility.
- **Imagery:** High-quality, relatable photography of Nigerian school environments, paired with abstract, clean UI mockups of the EduLafia platform.

## Lead Capture & Funnel Mechanics
- Sticky navigation bar with a prominent "Get Started" button.
- Exit-intent modal offering a downloadable guide ("The 2026 Guide to Digitizing Your School in Nigeria").
- Direct integration with a CRM or email marketing tool for lead nurturing.

## Implementation Phases
1. **Phase 1:** Scaffold Next.js project in `website/`, configure Tailwind and Shadcn.
2. **Phase 2:** Build global components (Nav, Footer, Buttons, Cards).
3. **Phase 3:** Develop Homepage and integrate Framer Motion animations.
4. **Phase 4:** Develop Pricing page with interactive ROI calculator.
5. **Phase 5:** Final polish, SEO optimization, and responsive testing.
