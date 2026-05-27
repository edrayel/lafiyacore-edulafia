# EduLafia UI/UX Design Guidelines

## Document Information

- **Version**: 1.0.0
- **Last Updated**: 2026-03-26
- **Status**: Draft
- **Purpose**: Define frontend design standards, component patterns, accessibility requirements, and localization approach for EduLafia

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Design System](#2-design-system)
3. [Layout and Grid](#3-layout-and-grid)
4. [Typography](#4-typography)
5. [Color System](#5-color-system)
6. [Component Library](#6-component-library)
7. [Form Design](#7-form-design)
8. [Data Display Patterns](#8-data-display-patterns)
9. [Navigation Patterns](#9-navigation-patterns)
10. [Offline UX Patterns](#10-offline-ux-patterns)
11. [Accessibility Standards](#11-accessibility-standards)
12. [Localization (Igbo/Hausa)](#12-localization-igbohausa)
13. [PWA Requirements](#13-pwa-requirements)
14. [Implementation Checklists](#14-implementation-checklists)

---

## 1. Design Principles

### 1.1 Core Principles

| Principle | Description |
|-----------|-------------|
| **Mobile First** | Design for small screens first, enhance for larger screens |
| **Low Bandwidth** | Minimal data transfer, optimize for 2G/3G connections |
| **Offline Resilient** | Every feature works without internet |
| **Accessible** | WCAG 2.1 AA, screen reader compatible |
| **Culturally Relevant** | Nigerian context, local language support |
| **Simple** | Minimize cognitive load for non-technical users |
| **Consistent** | Predictable patterns across all modules |

### 1.2 User Personas

| Persona | Device | Connectivity | Tech Level | Primary Tasks |
|---------|--------|-------------|------------|---------------|
| School Admin | Laptop + Phone | Variable | Medium | Setup, reports, oversight |
| Teacher | Phone primary | Often poor | Medium | Attendance, grades, schedule |
| School Nurse | Phone only | Often poor | Low-Medium | Health visits, referrals |
| Finance Officer | Laptop primary | Variable | Medium | Fees, payments, receipts |
| Parent | Phone only | Variable | Low | View child data, pay fees |
| State Admin | Laptop | Good | High | Analytics, compliance |

### 1.3 Screen Size Targets

| Breakpoint | Width | Devices | Priority |
|------------|-------|---------|----------|
| xs | 320-479px | Small phones | Primary |
| sm | 480-767px | Large phones | Primary |
| md | 768-1023px | Tablets | Secondary |
| lg | 1024-1279px | Small laptops | Secondary |
| xl | 1280px+ | Desktops | Tertiary |

---

## 2. Design System

### 2.1 Technology Stack

| Technology | Purpose |
|------------|---------|
| Tailwind CSS | Utility-first CSS framework |
| Radix UI | Accessible primitive components |
| Lucide Icons | Consistent icon set |
| Framer Motion | Minimal animations (respects prefers-reduced-motion) |

### 2.2 Design Tokens

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#b9dffd',
          300: '#7cc5fc',
          400: '#36a7f8',
          500: '#0c8ce9',  // Main primary
          600: '#006ec7',
          700: '#0158a1',
          800: '#064b85',
          900: '#0b3f6e',
        },
        success: {
          50: '#f0fdf4',
          500: '#22c55e',  // Main success
          700: '#15803d',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',  // Main warning
          700: '#b45309',
        },
        danger: {
          50: '#fef2f2',
          500: '#ef4444',  // Main danger
          700: '#b91c1c',
        },
        sentinel: {
          50: '#fdf2f8',
          500: '#ec4899',  // LafiyaSentinel alert color
          700: '#be185d',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      },
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
        'safe-left': 'env(safe-area-inset-left)',
        'safe-right': 'env(safe-area-inset-right)',
      },
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
      },
    },
  },
};
```

---

## 3. Layout and Grid

### 3.1 Page Layout Structure

```
┌──────────────────────────────────────────────┐
│                 Top Bar                       │
│  [Logo] [School Name]     [Sync] [Notif] [👤]│
├──────────────────────────────────────────────┤
│                                              │
│              Page Content                    │
│  ┌────────────────────────────────────────┐  │
│  │  Page Header (Title + Actions)         │  │
│  ├────────────────────────────────────────┤  │
│  │                                        │  │
│  │  Main Content Area                     │  │
│  │  (responsive grid)                     │  │
│  │                                        │  │
│  └────────────────────────────────────────┘  │
│                                              │
├──────────────────────────────────────────────┤
│  [Home] [Students] [Attendance] [+] [More]   │
│              Bottom Nav (Mobile)             │
└──────────────────────────────────────────────┘
```

### 3.2 Grid System

```
Mobile (< 768px):
  - Single column layout
  - 16px horizontal padding
  - Bottom navigation bar
  - Floating action button for primary actions

Tablet (768-1023px):
  - 2-column grid for cards
  - Sidebar navigation (collapsible)
  - 24px horizontal padding

Desktop (1024px+):
  - 3-4 column grid for cards
  - Fixed sidebar navigation
  - Max content width: 1200px
  - Centered with auto margins
```

### 3.3 Spacing Scale

| Token | Value | Use Case |
|-------|-------|----------|
| `space-1` | 4px | Tight inner spacing |
| `space-2` | 8px | Default inner spacing |
| `space-3` | 12px | Form field spacing |
| `space-4` | 16px | Section spacing |
| `space-6` | 24px | Card padding |
| `space-8` | 32px | Section gaps |
| `space-12` | 48px | Page section gaps |
| `space-16` | 64px | Major section gaps |

---

## 4. Typography

### 4.1 Type Scale

| Element | Size | Weight | Line Height | Font |
|---------|------|--------|-------------|------|
| H1 - Page Title | 24px (mobile) / 30px (desktop) | 700 | 1.2 | Display |
| H2 - Section Title | 20px / 24px | 600 | 1.3 | Display |
| H3 - Card Title | 18px / 20px | 600 | 1.3 | Sans |
| H4 - Subsection | 16px / 18px | 600 | 1.4 | Sans |
| Body | 16px | 400 | 1.5 | Sans |
| Body Small | 14px | 400 | 1.5 | Sans |
| Caption | 12px | 400 | 1.4 | Sans |
| Button | 14px / 16px | 600 | 1 | Sans |
| Table Header | 12px | 600 | 1 | Sans |
| Input | 16px | 400 | 1.5 | Sans |

### 4.2 Text Guidelines

- Minimum body text size: 16px (prevents iOS zoom on input focus)
- Maximum line length: 70 characters for body text
- Paragraph spacing: 1em
- Link color: primary-600, underline on hover
- Truncation: Use ellipsis for single-line, clamp for multi-line

---

## 5. Color System

### 5.1 Semantic Colors

| Semantic | Light Mode | Dark Mode | Use Case |
|----------|-----------|-----------|----------|
| Background | `white` | `gray-900` | Page background |
| Surface | `gray-50` | `gray-800` | Cards, panels |
| Border | `gray-200` | `gray-700` | Dividers, borders |
| Text Primary | `gray-900` | `gray-100` | Main text |
| Text Secondary | `gray-600` | `gray-400` | Descriptions, captions |
| Text Disabled | `gray-400` | `gray-600` | Disabled elements |
| Interactive | `primary-500` | `primary-400` | Buttons, links |
| Interactive Hover | `primary-600` | `primary-300` | Hover states |
| Success | `success-500` | `success-500` | Present, paid |
| Warning | `warning-500` | `warning-500` | Alerts, pending |
| Danger | `danger-500` | `danger-500` | Errors, absent |
| Sentinel | `sentinel-500` | `sentinel-500` | Health alerts |

### 5.2 Attendance Status Colors

| Status | Color | Background | Icon |
|--------|-------|------------|------|
| Present | `success-700` | `success-500` | CheckCircle |
| Absent | `danger-700` | `danger-500` | XCircle |
| Late | `warning-700` | `warning-500` | Clock |
| Excused | `primary-700` | `primary-100` | FileCheck |

### 5.3 Health Severity Colors

| Severity | Color | Background |
|----------|-------|------------|
| Low | `gray-600` | `gray-100` |
| Medium | `warning-600` | `warning-100` |
| High | `danger-600` | `danger-100` |
| Critical | `danger-700` | `danger-200` |

---

## 6. Component Library

### 6.1 Buttons

| Variant | Use Case | Styling |
|---------|----------|---------|
| Primary | Main actions (Save, Submit) | `bg-primary-500 text-white` |
| Secondary | Cancel, back | `bg-gray-100 text-gray-700 border` |
| Danger | Destructive actions (Delete) | `bg-danger-500 text-white` |
| Ghost | Less prominent actions | `text-primary-600 hover:bg-primary-50` |
| Icon-only | Toolbar actions | `p-2 rounded-lg hover:bg-gray-100` |

```
Button Sizes:
  sm: h-8 px-3 text-sm
  md: h-10 px-4 text-base  (default)
  lg: h-12 px-6 text-lg

Minimum touch target: 44x44px (accessibility)
```

### 6.2 Input Fields

```
States: default, focused, error, disabled, success

Structure:
┌─────────────────────────────────────┐
│ Label *                             │
├─────────────────────────────────────┤
│ [Icon] Placeholder text        [👁] │
├─────────────────────────────────────┤
│ Helper text or error message        │
└─────────────────────────────────────┘

Height: 44px (mobile), 40px (desktop)
Border: 1px solid gray-300
Border radius: 8px
Focus ring: 2px primary-200
Error border: danger-500
```

### 6.3 Cards

```tsx
// Card Component Structure
<div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
  <div className="p-4 border-b border-gray-100">
    <h3 className="text-lg font-semibold">Card Title</h3>
    <p className="text-sm text-gray-500">Subtitle</p>
  </div>
  <div className="p-4">
    {/* Card content */}
  </div>
  <div className="p-4 bg-gray-50 border-t border-gray-100">
    {/* Card actions */}
  </div>
</div>
```

### 6.4 Data Tables

```
Mobile: Convert to card list
Desktop: Full table with sorting, filtering

Table Structure:
┌──────────────────────────────────────────────────┐
│ [Search...] [Filter ▼] [Export]    Showing 1-20 │
├──────────────────────────────────────────────────┤
│ ▲ Name  │ Class │ Status │ Last Active │ Actions│
├─────────┼───────┼────────┼─────────────┼────────┤
│ Emeka   │ JSS2A │ Active │ 2h ago      │ [···]  │
│ Chioma  │ JSS2A │ Active │ 1d ago      │ [···]  │
├──────────────────────────────────────────────────┤
│ < 1 2 3 ... 10 >          200 total records     │
└──────────────────────────────────────────────────┘
```

### 6.5 Modals and Dialogs

```
Mobile: Full-screen bottom sheet
Desktop: Centered modal (max-width: 480px)

Structure:
┌────────────────────────────┐
│ Title              [Close] │
├────────────────────────────┤
│                            │
│   Content                  │
│                            │
├────────────────────────────┤
│     [Cancel]  [Confirm]    │
└────────────────────────────┘

- Backdrop: black/50
- Animation: slide-up (mobile), fade-in (desktop)
- Focus trap inside modal
- Escape key closes
- Click outside closes (unless destructive action)
```

### 6.6 Toast Notifications

```
Position: Top-right (desktop), Top-center (mobile)
Duration: 5s (success/info), 10s (error), manual dismiss (warning)

Types:
┌──────────────────────────────┐
│ ✓ Attendance saved           │  Success (green)
└──────────────────────────────┘

┌──────────────────────────────┐
│ ⚠ 3 students marked absent   │  Warning (amber)
└──────────────────────────────┘

┌──────────────────────────────┐
│ ✗ Failed to save. Retry.     │  Error (red)
│                     [Retry]  │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 📴 Offline - changes queued  │  Info (blue)
└──────────────────────────────┘
```

---

## 7. Form Design

### 7.1 Form Layout

```
Single Column (Mobile):
┌──────────────────────────────┐
│ First Name *                 │
│ ┌──────────────────────────┐ │
│ │                          │ │
│ └──────────────────────────┘ │
│ Last Name *                  │
│ ┌──────────────────────────┐ │
│ │                          │ │
│ └──────────────────────────┘ │
│ Email *                      │
│ ┌──────────────────────────┐ │
│ │                          │ │
│ └──────────────────────────┘ │
│                              │
│ [Cancel]       [Save Student]│
└──────────────────────────────┘

Two Column (Desktop):
┌──────────────────────────────┐
│ First Name *    │ Last Name *│
│ ┌──────────────┐│┌──────────┐│
│ │              │││          ││
│ └──────────────┘│└──────────┘│
│ Email *                        │
│ ┌──────────────────────────┐ │
│ │                          │ │
│ └──────────────────────────┘ │
│ [Cancel]       [Save Student]│
└──────────────────────────────┘
```

### 7.2 Form Validation UX

```
Validation Timing:
- On blur: Validate field when user leaves it
- On submit: Validate all fields
- Real-time: Only for character counters, password strength

Error Display:
- Inline below the field (red text)
- Error icon in the field
- Red border on the field
- Announce to screen readers

Success Display:
- Green checkmark icon in the field
- Green border (optional)
```

### 7.3 Touch-Friendly Forms

```
Requirements:
- Minimum input height: 44px
- Label above input (not beside)
- Large tap targets for radio/checkbox
- Native date/time pickers on mobile
- Numeric keyboard for number/phone fields
- Auto-focus first field on form load
- Tab order follows visual flow
- Submit button fixed at bottom on mobile (sticky)
```

---

## 8. Data Display Patterns

### 8.1 Student Profile Card

```
┌────────────────────────────────────────┐
│ [Avatar]  Chioma Okonkwo               │
│           JSS 2A • EDU/2026/001        │
│           Female • 14 years            │
├────────────────────────────────────────┤
│ 📊 Attendance    │ 94% (47/50 days)   │
│ 📚 Avg Grade     │ 78.5% (B+)         │
│ 🏥 Health Visits │ 2 this term        │
│ 💰 Fee Status    │ ✅ Paid            │
├────────────────────────────────────────┤
│ [View Profile] [Mark Attendance] [+]   │
└────────────────────────────────────────┘
```

### 8.2 Dashboard Cards

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Students │ │ Present  │ │ Fees Due │ │ Alerts   │
│   450    │ │   92%    │ │  ₦2.1M   │ │    3     │
│  ↑ 12    │ │  today   │ │ overdue  │ │ sentinel │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### 8.3 List Patterns

```
Standard List Item:
┌──────────────────────────────────────────┐
│ [Avatar] Name               [Chevron →] │
│          Secondary info                  │
└──────────────────────────────────────────┘

Selectable List Item:
┌──────────────────────────────────────────┐
│ [☐] Name                    Secondary    │
└──────────────────────────────────────────┘

Swipeable List Item (Mobile):
┌──────────────────────────────────────────┐
│ ← [Edit] │ Name              [Delete] → │
└──────────────────────────────────────────┘
```

---

## 9. Navigation Patterns

### 9.1 Mobile Navigation

```
Bottom Navigation (5 items max):
┌─────────────────────────────────────┐
│  🏠    👥    📋    ＋    ⋯         │
│ Home Students  More  Add            │
└─────────────────────────────────────┘

"+" Button: Floating action button for
context-sensitive primary action

"⋯" Menu: Opens additional options sheet
  - Attendance
  - Grades
  - Health
  - Fees
  - Reports
  - Settings
```

### 9.2 Desktop Navigation

```
Side Navigation (Fixed, 240px):
┌──────────┬─────────────────────────────┐
│ 🏠 Home  │                             │
│ 👥 Students                           │
│ 📋 Attendance                         │
│ 📚 Grades                             │
│ 🏥 Health                             │
│ 💰 Fees                               │
│ 📊 Reports                            │
│ ⚙️ Settings                           │
│ ──────────────────────────────────── │
│ 📴 Offline (3 pending)                │
│ 👤 Admin Name                         │
└──────────┴─────────────────────────────┘
```

### 9.3 Breadcrumbs

```
Desktop: Home > Students > Chioma Okonkwo
Mobile: < Back to Students
```

---

## 10. Offline UX Patterns

### 10.1 Offline Indicator

```
Persistent Banner (when offline):
┌──────────────────────────────────────┐
│ 📴 You're offline. Changes will sync.│
└──────────────────────────────────────┘

Position: Below top bar
Style: bg-warning-100 text-warning-800
Dismissible: No
```

### 10.2 Sync Status Indicators

```
Per-Record Sync Status:
  ⏳ Pending - Gray clock icon
  🔄 Syncing - Blue spinner
  ✅ Synced - Green checkmark (brief, then disappears)
  ❌ Failed - Red alert icon with retry button
  ⚠️ Conflict - Yellow warning with resolve button

Global Sync Status (top bar):
  🔄 3 syncing    - Blue
  📴 5 pending    - Orange
  ⚠️ 1 conflict   - Red
  ✅ All synced   - Green (brief, then hidden)
```

### 10.3 Offline-First Interactions

```
Save Action (Offline):
1. Save to local IndexedDB immediately
2. Show success toast: "Saved locally. Will sync when online."
3. Add sync indicator to the record
4. Queue for background sync

Payment Action (Offline):
1. Show message: "Payments require internet connection"
2. Offer: "Save payment details and process later?"
3. If yes, save to local queue
4. When online: Show notification to complete payment
```

### 10.4 Last Updated Timestamps

```
Data Freshness Indicator:
┌────────────────────────────────────┐
│ Student List                       │
│ Updated: 2 minutes ago  [Refresh]  │
├────────────────────────────────────┤
│ ...                                │

Show on:
- Lists (last successful sync time)
- Dashboard cards
- Report data
```

---

## 11. Accessibility Standards

### 11.1 WCAG 2.1 AA Requirements

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 | Non-text alternatives | Alt text for all images |
| 1.3.1 | Info and relationships | Semantic HTML, ARIA labels |
| 1.4.3 | Contrast minimum | 4.5:1 for normal text, 3:1 for large text |
| 1.4.4 | Resize text | Support up to 200% zoom |
| 2.1.1 | Keyboard | All functionality keyboard accessible |
| 2.4.3 | Focus order | Logical tab order |
| 2.4.7 | Focus visible | Clear focus indicators |
| 3.3.1 | Error identification | Clear error messages |
| 3.3.2 | Labels | All inputs have visible labels |
| 4.1.2 | Name, role, value | ARIA attributes where needed |

### 11.2 Focus Management

```
Focus Ring Style:
  outline: 2px solid primary-500
  outline-offset: 2px
  border-radius: 4px

Skip Links:
  "Skip to main content" - visible on focus
  First element on page

Focus Trap:
  - Modals trap focus inside
  - Dropdown menus trap focus
  - Escape returns focus to trigger element
```

### 11.3 Screen Reader Support

```
Requirements:
- All images have descriptive alt text
- Form inputs linked to labels via htmlFor/id
- Error messages linked via aria-describedby
- Dynamic content changes announced via aria-live regions
- Loading states have aria-busy="true"
- Buttons/links have descriptive text (not "click here")
- Tables have proper headers (th with scope)
- Language changes marked with lang attribute

ARIA Live Regions:
  - Toast notifications: aria-live="polite"
  - Error messages: aria-live="assertive"
  - Sync status updates: aria-live="polite"
```

### 11.4 Color Accessibility

```
Rules:
- Never use color alone to convey information
- Always pair color with icon or text
- Test with color blindness simulators
- Maintain 4.5:1 contrast ratio minimum

Examples:
  Status indicators: Color + icon (✓ ✗ ⚠)
  Required fields: Label + asterisk (*) + aria-required
  Error states: Red border + error icon + error text
```

---

## 12. Localization (Igbo/Hausa)

### 12.1 Supported Languages

| Language | Code | Direction | Status |
|----------|------|-----------|--------|
| English | `en` | LTR | Primary |
| Igbo | `ig` | LTR | Secondary |
| Hausa | `ha` | LTR | Secondary |

### 12.2 Translation Structure

```
frontend/
├── public/
│   └── locales/
│       ├── en/
│       │   ├── common.json
│       │   ├── students.json
│       │   ├── attendance.json
│       │   ├── grades.json
│       │   ├── health.json
│       │   └── fees.json
│       ├── ig/
│       │   └── ...
│       └── ha/
│           └── ...
```

### 12.3 Translation Keys

```json
// en/common.json
{
  "nav": {
    "home": "Home",
    "students": "Students",
    "attendance": "Attendance",
    "grades": "Grades",
    "health": "Health",
    "fees": "Fees",
    "reports": "Reports",
    "settings": "Settings"
  },
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "create": "Create",
    "search": "Search",
    "filter": "Filter",
    "export": "Export"
  },
  "status": {
    "loading": "Loading...",
    "saving": "Saving...",
    "saved": "Saved successfully",
    "error": "An error occurred",
    "offline": "You are offline",
    "syncing": "Syncing...",
    "synced": "All data synced"
  }
}

// ig/common.json (Igbo)
{
  "nav": {
    "home": "Ụlọ",
    "students": "Ụmụ akwụkwọ",
    "attendance": "Ọbịbịa",
    "grades": "Ọnụ ọgụgụ",
    "health": "Ahụike",
    "fees": "Ego",
    "reports": "Akụkọ",
    "settings": "Ntọala"
  },
  "actions": {
    "save": "Chekwaa",
    "cancel": "Kagbuo",
    "delete": "Hichapụ",
    "edit": "Dezie",
    "create": "Mepụta",
    "search": "Chọọ",
    "filter": "Nyocha",
    "export": "Bupụ"
  }
}

// ha/common.json (Hausa)
{
  "nav": {
    "home": "Gida",
    "students": "Ɗalibai",
    "attendance": "Halarta",
    "grades": "Maki",
    "health": "Lafiya",
    "fees": "Kuɗi",
    "reports": "Rahotanni",
    "settings": "Saituna"
  },
  "actions": {
    "save": "Ajiye",
    "cancel": "Soke",
    "delete": "Share",
    "edit": "Gyara",
    "create": "Ƙirƙiri",
    "search": "Nemo",
    "filter": "Tace",
    "export": "Fito"
  }
}
```

### 12.4 Localization Guidelines

```
Text Handling:
- Never hardcode strings in components
- Use translation function: t('key.path')
- Support interpolation: t('greeting', { name: 'Chioma' })
- Handle pluralization: t('students_count', { count: 5 })
- Support date/number formatting per locale

Layout Considerations:
- Text may expand 30-50% in translation
- Avoid fixed-width containers for text
- Use flexible layouts that accommodate text length
- Test with longest translations

Date/Number Formatting:
- Dates: DD/MM/YYYY (Nigerian standard)
- Currency: ₦ (Naira symbol) with 2 decimal places
- Numbers: Use locale-specific formatting
  - 1,234.56 (English)
  - 1.234,56 (if applicable)
```

---

## 13. PWA Requirements

### 13.1 Manifest Configuration

```json
{
  "name": "EduLafia - School Management",
  "short_name": "EduLafia",
  "description": "Integrated school management and health surveillance",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0c8ce9",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["education", "health"],
  "screenshots": [
    {
      "src": "/screenshots/dashboard.png",
      "sizes": "1080x1920",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ]
}
```

### 13.2 Service Worker Strategy

```
Caching Strategy:
- App Shell: Cache-first (HTML, CSS, JS)
- API Data: Network-first with offline fallback
- Images: Cache-first with network fallback
- Fonts: Cache-first (long TTL)

Cache Names:
- edulafia-shell-v1
- edulafia-data-v1
- edulafia-images-v1
- edulafia-fonts-v1
```

### 13.3 Install Prompt

```
Trigger: After 3rd session or significant usage
Design:
┌──────────────────────────────────┐
│ 📱 Install EduLafia              │
│                                  │
│ Get faster access and work       │
│ offline. Install the app on      │
│ your device.                     │
│                                  │
│ [Install Now]  [Not Now]         │
└──────────────────────────────────┘
```

---

## 14. Implementation Checklists

### 14.1 Design System Setup

- [ ] Install and configure Tailwind CSS
- [ ] Define all design tokens in tailwind.config
- [ ] Install Radix UI primitives
- [ ] Install Lucide icons
- [ ] Create Button component with all variants
- [ ] Create Input, Select, Checkbox, Radio components
- [ ] Create Card component
- [ ] Create Modal/Dialog component
- [ ] Create Toast notification system
- [ ] Create Data Table component
- [ ] Create Avatar component
- [ ] Create Badge/Tag component

### 14.2 Layout Implementation

- [ ] Create responsive page layout wrapper
- [ ] Implement mobile bottom navigation
- [ ] Implement desktop sidebar navigation
- [ ] Create top bar with sync status
- [ ] Implement floating action button
- [ ] Create breadcrumb component
- [ ] Implement safe area padding for notch devices

### 14.3 Form Implementation

- [ ] Create reusable form field components
- [ ] Implement inline validation with error display
- [ ] Create form submission handling with loading states
- [ ] Implement keyboard navigation
- [ ] Create date picker (native on mobile)
- [ ] Create searchable select component
- [ ] Implement file upload component

### 14.4 Offline UX Implementation

- [ ] Create offline banner component
- [ ] Implement sync status indicators
- [ ] Create conflict resolution dialog
- [ ] Implement last-updated timestamp display
- [ ] Create offline queue status widget
- [ ] Implement graceful degradation states

### 14.5 Accessibility Implementation

- [ ] Add skip-to-content link
- [ ] Implement focus management for modals
- [ ] Add ARIA labels to all interactive elements
- [ ] Create focus-visible styles
- [ ] Test with keyboard-only navigation
- [ ] Test with screen reader (VoiceOver/NVDA)
- [ ] Verify color contrast ratios
- [ ] Add aria-live regions for dynamic content

### 14.6 Localization Implementation

- [ ] Install and configure i18next
- [ ] Create translation file structure
- [ ] Extract all strings to translation files
- [ ] Create Igbo translation files
- [ ] Create Hausa translation files
- [ ] Implement language switcher component
- [ ] Test text expansion in layouts
- [ ] Implement locale-aware date/number formatting

### 14.7 PWA Implementation

- [ ] Create web app manifest
- [ ] Generate all icon sizes
- [ ] Configure service worker with Workbox
- [ ] Implement offline page
- [ ] Create install prompt component
- [ ] Test add-to-homescreen flow
- [ ] Verify offline functionality

---

**End of UI/UX Design Guidelines**
