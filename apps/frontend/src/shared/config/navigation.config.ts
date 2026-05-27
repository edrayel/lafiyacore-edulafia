import React from 'react';
import {
  Dashboard,
  School,
  People,
  EventNote,
  AutoStories,
  LocalHospital,
  AttachMoney,
  Badge,
  AccountCircle,
  BarChart,
  Settings,
  HowToReg,
  Emergency,
  Accessibility,
  Inventory,
  LocalLibrary,
  Payments,
  EventBusy,
  Assignment,
  Gavel,
  SupervisorAccount,
  Verified,
  Description,
  VolunteerActivism,
  Construction,
  Groups,
  DirectionsBus,
  Restaurant,
  Female,
  FactCheck,
  Assessment,
  Security,
  DeleteSweep,
  Chat,
  MenuBook,
  Hotel,
  CalendarMonth,
} from '@mui/icons-material';

export interface NavItem {
  label: string;
  icon: React.ComponentType;
  path: string;
  perm?: string;
}

export const navSections = [
  {
    label: 'Core',
    items: [
      { label: 'Dashboard', icon: Dashboard, path: '/' },
      { label: 'Students', icon: School, path: '/students' },
      { label: 'Guardians', icon: People, path: '/guardians' },
      { label: 'Attendance', icon: EventNote, path: '/attendance' },
      { label: 'Academics', icon: AutoStories, path: '/academics' },
      { label: 'Health', icon: LocalHospital, path: '/health', perm: 'health:view' },
      { label: 'Finance', icon: AttachMoney, path: '/finance', perm: 'finance:view' },
      { label: 'Staff', icon: Badge, path: '/staff' },
      { label: 'Messages', icon: Chat, path: '/messaging' },
      { label: 'LMS', icon: MenuBook, path: '/lms' },
      { label: 'Calendar', icon: CalendarMonth, path: '/calendar' },
    ],
  },
  {
    label: 'Operations',
    items: [
      { label: 'Admissions', icon: HowToReg, path: '/admissions' },
      { label: 'Emergency', icon: Emergency, path: '/emergency' },
      { label: 'Special Needs', icon: Accessibility, path: '/special-needs' },
      { label: 'Inventory', icon: Inventory, path: '/inventory' },
      { label: 'Library', icon: LocalLibrary, path: '/library' },
      { label: 'Cafeteria', icon: Restaurant, path: '/cafeteria' },
      { label: 'Clubs', icon: Groups, path: '/clubs' },
      { label: 'Bus Tracking', icon: DirectionsBus, path: '/bus-tracking' },
      { label: 'Hostels', icon: Hotel, path: '/hostel' },
    ],
  },
  {
    label: 'HR',
    items: [
      { label: 'Payroll', icon: Payments, path: '/payroll' },
      { label: 'Leave', icon: EventBusy, path: '/leave' },
    ],
  },
  {
    label: 'Compliance',
    items: [
      { label: 'Exam Registration', icon: Assignment, path: '/exam-registration' },
      { label: 'WAEC Bulk', icon: Description, path: '/waec-registration' },
      { label: 'Discipline', icon: Gavel, path: '/discipline' },
      { label: 'Girl-Child', icon: Female, path: '/girl-child' },
      { label: 'Accreditation', icon: Verified, path: '/accreditation' },
      { label: 'Inspections', icon: FactCheck, path: '/inspections' },
      { label: 'Ministry Reports', icon: Assessment, path: '/ministry-reports' },
      { label: 'SMC Reports', icon: SupervisorAccount, path: '/smc-reports' },
    ],
  },
  {
    label: 'Management',
    items: [
      { label: 'Proprietor', icon: SupervisorAccount, path: '/proprietor', perm: 'proprietor:view' },
      { label: 'Fundraising', icon: VolunteerActivism, path: '/fundraising' },
      { label: 'Projects', icon: Construction, path: '/projects' },
      { label: 'Custody', icon: Security, path: '/custody' },
      { label: 'Data Retention', icon: DeleteSweep, path: '/data-retention' },
      { label: 'Alumni', icon: Groups, path: '/alumni' },
    ],
  },
  {
    label: 'Portals',
    items: [
      { label: 'Parent Portal', icon: AccountCircle, path: '/parent/children' },
      { label: 'Intelligence', icon: BarChart, path: '/intelligence' },
      { label: 'Admin', icon: Settings, path: '/admin', perm: 'admin:view' },
    ],
  },
];
