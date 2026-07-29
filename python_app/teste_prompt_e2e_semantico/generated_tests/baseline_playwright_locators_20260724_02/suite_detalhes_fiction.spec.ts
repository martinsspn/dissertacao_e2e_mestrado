import { test, expect } from '@playwright/test';

test.describe('Product Details Test', () => {
  test('should display product details and price information', async ({ page }) => {
    // Navigate to the search page
    await page.goto('https://example.com/search');

    // Search for the product "Fiction"
    await page.fill('input[name="search"]', 'Fiction');
    await page.click('button[type="submit"]');

    // Open the product details page
    const productLink = page.locator('a[href*="/fiction"]');
    await productLink.click();

    // Verify that the correct product details page is displayed
    await expect(page).toHaveTitle(/Fiction/);

    // Check if price information is presented
    const priceElement = page.locator('.price');
    await expect(priceElement).toBeVisible();
  });
});
