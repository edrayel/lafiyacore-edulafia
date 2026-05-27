const fs = require('fs');

const file = 'apps/frontend/src/features/attendance/AttendancePage.tsx';
let content = fs.readFileSync(file, 'utf8');

// Manual safe fixes
content = content.replace(/\[_key, config\]ew Date/g, 'new Date');
content = content.replace(/\[_key, config\]alse/g, 'false');
content = content.replace(/\[_key, config\]ull/g, 'null');
content = content.replace(/\[_key, config\]sInitialized/g, 'isInitialized');
content = content.replace(/\[_key, config\]sStudentsSuccess/g, 'isStudentsSuccess');
content = content.replace(/\[_key, config\]lassId/g, 'classId');
content = content.replace(/\[_key, config\]rror/g, 'error');
content = content.replace(/\(\[_key, config\]\) => c !== code/g, '(c) => c !== code');
content = content.replace(/\(\[_key, config\]\) => updateActiveRow\(\{ notes: e/g, '(e) => updateActiveRow({ notes: e');
content = content.replace(/\(\[_key, config\]\) => handleClassChange\(\[_key, config\]/g, '(e) => handleClassChange(e');
content = content.replace(/\(\[_key, config\]\) => setBulkStatus\(\[_key, config\]/g, '(e) => setBulkStatus(e');
content = content.replace(/\(\[_key, config\]\) => updateActiveRow\(\{ reason_code: e/g, '(e) => updateActiveRow({ reason_code: e');
content = content.replace(/\[_key, config\]ode: string/g, 'code: string');

fs.writeFileSync(file, content);
console.log('Fixed AttendancePage.tsx');
