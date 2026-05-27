const fs = require('fs');

const replaces = [
  ['apps/frontend/src/features/academics/AcademicsPage.tsx', /const existingResults =/g, 'const _existingResults ='],
  ['apps/frontend/src/features/attendance/AttendancePage.tsx', /\(value, key\)/g, '(value, _key)'],
  ['apps/frontend/src/features/parent/ParentLoginPage.tsx', /const sessionId =/g, 'const _sessionId ='],
  ['apps/frontend/src/features/parent/ParentPage.tsx', /type FinanceRecord/g, 'type _FinanceRecord'],
  ['apps/frontend/src/features/parent/ParentPage.tsx', /const financeStatusConfig =/g, 'const _financeStatusConfig ='],
  ['apps/frontend/src/features/parent/ParentPage.tsx', /const \[excusalOpen/g, 'const [_excusalOpen'],
  ['apps/frontend/src/features/parent/ParentPage.tsx', /const \[feedbackOpen/g, 'const [_feedbackOpen'],
  ['apps/frontend/src/shared/components/SyncStatusIndicator.tsx', /CircularProgress, /g, ''],
];

for (const [file, regex, replacement] of replaces) {
  if (fs.existsSync(file)) {
    let content = fs.readFileSync(file, 'utf8');
    content = content.replace(regex, replacement);
    fs.writeFileSync(file, content);
  }
}
