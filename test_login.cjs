const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
  await page.fill('input[type="email"]', 'admin@demo.edu.ng');
  await page.fill('input[type="password"]', 'DemoPass123!');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2000);
  
  console.log('Current URL:', page.url());
  
  await browser.close();
})();
