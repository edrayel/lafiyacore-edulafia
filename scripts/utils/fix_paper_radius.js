const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
  });
}

let changedFiles = 0;
const rootDir = path.join(__dirname, '../../apps/frontend/src/features');

walkDir(rootDir, file => {
  if (!file.endsWith('.tsx')) return;
  
  let content = fs.readFileSync(file, 'utf8');
  const regex = /borderRadius:\s*[34],?\s*/g;
  
  if (regex.test(content)) {
    content = content.replace(regex, '');
    content = content.replace(/sx=\{\{\s*,\s*/g, 'sx={{ ');
    content = content.replace(/,\s*\}/g, ' }');
    fs.writeFileSync(file, content);
    changedFiles++;
    console.log(`Updated: ${file}`);
  }
});

console.log(`Finished. Changed ${changedFiles} files.`);
