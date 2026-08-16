```typescript
import { test, expect } from '@playwright/test';

test.describe('Book Catalog View', () => {
  test('user can switch Books category view from Grid to List', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Access the application home page
    await page.goto(baseUrl);

    // Access the Books category
    const booksNavLink = page.getByRole('link', { name: 'Books' }).first();
    await booksNavLink.click();

    // Confirm the Books category page is loaded and visible
    const booksHeading = page.getByRole('heading', { name: 'Books' });
    await expect(booksHeading).toBeVisible();

    // Select 'List' in the 'View as' control
    const viewAsSelect = page.getByLabel('View as');
    await viewAsSelect.selectOption({ label: 'List' });

    // Verify the system keeps the Books category visible
    await expect(booksHeading).toBeVisible();

    // Verify the 'View as' selector now reflects the List view selection
    await expect(viewAsSelect).toHaveValue(/list/i);

    // Verify the product list container displays the products in list format
    const productList = page.locator('.product-list, .products-wrapper').first();
    await expect(productList).toBeVisible();

    // Ensure no grid elements are visible when List view is selected
    const gridProducts = page.locator('.product-grid');
    await expect(gridProducts).not.toBeVisible();
  });
});
```