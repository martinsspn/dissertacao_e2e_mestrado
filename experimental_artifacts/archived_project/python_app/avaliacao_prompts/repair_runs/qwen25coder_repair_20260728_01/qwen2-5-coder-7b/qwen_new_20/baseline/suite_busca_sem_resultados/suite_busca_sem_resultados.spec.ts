import { test, expect } from '@playwright/test';

test.describe('Search for nonexistent product', () => {
  test('should display no results message when searching for a nonexistent product', async ({ page }) => {
    // Navigate to the Demo Web Shop homepage
    await page.goto('https://demowebshop.tricentis.com');

    // Click on the search icon or link if present
    const searchIcon = page.locator('#small-search-box-form > input[type="text"]');
    if (await searchIcon.isVisible()) {
      await searchIcon.fill('nonexistent-product-term');
    } else {
      const searchLink = page.locator('#top-menu > ul > li:nth-child(4) > a');
      await searchLink.click();
      const searchInput = page.locator('#small-search-box-form > input[type="text"]');
      await searchInput.fill('nonexistent-product-term');
    }

    // Submit the search
    const searchButton = page.locator('#search-box-button');
    await searchButton.click();

    // Verify that the Search page is displayed
    expect(page.url()).toContain('/search');

    // Verify that no products matched the search criteria
    const noResultsMessage = page.locator('.message-error > div');
    await expect(noResultsMessage).toBeVisible();
    await expect(noResultsMessage).toHaveText('No products were found matching your query!');
  });
});
