const fs = require('fs');
const path = require('path');

const filesToFixAny = [
  'apps/frontend/src/app/router.tsx',
  'apps/frontend/src/features/attendance/AttendancePage.tsx',
  'apps/frontend/src/features/attendance/api.ts',
  'apps/frontend/src/features/auth/ResetPasswordPage.tsx',
  'apps/frontend/src/features/guardians/GuardianDetailPage.tsx',
  'apps/frontend/src/features/staff/TimetablePage.tsx',
  'apps/frontend/src/features/staff/api.ts',
  'apps/frontend/src/shared/api/offline/db.test.ts',
  'apps/frontend/src/shared/stores/authStore.test.ts',
  'apps/frontend/src/shared/stores/authStore.ts'
];

for (const file of filesToFixAny) {
  if (fs.existsSync(file)) {
    let content = fs.readFileSync(file, 'utf8');
    content = content.replace(/: any/g, ': unknown');
    content = content.replace(/as any/g, 'as unknown');
    content = content.replace(/<any>/g, '<unknown>');
    fs.writeFileSync(file, content);
  }
}
