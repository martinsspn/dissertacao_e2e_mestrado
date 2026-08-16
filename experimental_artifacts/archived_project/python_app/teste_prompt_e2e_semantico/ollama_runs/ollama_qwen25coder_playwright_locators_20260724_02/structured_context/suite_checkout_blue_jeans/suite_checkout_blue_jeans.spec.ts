import { test, expect } from '@playwright/test';

test.describe('Suite Checkout Blue Jeans', () => {
  test('should complete the checkout process for blue jeans', async ({ page }) => {
    // Step 2: Search for Blue Jeans and open the product page
    await page.goto('https://demowebshop.tricentis.com/');
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
    await page.locator("[id=\"BillingAddress_FirstName\"]").fill('John');
    await page.locator("[id=\"BillingAddress_LastName\"]").fill('Doe');
    await page.locator("[id=\"BillingAddress_Email\"]").fill('john.doe@example.com');
    await page.locator("[id=\"BillingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"BillingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"BillingAddress_City\"]").fill('Montgomery');
    await page.locator("[id=\"BillingAddress_Address1\"]").fill('123 Main St');
    await page.locator("[id=\"BillingAddress_ZipPostalCode\"]").fill('36104');

    // Step 7: Confirm or provide valid Shipping address data
    await page.locator("[id=\"ShippingAddress_FirstName\"]").fill('John');
    await page.locator("[id=\"ShippingAddress_LastName\"]").fill('Doe');
    await page.locator("[id=\"ShippingAddress_Email\"]").fill('john.doe@example.com');
    await page.locator("[id=\"ShippingAddress_CountryId\"]").selectOption({ label: 'United States' });
    await page.locator("[id=\"ShippingAddress_StateProvinceId\"]").selectOption({ label: 'Alabama' });
    await page.locator("[id=\"ShippingAddress_City\"]").fill('Montgomery');
    await page.locator("[id=\"ShippingAddress_Address1\"]").fill('123 Main St');
    await page.locator("[id=\"ShippingAddress_ZipPostalCode\"]").fill('36104');

    // Step 8: Select an available Shipping method option
    await page.getByRole("radio", { name: "Next Day Air" }).click();

    // Step 9: Select an available Payment method option
    await page.getByLabel("Credit Card (Visa, MasterCard)").check();

    // Step 10: Review Payment information and proceed
    await page.locator("[id=\"CardholderName\"]").fill('John Doe');
    await page.locator("[id=\"CardNumber\"]").fill('4111111111111111');
    await page.locator("[id=\"ExpireMonth\"]").selectOption({ label: '01' });
    await page.locator("[id=\"ExpireYear\"]").selectOption({ label: '2025' });
    await page.locator("[id=\"CardCode\"]").fill('123');
    await page.getByRole("button", { name: "Continue" }).click();

    // Step 11: Review the order and select Confirm
    await expect(page.locator('h1').textContent()).toBe('Order review');
    await page.getByRole("button", { name: "Confirm" }).click();

    // Step 12: System informs that the order was processed successfully
    await expect(page.locator('h1').textContent()).toBe('Your order has been successfully processed!');
  });
});
