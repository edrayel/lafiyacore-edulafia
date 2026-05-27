const fs = require('fs');

function regexReplaceInFile(path, regex, newStr) {
  if (fs.existsSync(path)) {
    const content = fs.readFileSync(path, 'utf8');
    fs.writeFileSync(path, content.replace(regex, newStr), 'utf8');
  }
}

// router.tsx
regexReplaceInFile('apps/frontend/src/app/router.tsx', /error: any/g, 'error: unknown');

// AcademicsPage.tsx
regexReplaceInFile('apps/frontend/src/features/academics/AcademicsPage.tsx', /const existingResults = \[\];/g, '');
regexReplaceInFile('apps/frontend/src/features/academics/AcademicsPage.tsx', /const existingResults = await [^\n]+\n/g, '');
regexReplaceInFile('apps/frontend/src/features/academics/AcademicsPage.tsx', /if \(existingResults/g, 'if (false');

// AdminPage.tsx
regexReplaceInFile('apps/frontend/src/features/admin/AdminPage.tsx', /useQueryClient,\s*/g, '');

// AttendancePage.tsx
regexReplaceInFile('apps/frontend/src/features/attendance/AttendancePage.tsx', /const handleDateChange = useCallback[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n/g, '');
regexReplaceInFile('apps/frontend/src/features/attendance/AttendancePage.tsx', /error: any/g, 'error: unknown');

// attendance/api.ts
regexReplaceInFile('apps/frontend/src/features/attendance/api.ts', /error: any/g, 'error: unknown');

// ResetPasswordPage.tsx
regexReplaceInFile('apps/frontend/src/features/auth/ResetPasswordPage.tsx', /error: any/g, 'error: unknown');

// GuardianDetailPage.tsx
regexReplaceInFile('apps/frontend/src/features/guardians/GuardianDetailPage.tsx', /error: any/g, 'error: unknown');

// ParentLoginPage.tsx
regexReplaceInFile('apps/frontend/src/features/parent/ParentLoginPage.tsx', /const sessionId = [^\n]+\n/g, '');

// ParentPage.tsx
regexReplaceInFile('apps/frontend/src/features/parent/ParentPage.tsx', /FinanceRecord,\s*/g, '');
regexReplaceInFile('apps/frontend/src/features/parent/ParentPage.tsx', /const financeStatusConfig = \{[\s\S]*?\};\n/g, '');

// TimetablePage.tsx
regexReplaceInFile('apps/frontend/src/features/staff/TimetablePage.tsx', /error: any/g, 'error: unknown');

// staff/api.ts
regexReplaceInFile('apps/frontend/src/features/staff/api.ts', /error: any/g, 'error: unknown');

// SyncStatusIndicator.tsx
regexReplaceInFile('apps/frontend/src/shared/components/SyncStatusIndicator.tsx', /CircularProgress,\s*/g, '');

// authStore.test.ts
regexReplaceInFile('apps/frontend/src/shared/stores/authStore.test.ts', /catch \(_e\)/g, 'catch');

// authStore.ts
regexReplaceInFile('apps/frontend/src/shared/stores/authStore.ts', /error: any/g, 'error: unknown');
regexReplaceInFile('apps/frontend/src/shared/stores/authStore.ts', /error\.response\?\.data\?\.detail/g, '((error as { response?: { data?: { detail?: string } } }).response?.data?.detail)');

console.log('Done fixing lint issues 3');
