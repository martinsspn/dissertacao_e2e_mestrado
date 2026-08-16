import { test, expect } from '@playwright/test';

test.describe('Shopping Cart - Add Multiple Products', () => {
  test('should display both Computing and Internet and Fiction in cart with quantity and price', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Navigate to the e-commerce store
    await page.goto(baseUrl);

    // 1. Navigate to Books category and add "Computing and Internet"
    await page.getByRole('link', { name: 'Books' }).first().click();
    await expect(page).toHaveURL(/.*\/books/);

    await page.getByRole('link', { name: 'Computing and Internet' }).first().click();
    await expect(page.getByRole('heading', { name: 'Computing and Internet' })).toBeVisible();

    // Click 'Add to cart' and wait for notification
    await page.getByRole('button', { name: 'Add to cart' }).click();
    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('The product has been added to your');

    // 2. Navigate back to Books category and add "Fiction"
    await page.getByRole('link', { name: 'Books' }).first().click();
    await page.getByRole('link', { name: 'Fiction', exact: true }).first().click();
    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();

    // Click 'Add to cart' and wait for notification
    await page.getByRole('button', { name: 'Add to cart' }).click();
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('The product has been added to your');

    // 3. Access Shopping cart
    await page.getByRole('link', { name: 'Shopping cart' }).first().click();
    await expect(page).toHaveURL(/.*\/cart/);
    await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();

    // 4. Verify Computing and Internet item in cart table
    const computingRow = page.locator('tr.cart-item-row').filter({ hasText: 'Computing and Internet' });
    await expect(computingRow).toBeVisible();
    await expect(computingRow.locator('input.qty-input')).toBeVisible();
    await expect(computingRow.locator('.product-unit-price')).toBeVisible();
    await expect(computingRow.locator('.product-subtotal')).toBeVisible();

    // 5. Verify Fiction item in cart table
    const fictionRow = page.locator('tr.cart-item-row').filter({ hasText: 'Fiction' });
    await expect(fictionRow).toBeVisible();
    await expect(fictionRow.locator('input.qty-input')).toBeVisible();
    await expect(fictionRow.locator('.product-unit-price')).toBeVisible();
    await expect(fictionRow.locator('.product-subtotal')).toBeVisible();
  });
});
