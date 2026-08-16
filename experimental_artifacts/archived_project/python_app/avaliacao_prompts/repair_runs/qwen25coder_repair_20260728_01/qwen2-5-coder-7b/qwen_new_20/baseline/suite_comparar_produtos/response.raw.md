```typescript
import { test, expect } from '@playwright/test';

test.describe('Product Comparison', () => {
  test('should add two products to compare list and display them on Compare Products page', async ({ page }) => {
    // Navigate to Computing and Internet product page
    await page.goto('/computing-and-internet');
    // Select Add to compare list
    await page.click('#addToCompareButton');

    // Navigate to Fiction product page
    await page.goto('/fiction');
    // Select Add to compare list
    await page.click('#addToCompareButton');

    // Navigate to Compare Products page
    await page.goto('/compare-products');

    // Verify both products are displayed in the comparison list
    expect(await page.isVisible('h2:has-text("Computing and Internet")')).toBe(true);
    expect(await page.isVisible('h2:has-text("Fiction")')).toBe(true);

    // Clear the comparison list
    await page.click('#clearCompareButton');
  });
});
```