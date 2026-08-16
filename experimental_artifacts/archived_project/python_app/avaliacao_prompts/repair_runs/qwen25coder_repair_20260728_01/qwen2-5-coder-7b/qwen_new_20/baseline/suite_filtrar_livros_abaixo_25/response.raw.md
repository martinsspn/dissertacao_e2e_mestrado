```typescript
import { test, expect } from '@playwright/test';

test.describe('Filtering books by price', () => {
  test('should keep the Books category visible and display only products under 25.00', async ({ page }) => {
    // Access the Books category
    await page.goto('/books');

    // Select the Under 25.00 price filter
    await page.click('text=Under 25.00');

    // Verify that the Books category is still visible
    expect(await page.isVisible('text=Books')).toBe(true);

    // Verify that only products under 25.00 are displayed
    const productPrices = await page.textContent('.product-price');
    expect(productPrices).not.toContain('Over 25.00');

    // Additional verification: Check if all prices are below 25.00
    const pricesArray = productPrices.split('\n').filter(price => price.includes('$'));
    for (const price of pricesArray) {
      const numericPrice = parseFloat(price.replace(/[^\d.-]/g, ''));
      expect(numericPrice).toBeLessThan(25);
    }
  });
});
```