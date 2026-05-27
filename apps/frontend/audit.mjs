import { chromium } from '@playwright/test';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const OUT_DIR = path.join(__dirname, '../../dogfood-output/screenshots');

async function run() {
  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log(`PAGE ERROR: ${msg.text()}`);
    }
  });
  
  page.on('pageerror', exception => {
    console.log(`UNCAUGHT EXCEPTION: ${exception}`);
  });

  console.log("Navigating to login page...");
  await page.goto('http://localhost:5174/');

  // Wait for login form
  await page.waitForSelector('input[type="email"]');
  
  console.log("Filling credentials...");
  await page.fill('input[type="email"]', 'admin@edulafia.com');
  await page.fill('input[type="password"]', 'Admin123!');
  
  console.log("Submitting login...");
  await page.click('button[type="submit"]');

  // Wait for dashboard to load (wait for a known element or network idle)
  console.log("Waiting for dashboard to load...");
  await page.waitForURL('**/dashboard', { timeout: 10000 }).catch(() => console.log("Did not reach /dashboard, staying on current page."));
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000); // extra wait for animations

  console.log("Taking dashboard screenshot...");
  await page.screenshot({ path: path.join(OUT_DIR, '01-dashboard.png') });

  // Get all navigation links from the sidebar
  // Typically they are inside a nav element or have specific classes.
  // Let's just find all unique hrefs that start with '/' or the base URL.
  const links = await page.evaluate(() => {
    const anchors = Array.from(document.querySelectorAll('a'));
    const hrefs = anchors.map(a => a.getAttribute('href')).filter(h => h && h.startsWith('/') && !h.startsWith('/auth'));
    return Array.from(new Set(hrefs));
  });

  console.log(`Found ${links.length} internal links to visit:`, links);

  let counter = 2;
  for (const link of links.slice(0, 10)) { // Limit to 10 for time constraints, or we can do all.
    console.log(`Visiting ${link}...`);
    try {
      await page.goto(`http://localhost:5174${link}`);
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(1000); // wait for data fetch
      
      const safeName = link.replace(/[\/\?]/g, '_') || 'home';
      const fileName = `${counter.toString().padStart(2, '0')}-${safeName}.png`;
      await page.screenshot({ path: path.join(OUT_DIR, fileName), fullPage: true });
      console.log(`Saved ${fileName}`);
      counter++;
    } catch (e) {
      console.error(`Failed to visit ${link}:`, e.message);
    }
  }

  await browser.close();
  console.log("Audit screenshots complete.");
}

run().catch(console.error);
