const fs = require('fs');

let file = 'src/features/auth/ResetPasswordPage.tsx';
let content = fs.readFileSync(file, 'utf8');
content = content.replace(/catch \(e: unknown\) {/g, 'catch (e: any) {');
fs.writeFileSync(file, content);

file = 'src/features/guardians/GuardianDetailPage.tsx';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/\{mockGuardian\.students\.map\(\(student: unknown\) => \(/g, '{mockGuardian.students.map((student: any) => (');
fs.writeFileSync(file, content);

file = 'src/shared/api/offline/db.test.ts';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/\(retrieved as unknown\)\._id/g, '(retrieved as any)._id');
content = content.replace(/\(retrieved as unknown\)\.data\.status/g, '(retrieved as any).data.status');
fs.writeFileSync(file, content);

file = 'src/shared/stores/authStore.test.ts';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/\(authApi\.login as unknown\)\./g, '(authApi.login as any).');
content = content.replace(/\(authApi\.getMe as unknown\)\./g, '(authApi.getMe as any).');
content = content.replace(/\(authApi\.logout as unknown\)\./g, '(authApi.logout as any).');
content = content.replace(/\} as unknown/g, '} as any');
fs.writeFileSync(file, content);

file = 'src/shared/stores/authStore.ts';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/catch \(err: unknown\) {/g, 'catch (err: any) {');
content = content.replace(/catch \(e: unknown\) {/g, 'catch (e: any) {');
fs.writeFileSync(file, content);
