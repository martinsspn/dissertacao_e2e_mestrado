import { test, expect } from '@playwright/test';

test.describe('Digital Downloads Category', () => {
  test('should access Digital downloads, view items, and confirm page visibility', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // 1. Access the homepage
    await page.goto(baseUrl);

    // 2. Locate and click on the 'Digital downloads' category
    const categoryLink = page.getByRole('link', { name: 'Digital downloads', exact: true }).first();
    await expect(categoryLink).toBeVisible();
    await categoryLink.click();

    // 3. Validate that the Digital downloads page is visible
    const pageHeading = page.getByRole('heading', { name: 'Digital downloads', exact: true });
    await expect(pageHeading).toBeVisible();
    await expect(page).toHaveURL(/.*digital-downloads/);

    // 4. View and validate available digital items
    const productGrid = page.locator('.product-grid, .products-container, .product-list').first();
    await expect(productGrid).toBeVisible();

    const productItems = page.locator('.product-item, .product-card, [data-productid]');
    await expect(productItems.first()).toBeVisible();

    const itemCount = await productItems.count();
    expect(itemCount).toBeGreaterThan(0);
  });
});
