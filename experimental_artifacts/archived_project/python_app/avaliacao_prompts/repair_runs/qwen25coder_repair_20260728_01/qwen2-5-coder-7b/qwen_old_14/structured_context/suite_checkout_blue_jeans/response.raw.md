```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Checkout Blue Jeans', () => {
  test('should complete the checkout process for blue jeans', async ({ page }) => {
    // Step 1: Authenticate in an account with a valid billing and shipping address
    await page.goto('https://demowebshop.tricentis.com/login');
    await page.locator("[id=\"Email\"]").fill(process.env.TEST_EMAIL);
    await page.locator("[id=\"Password\"]").fill(process.env.TEST_PASSWORD);
    await page.getByRole("button", { name: "Log in" }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Step 2: Search for Blue Jeans and open the product page
    await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans');
    await page.getByRole("button", { name: "Search", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Step 3: Add Blue Jeans to the cart
    await page.locator("[id=\"add-to-cart-button-36\"]").click();

    // Step 4: Access Shopping cart and confirm that the product is present
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1').textContent()).toBe('Shopping cart');

    // Step 5: Accept the Terms of service and select Checkout
    await page.getByLabel('I agree with the terms', { exact: true }).check();
    await page.getByRole("button", { name: "Checkout", exact: true }).click();

    // Step 6: Confirm or provide valid Billing address data
    await page.locator("[id=\"BillingAddress_FirstName\"]").fill(process.env.BILLING_FIRST_NAME);
    await page.locator("[id=\"BillingAddress_LastName\"]").fill(process.env.BILLING_LAST_NAME);
    await page.locator("[id=\"BillingAddress_Email\"]").fill(process.env.BILLING_EMAIL);
    await page.locator("[id=\"BillingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"BillingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"BillingAddress_City\"]").fill(process.env.BILLING_CITY);
    await page.locator("[id=\"BillingAddress_Address1\"]").fill(process.env.BILLING_ADDRESS1);
    await page.locator("[id=\"BillingAddress_ZipPostalCode\"]").fill(process.env.BILLING_ZIP);

    // Step 7: Confirm or provide valid Shipping address data
    await page.locator("[id=\"ShippingAddress_FirstName\"]").fill(process.env.SHIPPING_FIRST_NAME);
    await page.locator("[id=\"ShippingAddress_LastName\"]").fill(process.env.SHIPPING_LAST_NAME);
    await page.locator("[id=\"ShippingAddress_Email\"]").fill(process.env.SHIPPING_EMAIL);
    await page.locator("[id=\"ShippingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"ShippingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"ShippingAddress_City\"]").fill(process.env.SHIPPING_CITY);
    await page.locator("[id=\"ShippingAddress_Address1\"]").fill(process.env.SHIPPING_ADDRESS1);
    await page.locator("[id=\"ShippingAddress_ZipPostalCode\"]").fill(process.env.SHIPPING_ZIP);

    // Step 8: Select an available Shipping method option
    await page.getByRole("radio", { name: "Next Day Air" }).click();

    // Step 9: Select an available Payment method option
    await page.getByLabel("Credit Card (Visa, MasterCard)").check();

    // Step 10: Review Payment information and proceed
    await page.locator("[id=\"CardholderName\"]").fill(process.env.CARDHOLDER_NAME);
    await page.locator("[id=\"CardNumber\"]").fill(process.env.CARD_NUMBER);
    await page.locator("[id=\"ExpireMonth\"]").selectOption({ label: '01' });
    await page.locator("[id=\"ExpireYear\"]").selectOption({ label: '2025' });
    await page.locator("[id=\"CardCode\"]").fill(process.env.CARD_CODE);
    await page.getByRole("button", { name: "Continue" }).click();

    // Step 11: Review the order and select Confirm
    await expect(page.locator('h1').textContent()).toBe('Order review');
    await page.getByRole("button", { name: "Confirm" }).click();

    // Step 12: System informs that the order was processed successfully
    await expect(page.locator('h1').textContent()).toBe('Your order has been successfully processed!');
  });
});
```