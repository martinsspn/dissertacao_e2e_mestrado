import { test, expect } from '@playwright/test';

test.describe('User Session Termination', () => {
  test('should terminate session and display login link', async ({ page }) => {
    // Navigate to the application's login page
    await page.goto('https://demowebshop.tricentis.com/login');

    // Fill in valid credentials and submit the form
    await page.fill('#Email', process.env.DEMO_WEB_SHOP_USERNAME || 'validUsername');
    await page.fill('#Password', process.env.DEMO_WEB_SHOP_PASSWORD || 'validPassword');
    await page.click('input[type="submit"]');

    // Wait for the dashboard or home page to load after successful login
    await expect(page.locator('.account-information')).toBeVisible();

    // Click on the logout button
    await page.click('a[href="/logout"]');

    // Verify that the session is terminated and the login link is displayed
    await expect(page.locator('#loginLink')).toBeVisible();
  });
});
