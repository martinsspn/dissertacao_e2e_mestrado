```typescript
import { test, expect } from '@playwright/test';

test.describe('Gift Cards Category', () => {
  test('displays the Gift Cards category page with breadcrumb and products', async ({ page }) => {
    // Access the Demo Web Shop home page
    await page.goto('https://demowebshop.tricentis.com/');

    // Select Gift Cards in the main category menu
    await page.click('text=Gift Cards');

    // System displays the Gift Cards category page, its breadcrumb, and the available gift card products
    await expect(page.locator('h1')).toHaveText('Gift Cards');
    await expect(page.locator('.breadcrumb')).toContainText('Home > Gift Cards');
    await expect(page.locator('.product-list-item')).toBeVisible();
  });
});
```