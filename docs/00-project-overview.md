# EduLafia Platform - Project Overview

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft

## 1. Introduction

### 1.1 What is EduLafia?
EduLafia is Nigeria's most comprehensive school management and adolescent health surveillance platform. It combines five school management modules (student records, academics, attendance, finance, and health) with an embedded, automated disease surveillance engine (the LafiyaSentinel layer) that turns every enrolled school into a real-time public health early-warning node.

### 1.2 Mission Statement
EduLafia exists to give Nigerian secondary schools the operational infrastructure they deserve and to give Nigeria's public health system the adolescent health surveillance capability it has never had — by making one product indispensable to schools and invaluable to governments.

### 1.3 Vision Statement
A Nigeria where every secondary school student has a complete digital health and academic record from enrolment to graduation — and where no disease outbreak begins in a school without the health system knowing about it first.

## 2. Problem Statement

### 2.1 The School Administration Crisis
The average Nigerian secondary school headteacher manages hundreds of student records with no digital system. Fee collection is tracked in handwritten ledgers. Attendance registers are paper-based, often completed in arrears, and never analysed. Report cards are typed manually at the end of each term — a process that takes weeks.

### 2.2 The Adolescent Health Invisibility Problem
Nigeria's adolescent population — roughly 11-to-18-year-olds in secondary school — is among the most data-invisible health populations in the country. School health programmes have existed on paper since the National School Health Policy of 2006 but have almost no digital implementation anywhere in Nigeria.

### 2.3 The Data Gap for Government
Nigeria's Federal Ministry of Health has no real-time adolescent health surveillance capability. The Federal Ministry of Education's EMIS (Education Management Information System) relies on annual paper returns from schools that are often incomplete, inaccurate, or submitted years late.

## 3. Solution Overview

### 3.1 Core Value Proposition
EduLafia gives schools a platform they actually need and can afford — one that dramatically reduces administrative burden and impresses parents — while simultaneously generating the most valuable adolescent health dataset Nigeria has never had.

### 3.2 Key Features
1. **Offline-First Design**: Works without internet connectivity
2. **WhatsApp-Native Communication**: Parent engagement via WhatsApp
3. **Real-Time Surveillance**: Automated disease outbreak detection
4. **Comprehensive Modules**: 9 integrated modules covering all school operations
5. **Government Integration**: EMIS and DHIS2 compatibility

## 4. Target Market

### 4.1 Primary Market: Private Secondary Schools
- Budget private schools: ~25,000 schools (₦60,000–₦90,000/year)
- Mid-tier private schools: ~8,000 schools (₦90,000–₦150,000/year)
- Premium private schools: ~2,000 schools (₦150,000–₦250,000/year)
- International-curriculum schools: ~500 schools (₦250,000+/year)

### 4.2 Scale Market: State Government Schools
Hundreds of schools in a single procurement contract, funded through SUBEB, State Ministry of Education budgets, or donor grants.

### 4.3 Prestige Market: Federal Government Colleges
110 Federal Government Colleges (FGCs) - well-funded, politically visible, and nationally distributed.

## 5. Technology Stack

### 5.1 Backend
- **Framework**: Python FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Background Tasks**: Celery
- **Hosting**: AWS Lagos (af-south-1) for NDPA compliance

### 5.2 Frontend
- **Type**: Progressive Web Application (PWA)
- **Framework**: React/TypeScript
- **Offline Storage**: IndexedDB + PouchDB
- **Styling**: Tailwind CSS

### 5.3 Integrations
- **SMS**: Termii Gateway
- **WhatsApp**: WhatsApp Business API via Nigerian BSP
- **Payments**: Paystack, Flutterwave, Remita
- **Analytics**: Apache Superset

## 6. Project Scope

### 6.1 Core Modules (M1-M5)
1. Student Information System (SIS)
2. Academic & Grading System
3. Attendance & Absence Tracking
4. Fee & Finance Management
5. School Health & Sentinel Engine

### 6.2 Extended Modules (M6-M9)
6. Teacher & Staff Management
7. Parent & Guardian Portal
8. Intelligence & Analytics Dashboard
9. System Administration & Onboarding

### 6.3 Key Technical Requirements
- Offline-first architecture
- NDPA 2023 compliance
- WCAG 2.1 AA accessibility
- Support for English, Igbo, and Hausa languages
- Real-time surveillance alerts within 15 minutes

## 7. Success Metrics

### 7.1 Pilot Phase (2026)
- 30–50 enrolled schools
- 15,000–25,000 students covered
- Annual recurring revenue: ₦4.5M–₦9M

### 7.2 Scale Phase (2027)
- 150–200 enrolled schools
- 75,000–100,000 students covered
- Annual recurring revenue: ₦22M–₦40M

### 7.3 National Phase (2028-2029)
- 1,000+ enrolled schools
- 500,000+ students covered
- Annual recurring revenue: ₦120M+

## 8. Project Constraints

### 8.1 Technical Constraints
- Offline-first requirement increases development complexity
- Must work on Android 8.0+ with Chrome browser
- Data residency requirement (all data must stay in Nigeria)
- Must support intermittent 3G connectivity

### 8.2 Business Constraints
- Early-stage company with limited engineering bandwidth
- Government procurement cycles are slow and unpredictable
- Data quality depends on teacher training and engagement

## 9. Documentation Purpose

### 9.1 For LLM Code Agent
This documentation package provides a comprehensive specification for an LLM code agent to implement the EduLafia platform. It includes:

1. **Architecture Specification**: How the system should be built
2. **Data Models**: Database schemas and relationships
3. **API Specifications**: All endpoints and data flows
4. **Module Specifications**: Detailed requirements for each module
5. **Implementation Guides**: Technical implementation details
6. **Testing Strategy**: How to verify the implementation
7. **Deployment Guide**: How to deploy the system

### 9.2 Documentation Structure
```
docs/
├── 00-project-overview.md (this file)
├── 01-technical-architecture.md
├── 02-data-model.md
├── 03-api-specification.md
├── 04-module-specifications/
│   ├── 04-01-student-information-system.md
│   ├── 04-02-academic-grading.md
│   ├── 04-03-attendance-tracking.md
│   ├── 04-04-fee-finance.md
│   ├── 04-05-school-health-sentinel.md
│   ├── 04-06-teacher-staff.md
│   ├── 04-07-parent-guardian-portal.md
│   ├── 04-08-intelligence-analytics.md
│   └── 04-09-system-administration.md
├── 05-integration-specifications.md
├── 06-development-setup.md
├── 07-coding-standards.md
├── 08-offline-first-implementation.md
├── 09-security-guidelines.md
├── 10-testing-strategy.md
├── 11-deployment-guide.md
└── 12-ui-ux-guidelines.md
```

## 10. How to Use This Documentation

### 10.1 For Developers
1. Start with `01-technical-architecture.md` to understand the system design
2. Review `02-data-model.md` for database schemas
3. Use `03-api-specification.md` for API implementation
4. Refer to module specifications for specific feature requirements
5. Follow `07-coding-standards.md` for consistent code style

### 10.2 For Project Managers
1. Review `00-project-overview.md` for project scope
2. Use module specifications for feature tracking
3. Reference `10-testing-strategy.md` for QA planning
4. Use `11-deployment-guide.md` for deployment planning

### 10.3 For QA Engineers
1. Use `10-testing-strategy.md` for test planning
2. Refer to module specifications for acceptance criteria
3. Use `09-security-guidelines.md` for security testing
4. Reference `08-offline-first-implementation.md` for offline testing

## 11. Next Steps

### 11.1 Immediate Actions
1. Set up development environment using `06-development-setup.md`
2. Create database using `02-data-model.md`
3. Implement API endpoints using `03-api-specification.md`
4. Build core modules using module specifications

### 11.2 Development Phases
1. **Phase 1**: Core backend (FastAPI + PostgreSQL)
2. **Phase 2**: Offline-first PWA frontend
3. **Phase 3**: Module implementation
4. **Phase 4**: Integration implementation
5. **Phase 5**: Testing and deployment

## 12. Support and Resources

### 12.1 Technical Resources
- PRD: `../EduLafia_PRD_v2.0.md`
- API Documentation: `03-api-specification.md`
- Database Schema: `02-data-model.md`

### 12.2 Contact Information
- **Product Owner**: LafiyaCore Product Team
- **Technical Lead**: LafiyaCore CTO
- **Email**: hello@lafiyacore.com
- **Website**: www.lafiyacore.com

---

*EduLafia — where education and health finally meet.*
*A LafiyaCore Product · RC 9347000*

---

**End of Project Overview**