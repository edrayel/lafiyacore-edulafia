# EduLafia Platform - Module Specification: Intelligence & Analytics Dashboard (M8)

## Document Information
- **Version:** 1.0
- **Date:** March 2026
- **Author:** LafiyaCore Technical Team
- **Status:** Draft
- **Module:** M8 - Intelligence & Analytics Dashboard
- **Priority:** Medium (Extended Module)
- **LafiyaSentinel Layer:** YES — Surveillance analytics surface here

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Data Model Implementation](#3-data-model-implementation)
4. [API Implementation](#4-api-implementation)
5. [Business Logic Implementation](#5-business-logic-implementation)
6. [UI Component Specifications](#6-ui-component-specifications)
7. [Testing Requirements](#7-testing-requirements)
8. [Security Considerations](#8-security-considerations)
9. [Performance Requirements](#9-performance-requirements)
10. [Integration Points](#10-integration-points)
11. [Implementation Checklist](#11-implementation-checklist)

## 1. Module Overview

### 1.1 Purpose
The Intelligence & Analytics Dashboard module provides comprehensive data analytics and reporting capabilities at school, LGA, state, and national levels. It aggregates data from all other modules to provide actionable insights for school administrators, education officials, health officers, and researchers. This module includes the Sentinel surveillance analytics dashboard for disease outbreak monitoring.

### 1.2 Scope
- School-level dashboards and KPIs
- LGA-level aggregated analytics
- State-level surveillance and education dashboards
- National-level reporting and data export
- Anonymized data portal for researchers
- Real-time and historical analytics
- Geospatial mapping of health signals
- EMIS and IDSR export capabilities
- Custom report generation
- Data visualization and charts

### 1.3 Dependencies
- **Required Modules:** All other modules (M1-M7) provide data
- **External Dependencies:** Apache Superset for advanced analytics, mapping services
- **Data Sources:** All module data feeds into intelligence layer

## 2. Functional Requirements

### 2.1 Core Capabilities

#### 2.1.1 School-Level Dashboard
```yaml
Feature: School-Level Dashboard
Description: Daily management dashboard for school administrators
Acceptance Criteria:
  - Morning snapshot: attendance rate, health alerts, pending fees, academic alerts
  - Single screen view loading in under 5 seconds
  - Real-time data updates
  - Drill-down capability to student details
  - Customizable widget layout
  - Alert prioritization (urgent, high, normal, low)
  - Quick action buttons (mark attendance, view alerts)
  - Term-end report generation (one-click)
  - Comparison with previous terms
  - Export capabilities (PDF, CSV)
```

#### 2.1.2 LGA-Level Dashboard
```yaml
Feature: LGA-Level Dashboard
Description: Aggregated analytics for Local Government Education Authority
Acceptance Criteria:
  - Education metrics: enrolment by school, attendance rates, academic performance comparison
  - Health metrics: illness signal map, alert history, outbreak investigation status
  - Vaccination coverage by school and antigen
  - School performance ranking
  - Resource allocation insights
  - EMIS-compatible data export
  - Comparative analysis across schools
  - Trend analysis over time
  - Geospatial visualization
  - Drill-down to school level (with authorization)
```

#### 2.1.3 State-Level Dashboard
```yaml
Feature: State-Level Dashboard
Description: Comprehensive state-level analytics for Ministry officials
Acceptance Criteria:
  - Education: EMIS-compatible aggregate, performance benchmarking by LGA
  - Health: Sentinel surveillance overview, time-series disease trends
  - Geographic cluster analysis for outbreak detection
  - IDSR-formatted export for Federal Ministry of Health
  - Historical trend analysis (multi-year)
  - Cross-LGA comparison
  - Policy impact analysis
  - Resource allocation optimization
  - Predictive analytics for planning
  - Automated reporting to federal agencies
```

#### 2.1.4 Sentinel Surveillance Dashboard
```yaml
Feature: Sentinel Surveillance Dashboard
Description: Disease surveillance and outbreak monitoring
Acceptance Criteria:
  - Real-time illness signal heat map
  - Active alerts list with status tracking
  - Symptom trend charts over time
  - Geographic cluster visualization
  - School comparison matrix
  - Alert history timeline
  - Threshold configuration panel
  - Outbreak investigation workflow
  - Correlation with confirmed outbreaks
  - Model accuracy tracking
  - Retrospective analysis tools
```

#### 2.1.5 Anonymized Data Portal
```yaml
Feature: Anonymized Data Portal
Description: Secure data access for researchers and donors
Acceptance Criteria:
  - Self-service data request application
  - Required fields: organization, intended use, ethics approval reference
  - LafiyaCore review workflow (5 business days)
  - Granularity controls (minimum population size)
  - Anonymized dataset delivery as encrypted CSV
  - Usage tracking and audit
  - MOU management
  - Data use agreement enforcement
  - Access revocation capability
  - Usage analytics for LafiyaCore
```

#### 2.1.6 Custom Report Generation
```yaml
Feature: Custom Report Generation
Description: Generate custom reports and exports
Acceptance Criteria:
  - Report template builder
  - Data selection (modules, date range, schools)
  - Visualization options (charts, tables, maps)
  - Export formats: PDF, CSV, Excel, JSON
  - Scheduled report generation
  - Email delivery of reports
  - Report sharing with stakeholders
  - Version control for reports
  - Comparison reports (term-over-term, year-over-year)
  - Benchmark reports (school vs. LGA average)
```

### 2.2 Business Rules

#### 2.2.1 Data Aggregation Business Rules
1. **Anonymization:** Individual student data never exposed at LGA/state level
2. **Minimum Threshold:** No aggregates shown for populations <10 students
3. **Data Freshness:** Dashboard data updated at least daily; Sentinel data near real-time
4. **Historical Data:** 5 years of historical data retained for analysis
5. **Data Quality:** Incomplete data flagged in dashboards
6. **Access Control:** Role-based access to different dashboard levels
7. **Audit Trail:** All data access logged for compliance
8. **Export Control:** Bulk exports require approval

#### 2.2.2 Dashboard Business Rules
1. **Performance:** Dashboard loads in under 5 seconds
2. **Refresh:** Auto-refresh every 5 minutes for real-time data
3. **Offline Access:** Cached data available offline
4. **Mobile Responsive:** Dashboards work on tablets and phones
5. **Print Friendly:** Dashboard views optimized for printing
6. **Accessibility:** WCAG 2.1 AA compliance
7. **Branding:** Customizable branding for government dashboards
8. **Localization:** Support for English, Igbo, Hausa

#### 2.2.3 Sentinel Analytics Business Rules
1. **Data Latency:** Sentinel alerts within 15 minutes of threshold crossing
2. **False Positive Management:** Historical calibration to reduce false positives
3. **Threshold Tuning:** Configurable thresholds per state/LGA
4. **Alert Retention:** All alerts retained for 7 years
5. **Model Validation:** Regular validation against confirmed outbreaks
6. **Geographic Accuracy:** School geolocation verified annually
7. **Privacy:** Individual student data never exposed in Sentinel analytics

## 3. Data Model Implementation

### 3.1 Database Tables
```sql
-- Dashboard configurations
CREATE TABLE dashboard_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_type VARCHAR(50) NOT NULL CHECK (dashboard_type IN ('school', 'lga', 'state', 'sentinel', 'researcher')),
    owner_type VARCHAR(50) NOT NULL CHECK (owner_type IN ('school', 'lga', 'state', 'system')),
    owner_id UUID NOT NULL,  -- school_id, lga_id, or state_id
    name VARCHAR(255) NOT NULL,
    layout JSONB NOT NULL,  -- Widget positions and configurations
    refresh_interval INTEGER DEFAULT 300,  -- seconds
    is_default BOOLEAN DEFAULT FALSE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Dashboard widgets
CREATE TABLE dashboard_widgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_id UUID NOT NULL REFERENCES dashboard_configurations(id) ON DELETE CASCADE,
    widget_type VARCHAR(50) NOT NULL CHECK (widget_type IN ('kpi_card', 'chart', 'table', 'map', 'alert_feed', 'trend')),
    title VARCHAR(255) NOT NULL,
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    config JSONB NOT NULL,  -- Widget-specific configuration
    data_source VARCHAR(100) NOT NULL,  -- Which module/data to display
    refresh_interval INTEGER,  -- Override dashboard refresh
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- KPI definitions
CREATE TABLE kpi_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kpi_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    data_source VARCHAR(100) NOT NULL,
    calculation_query JSONB NOT NULL,  -- Query definition
    unit VARCHAR(20),  -- percent, count, currency, rate
    target_value DECIMAL(10,2),
    warning_threshold DECIMAL(10,2),
    critical_threshold DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- School KPIs (daily snapshots)
CREATE TABLE school_kpi_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    kpi_code VARCHAR(50) NOT NULL REFERENCES kpi_definitions(kpi_code),
    value DECIMAL(15,4) NOT NULL,
    previous_value DECIMAL(15,4),
    trend VARCHAR(20) CHECK (trend IN ('up', 'down', 'stable')),
    metadata JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(school_id, snapshot_date, kpi_code)
);

-- Indexes for KPI snapshots
CREATE INDEX idx_school_kpi_date ON school_kpi_snapshots(school_id, snapshot_date);
CREATE INDEX idx_school_kpi_code ON school_kpi_snapshots(kpi_code, snapshot_date);

-- LGA aggregates
CREATE TABLE lga_aggregates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lga VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    aggregate_date DATE NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL CHECK (aggregate_type IN ('daily', 'weekly', 'monthly', 'termly', 'yearly')),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    school_count INTEGER,
    student_count INTEGER,
    metadata JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(lga, state, aggregate_date, aggregate_type, metric_name)
);

-- State aggregates
CREATE TABLE state_aggregates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state VARCHAR(100) NOT NULL,
    aggregate_date DATE NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL CHECK (aggregate_type IN ('daily', 'weekly', 'monthly', 'termly', 'yearly')),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    lga_count INTEGER,
    school_count INTEGER,
    student_count INTEGER,
    metadata JSONB,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(state, aggregate_date, aggregate_type, metric_name)
);

-- Research data requests
CREATE TABLE research_data_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization VARCHAR(255) NOT NULL,
    requester_name VARCHAR(255) NOT NULL,
    requester_email VARCHAR(255) NOT NULL,
    intended_use TEXT NOT NULL,
    ethics_approval_reference VARCHAR(255),
    data_set_required VARCHAR(100) NOT NULL,
    date_range JSONB NOT NULL,  -- {start: "YYYY-MM-DD", end: "YYYY-MM-DD"}
    geographic_scope JSONB,  -- {states: [], lgas: [], schools: []}
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'delivered', 'expired')),
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    review_notes TEXT,
    data_file_url VARCHAR(500),
    data_file_expires_at TIMESTAMP WITH TIME ZONE,
    usage_agreement_accepted BOOLEAN DEFAULT FALSE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Report templates
CREATE TABLE report_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID REFERENCES schools(id),  -- NULL for system-wide templates
    name VARCHAR(255) NOT NULL,
    description TEXT,
    report_type VARCHAR(50) NOT NULL CHECK (report_type IN ('attendance', 'academic', 'finance', 'health', 'sentinel', 'custom')),
    data_sources JSONB NOT NULL,  -- Which modules/data to include
    filters JSONB,  -- Default filters
    columns JSONB,  -- Which columns to include
    group_by JSONB,  -- Grouping configuration
    charts JSONB,  -- Chart configurations
    is_system_template BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    version INTEGER DEFAULT 1
);

-- Generated reports
CREATE TABLE generated_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES report_templates(id),
    school_id UUID REFERENCES schools(id),
    lga VARCHAR(100),
    state VARCHAR(100),
    report_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    parameters JSONB NOT NULL,  -- Filters and date ranges used
    generated_by UUID NOT NULL REFERENCES users(id),
    file_url VARCHAR(500),
    file_format VARCHAR(10) CHECK (file_format IN ('pdf', 'csv', 'excel', 'json')),
    file_size INTEGER,
    status VARCHAR(20) DEFAULT 'generating' CHECK (status IN ('generating', 'completed', 'failed')),
    error_message TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    download_count INTEGER DEFAULT 0,
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);
```

### 3.2 Materialized Views for Performance
```sql
-- Daily school KPI materialized view (refreshed nightly)
CREATE MATERIALIZED VIEW mv_daily_school_kpis AS
SELECT 
    s.id as school_id,
    s.name as school_name,
    s.lga,
    s.state,
    CURRENT_DATE as snapshot_date,
    
    -- Attendance KPI
    (
        SELECT ROUND(
            COUNT(CASE WHEN ar.status = 'present' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0),
            2
        )
        FROM attendance_records ar
        WHERE ar.school_id = s.id 
            AND ar.date = CURRENT_DATE - INTERVAL '1 day'
    ) as yesterday_attendance_rate,
    
    -- Health KPI
    (
        SELECT COUNT(*)
        FROM sick_bay_visits sbv
        WHERE sbv.school_id = s.id 
            AND DATE(sbv.visit_date) = CURRENT_DATE - INTERVAL '1 day'
    ) as yesterday_sick_bay_visits,
    
    -- Finance KPI
    (
        SELECT COALESCE(SUM(fl.amount), 0)
        FROM fee_ledger fl
        WHERE fl.school_id = s.id 
            AND fl.transaction_type = 'payment'
            AND DATE(fl.transaction_date) = CURRENT_DATE - INTERVAL '1 day'
    ) as yesterday_collections,
    
    -- Active alerts
    (
        SELECT COUNT(*)
        FROM sentinel_signals ss
        WHERE s.id = ANY(ss.school_ids)
            AND ss.status = 'open'
    ) as open_sentinel_alerts
    
FROM schools s
WHERE s.status = 'active' AND s.deleted_at IS NULL;

-- Create index on materialized view
CREATE UNIQUE INDEX idx_mv_daily_school_kpis ON mv_daily_school_kpis(school_id, snapshot_date);

-- LGA daily summary materialized view
CREATE MATERIALIZED VIEW mv_lga_daily_summary AS
SELECT 
    s.lga,
    s.state,
    CURRENT_DATE as summary_date,
    COUNT(DISTINCT s.id) as school_count,
    COUNT(DISTINCT st.id) as student_count,
    
    -- Aggregate attendance
    ROUND(AVG(
        (SELECT COUNT(CASE WHEN ar.status = 'present' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)
         FROM attendance_records ar
         WHERE ar.school_id = s.id AND ar.date = CURRENT_DATE - INTERVAL '1 day')
    ), 2) as avg_attendance_rate,
    
    -- Aggregate sick bay visits
    SUM(
        (SELECT COUNT(*)
         FROM sick_bay_visits sbv
         WHERE sbv.school_id = s.id AND DATE(sbv.visit_date) = CURRENT_DATE - INTERVAL '1 day')
    ) as total_sick_bay_visits,
    
    -- Open Sentinel alerts
    SUM(
        (SELECT COUNT(*)
         FROM sentinel_signals ss
         WHERE s.id = ANY(ss.school_ids) AND ss.status = 'open')
    ) as total_open_alerts
    
FROM schools s
LEFT JOIN students st ON s.id = st.school_id AND st.status = 'active'
WHERE s.status = 'active' AND s.deleted_at IS NULL
GROUP BY s.lga, s.state;

-- Refresh function for materialized views
CREATE OR REPLACE FUNCTION refresh_dashboard_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_school_kpis;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_lga_daily_summary;
END;
$$ LANGUAGE plpgsql;
```

## 4. API Implementation

### 4.1 Endpoints to Implement

#### 4.1.1 School Dashboard Endpoints
```yaml
Endpoints:
  GET /api/v1/intelligence/school/{school_id}/dashboard:
    - Description: Get school dashboard data
    - Query Parameters: date, term_id
    - Response: SchoolDashboardResponse schema
    - Auth: Required (school_admin)
    - Includes:
      - KPI cards (attendance, health, finance, academic)
      - Alert feed
      - Quick stats
      - Trend charts
    - Performance: < 5 seconds

  GET /api/v1/intelligence/school/{school_id}/kpis:
    - Description: Get school KPIs
    - Query Parameters: date_range, kpi_codes
    - Response: List of SchoolKPIResponse
    - Auth: Required (school_admin)

  GET /api/v1/intelligence/school/{school_id}/alerts:
    - Description: Get school alerts
    - Query Parameters: type, status, priority, date_range
    - Response: Paginated list of AlertResponse
    - Auth: Required (school_admin)

  GET /api/v1/intelligence/school/{school_id}/report:
    - Description: Generate school term report
    - Query Parameters: term_id, format
    - Response: Report file (PDF/CSV)
    - Auth: Required (school_admin)
    - Business Rules:
      - One-click generation
      - Covers all modules
      - School branding
```

#### 4.1.2 LGA Dashboard Endpoints
```yaml
Endpoints:
  GET /api/v1/intelligence/lga/{lga}/dashboard:
    - Description: Get LGA dashboard
    - Query Parameters: state, date
    - Response: LGADashboardResponse schema
    - Auth: Required (lga_education, lga_health)
    - Includes:
      - Education metrics
      - Health metrics
      - School performance list
      - Alert summary
    - Business Rules:
      - Anonymized student data
      - Minimum thresholds applied

  GET /api/v1/intelligence/lga/{lga}/schools:
    - Description: Get LGA school comparison
    - Query Parameters: state, metric
    - Response: List of SchoolComparisonResponse
    - Auth: Required (lga_education)

  GET /api/v1/intelligence/lga/{lga}/health-map:
    - Description: Get LGA health signal map
    - Query Parameters: state, date_range
    - Response: HealthMapResponse schema
    - Auth: Required (lga_health)
    - Includes:
      - Geographic distribution of signals
      - School pins with status
      - Heat map overlay

  GET /api/v1/intelligence/lga/{lga}/export/emis:
    - Description: Export LGA EMIS data
    - Query Parameters: state, term_id, format
    - Response: EMIS export file
    - Auth: Required (lga_education)
```

#### 4.1.3 State Dashboard Endpoints
```yaml
Endpoints:
  GET /api/v1/intelligence/state/{state}/dashboard:
    - Description: Get state dashboard
    - Query Parameters: date
    - Response: StateDashboardResponse schema
    - Auth: Required (state_education, state_health)
    - Includes:
      - State-wide education metrics
      - Sentinel surveillance overview
      - LGA comparison
      - Trend analysis

  GET /api/v1/intelligence/state/{state}/sentinel:
    - Description: Get state Sentinel dashboard
    - Query Parameters: date_range
    - Response: StateSentinelResponse schema
    - Auth: Required (state_health)
    - Includes:
      - Active alerts
      - Time-series trends
      - Geographic cluster analysis
      - Historical outbreak comparison

  GET /api/v1/intelligence/state/{state}/analytics:
    - Description: Get state analytics
    - Query Parameters: metric, period
    - Response: AnalyticsResponse schema
    - Auth: Required (state_education, state_health)
    - Features:
      - Predictive analytics
      - Trend analysis
      - Comparative analysis
      - What-if scenarios

  GET /api/v1/intelligence/state/{state}/export/idsr:
    - Description: Export IDSR data
    - Query Parameters: date_range, format
    - Response: IDSR export file
    - Auth: Required (state_health)
    - Business Rules:
      - IDSR-compliant format
      - Weekly and outbreak-triggered
```

#### 4.1.4 Sentinel Analytics Endpoints
```yaml
Endpoints:
  GET /api/v1/intelligence/sentinel/dashboard:
    - Description: Get Sentinel surveillance dashboard
    - Query Parameters: school_id, lga, state, date_range
    - Response: SentinelDashboardResponse schema
    - Auth: Required (school_admin, lga_health, state_health)
    - Includes:
      - Active alerts map
      - Symptom trends
      - Alert history
      - Threshold configuration
    - Performance: < 3 seconds

  GET /api/v1/intelligence/sentinel/alerts:
    - Description: Get Sentinel alerts
    - Query Parameters: tier, status, date_range
    - Response: Paginated list of SentinelAlertResponse
    - Auth: Required

  GET /api/v1/intelligence/sentinel/signals:
    - Description: Get illness signal data
    - Query Parameters: school_id, lga, state, date_range, symptom_category
    - Response: List of SignalResponse
    - Auth: Required

  GET /api/v1/intelligence/sentinel/clusters:
    - Description: Get geographic cluster analysis
    - Query Parameters: state, date_range
    - Response: ClusterAnalysisResponse schema
    - Auth: Required (state_health)
    - Includes:
      - Active clusters
      - Cluster boundaries
      - Severity indicators
      - Recommended actions

  GET /api/v1/intelligence/sentinel/trends:
    - Description: Get disease trend analysis
    - Query Parameters: state, symptom_category, period
    - Response: TrendAnalysisResponse schema
    - Auth: Required
    - Includes:
      - Time-series charts
      - Seasonal patterns
      - Year-over-year comparison
      - Predictive forecasts
```

#### 4.1.5 Research Data Portal Endpoints
```yaml
Endpoints:
  POST /api/v1/intelligence/research/requests:
    - Description: Submit data access request
    - Request Body: DataRequestCreate schema
    - Response: DataRequestResponse schema
    - Auth: Required (researcher - separate auth)
    - Business Rules:
      - Require ethics approval reference
      - LafiyaCore review required
      - 5 business day SLA

  GET /api/v1/intelligence/research/requests/{request_id}:
    - Description: Get request status
    - Response: DataRequestStatusResponse
    - Auth: Required (requester)

  GET /api/v1/intelligence/research/datasets:
    - Description: List available datasets
    - Query Parameters: category, geography
    - Response: List of DatasetResponse
    - Auth: Required (researcher)
    - Business Rules:
      - Shows aggregated, anonymized data
      - Minimum population thresholds applied

  GET /api/v1/intelligence/research/exports/{export_id}:
    - Description: Download approved dataset
    - Response: Encrypted CSV file
    - Auth: Required (requester)
    - Business Rules:
      - Time-limited access
      - Usage tracking
      - Download limited
```

#### 4.1.6 Report Generation Endpoints
```yaml
Endpoints:
  POST /api/v1/intelligence/reports/generate:
    - Description: Generate custom report
    - Request Body: ReportGenerateRequest schema
    - Response: ReportGenerationResponse schema
    - Auth: Required
    - Business Rules:
      - Async generation for large reports
      - Progress tracking
      - Email notification on completion

  GET /api/v1/intelligence/reports/templates:
    - Description: List available report templates
    - Query Parameters: school_id, report_type
    - Response: List of ReportTemplateResponse
    - Auth: Required

  POST /api/v1/intelligence/reports/templates:
    - Description: Create custom report template
    - Request Body: ReportTemplateCreate schema
    - Response: ReportTemplateResponse schema
    - Auth: Required (school_admin)

  GET /api/v1/intelligence/reports/{report_id}:
    - Description: Get report status/download
    - Response: ReportStatusResponse or file
    - Auth: Required
```

## 5. Business Logic Implementation

### 5.1 Dashboard Data Aggregation
```python
class DashboardService:
    async def get_school_dashboard(
        self,
        school_id: UUID,
        date: Optional[date] = None
    ) -> SchoolDashboard:
        """Get school dashboard data."""
        
        if not date:
            date = datetime.now().date()
        
        # 1. Get KPIs
        kpis = await self.get_school_kpis(school_id, date)
        
        # 2. Get active alerts
        alerts = await self.get_school_alerts(school_id)
        
        # 3. Get trends
        trends = await self.get_school_trends(school_id, days=30)
        
        # 4. Get quick stats
        quick_stats = await self.get_quick_stats(school_id, date)
        
        return SchoolDashboard(
            school_id=school_id,
            date=date,
            kpis=kpis,
            alerts=alerts,
            trends=trends,
            quick_stats=quick_stats,
            last_updated=datetime.utcnow()
        )
    
    async def get_school_kpis(
        self,
        school_id: UUID,
        date: date
    ) -> List[KPICard]:
        """Get school KPIs for dashboard."""
        
        kpis = []
        
        # Attendance KPI
        attendance_rate = await self.calculate_attendance_rate(school_id, date)
        kpis.append(KPICard(
            name='Attendance Rate',
            value=attendance_rate,
            unit='percent',
            trend=self.calculate_trend(attendance_rate, await self.get_previous_attendance(school_id, date)),
            target=95.0,
            status=self.get_kpi_status(attendance_rate, 95.0, 85.0)
        ))
        
        # Sick bay visits KPI
        sick_bay_visits = await self.get_sick_bay_count(school_id, date)
        kpis.append(KPICard(
            name='Sick Bay Visits',
            value=sick_bay_visits,
            unit='count',
            trend=self.calculate_trend(sick_bay_visits, await self.get_previous_sick_bay_count(school_id, date)),
            target=None,
            status='normal' if sick_bay_visits < 10 else 'warning'
        ))
        
        # Fee collection KPI
        collections = await self.get_daily_collections(school_id, date)
        outstanding = await self.get_total_outstanding(school_id)
        kpis.append(KPICard(
            name='Daily Collections',
            value=collections,
            unit='currency',
            trend=self.calculate_trend(collections, await self.get_previous_collections(school_id, date)),
            target=None,
            status='normal'
        ))
        
        kpis.append(KPICard(
            name='Outstanding Balance',
            value=outstanding,
            unit='currency',
            trend=self.calculate_trend(outstanding, await self.get_previous_outstanding(school_id, date)),
            target=None,
            status='warning' if outstanding > 1000000 else 'normal'  # ₦1M threshold
        ))
        
        # Sentinel alerts KPI
        open_alerts = await self.get_open_sentinel_alerts(school_id)
        kpis.append(KPICard(
            name='Open Health Alerts',
            value=open_alerts,
            unit='count',
            trend=None,
            target=0,
            status='critical' if open_alerts > 0 else 'normal'
        ))
        
        return kpis
    
    async def get_lga_dashboard(
        self,
        lga: str,
        state: str,
        date: Optional[date] = None
    ) -> LGADashboard:
        """Get LGA dashboard data."""
        
        if not date:
            date = datetime.now().date()
        
        # 1. Get LGA aggregates
        aggregates = await self.get_lga_aggregates(lga, state, date)
        
        # 2. Get school comparison
        school_comparison = await self.get_lga_school_comparison(lga, state)
        
        # 3. Get health signals
        health_signals = await self.get_lga_health_signals(lga, state, date)
        
        # 4. Get alert summary
        alert_summary = await self.get_lga_alert_summary(lga, state)
        
        return LGADashboard(
            lga=lga,
            state=state,
            date=date,
            aggregates=aggregates,
            school_comparison=school_comparison,
            health_signals=health_signals,
            alert_summary=alert_summary,
            last_updated=datetime.utcnow()
        )
    
    async def get_sentinel_dashboard(
        self,
        state: Optional[str] = None,
        lga: Optional[str] = None,
        school_id: Optional[UUID] = None,
        date_range: Optional[DateRange] = None
    ) -> SentinelDashboard:
        """Get Sentinel surveillance dashboard."""
        
        if not date_range:
            date_range = DateRange(
                start=datetime.now().date() - timedelta(days=30),
                end=datetime.now().date()
            )
        
        # 1. Get active alerts
        active_alerts = await self.get_active_alerts(state, lga, school_id)
        
        # 2. Get illness signal trends
        signal_trends = await self.get_signal_trends(state, lga, school_id, date_range)
        
        # 3. Get geographic clusters
        clusters = await self.get_active_clusters(state, lga, date_range)
        
        # 4. Get historical comparison
        historical = await self.get_historical_comparison(state, lga, date_range)
        
        # 5. Get model accuracy metrics
        accuracy = await self.get_model_accuracy(state, date_range)
        
        return SentinelDashboard(
            state=state,
            lga=lga,
            school_id=school_id,
            date_range=date_range,
            active_alerts=active_alerts,
            signal_trends=signal_trends,
            clusters=clusters,
            historical=historical,
            model_accuracy=accuracy,
            last_updated=datetime.utcnow()
        )
```

### 5.2 Data Aggregation Logic
```python
class DataAggregationService:
    async def aggregate_lga_daily(self, lga: str, state: str, date: date):
        """Aggregate daily data for LGA."""
        
        # 1. Get all schools in LGA
        schools = await self.get_schools_in_lga(lga, state)
        
        # 2. Calculate metrics
        total_students = 0
        total_attendance_rate = 0
        total_sick_bay_visits = 0
        total_collections = 0
        open_alerts = 0
        
        for school in schools:
            # Student count
            student_count = await self.get_student_count(school.id)
            total_students += student_count
            
            # Attendance rate
            attendance_rate = await self.calculate_attendance_rate(school.id, date)
            total_attendance_rate += attendance_rate * student_count  # Weighted
            
            # Sick bay visits
            sick_bay_visits = await self.get_sick_bay_count(school.id, date)
            total_sick_bay_visits += sick_bay_visits
            
            # Collections
            collections = await self.get_daily_collections(school.id, date)
            total_collections += collections
            
            # Open alerts
            school_alerts = await self.get_open_alerts_count(school.id)
            open_alerts += school_alerts
        
        # 3. Calculate averages
        avg_attendance_rate = total_attendance_rate / total_students if total_students > 0 else 0
        
        # 4. Store aggregates
        aggregates = [
            LGAAggregate(
                lga=lga,
                state=state,
                aggregate_date=date,
                aggregate_type='daily',
                metric_name='student_count',
                metric_value=total_students,
                school_count=len(schools)
            ),
            LGAAggregate(
                lga=lga,
                state=state,
                aggregate_date=date,
                aggregate_type='daily',
                metric_name='avg_attendance_rate',
                metric_value=avg_attendance_rate,
                school_count=len(schools),
                student_count=total_students
            ),
            LGAAggregate(
                lga=lga,
                state=state,
                aggregate_date=date,
                aggregate_type='daily',
                metric_name='total_sick_bay_visits',
                metric_value=total_sick_bay_visits,
                school_count=len(schools),
                student_count=total_students
            ),
            LGAAggregate(
                lga=lga,
                state=state,
                aggregate_date=date,
                aggregate_type='daily',
                metric_name='total_collections',
                metric_value=total_collections,
                school_count=len(schools)
            ),
            LGAAggregate(
                lga=lga,
                state=state,
                aggregate_date=date,
                aggregate_type='daily',
                metric_name='open_alerts',
                metric_value=open_alerts,
                school_count=len(schools),
                student_count=total_students
            )
        ]
        
        # 5. Bulk upsert
        for aggregate in aggregates:
            await self.upsert_aggregate(aggregate)
        
        await self.session.commit()
    
    async def calculate_school_kpis(self, school_id: UUID, date: date):
        """Calculate and store school KPIs for date."""
        
        kpi_calculators = {
            'ATTENDANCE_RATE': self.calculate_attendance_rate,
            'SICK_BAY_VISITS': self.get_sick_bay_count,
            'FEE_COLLECTIONS': self.get_daily_collections,
            'OPEN_ALERTS': self.get_open_alerts_count,
            'ACADEMIC_AVG': self.calculate_academic_average,
            'VACCINATION_COVERAGE': self.calculate_vaccination_coverage
        }
        
        for kpi_code, calculator in kpi_calculators.items():
            try:
                value = await calculator(school_id, date)
                
                # Get previous value for trend
                previous_value = await self.get_previous_kpi_value(
                    school_id, kpi_code, date
                )
                
                # Calculate trend
                trend = self.calculate_trend(value, previous_value)
                
                # Store snapshot
                snapshot = SchoolKPISnapshot(
                    school_id=school_id,
                    snapshot_date=date,
                    kpi_code=kpi_code,
                    value=value,
                    previous_value=previous_value,
                    trend=trend
                )
                
                self.session.merge(snapshot)  # Upsert
                
            except Exception as e:
                logger.error(f"Error calculating KPI {kpi_code} for school {school_id}: {e}")
        
        await self.session.commit()
```

## 6. UI Component Specifications

### 6.1 School Dashboard Component
```typescript
interface SchoolDashboardProps {
  schoolId: string;
  date?: Date;
  onRefresh: () => void;
}

// Dashboard Layout:
// 1. Header with school name and date selector
// 2. KPI cards row (4-5 cards)
// 3. Alert feed (scrollable)
// 4. Trend charts (attendance, collections, health)
// 5. Quick action buttons
// 6. Refresh indicator

// KPI Card:
interface KPICardProps {
  title: string;
  value: number;
  unit: string;
  trend?: 'up' | 'down' | 'stable';
  target?: number;
  status: 'normal' | 'warning' | 'critical';
  onClick?: () => void;
}

// Alert Feed:
interface AlertFeedProps {
  alerts: Alert[];
  onAcknowledge: (alertId: string) => void;
  onViewDetails: (alertId: string) => void;
  maxItems?: number;
}
```

### 6.2 Sentinel Dashboard Component
```typescript
interface SentinelDashboardProps {
  state?: string;
  lga?: string;
  schoolId?: string;
  dateRange?: DateRange;
  onViewAlert: (alert: SentinelAlert) => void;
  onConfigureThresholds: () => void;
}

// Dashboard Components:
// 1. Geographic map with school pins
// 2. Active alerts panel
// 3. Symptom trend chart
// 4. Alert history timeline
// 5. School comparison matrix
// 6. Threshold configuration panel
// 7. Export controls

// Map Component:
interface SentinelMapProps {
  schools: SchoolLocation[];
  alerts: SentinelAlert[];
  clusters: GeoCluster[];
  onSchoolClick: (schoolId: string) => void;
  onClusterClick: (clusterId: string) => void;
}

// Alert Detail Modal:
interface AlertDetailModalProps {
  alert: SentinelAlert;
  onClose: () => void;
  onAcknowledge: () => void;
  onResolve: (notes: string) => void;
}
```

### 6.3 Report Generator Component
```typescript
interface ReportGeneratorProps {
  schoolId?: string;
  lga?: string;
  state?: string;
  onReportGenerated: (report: GeneratedReport) => void;
}

// Report Builder:
// 1. Report type selection
// 2. Date range picker
// 3. Data source selection (modules)
// 4. Column selection
// 5. Grouping options
// 6. Chart inclusion
// 7. Format selection (PDF, CSV, Excel)
// 8. Preview button
// 9. Generate button
// 10. Schedule option

// Report Preview:
interface ReportPreviewProps {
  reportConfig: ReportConfig;
  onGenerate: () => void;
  onCancel: () => void;
}
```

## 7. Testing Requirements

### 7.1 Unit Tests
```python
# Test cases for DashboardService
class TestDashboardService:
    async def test_get_school_dashboard(self):
        """Test school dashboard data retrieval."""
        pass
    
    async def test_get_lga_dashboard(self):
        """Test LGA dashboard data retrieval."""
        pass
    
    async def test_get_sentinel_dashboard(self):
        """Test Sentinel dashboard data retrieval."""
        pass
    
    async def test_calculate_school_kpis(self):
        """Test KPI calculation."""
        pass

# Test cases for DataAggregationService
class TestDataAggregationService:
    async def test_aggregate_lga_daily(self):
        """Test daily LGA aggregation."""
        pass
    
    async def test_calculate_school_kpis(self):
        """Test school KPI calculation."""
        pass
    
    async def test_refresh_materialized_views(self):
        """Test materialized view refresh."""
        pass
```

### 7.2 Integration Tests
```python
class TestIntelligenceAPI:
    async def test_school_dashboard_endpoint(self):
        """Test GET /api/v1/intelligence/school/{school_id}/dashboard endpoint."""
        pass
    
    async def test_sentinel_dashboard_endpoint(self):
        """Test GET /api/v1/intelligence/sentinel/dashboard endpoint."""
        pass
    
    async def test_report_generation_endpoint(self):
        """Test POST /api/v1/intelligence/reports/generate endpoint."""
        pass
    
    async def test_research_data_request_endpoint(self):
        """Test POST /api/v1/intelligence/research/requests endpoint."""
        pass
```

## 8. Security Considerations

### 8.1 Access Control
```python
# Role-based access for Intelligence module
INTELLIGENCE_PERMISSIONS = {
    "school_admin": [
        "intelligence:read:school_dashboard",
        "intelligence:read:school_kpis",
        "intelligence:read:school_alerts",
        "intelligence:create:school_report",
        "intelligence:export:school_data"
    ],
    "lga_education": [
        "intelligence:read:lga_dashboard",
        "intelligence:read:lga_schools",
        "intelligence:export:emis"
    ],
    "lga_health": [
        "intelligence:read:lga_dashboard",
        "intelligence:read:lga_health_map",
        "intelligence:read:sentinel_alerts"
    ],
    "state_education": [
        "intelligence:read:state_dashboard",
        "intelligence:read:state_analytics",
        "intelligence:export:emis"
    ],
    "state_health": [
        "intelligence:read:state_dashboard",
        "intelligence:read:sentinel_dashboard",
        "intelligence:export:idsr"
    ],
    "researcher": [
        "intelligence:read:research_portal",
        "intelligence:create:data_request",
        "intelligence:download:approved_data"
    ]
}
```

### 8.2 Data Privacy
```python
# Anonymization rules for aggregated data
ANONYMIZATION_RULES = {
    "lga_level": {
        "minimum_population": 10,
        "aggregate_only": True,
        "no_individual_data": True,
        "suppression_threshold": 5  # Suppress counts < 5
    },
    "state_level": {
        "minimum_population": 30,
        "aggregate_only": True,
        "no_individual_data": True,
        "suppression_threshold": 10
    },
    "research_data": {
        "minimum_population": 50,
        "k_anonymity": 5,
        "no_names": True,
        "no_contact_info": True,
        "date_generalization": "month"  # Generalize dates to month
    }
}

# Access logging for intelligence data
INTELLIGENCE_ACCESS_LOGGING = True
```

## 9. Performance Requirements

### 9.1 Performance Metrics
```yaml
Performance Requirements:
  School Dashboard:
    - Target: < 5 seconds for dashboard load
    - Target: < 3 seconds for KPI refresh
    - Caching: 5-minute cache for dashboard data
  
  LGA/State Dashboard:
    - Target: < 10 seconds for LGA dashboard
    - Target: < 15 seconds for state dashboard
    - Caching: 15-minute cache for aggregates
  
  Sentinel Dashboard:
    - Target: < 3 seconds for Sentinel dashboard
    - Target: < 5 seconds for map rendering
    - Alert updates: Near real-time (< 1 minute)
  
  Report Generation:
    - Target: < 30 seconds for school report
    - Target: < 2 minutes for LGA report
    - Target: < 5 minutes for state report
    - Async processing for large reports
  
  Data Aggregation:
    - Target: < 30 minutes for daily LGA aggregation
    - Target: < 2 hours for daily state aggregation
    - Materialized view refresh: < 1 hour
```

### 9.2 Caching Strategy
```python
# Cache frequently accessed intelligence data
INTELLIGENCE_CACHE_CONFIG = {
    "school_dashboard": {
        "ttl": 300,  # 5 minutes
        "key": "school:{school_id}:dashboard:date:{date}"
    },
    "lga_dashboard": {
        "ttl": 900,  # 15 minutes
        "key": "lga:{lga}:state:{state}:dashboard:date:{date}"
    },
    "sentinel_dashboard": {
        "ttl": 60,  # 1 minute for real-time alerts
        "key": "sentinel:state:{state}:dashboard"
    },
    "school_kpis": {
        "ttl": 300,  # 5 minutes
        "key": "school:{school_id}:kpis:date:{date}"
    },
    "lga_aggregates": {
        "ttl": 3600,  # 1 hour
        "key": "lga:{lga}:state:{state}:aggregates:date:{date}"
    }
}
```

## 10. Integration Points

### 10.1 Internal Integrations
```python
# Integration with other EduLafia modules
INTELLIGENCE_INTEGRATIONS = {
    "sis": {
        "student_data": "enrolment counts, demographics",
        "validation": "anonymization for aggregates"
    },
    "academics": {
        "results_data": "academic performance metrics",
        "aggregation": "class/school averages"
    },
    "attendance": {
        "attendance_data": "daily attendance rates",
        "absence_patterns": "for Sentinel analysis"
    },
    "finance": {
        "financial_data": "collections, balances",
        "aggregation": "revenue analytics"
    },
    "health": {
        "health_data": "sick bay visits, screenings",
        "sentinel_signals": "outbreak alerts"
    },
    "sentinel": {
        "alert_data": "Sentinel alerts and signals",
        "analysis": "cluster detection, trends"
    },
    "teacher": {
        "staff_data": "teacher attendance, assignments"
    },
    "parent_portal": {
        "engagement_data": "parent portal usage"
    }
}
```

### 10.2 External Integrations
```python
# External service integrations
EXTERNAL_INTELLIGENCE_INTEGRATIONS = {
    "apache_superset": {
        "purpose": "Advanced analytics and visualization",
        "integration": "Embedded dashboards or API",
        "data_sync": "Scheduled data sync to analytics DB"
    },
    "emis": {
        "purpose": "Federal Ministry of Education reporting",
        "format": "EMIS-compatible CSV",
        "frequency": "Termly and annual"
    },
    "idsr": {
        "purpose": "Integrated Disease Surveillance and Response",
        "format": "IDSR standard format",
        "frequency": "Weekly and outbreak-triggered"
    },
    "dhis2": {
        "purpose": "National Health Management Information System",
        "format": "DHIS2 API",
        "frequency": "Weekly sync"
    },
    "mapping_service": {
        "purpose": "Geographic visualization",
        "provider": "Leaflet/Mapbox/OpenStreetMap",
        "usage": "School locations, cluster mapping"
    }
}
```

## 11. Implementation Checklist

### 11.1 Backend Tasks
- [ ] Create DashboardConfiguration model and schema
- [ ] Create DashboardWidget model and schema
- [ ] Create KPIDefinition model and schema
- [ ] Create SchoolKPISnapshot model and schema
- [ ] Create LGAAggregate model and schema
- [ ] Create StateAggregate model and schema
- [ ] Create ResearchDataRequest model and schema
- [ ] Create ReportTemplate model and schema
- [ ] Create GeneratedReport model and schema
- [ ] Implement DashboardService
- [ ] Implement DataAggregationService
- [ ] Implement ReportService
- [ ] Create intelligence API endpoints
- [ ] Implement KPI calculation logic
- [ ] Implement data aggregation
- [ ] Implement report generation
- [ ] Implement research data portal
- [ ] Create materialized views
- [ ] Implement scheduled aggregation jobs
- [ ] Add validation and error handling
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add logging and audit trail
- [ ] Implement caching
- [ ] Performance optimization

### 11.2 Frontend Tasks
- [ ] Create SchoolDashboard component
- [ ] Create LGADashboard component
- [ ] Create StateDashboard component
- [ ] Create SentinelDashboard component
- [ ] Create KPICard component
- [ ] Create AlertFeed component
- [ ] Create SentinelMap component
- [ ] Create ReportGenerator component
- [ ] Create ResearchPortal component
- [ ] Implement dashboard customization
- [ ] Implement real-time updates
- [ ] Implement chart components
- [ ] Implement data tables
- [ ] Implement export functionality
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Error handling and validation

### 11.3 Data Pipeline Tasks
- [ ] Implement daily aggregation jobs
- [ ] Implement KPI calculation jobs
- [ ] Implement materialized view refresh
- [ ] Implement data quality checks
- [ ] Implement anomaly detection
- [ ] Test aggregation accuracy
- [ ] Performance optimization

### 11.4 Testing Tasks
- [ ] Unit tests for DashboardService
- [ ] Unit tests for DataAggregationService
- [ ] Integration tests for API endpoints
- [ ] E2E tests for dashboard workflows
- [ ] Performance testing
- [ ] Security testing (data privacy)
- [ ] Load testing for aggregation

---

*This module specification provides a comprehensive guide for implementing the Intelligence & Analytics Dashboard system. The module transforms raw data from all other modules into actionable insights for decision-makers at school, LGA, state, and national levels, while providing the analytics surface for the LafiyaSentinel surveillance system.*

---

**End of Intelligence & Analytics Dashboard (M8) Specification**