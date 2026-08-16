import { test, expect } from '@playwright/test';

test.describe('Book purchase flow (registration + cart)', () => {
  test('should register a new user, add a book to the cart, and verify the cart', async ({ page }) => {
    // Access the Demo Web Shop website
    await page.goto('https://demowebshop.tricentis.com/');

    // Click on the Register link to access the registration page
    await page.click('text=Register');

    // Fill in the email field with a valid email
    await page.fill('#Email', 'testuser@example.com');

    // Fill in the password field with a secure password
    await page.fill('#Password', 'P@ssw0rd123');

    // Confirm the password by typing it again
    await page.fill('#ConfirmPassword', 'P@ssw0rd123');

    // Fill in the First Name field with their first name
    await page.fill('#FirstName', 'John');

    // Fill in the Last Name field with their last name
    await page.fill('#LastName', 'Doe');

    // Click on the Register button to complete the registration
    await page.click('button[type="submit"]');

    // Verify that the user is logged in and redirected to the home page
    expect(page.url()).toContain('/customer/account');
    expect(await page.isVisible('text=Welcome, John Doe!')).toBe(true);

    // Click on the Books menu or link to access the book list
    await page.click('text=Books');

    // Locate and click on the book Health Book to open its details page
    await page.click('text=Health Book');

    // Add the book to the cart
    await page.click('button[type="submit"]');

    // Verify that the product has been added to the cart (success notification)
    expect(await page.isVisible('text=The product has been added to your shopping cart.'));

    // Navigate to the shopping cart to check the added item
    await page.click('text=Shopping cart');

    // Verify that the book was successfully added to the cart
    expect(await page.isVisible('text=Health Book'));
  });
});
