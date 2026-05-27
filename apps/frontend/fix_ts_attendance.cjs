const fs = require('fs');

let file = 'src/features/attendance/AttendancePage.tsx';
let content = fs.readFileSync(file, 'utf8');
content = content.replace(/\(error as unknown\)\?\.response/g, '(error as any)?.response');
fs.writeFileSync(file, content);

file = 'src/features/attendance/api.ts';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/\(row.doc as unknown\).type/g, '(row.doc as any).type');
content = content.replace(/const { _id, _rev, type: _type, ...rest } = doc;/g, 'const { _id, _rev, type: _type, ...rest } = doc as any;');
content = content.replace(/return results as unknown;/g, 'return results as any;');
fs.writeFileSync(file, content);
