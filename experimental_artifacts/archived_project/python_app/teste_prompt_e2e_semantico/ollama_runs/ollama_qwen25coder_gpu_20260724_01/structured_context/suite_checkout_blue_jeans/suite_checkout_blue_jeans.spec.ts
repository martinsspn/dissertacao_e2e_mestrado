import { test, expect } from '@playwright/test';

test.describe('Suite Checkout Blue Jeans', () => {
  test('should complete the checkout process for blue jeans', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Step 2: Search for Blue Jeans and open the product page
    await page.fill('#small-searchterms', 'Blue Jeans');
    await page.click('role_name:Search');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');
    await expect(page.locator('h1')).toHaveText('Blue Jeans');

    // Step 3: Add Blue Jeans to the cart
    await page.click('#add-to-cart-button-36');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Step 4: Access Shopping cart and confirm that the product is present
    await page.click('page.getByRole("link", { name: "Shopping cart", exact: true })');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1')).toHaveText('Shopping cart');

    // Step 5: Accept the Terms of service and select Checkout
    await page.click('#termsofservice');
    await page.click('button[name="checkout"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout');

    // Step 6: Confirm or provide valid Billing address data
    await page.fill('#Billing_FirstName', 'John');
    await page.fill('#Billing_LastName', 'Doe');
    await page.fill('#Billing_Email', 'john.doe@example.com');
    await page.fill('#Billing_PhoneNumber', '1234567890');
    await page.fill('#Billing_FaxNumber', '');
    await page.fill('#Billing_Company', '');
    await page.fill('#Billing_Address1', '123 Main St');
    await page.fill('#Billing_City', 'Anytown');
    await page.fill('#Billing_StateProvinceRegion', 'CA');
    await page.fill('#Billing_ZipPostalCode', '12345');
    await page.selectOption('#Billing_CountryId', { label: 'United States' });
    await page.click('button[name="save"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout');

    // Step 7: Confirm or provide valid Shipping address data
    await page.fill('#Shipping_FirstName', 'John');
    await page.fill('#Shipping_LastName', 'Doe');
    await page.fill('#Shipping_Email', 'john.doe@example.com');
    await page.fill('#Shipping_PhoneNumber', '1234567890');
    await page.fill('#Shipping_FaxNumber', '');
    await page.fill('#Shipping_Company', '');
    await page.fill('#Shipping_Address1', '123 Main St');
    await page.fill('#Shipping_City', 'Anytown');
    await page.fill('#Shipping_StateProvinceRegion', 'CA');
    await page.fill('#Shipping_ZipPostalCode', '12345');
    await page.selectOption('#Shipping_CountryId', { label: 'United States' });
    await page.click('button[name="save"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout');

    // Step 8: Select an available Shipping method option
    await page.click('#shipping-method-buttons-block input[type="radio"][value="1"]');
    await page.click('button[name="save"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout');

    // Step 9: Select an available Payment method option
    await page.click('#payment-method-buttons-block input[type="radio"][value="1"]');
    await page.click('button[name="save"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout');

    // Step 10: Review Payment information and proceed
    await page.click('button[name="paymentmethodnextstep"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout/review');
    await page.click('button[name="confirmorder"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/onepagecheckout/completed');

    // Step 12: The system informs that the order was processed successfully
    await expect(page.locator('.result')).toHaveText('Your order has been successfully processed!');
  });
});
