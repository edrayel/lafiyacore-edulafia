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

const H2_REGEX = /<Typography\s+variant="h2"([^>]*)>([\s\S]*?)<\/Typography>/g;
const H2_REPLACEMENT = `<Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}>$2</Typography>
      </Box>`;

const PAPER_P2_REGEX = /<Paper\s+sx=\{\{\s*p:\s*2,\s*mb:\s*2\s*\}\}>/g;
const PAPER_P2_REPLACEMENT = `<Paper elevation={0} sx={{ p: 2, mb: 3, borderRadius: 3, border: '1px solid', borderColor: 'divider', bgcolor: 'background.paper' }}>`;

const PAPER_HEIGHT_DATAGRID_REGEX = /<Paper\s+sx=\{\{\s*height:\s*([0-9]+)\s*\}\}>(\s*)<DataGrid/g;
const PAPER_HEIGHT_DATAGRID_REPLACEMENT = `<Paper elevation={0} sx={{ height: $1, width: '100%', borderRadius: 3, border: '1px solid', borderColor: 'divider', bgcolor: 'background.paper', overflow: 'hidden' }}>$2<DataGrid`;

// Fix <Paper sx={{ mb: 3 }}> containing <Tabs
const PAPER_TABS_REGEX = /<Paper\s+sx=\{\{\s*mb:\s*3\s*\}\}>(\s*)<Tabs/g;
const PAPER_TABS_REPLACEMENT = `<Paper elevation={0} sx={{ mb: 3, borderRadius: 3, border: '1px solid', borderColor: 'divider', bgcolor: 'background.paper', overflow: 'hidden' }}>$1<Tabs`;

walk(featuresDir, (filePath) => {
  if (filePath.endsWith('.tsx')) {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    content = content.replace(H2_REGEX, H2_REPLACEMENT);
    content = content.replace(PAPER_P2_REGEX, PAPER_P2_REPLACEMENT);
    content = content.replace(PAPER_HEIGHT_DATAGRID_REGEX, PAPER_HEIGHT_DATAGRID_REPLACEMENT);
    content = content.replace(PAPER_TABS_REGEX, PAPER_TABS_REPLACEMENT);
    
    // Safer button replacement: 
    // Find: <Button variant="contained" startIcon={<AddIcon />}
    // and if there's no `sx=` before the next `>`, inject `sx={{ ... }}` before it.
    // We can do this safely by matching the exact string up to the `>`
    // The issue with my previous regex was `([^>]*?)>` matched `onClick={() =>` because `>` was in it.
    // Instead, match `<Button[^>]*startIcon={<AddIcon />}[^>]*>`
    // Wait, the `>` in the arrow function `=>` breaks `[^>]*`.
    // Let's use a function to parse the tag.
    
    // A much safer way: just do string replacement on the exact literal if it's common
    // `variant="contained" startIcon={<AddIcon />}`
    // Let's just find `variant="contained" startIcon={<AddIcon />}` and replace it with `variant="contained" startIcon={<AddIcon />} sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}`
    // Wait, what if it already has `sx=`?
    // We can use a lookahead or just assume none of them do (which is mostly true for these Add buttons).
    content = content.replace(/variant="contained"\s*startIcon=\{<AddIcon \/>\}(?!\s*sx=)/g, `variant="contained" startIcon={<AddIcon />} sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600, boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)', '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' } }}`);

    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Updated ${path.basename(filePath)}`);
    }
  }
});
