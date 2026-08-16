```typescript
import { test, expect } from '@playwright/test';

test.describe('Books Category Display Control', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/books');
  });

  test('displays no more than four product items when 4 is selected in the Display control', async ({ page }) => {
    // Select 4 in the Display control
    await page.locator('#product-list-page-size').selectOption('4');

    // Wait for the products to update
    await page.waitForSelector('.product-item');

    // Get all product items on the current page
    const productItems = await page.locator('.product-item').all();

    // Expect no more than four product items to be displayed
    expect(productItems.length).toBeLessThanOrEqual(4);
  });
});
```