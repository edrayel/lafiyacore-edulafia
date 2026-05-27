import {
  createRoute,
  createRootRoute,
  Outlet,
  redirect,
  lazyRouteComponent,
} from '@tanstack/react-router';
import { useAuthStore } from '../shared/stores/authStore';

import { StudentDetailPage } from '../features/students/StudentDetailPage';
import { GuardianDetailPage } from '../features/guardians/GuardianDetailPage';
import { AppLayout } from '../shared/components/AppLayout';
import { NotFoundPage } from '../shared/components/NotFoundPage';

import { GlobalErrorBoundary } from '../shared/components/GlobalErrorBoundary';

function isAuthenticated() {
  return !!useAuthStore.getState().user;
}

function hasRole(allowedRoles: string[]) {
  const user = useAuthStore.getState().user;
  if (!user) return false;
  return allowedRoles.includes(user.role);
}

const rootRoute = createRootRoute({
  component: () => (
    <GlobalErrorBoundary>
      <Outlet />
    </GlobalErrorBoundary>
  ),
});

const notFoundRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '$',
  component: NotFoundPage,
});

const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: lazyRouteComponent(() => import('../features/auth/LoginPage'), 'LoginPage'),
  beforeLoad: () => {
    if (isAuthenticated()) throw redirect({ to: '/' });
  },
});

const forgotPasswordRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/forgot-password',
  component: lazyRouteComponent(
    () => import('../features/auth/ForgotPasswordPage'),
    'ForgotPasswordPage'
  ),
  beforeLoad: () => {
    if (isAuthenticated()) throw redirect({ to: '/' });
  },
});

const resetPasswordRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/reset-password',
  component: lazyRouteComponent(() => import('../features/auth/ResetPasswordPage'), 'default'),
  beforeLoad: () => {
    if (isAuthenticated()) throw redirect({ to: '/' });
  },
  validateSearch: (search: Record<string, unknown>) => {
    return {
      token: search.token as string,
    };
  },
});

const authRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: '_auth',
  component: () => (
    <AppLayout>
      <Outlet />
    </AppLayout>
  ),
  loader: async () => {
    try {
      await useAuthStore.getState().loadUser();
      if (!isAuthenticated()) {
        throw redirect({ to: '/login' });
      }
    } catch (error) {
      if (error instanceof Error && error.message.includes('redirect')) {
        throw error; // Let TanStack Router handle the redirect
      }
      throw redirect({ to: '/login' });
    }
  },
});

const indexRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/',
  component: lazyRouteComponent(
    () => import('../features/dashboard/DashboardPage'),
    'DashboardPage'
  ),
});

const studentsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/students',
  component: lazyRouteComponent(() => import('../features/students/StudentsPage'), 'StudentsPage'),
});

const studentDetailRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/students/$id',
  component: () => {
    const { id } = studentDetailRoute.useParams();
    return <StudentDetailPage studentId={id} onBack={() => window.history.back()} />;
  },
});

const guardiansRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/guardians',
  component: lazyRouteComponent(
    () => import('../features/guardians/GuardiansPage'),
    'GuardiansPage'
  ),
});

const guardianDetailRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/guardians/$id',
  component: () => {
    const { id } = guardianDetailRoute.useParams();
    return <GuardianDetailPage guardianId={id} onBack={() => window.history.back()} />;
  },
});

const attendanceRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/attendance',
  component: lazyRouteComponent(
    () => import('../features/attendance/AttendancePage'),
    'AttendancePage'
  ),
});

const parentLoginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/parent/login',
  component: lazyRouteComponent(
    () => import('../features/parent/ParentLoginPage'),
    'ParentLoginPage'
  ),
  beforeLoad: () => {
    if (isAuthenticated()) throw redirect({ to: '/parent/children' });
  },
});

const staffRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/staff',
  component: lazyRouteComponent(() => import('../features/staff/StaffPage'), 'StaffPage'),
});

const staffTimetableRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/staff/timetable',
  component: lazyRouteComponent(() => import('../features/staff/TimetablePage'), 'TimetablePage'),
});

const staffAttendanceRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/staff/attendance',
  component: lazyRouteComponent(
    () => import('../features/staff/TeacherAttendancePage'),
    'TeacherAttendancePage'
  ),
});

const parentChildrenRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/parent/children',
  component: lazyRouteComponent(() => import('../features/parent/ParentPage'), 'ParentPage'),
});

const intelligenceRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/intelligence',
  component: lazyRouteComponent(
    () => import('../features/intelligence/IntelligencePage'),
    'IntelligencePage'
  ),
});

const adminRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/admin',
  component: lazyRouteComponent(() => import('../features/admin/AdminPage'), 'AdminPage'),
  beforeLoad: () => {
    if (!hasRole(['admin', 'superadmin', 'owner'])) throw redirect({ to: '/' });
  },
});

const financeRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/finance',
  component: lazyRouteComponent(() => import('../features/finance/FinancePage'), 'FinancePage'),
  beforeLoad: () => {
    if (!hasRole(['admin', 'superadmin', 'owner', 'bursar', 'principal']))
      throw redirect({ to: '/' });
  },
});

const healthRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/health',
  component: lazyRouteComponent(() => import('../features/health/HealthPage'), 'HealthPage'),
  beforeLoad: () => {
    if (!hasRole(['admin', 'superadmin', 'owner', 'nurse', 'health_officer']))
      throw redirect({ to: '/' });
  },
});

const academicsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/academics',
  component: lazyRouteComponent(
    () => import('../features/academics/AcademicsPage'),
    'AcademicsPage'
  ),
});

// New module routes
const admissionsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/admissions',
  component: lazyRouteComponent(
    () => import('../features/admissions/ApplicationListPage'),
    'ApplicationListPage'
  ),
});
const emergencyRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/emergency',
  component: lazyRouteComponent(
    () => import('../features/emergency/EmergencyPage'),
    'EmergencyPage'
  ),
});
const specialNeedsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/special-needs',
  component: lazyRouteComponent(() => import('../features/special_needs/IEPPage'), 'IEPPage'),
});
const inventoryRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/inventory',
  component: lazyRouteComponent(
    () => import('../features/inventory/InventoryPage'),
    'InventoryPage'
  ),
});
const libraryRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/library',
  component: lazyRouteComponent(() => import('../features/library/LibraryPage'), 'LibraryPage'),
});
const payrollRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/payroll',
  component: lazyRouteComponent(() => import('../features/payroll/PayrollPage'), 'PayrollPage'),
});
const leaveRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/leave',
  component: lazyRouteComponent(
    () => import('../features/leave_management/LeavePage'),
    'LeavePage'
  ),
});
const examRegRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/exam-registration',
  component: lazyRouteComponent(
    () => import('../features/exam_registration/ExamRegPage'),
    'ExamRegPage'
  ),
});
const disciplineRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/discipline',
  component: lazyRouteComponent(
    () => import('../features/discipline/DisciplinePage'),
    'DisciplinePage'
  ),
});
const proprietorRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/proprietor',
  component: lazyRouteComponent(
    () => import('../features/proprietor/ProprietorPage'),
    'ProprietorPage'
  ),
  beforeLoad: () => {
    if (!hasRole(['superadmin', 'owner'])) throw redirect({ to: '/' });
  },
});
const accreditationRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/accreditation',
  component: lazyRouteComponent(
    () => import('../features/accreditation/AccreditationPage'),
    'AccreditationPage'
  ),
});
const ministryRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/ministry-reports',
  component: lazyRouteComponent(
    () => import('../features/ministry_reporting/MinistryPage'),
    'MinistryPage'
  ),
});
const waecBulkRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/waec-registration',
  component: lazyRouteComponent(() => import('../features/waec_bulk/WAECBulkPage'), 'WAECBulkPage'),
});
const fundraisingRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/fundraising',
  component: lazyRouteComponent(
    () => import('../features/fundraising/FundraisingPage'),
    'FundraisingPage'
  ),
});
const projectsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/projects',
  component: lazyRouteComponent(
    () => import('../features/building_projects/ProjectsPage'),
    'ProjectsPage'
  ),
});
const clubsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/clubs',
  component: lazyRouteComponent(() => import('../features/clubs/ClubsPage'), 'ClubsPage'),
});
const busRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/bus-tracking',
  component: lazyRouteComponent(() => import('../features/bus_tracking/BusPage'), 'BusPage'),
});
const cafeteriaRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/cafeteria',
  component: lazyRouteComponent(
    () => import('../features/cafeteria/CafeteriaPage'),
    'CafeteriaPage'
  ),
});
const girlChildRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/girl-child',
  component: lazyRouteComponent(
    () => import('../features/girl_child_tracking/GirlChildPage'),
    'GirlChildPage'
  ),
});
const inspectionRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/inspections',
  component: lazyRouteComponent(
    () => import('../features/inspection_tracking/InspectionPage'),
    'InspectionPage'
  ),
});
const smcRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/smc-reports',
  component: lazyRouteComponent(() => import('../features/smc_reporting/SMCPage'), 'SMCPage'),
});
const custodyRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/custody',
  component: lazyRouteComponent(() => import('../features/custody/CustodyPage'), 'CustodyPage'),
});
const retentionRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/data-retention',
  component: lazyRouteComponent(
    () => import('../features/data_retention/RetentionPage'),
    'RetentionPage'
  ),
});
const messagingRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/messaging',
  component: lazyRouteComponent(
    () => import('../features/messaging/MessagingPage'),
    'MessagingPage'
  ),
});
const lmsRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/lms',
  component: lazyRouteComponent(() => import('../features/lms/AssignmentsPage'), 'AssignmentsPage'),
});
const hostelRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/hostel',
  component: lazyRouteComponent(() => import('../features/hostel/HostelPage'), 'HostelPage'),
});
const calendarRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/calendar',
  component: lazyRouteComponent(() => import('../features/calendar/CalendarPage'), 'CalendarPage'),
});
const alumniRoute = createRoute({
  getParentRoute: () => authRoute,
  path: '/alumni',
  component: lazyRouteComponent(() => import('../features/alumni/AlumniPage'), 'AlumniPage'),
});

export const routeTree = rootRoute.addChildren([
  loginRoute,
  forgotPasswordRoute,
  resetPasswordRoute,
  parentLoginRoute,
  authRoute.addChildren([
    indexRoute,
    studentsRoute,
    studentDetailRoute,
    guardiansRoute,
    guardianDetailRoute,
    attendanceRoute,
    staffRoute,
    staffTimetableRoute,
    staffAttendanceRoute,
    parentChildrenRoute,
    intelligenceRoute,
    adminRoute,
    financeRoute,
    healthRoute,
    academicsRoute,
    admissionsRoute,
    emergencyRoute,
    specialNeedsRoute,
    inventoryRoute,
    libraryRoute,
    payrollRoute,
    leaveRoute,
    examRegRoute,
    disciplineRoute,
    proprietorRoute,
    accreditationRoute,
    ministryRoute,
    waecBulkRoute,
    fundraisingRoute,
    projectsRoute,
    clubsRoute,
    busRoute,
    cafeteriaRoute,
    girlChildRoute,
    inspectionRoute,
    smcRoute,
    custodyRoute,
    retentionRoute,
    messagingRoute,
    lmsRoute,
    hostelRoute,
    calendarRoute,
    alumniRoute,
  ]),
  notFoundRoute,
]);
