const fs = require('fs');

const files = [
  'src/features/guardians/GuardianDetailPage.tsx',
  'src/features/parent/ParentPage.tsx',
  'src/features/students/StudentDetailPage.tsx',
  'src/features/auth/LoginPage.tsx',
  'src/features/auth/ForgotPasswordPage.tsx',
  'src/features/auth/ResetPasswordPage.tsx',
];

for (const file of files) {
  if (fs.existsSync(file)) {
    let content = fs.readFileSync(file, 'utf8');

    // Fix IconButton aria-labels
    content = content.replace(
      /<IconButton onClick=\{onBack\}>/g,
      '<IconButton aria-label="Go back" onClick={onBack}>'
    );
    content = content.replace(
      /<IconButton\s+size="small"\s+color="error"\s+onClick=\{/g,
      '<IconButton aria-label="Unlink student" size="small" color="error" onClick={'
    );
    content = content.replace(
      /<IconButton onClick=\{/g,
      '<IconButton aria-label="Action" onClick={'
    );

    // Fix invisible links
    content = content.replace(
      /style=\{\{ textDecoration: 'none', color: 'inherit' \}\}/g,
      'style={{ textDecoration: "underline", color: "inherit" }}'
    );

    fs.writeFileSync(file, content);
  }
}
