import { test, expect } from '@playwright/test';

test.describe('Sorting books by ascending price', () => {
  test('should sort books by ascending price', async ({ page }) => {
    // Access the Books category
    await page.goto('/books');

    // Select Price: Low to High in the Sort by control
    await page.click('text=Sort by');
    await page.click('text=Price: Low to High');

    // The system keeps the Books category visible and displays the products in nondecreasing order according to their current sale prices
    const productPrices = await page.locator('.product-price').allTextContents();
    for (let i = 0; i < productPrices.length - 1; i++) {
      expect(parseFloat(productPrices[i])).toBeLessThanOrEqual(parseFloat(productPrices[i + 1]));
    }
  });
});
