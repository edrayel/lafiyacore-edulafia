# UI Border Radius Standardization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize the border radius across the application to a consistent 12px for all core UI elements (Buttons, TextInputs, Cards, Dialogs, DataGrids, and Papers).

**Architecture:** We will modify the core Material-UI theme configurations (`apps/frontend/src/shared/theme/index.ts`) to enforce the new `12px` border radius globally. Additionally, we will run a codebase-wide sweep to remove any hardcoded `borderRadius: 3` (which scales to 24px) or pill-shaped `borderRadius: 24` overrides that are currently overriding the theme on specific components like `Paper` or `Button`.

**Tech Stack:** React, Material-UI (MUI), Node.js (for AST/Regex codebase sweeping).

---

### Task 1: Update Global MUI Theme Configuration

**Files:**
- Modify: `apps/frontend/src/shared/theme/index.ts`

- [ ] **Step 1: Update the BASE_CONFIG shape**
Change `shape: { borderRadius: 12 }` to ensure the base multiplier is exactly what we want. (It is currently 12, but we need to ensure components aren't multiplying it).

- [ ] **Step 2: Standardize Button borderRadius in LIGHT_THEME and DARK_THEME**
Locate `MuiButton.styleOverrides.root.borderRadius` in both themes. Change it from `24` to `12`.

- [ ] **Step 3: Standardize Card and TextField borderRadius**
Locate `MuiCard.styleOverrides.root.borderRadius` and change from `16` to `12`.
Locate `MuiTextField.styleOverrides.root['& .MuiOutlinedInput-root'].borderRadius` and change from `10` to `12`.

- [ ] **Step 4: Commit Theme Changes**
```bash
git add apps/frontend/src/shared/theme/index.ts
git commit -m "style: standardize global theme border radius to 12px"
```

---

### Task 2: Remove Hardcoded `borderRadius: 3` Overrides on Paper Components

**Files:**
- Modify: `apps/frontend/src/features/**/*.tsx`

- [ ] **Step 1: Create a sweeping script to remove hardcoded `borderRadius: 3` from `Paper`**
Create `scripts/utils/fix_paper_radius.js` to search and replace `borderRadius: 3` (which MUI calculates as 3 * 8px = 24px) from `sx` props on `Paper` components.

```javascript
const fs = require('fs');
const glob = require('glob');

const files = glob.sync('apps/frontend/src/features/**/*.tsx');
let changedFiles = 0;

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  // Replace `borderRadius: 3` inside sx props
  const regex = /borderRadius:\s*3,?/g;
  
  if (regex.test(content)) {
    content = content.replace(regex, '');
    // Clean up empty sx props or dangling commas if necessary
    content = content.replace(/sx=\{\{\s*,\s*/g, 'sx={{ ');
    content = content.replace(/,\s*\}/g, ' }');
    fs.writeFileSync(file, content);
    changedFiles++;
    console.log(`Updated: ${file}`);
  }
});

console.log(`Finished. Changed ${changedFiles} files.`);
```

- [ ] **Step 2: Execute the script**
Run: `node scripts/utils/fix_paper_radius.js`

- [ ] **Step 3: Verify TypeScript Compilation**
Run: `cd apps/frontend && pnpm -s type-check`
Expected: No type errors.

- [ ] **Step 4: Commit Codebase Changes**
```bash
git add apps/frontend/src/features/
git commit -m "style: remove hardcoded borderRadius overrides from Paper components"
```
