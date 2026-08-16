```typescript
import { test, expect } from '@playwright/test';

test.describe('Blue Jeans Purchase', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming authentication is handled by a fixture or setup function
    await page.goto('https://example.com/login');
    await page.fill('#username', 'testuser');
    await page.fill('#password', 'testpass');
    await page.click('#login-button');
  });

  test('should complete the purchase of Blue Jeans', async ({ page }) => {
    // Search for Blue Jeans
    await page.goto('https://example.com/search?q=Blue+Jeans');
    await page.click('.product-link');

    // Add to cart
    await page.click('#add-to-cart-button');

    // Access shopping cart and confirm product presence
    await page.click('#cart-icon');
    expect(page.locator('.cart-item').first()).toContainText('Blue Jeans');

    // Checkout process
    await page.click('#checkout-button');
    await page.check('#terms-of-service');
    await page.click('#continue-to-checkout');

    // Provide valid billing and shipping addresses
    await page.fill('#billing-address', '123 Test St, Test City, Test Country');
    await page.fill('#shipping-address', '456 Test St, Test City, Test Country');

    // Select shipping and payment methods
    await page.click('#shipping-method-option');
    await page.click('#payment-method-option');

    // Review order and confirm
    await page.click('#review-order-button');
    await page.click('#confirm-order-button');

    // Verify successful order processing
    expect(page.locator('.order-confirmation-message')).toContainText('Order processed successfully');
  });
});
```