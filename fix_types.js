const fs = require('fs');

function regexReplaceInFile(path, regex, newStr) {
  if (fs.existsSync(path)) {
    const content = fs.readFileSync(path, 'utf8');
    fs.writeFileSync(path, content.replace(regex, newStr), 'utf8');
  }
}

// AdminPage.tsx
let adminContent = fs.readFileSync('apps/frontend/src/features/admin/AdminPage.tsx', 'utf8');
if (!adminContent.includes('const queryClient = useQueryClient();')) {
  adminContent = adminContent.replace('export function AdminPage() {', "import { useQueryClient } from '@tanstack/react-query';\nexport function AdminPage() {\n  const queryClient = useQueryClient();");
  fs.writeFileSync('apps/frontend/src/features/admin/AdminPage.tsx', adminContent, 'utf8');
}

// AttendancePage.tsx
regexReplaceInFile('apps/frontend/src/features/attendance/AttendancePage.tsx', /Object\.entries\(statusConfig\)\.map\(\(\[, config\]/g, 'Object.entries(statusConfig).map(([key, config]');
let attContent = fs.readFileSync('apps/frontend/src/features/attendance/AttendancePage.tsx', 'utf8');
if (!attContent.includes('const chartData = [')) {
  const chartDataStr = `
  const chartData = [
    { name: 'Present', value: stats?.present || 0, hex: statusConfig.present.hex },
    { name: 'Absent', value: stats?.absent || 0, hex: statusConfig.absent.hex },
    { name: 'Late', value: stats?.late || 0, hex: statusConfig.late.hex },
    { name: 'Excused', value: stats?.excused || 0, hex: statusConfig.excused.hex },
  ];
  const isLoading = isStudentsLoading || isAttendanceLoading;
  const isError = isStudentsError || isAttendanceError;
`;
  attContent = attContent.replace('return (', chartDataStr + '\n  return (');
  fs.writeFileSync('apps/frontend/src/features/attendance/AttendancePage.tsx', attContent, 'utf8');
}

// ParentPage.tsx
let parentContent = fs.readFileSync('apps/frontend/src/features/parent/ParentPage.tsx', 'utf8');
if (!parentContent.includes('const [excusalOpen, setExcusalOpen] = useState(false);')) {
  parentContent = parentContent.replace('export function ParentPage() {', "export function ParentPage() {\n  const [excusalOpen, setExcusalOpen] = useState(false);\n  const [feedbackOpen, setFeedbackOpen] = useState(false);");
  fs.writeFileSync('apps/frontend/src/features/parent/ParentPage.tsx', parentContent, 'utf8');
}

// db.test.ts
regexReplaceInFile('apps/frontend/src/shared/api/offline/db.test.ts', /expect\(retrieved\._id\)/g, 'expect((retrieved as any)._id)');
regexReplaceInFile('apps/frontend/src/shared/api/offline/db.test.ts', /expect\(retrieved\.data\.status\)/g, 'expect((retrieved as any).data.status)');

console.log('Done fixing types');
