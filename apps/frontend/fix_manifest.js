const fs = require('fs');

if (fs.existsSync('public/manifest.json')) {
  fs.unlinkSync('public/manifest.json');
  console.log('Removed redundant public/manifest.json');
}

let content = fs.readFileSync('index.html', 'utf8');
content = content.replace(/<link rel="manifest" href="\/manifest\.json" \/>\n\s*/g, '');
fs.writeFileSync('index.html', content);
console.log('Removed manual manifest link from index.html');
