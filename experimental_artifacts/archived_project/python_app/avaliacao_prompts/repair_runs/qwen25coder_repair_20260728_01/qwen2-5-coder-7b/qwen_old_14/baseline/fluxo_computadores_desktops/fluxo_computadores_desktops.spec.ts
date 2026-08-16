import { test, expect } from '@playwright/test';

test.describe('Digital Downloads Page', () => {
  test('should display the digital downloads page', async ({ page }) => {
    // Navigate to the Digital downloads category
    await page.goto('/digital-downloads');

    // Wait for the digital items to be visible
    const digitalItems = page.locator('.product-item');
    await expect(digitalItems).toBeVisible();

    // Validate that the digital downloads page is visible
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toHaveText('Digital Downloads');

    // Optionally, you can add more specific validations here
  });
});
