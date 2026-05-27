const fs = require('fs');
const path = require('path');

const featuresDir = path.join(__dirname, 'apps/frontend/src/features');

function walk(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walk(dirPath, callback) : callback(dirPath);
  });
}

walk(featuresDir, (filePath) => {
  if (filePath.endsWith('.tsx')) {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    const toRemove = "} sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}>";
    const toRemove2 = "}} sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}>";
    
    // Replace where it is appended to another sx
    content = content.split(toRemove2).join("}}>");
    content = content.split(toRemove).join("}>");

    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Fixed duplicates in ${path.basename(filePath)}`);
    }
  }
});
