```typescript
import { test, expect } from '@playwright/test';

test.describe('Books Category Test', () => {
  test('should display the Books category page with correct breadcrumb and products', async ({ page }) => {
    // Access the Demo Web Shop home page
    await page.goto('https://demowebshop.tricentis.com/');

    // Select Books in the main category menu
    await page.click('text=Books');

    // System displays the Books category page, its breadcrumb, and the available book products
    await expect(page.locator('.breadcrumb')).toContainText('Home > Books');
    await expect(page.locator('.product-list-item')).toHaveCount(3);
    await expect(page.locator('.product-name:has-text("Computing and Internet")')).toBeVisible();
    await expect(page.locator('.product-name:has-text("Fiction")')).toBeVisible();
    await expect(page.locator('.product-name:has-text("Health Book")')).toBeVisible();
  });
});
```