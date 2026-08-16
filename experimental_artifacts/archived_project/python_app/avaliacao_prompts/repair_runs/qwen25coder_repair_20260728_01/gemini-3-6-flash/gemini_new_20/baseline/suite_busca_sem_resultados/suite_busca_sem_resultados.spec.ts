import { test, expect } from '@playwright/test';

test.describe('Store Product Search', () => {
  test('should inform user when searching for a nonexistent product', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';
    const nonexistentTerm = `nonexistent_item_${Date.now()}`;

    // Navigate to the store homepage
    await page.goto(baseUrl);

    // Locate the "Search store" field using user-facing locators
    const searchInput = page.locator('input[name="q"]');

    await expect(searchInput).toBeVisible();

    // Enter a unique search term that does not match any product
    await searchInput.fill(nonexistentTerm);

    // Submit the search
    const searchButton = page.getByRole('button', { name: /search/i }).first();
    if (await searchButton.isVisible()) {
      await searchButton.click();
    } else {
      await searchInput.press('Enter');
    }

    // Verify the system navigates to/displays the search results page
    await expect(page).toHaveURL(/search/i);

    // Verify the system informs that no products matched the search criteria
    const noResultsText = page.locator('.no-result');

    await expect(noResultsText).toBeVisible();
  });
});
