# EduLafia UI/UX Style Guide

## Overview

Welcome to the EduLafia UI/UX Style Guide! This document outlines the design system and guidelines for creating consistent, premium, and accessible user experiences across all EduLafia applications. Our goal is to provide students, teachers, and administrators with a seamless, modern interface that enhances the learning and teaching experience.

## Design Philosophy

Our design philosophy is centered around three core principles:

1. **Clarity**: Ensure all information is easy to understand and navigate
2. **Consistency**: Maintain uniform design patterns across all application
3. **Accessibility**: Create experiences that are inclusive for all users

## Color System

### Primary Colors

- **Primary Blue**: #0C8CE9 (used for main actions and important information)
- **Light Blue**: #7CC5FC (used for secondary actions and highlights)
- **Dark Blue**: #0158A1 (used for hover states and dark theme primary)

### Secondary Colors

- **Primary Pink**: #EC4899 (used for accents and secondary actions)
- **Light Pink**: #F472B6 (used for hover states and light theme)
- **Dark Pink**: #BE185D (used for hover states and dark theme)

### Background Colors

#### Light Theme
- Default: #F8FAFC (soft gray-blue)
- Paper: #FFFFFF (white)

#### Dark Theme
- Default: #0F172A (dark blue-gray)
- Paper: #1E293B (dark gray-blue)

### Text Colors

#### Light Theme
- Primary: #1E293B (dark blue-gray)
- Secondary: #64748B (gray-blue)
- Disabled: #94A3B8 (light gray)

#### Dark Theme
- Primary: #F1F5F9 (light gray)
- Secondary: #94A3B8 (gray-blue)
- Disabled: #64748B (dark gray)

### High Contrast Mode
- Primary: #000000 (black)
- Secondary: #000080 (dark blue)
- Background: #FFFFFF (white)
- Text: #000000 (black)

## Typography

### Font Family
- Primary: Inter
- Fallbacks: Roboto, Helvetica, Arial, sans-serif

### Font Sizes

| Variant | Size | Weight | Letter Spacing |
|---------|------|--------|----------------|
| h1      | 3rem | 700    | -0.02em        |
| h2      | 2.25rem | 600    | -0.01em        |
| h3      | 1.875rem | 600    | 0              |
| h4      | 1.5rem | 600    | 0              |
| h5      | 1.25rem | 600    | 0              |
| h6      | 1.125rem | 600    | 0              |
| subtitle1 | 1rem | 500    | 0              |
| subtitle2 | 0.875rem | 500    | 0              |
| body1   | 1rem | 400    | 0              |
| body2   | 0.875rem | 400    | 0              |
| caption | 0.75rem | 400    | 0              |
| button  | 0.875rem | 600    | 0              |

### Responsive Typography

We use Material UI's responsive font sizes to ensure text scales appropriately on different screen sizes:

- Breakpoints: sm, md, lg, xl
- Factor: 0.5 (50% reduction for smaller screens)

## Spacing

We use a 4px grid system for consistent spacing:

| Factor | Pixels | Rem | Usage |
|--------|--------|-----|-------|
| 1      | 4px    | 0.25rem | Small gaps and padding |
| 2      | 8px    | 0.5rem | Medium gaps and padding |
| 3      | 12px   | 0.75rem | Card padding |
| 4      | 16px   | 1rem | Section padding |
| 5      | 20px   | 1.25rem | Large gaps and margins |
| 6      | 24px   | 1.5rem | Page margins |

## Elevation and Shadows

### Light Theme

| Elevation | Box Shadow | Usage |
|-----------|-----------|-------|
| 1         | 0 1px 2px 0 rgba(0, 0, 0, 0.05) | Cards, Paper |
| 2         | 0 4px 6px -1px rgba(0, 0, 0, 0.1) | Hover states, Dialogs |
| 3         | 0 10px 15px -3px rgba(0, 0, 0, 0.1) | Modals, Dropdowns |

### Dark Theme

| Elevation | Box Shadow | Usage |
|-----------|-----------|-------|
| 1         | 0 1px 2px 0 rgba(0, 0, 0, 0.3) | Cards, Paper |
| 2         | 0 4px 6px -1px rgba(0, 0, 0, 0.4) | Hover states, Dialogs |
| 3         | 0 10px 15px -3px rgba(0, 0, 0, 0.5) | Modals, Dropdowns |

## Border Radius

We use consistent border radius values for all components:

- Small: 8px (Buttons, Chips, Inputs)
- Medium: 12px (Cards, Paper, Dialogs)
- Large: 16px (PremiumCards, Modal Dialogs)

## Animations and Transitions

### Duration and Easing

We use consistent timing and easing functions for all animations:

- Standard: 0.3s cubic-bezier(0.16, 1, 0.3, 1)
- Fast: 0.2s cubic-bezier(0.16, 1, 0.3, 1)
- Slow: 0.4s cubic-bezier(0.16, 1, 0.3, 1)

### Animation Types

1. **Fade In**: Fades elements in from transparent with slight upward movement
2. **Slide In**: Slides elements from left, right, or bottom
3. **Scale In**: Scales elements from 95% to 100%
4. **Pulse**: Gentle pulsing animation for loading states
5. **Shimmer**: Shimmer effect for loading skeletons
6. **Typing**: Typewriter effect for text

### Transition Properties

We animate the following properties for smooth transitions:

- opacity
- transform
- background-color
- box-shadow

## Components

### PremiumCard

A custom card component with premium styling:

- Includes gradient border
- Hover elevation effect
- Shimmering top border
- Optional badge, icon, and action areas

### ThemeSwitcher

A comprehensive theme switching component:

- Supports light, dark, auto, and high contrast modes
- Persists theme preference in localStorage
- Material Design iconography

### LoadingSpinner

A premium loading indicator:

- Circular progress with gradient effect
- Pulsing animation
- Optional text and full-screen mode

### ToastContainer

Enhanced toast notifications:

- Different severity levels (success, error, warning, info)
- Slide in/out animations
- Action buttons

## Accessibility

### High Contrast Mode

Our high contrast theme ensures:

- Text has minimum 4.5:1 contrast ratio
- Large text (18pt or 14pt bold) has 3:1 contrast ratio
- All interactive elements are clearly distinguishable

### Screen Reader Support

- All interactive elements have ARIA labels
- Semantic HTML structure
- Keyboard navigation support

### Keyboard Navigation

- All forms are accessible via keyboard
- Focus management is handled properly
- Clear focus indicators

## Responsive Design

### Breakpoints

We use Material UI's responsive breakpoints:

| Breakpoint | Range | Device Type |
|-----------|-------|-------------|
| xs        | < 600px | Mobile phones |
| sm        | 600px - 900px | Tablets |
| md        | 900px - 1200px | Laptops |
| lg        | 1200px - 1536px | Desktop monitors |
| xl        | > 1536px | Large desktop monitors |

### Adaptive Layouts

We use a responsive grid system that adapts to different screen sizes:

- Mobile: 1 column
- Tablet: 2 columns
- Desktop: 3-4 columns

## Performance

### Optimizations

We follow performance best practices:

- Code splitting
- Image optimization
- Lazy loading
- CSS-in-JS optimization

### 60fps Animation Target

We ensure all animations run at 60 frames per second by:

- Using CSS transforms and opacity for animations
- Avoiding expensive layout recalculations
- Debouncing and throttling events

## Testing

### Browser Support

We test our UI on the following browsers:

- Chrome (latest 3 versions)
- Firefox (latest 3 versions)
- Safari (latest 2 versions)
- Edge (latest 3 versions)

### Device Testing

We test on the following device types:

- Mobile phones (iOS and Android)
- Tablets (iOS and Android)
- Desktop monitors

### Usability Testing

We conduct usability testing with target user groups:

- Students (13-18 years old)
- Teachers and educators
- School administrators

## Implementation Roadmap

### Phase 1 (Current)

- ✅ Comprehensive theme system with light/dark/auto/high-contrast modes
- ✅ PremiumCard component
- ✅ ThemeSwitcher component
- ✅ LoadingSpinner component
- ✅ Enhanced animations and transitions
- ✅ Responsive design improvements

### Phase 2

- Enhanced data visualization components
- Advanced dashboard layouts
- Additional custom components
- Improved accessibility features
- Performance optimization

### Phase 3

- Localization support (multiple languages)
- Advanced interaction patterns
- Custom icon set
- Design tokens library

## Design Tokens

All design tokens are defined in `src/shared/theme/index.ts` and include:

- Colors (palette)
- Typography
- Spacing
- Elevation
- Border radius
- Breakpoints

## Quality Benchmarks

We measure our UI quality against industry standards:

- Accessibility: WCAG 2.1 AA compliance
- Performance: Google Lighthouse scores (90+ for accessibility, performance, SEO)
- Usability: User testing scores (Net Promoter Score, System Usability Scale)
- Consistency: Design system coverage (100% of UI components)

## References

- Material Design 3 Guidelines
- WCAG 2.1 Accessibility Standards
- Google Lighthouse Documentation
- React Material UI Documentation

---

**Last Updated**: April 8, 2026
**Version**: 1.0
