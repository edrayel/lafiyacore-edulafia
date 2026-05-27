import { test, expect, Page } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';

const USERS = [
  { role: 'school_admin', email: 'admin@demo.edu.ng', pass: 'DemoPass123!' },
  { role: 'teacher', email: 'teacher@demo.edu.ng', pass: 'DemoPass123!' },
  { role: 'parent', email: 'parent@demo.edu.ng', pass: 'DemoPass123!' },
];

async function login(page: Page, email: string, pass: string) {
  await page.goto(`${BASE_URL}/login`, { waitUntil: 'networkidle' });
  await page.fill('input[type="email"]', email);
  await page.fill('input[type="password"]', pass);
  await page.click('button[type="submit"]');
  // Wait for login to complete by waiting for network idle or a specific element
  await page.waitForLoadState('networkidle');
  // If it's the parent, they might go to /parent/children, otherwise /
  await page.waitForTimeout(2000); // safety buffer
}

async function logout(page: Page) {
  // Assuming there's a profile menu or logout button
  const menuButton = page.getByRole('button', { name: /open settings|account|profile|demo/i });
  if ((await menuButton.count()) > 0) {
    await menuButton.click();
    await page.getByRole('menuitem', { name: /logout|sign out/i }).click();
  } else {
    // fallback force logout via clearing storage
    await page.context().clearCookies();
    await page.evaluate(() => localStorage.clear());
  }
  await page.goto(`${BASE_URL}/login`);
}

test.describe('Autonomous Exploratory Test Across Roles', () => {
  test('School Admin Flow', async ({ page }) => {
    test.setTimeout(120000);
    await login(page, USERS[0].email, USERS[0].pass);

    // Verify dashboard
    await expect(page.locator('text=Dashboard').first()).toBeVisible({ timeout: 10000 });

    // Explore Admissions
    await page.goto(`${BASE_URL}/admissions`);
    await page.waitForLoadState('networkidle');

    // Create new application
    const newAppBtn = page.getByRole('button', { name: /New Application/i });
    if ((await newAppBtn.count()) > 0) {
      await newAppBtn.click();
      // Fill out the modal
      await page.fill('input[name="first_name"]', 'TestFirst');
      await page.fill('input[name="last_name"]', 'TestLast');
      await page.fill('input[name="guardian_email"]', 'testguardian@demo.edu.ng');
      await page.fill('input[name="guardian_phone"]', '+2348000000000');
      await page.click('button:has-text("Submit")');
      await page.waitForLoadState('networkidle');
    }

    // Explore Students
    await page.goto(`${BASE_URL}/students`);
    await page.waitForLoadState('networkidle');

    // Add Student
    const addStudentBtn = page.getByRole('button', { name: /Add Student/i });
    if ((await addStudentBtn.count()) > 0) {
      await addStudentBtn.click();
      await page.fill('input[name="first_name"]', 'John');
      await page.fill('input[name="last_name"]', 'Doe');
      await page.fill('input[name="admission_number"]', 'ADM' + Date.now());
      // Try to save
      await page.click(
        'button:has-text("Save"), button:has-text("Submit"), button:has-text("Add")'
      );
      await page.waitForTimeout(1000);
    }

    // Explore Staff
    await page.goto(`${BASE_URL}/staff`);
    await page.waitForLoadState('networkidle');

    // Add Staff
    const addStaffBtn = page.getByRole('button', { name: /Add Staff/i });
    if ((await addStaffBtn.count()) > 0) {
      await addStaffBtn.click();
      await page.fill('input[name="first_name"]', 'Jane');
      await page.fill('input[name="last_name"]', 'Smith');
      await page.fill('input[name="email"]', `staff${Date.now()}@demo.edu.ng`);
      await page.click(
        'button:has-text("Save"), button:has-text("Submit"), button:has-text("Add")'
      );
      await page.waitForTimeout(1000);
    }

    await logout(page);
  });

  test('Teacher Flow', async ({ page }) => {
    test.setTimeout(90000);
    await login(page, USERS[1].email, USERS[1].pass);

    // Verify Teacher access
    await page.goto(`${BASE_URL}/attendance`);
    await page.waitForLoadState('networkidle');

    // Select class (if dropdown exists)
    const classSelect = page.getByRole('combobox', { name: /Class/i });
    if ((await classSelect.count()) > 0) {
      await classSelect.click();
      await page.getByRole('option').first().click();
    }

    await logout(page);
  });

  test('Parent Flow', async ({ page }) => {
    test.setTimeout(90000);
    await login(page, USERS[2].email, USERS[2].pass);

    // Verify Parent access
    await page.goto(`${BASE_URL}/parent/children`);
    await page.waitForLoadState('networkidle');

    // Check if error boundary appears
    const errorBoundary = page.locator('text="Something went wrong!"');
    await expect(errorBoundary).not.toBeVisible();

    await logout(page);
  });
});
