```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart - Empty State', () => {
  test('displays empty cart message and zero item count when accessed without adding products', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Access the shopping cart directly in a fresh context
    await page.goto(`${baseUrl}/cart`);

    // Verify Shopping Cart page is displayed
    const cartHeading = page.getByRole('heading', { name: /shopping cart|your cart/i });
    await expect(cartHeading).toBeVisible();

    // Verify notice informing that the shopping cart is empty
    const emptyCartNotice = page.getByText(/shopping cart is empty|your cart is empty|you have no items/i);
    await expect(emptyCartNotice).toBeVisible();

    // Verify item count indicates 0 items
    const itemCount = page.getByText(/0 items|0 products|items \(0\)/i);
    await expect(itemCount.first()).toBeVisible();
  });
});
```