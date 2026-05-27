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

    const buggyStr = "onClick={() = sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}>";
    
    // Split by the buggy string
    if (content.includes(buggyStr)) {
        let parts = content.split(buggyStr);
        let newContent = parts[0];
        
        for (let i = 1; i < parts.length; i++) {
            let rest = parts[i];
            // ' setFeeDialogOpen(true)}'
            // We need to find where the `}` is for the onClick closure, but actually wait:
            // original was: `onClick={() => setFeeDialogOpen(true)}`
            // So `rest` is ` setFeeDialogOpen(true)}` (or whatever was after `>`)
            // We want to transform:
            // `onClick={() => setFeeDialogOpen(true)} sx={{ borderRadius... }}>`
            // Wait, `rest` continues until the `>` of the button? No, the button `>` is ALREADY consumed?
            // Original line:
            // `<Button variant="contained" startIcon={<AddIcon />} onClick={() => setFeeDialogOpen(true)}>`
            // My script replaced `<Button variant="contained" startIcon={<AddIcon />} onClick={() `
            // with `<Button variant="contained" startIcon={<AddIcon />} onClick={() sx={{ ... }}>`
            // So it became `<Button ... onClick={() sx={{...}}> => setFeeDialogOpen(true)}>`
            // Let's check `grep` output exactly.
            // `onClick={() = sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}> setFeeDialogOpen(true)}`
            // Wait, why is there an `=` in `onClick={() = sx`?
            // Because my regex was `([^>]*?)>`.
            // The original was `onClick={() => ...}`
            // The regex matched `onClick={() =` as `p1` because `>` was the next character!
            // So `p1` was ` onClick={() =`
            // Replacement: `onClick={() = sx={{...}}>`
            // Then the rest of the string was ` setFeeDialogOpen(true)}>`
        }
    }

    // A much simpler regex replacement:
    // Match: `onClick=\{\(\) = sx=\{\{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba\(56, 189, 248, 0.39\)', '&:hover': \{ boxShadow: '0 6px 20px rgba\(56, 189, 248, 0.23\)' \} \}\}> (.*?)\}>`
    // Wait, the rest of the line is ` setFeeDialogOpen(true)}>` or similar.
    // Sometimes it's on a new line! Let's just match `onClick={() = sx={{...}}>` and the following characters up to `}`
    
    let regex = /onClick=\{\(\) = sx=\{\{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba\(56, 189, 248, 0.39\)', '&:hover': \{ boxShadow: '0 6px 20px rgba\(56, 189, 248, 0.23\)' \} \}\}>([\s\S]*?)\}>/g;
    
    content = content.replace(regex, `onClick={() =>$1} sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}>`);

    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Fixed ${path.basename(filePath)}`);
    }
  }
});
