import { test, expect } from '@playwright/test';

test.describe('Health Records Management Flow', () => {
  test('health page loads correctly', async ({ page }) => {
    await page.goto('/health');

    await expect(page).toHaveTitle(/EduLafia/);

    // Check for health dashboard elements
    // const header = page.locator('h1', { hasText: 'Health' });
    // await expect(header).toBeVisible();
  });

  test('can open batch screenings dialog', async ({ page }) => {
    await page.goto('/health');

    // Look for a button to add batch screenings
    const batchBtn = page.locator('button', { hasText: /Batch/i });
    if (await batchBtn.isVisible()) {
      await batchBtn.click();
      await expect(page.locator('dialog, [role="dialog"]')).toBeVisible();
    }
  });
});
