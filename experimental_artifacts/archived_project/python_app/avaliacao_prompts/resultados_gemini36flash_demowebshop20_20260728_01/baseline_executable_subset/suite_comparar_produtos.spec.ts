import { test, expect } from '@playwright/test';

test.describe('Product Comparison', () => {
  test('should add two products to compare list, view comparison, and clear list', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // 1. Open Computing and Internet product page and select Add to compare list
    await page.goto(`${baseUrl}/computing-and-internet`);
    const addCompareBtn1 = page.getByRole('button', { name: /add to compare list/i });
    await expect(addCompareBtn1).toBeVisible();
    await addCompareBtn1.click();

    // 2. Open Fiction product page and select Add to compare list
    await page.goto(`${baseUrl}/fiction`);
    const addCompareBtn2 = page.getByRole('button', { name: /add to compare list/i });
    await expect(addCompareBtn2).toBeVisible();
    await addCompareBtn2.click();

    // 3. Navigate to Compare products page if not automatically redirected
    if (!page.url().includes('/compareproducts')) {
      await page.goto(`${baseUrl}/compareproducts`);
    }

    // Assert Compare products page displays
    await expect(page.getByRole('heading', { name: /compare products/i })).toBeVisible();

    // Assert both products are displayed for comparison
    const computingLink = page.getByRole('link', { name: 'Computing and Internet' });
    const fictionLink = page.getByRole('link', { name: 'Fiction' });
    await expect(computingLink.first()).toBeVisible();
    await expect(fictionLink.first()).toBeVisible();

    // 4. Clear the comparison list
    const clearList = page.getByRole('button', { name: /clear list/i })
      .or(page.getByRole('link', { name: /clear list/i }))
      .or(page.locator('.clear-list'));

    await expect(clearList.first()).toBeVisible();
    await clearList.first().click();

    // Assert comparison list is cleared
    const emptyMessage = page.getByText(/you have no items to compare/i);
    await expect(emptyMessage).toBeVisible();
  });
});
