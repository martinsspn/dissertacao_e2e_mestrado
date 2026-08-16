```typescript
import { test, expect } from '@playwright/test';

test.describe('Viewing an empty shopping cart', () => {
  test('should display the shopping cart page with zero items and an empty message', async ({ page }) => {
    // Navigate to the shopping cart page
    await page.goto('/ShoppingCart');

    // Check if the item count is displayed as zero
    const itemCount = await page.textContent('.cart-total');
    expect(itemCount).toBe('0 - Items');

    // Check if the empty cart message is displayed
    const emptyCartMessage = await page.textContent('.content-wrapper');
    expect(emptyCartMessage).toContain('Your shopping cart is empty.');
  });
});
```