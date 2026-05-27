const { chromium } = require('playwright');

const BASE_URL = 'http://localhost:5173';

const USERS = [
  { role: 'school_admin', email: 'admin@demo.edu.ng', pass: 'DemoPass123!' },
  { role: 'teacher', email: 'teacher@demo.edu.ng', pass: 'DemoPass123!' },
  { role: 'parent', email: 'parent@demo.edu.ng', pass: 'DemoPass123!' }
];

async function login(page, email, pass) {
  console.log(`\nLogging in as ${email}...`);
  await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle' });
  await page.fill('input[type="email"]', email);
  await page.fill('input[type="password"]', pass);
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);
}

async function logout(page) {
  console.log('Logging out...');
  const menuButton = page.locator('button', { hasText: /demo|admin|teacher|parent/i }).first();
  if (await menuButton.count() > 0) {
    await menuButton.click();
    await page.locator('text=Sign out').click().catch(() => {});
    await page.locator('text=Logout').click().catch(() => {});
  } else {
    await page.context().clearCookies();
    await page.evaluate(() => localStorage.clear());
  }
  await page.goto(`${BASE_URL}/login`);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Handle errors
  page.on('pageerror', err => console.log('PageError:', err.message));
  page.on('console', msg => {
    if (msg.type() === 'error') console.log('ConsoleError:', msg.text());
  });

  try {
    // 1. School Admin Flow
    await login(page, USERS[0].email, USERS[0].pass);
    
    console.log('Admin: Exploring Admissions...');
    await page.goto(`${BASE_URL}/admissions`, { waitUntil: 'networkidle' });
    const newAppBtn = page.locator('button', { hasText: 'New Application' }).first();
    if (await newAppBtn.count() > 0) {
      await newAppBtn.click();
      await page.fill('input[name="first_name"]', 'TestFirst');
      await page.fill('input[name="last_name"]', 'TestLast');
      await page.fill('input[name="guardian_email"]', 'testguardian@demo.edu.ng');
      await page.fill('input[name="guardian_phone"]', '+2348000000000');
      await page.locator('button:has-text("Submit")').first().click().catch(() => {});
      await page.waitForTimeout(1000);
    }

    console.log('Admin: Exploring Students...');
    await page.goto(`${BASE_URL}/students`, { waitUntil: 'networkidle' });
    const addStudentBtn = page.locator('button', { hasText: 'Add Student' }).first();
    if (await addStudentBtn.count() > 0) {
      await addStudentBtn.click();
      await page.fill('input[name="first_name"]', 'John');
      await page.fill('input[name="last_name"]', 'Doe');
      await page.fill('input[name="admission_number"]', 'ADM' + Date.now());
      await page.locator('button:has-text("Save")').first().click().catch(() => {});
      await page.waitForTimeout(1000);
    }

    await logout(page);

    // 2. Teacher Flow
    await login(page, USERS[1].email, USERS[1].pass);
    console.log('Teacher: Exploring Attendance...');
    await page.goto(`${BASE_URL}/attendance`, { waitUntil: 'networkidle' });
    const classSelect = page.locator('div[role="combobox"]').first();
    if (await classSelect.count() > 0) {
      await classSelect.click();
      await page.locator('li[role="option"]').first().click().catch(() => {});
    }
    await logout(page);

    // 3. Parent Flow
    await login(page, USERS[2].email, USERS[2].pass);
    console.log('Parent: Exploring Children Portal...');
    await page.goto(`${BASE_URL}/parent/children`, { waitUntil: 'networkidle' });
    
    // Check for crash
    const content = await page.content();
    if (content.includes('Something went wrong!')) {
      console.error('ERROR: Parent portal crashed with Error Boundary!');
    } else {
      console.log('SUCCESS: Parent portal loaded correctly.');
    }
    await logout(page);

    console.log('\n--- Autonomous Testing Complete! ---');

  } catch (e) {
    console.error('Script Error:', e);
  } finally {
    await browser.close();
  }
})();
