import { test, expect } from '@playwright/test';

test.describe('Mobile Viewport & Touch Gestures', () => {
  // We specify that these tests are meant to run on mobile viewports.
  // We can skip desktop projects explicitly if we want, or handle via config.
  test.skip(({ isMobile }) => !isMobile, 'Skipping on non-mobile devices');

  test.beforeEach(async ({ page }) => {
    // Inject auth state directly into localStorage or window so we bypass the auth check
    await page.addInitScript(() => {
      window.localStorage.setItem(
        'auth-storage',
        JSON.stringify({
          state: {
            user: {
              id: 1,
              email: 'admin@edulafia.com',
              first_name: 'Admin',
              last_name: 'User',
              role: 'system_admin',
              school_id: 'school-123',
            },
            isLoading: false,
            error: null,
          },
          version: 0,
        })
      );
    });

    // Also mock the auth/me endpoint just in case it still fires
    await page.route('**/auth/me', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 1,
          email: 'admin@edulafia.com',
          first_name: 'Admin',
          last_name: 'User',
          role: 'system_admin',
          school_id: 'school-123',
        }),
      });
    });

    await page.route('**/auth/refresh', async (route) => {
      await route.fulfill({ status: 401, body: 'unauthorized' });
    });

    await page.route('**/intelligence/school/*/dashboard', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          kpis: [],
          alerts: [],
          trends: [],
          quick_stats: {
            total_students: 100,
            total_teachers: 10,
            total_classes: 5,
            active_alerts: 0,
          },
          date: new Date().toISOString(),
          last_updated: new Date().toISOString(),
          cache_expires_at: new Date().toISOString(),
        }),
      });
    });
  });

  test('Responsive Layout & Navigation Drawer', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Check if we got redirected to login
    if (page.url().includes('/login')) {
      // Mock was not enough or failed, let's try to mock the store
      await page.evaluate(() => {
        // We can just create a fake user in localStorage and reload if we used persist,
        // but since it's zustand without persist, we can't easily inject it.
      });
      console.log('Redirected to login. Mocking failed!');
    }

    // On mobile, the drawer should be hidden initially and the hamburger menu should be visible
    const menuButton = page.locator('button[aria-label="open drawer"]');
    await expect(menuButton).toBeVisible();

    // Click the menu button to open the drawer
    await menuButton.click();

    // The drawer content should now be visible
    const drawer = page.locator('.MuiDrawer-paper');
    await expect(drawer).toBeVisible();

    // The core navigation section should be visible
    const coreSection = page.locator('text=Core');
    await expect(coreSection).toBeVisible();

    // Close the drawer by clicking outside or by triggering navigation
    // Let's trigger a navigation to the Admin page
    const adminLink = page.locator('a[href="/admin"]');
    await adminLink.click();

    // Verify navigation happened
    await page.waitForURL('**/admin');

    // After navigation on mobile, the drawer should auto-close
    await expect(drawer).not.toBeVisible();
  });

  test('Touch Gestures & Offline Capabilities', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/dashboard');

    // Touch tap on the menu button
    const menuButton = page.locator('button[aria-label="open drawer"]');
    await menuButton.tap();

    const drawer = page.locator('.MuiDrawer-paper');
    await expect(drawer).toBeVisible();

    // Close by tapping on the backdrop (outside the drawer)
    // The MUI backdrop has a class usually `.MuiBackdrop-root`
    const backdrop = page.locator('.MuiBackdrop-root');
    await backdrop.tap();
    await expect(drawer).not.toBeVisible();

    // Verify offline banner when going offline
    await page.context().setOffline(true);

    // Some apps use 'window.dispatchEvent(new Event("offline"))' or just react to navigator.onLine
    // The App might have an offline banner
    // Let's evaluate to trigger it if it relies on events
    await page.evaluate(() => window.dispatchEvent(new Event('offline')));

    // Try to find the OfflineBanner
    const offlineBanner = page.locator("text=You're offline. Changes will sync.");
    await expect(offlineBanner).toBeVisible();

    // Go back online
    await page.context().setOffline(false);
    await page.evaluate(() => window.dispatchEvent(new Event('online')));
    await expect(offlineBanner).not.toBeVisible();
  });
});
