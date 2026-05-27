const fs = require('fs');

function regexReplaceInFile(path, regex, newStr) {
  if (fs.existsSync(path)) {
    const content = fs.readFileSync(path, 'utf8');
    fs.writeFileSync(path, content.replace(regex, newStr), 'utf8');
  }
}

// AdminPage.tsx
regexReplaceInFile('apps/frontend/src/features/admin/AdminPage.tsx', /useQueryClient,\s*/g, '');
regexReplaceInFile('apps/frontend/src/features/admin/AdminPage.tsx', /import { useQuery, useMutation } from '@tanstack\/react-query';/, "import { useQuery, useMutation } from '@tanstack/react-query';");

// AttendancePage.tsx
regexReplaceInFile('apps/frontend/src/features/attendance/AttendancePage.tsx', /const handleDateChange = useCallback\([^}]+\};\n/g, '');
regexReplaceInFile('apps/frontend/src/features/attendance/AttendancePage.tsx', /error: any/g, 'error: unknown');

// authStore.ts
regexReplaceInFile('apps/frontend/src/shared/stores/authStore.ts', /error: any/g, 'error: unknown');

// AppLayout.tsx
regexReplaceInFile('apps/frontend/src/shared/components/AppLayout.tsx', /useNavigate,\s*/g, '');

// HealthPage.tsx
regexReplaceInFile('apps/frontend/src/features/health/HealthPage.tsx', /updateReferral,\s*/g, '');
regexReplaceInFile('apps/frontend/src/features/health/HealthPage.tsx', /createVaccination,\s*/g, '');
regexReplaceInFile('apps/frontend/src/features/health/HealthPage.tsx', /Vaccination,\s*/g, '');
regexReplaceInFile('apps/frontend/src/features/health/HealthPage.tsx', /CreateVaccinationPayload,\s*/g, '');

// ResetPasswordPage.tsx
regexReplaceInFile('apps/frontend/src/features/auth/ResetPasswordPage.tsx', /error: any/g, 'error: unknown');

// GuardianDetailPage.tsx
regexReplaceInFile('apps/frontend/src/features/guardians/GuardianDetailPage.tsx', /error: any/g, 'error: unknown');

// TimetablePage.tsx
regexReplaceInFile('apps/frontend/src/features/staff/TimetablePage.tsx', /error: any/g, 'error: unknown');

// staff/api.ts
regexReplaceInFile('apps/frontend/src/features/staff/api.ts', /error: any/g, 'error: unknown');

// attendance/api.ts
regexReplaceInFile('apps/frontend/src/features/attendance/api.ts', /error: any/g, 'error: unknown');

// SyncStatusIndicator.tsx
regexReplaceInFile('apps/frontend/src/shared/components/SyncStatusIndicator.tsx', /CircularProgress,\s*/g, '');

console.log('Done fixing lint issues 2');
