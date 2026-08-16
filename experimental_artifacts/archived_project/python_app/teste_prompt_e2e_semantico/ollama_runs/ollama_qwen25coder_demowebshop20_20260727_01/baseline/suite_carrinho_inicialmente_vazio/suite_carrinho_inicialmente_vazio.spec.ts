import { test, expect } from '@playwright/test';

test.describe('Viewing an empty shopping cart', () => {
  test('should display the shopping cart page with zero items and an empty message', async ({ page }) => {
    // Navigate to the shopping cart page
    await page.goto('/shopping-cart');

    // Check if the item count is displayed as zero
    const itemCount = await page.textContent('.item-count');
    expect(itemCount).toBe('0');

    // Check if the empty cart message is displayed
    const emptyCartMessage = await page.textContent('.empty-cart-message');
    expect(emptyCartMessage).toContain('The shopping cart is empty.');
  });
});
