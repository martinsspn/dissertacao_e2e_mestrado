```typescript
import { test, expect } from '@playwright/test';

test.describe('Blue Jeans Purchase', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming authentication is handled by a fixture or setup function
    await page.goto('https://demowebshop.tricentis.com/login');
    await page.fill('#Email', process.env.TEST_EMAIL);
    await page.fill('#Password', process.env.TEST_PASSWORD);
    await page.click('#login-button');
  });

  test('should complete the purchase of Blue Jeans', async ({ page }) => {
    // Search for Blue Jeans
    await page.goto('https://demowebshop.tricentis.com/search?q=Blue+Jeans');
    await page.click('.product-box a');

    // Add to cart
    await page.click('#add-to-cart-button-19');

    // Access shopping cart and confirm product presence
    await page.click('#topcartlink');
    expect(page.locator('.cart-item').first()).toContainText('Blue Jeans');

    // Checkout process
    await page.click('#checkout-button');
    await page.check('#termsofservice');
    await page.click('#continue');

    // Provide valid billing and shipping addresses
    await page.fill('#BillingAddress_FirstName', 'John');
    await page.fill('#BillingAddress_LastName', 'Doe');
    await page.fill('#BillingAddress_Email', process.env.TEST_EMAIL);
    await page.fill('#BillingAddress_Company', '');
    await page.fill('#BillingAddress_Address1', '123 Test St, Test City, Test Country');
    await page.fill('#BillingAddress_City', 'Test City');
    await page.fill('#BillingAddress_StateProvinceName', 'Test State');
    await page.fill('#BillingAddress_ZipPostalCode', '12345');
    await page.fill('#BillingAddress_PhoneNumber', '123-456-7890');

    await page.fill('#ShippingAddress_FirstName', 'John');
    await page.fill('#ShippingAddress_LastName', 'Doe');
    await page.fill('#ShippingAddress_Company', '');
    await page.fill('#ShippingAddress_Address1', '456 Test St, Test City, Test Country');
    await page.fill('#ShippingAddress_City', 'Test City');
    await page.fill('#ShippingAddress_StateProvinceName', 'Test State');
    await page.fill('#ShippingAddress_ZipPostalCode', '12345');

    // Select shipping and payment methods
    await page.click('#shipping-methods input[type="radio"]');
    await page.click('#payment-methods input[type="radio"]');

    // Review order and confirm
    await page.click('#order-review-button');
    await page.click('#confirm-order-button');

    // Verify successful order processing
    expect(page.locator('.result')).toContainText('Your order has been successfully processed!');
  });
});
```