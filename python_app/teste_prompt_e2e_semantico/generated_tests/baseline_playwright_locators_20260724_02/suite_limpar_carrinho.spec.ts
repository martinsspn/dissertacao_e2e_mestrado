import { test, expect } from '@playwright/test';

test.describe('Remove all products from the cart', () => {
  test.beforeEach(async ({ page }) => {
    // Add Blue Jeans to the cart
    await page.goto('/products');
    await page.click('text=Blue Jeans');
    await page.click('button=add-to-cart');
  });

  test('should remove Blue Jeans from the cart', async ({ page }) => {
    // Access Shopping cart
    await page.click('text=Shopping Cart');

    // Mark Blue Jeans for removal
    await page.check('input[name="remove-blue-jeans"]');

    // Select Update shopping cart
    await page.click('button=Update shopping cart');

    // System displays the empty cart
    await expect(page.locator('.cart-items')).toHaveText('');
  });
});
