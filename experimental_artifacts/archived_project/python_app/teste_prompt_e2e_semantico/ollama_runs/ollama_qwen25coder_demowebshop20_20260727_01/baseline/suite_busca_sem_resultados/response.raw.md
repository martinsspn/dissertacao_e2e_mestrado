```typescript
import { test, expect } from '@playwright/test';

test.describe('Search for nonexistent product', () => {
  test('should display no results message when searching for a nonexistent product', async ({ page }) => {
    // Navigate to the Search page
    await page.goto('/search');

    // Enter a unique term that does not correspond to any product
    const searchInput = page.locator('#search-input');
    await searchInput.fill('nonexistent-product-term');

    // Submit the search
    const searchButton = page.locator('#search-button');
    await searchButton.click();

    // Verify that the Search page is displayed
    expect(page.url()).toContain('/search');

    // Verify that no products matched the search criteria
    const noResultsMessage = page.locator('.no-results-message');
    await expect(noResultsMessage).toBeVisible();
    await expect(noResultsMessage).toHaveText('No products matched the search criteria.');
  });
});
```