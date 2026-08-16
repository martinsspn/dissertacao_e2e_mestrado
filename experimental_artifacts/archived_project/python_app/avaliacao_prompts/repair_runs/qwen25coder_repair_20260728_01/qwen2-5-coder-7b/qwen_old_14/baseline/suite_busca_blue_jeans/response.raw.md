```typescript
import { test, expect } from '@playwright/test';

test.describe('Searching and opening a product', () => {
  test('should display the details page for Blue Jeans', async ({ page }) => {
    // Navigate to the Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com');

    // Search for 'Blue Jeans'
    const searchInput = page.locator('#small-searchterms');
    await searchInput.fill('Blue Jeans');
    await searchInput.press('Enter');

    // Wait for results to load
    await page.waitForSelector('.product-list-item');

    // Click on the first product result
    const firstProductResult = page.locator('.product-list-item').first();
    await firstProductResult.click();

    // Verify that the details page is displayed with 'Blue Jeans'
    const productName = page.locator('#product-name');
    await expect(productName).toHaveText('Blue Jeans');
  });
});
```