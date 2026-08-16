import { test } from '@playwright/test';

describe('User Registration Book Purchase', () => {
  it('should register a user and access the books page', async () => {
    const page = await test.chromium.launch();

    // Navigate to the Demo Web Shop website
    await page.goto('https://demowebshop.tricentis.com/');

    // Click on the Register link to access the registration page
    await page.click(await page.locator('#register-button'));

    // Fill in the email field with a valid email
    await page.fill(await page.locator('#email'), 'test@example.com');

    // Fill in the password field with a secure password
    await page.fill(await page.locator('#password'), 'SecurePassword123');

    // Confirm the password by typing it again
    await page.fill(await page.locator('#confirm-password'), 'SecurePassword123');

    // Fill in the First Name and Last Name fields with their respective values
    await page.fill(await page.locator('#firstName'), 'John Doe');
    await page.fill(await page.locator('#lastname'), 'Doe');

    // Click on the Register button to complete the registration
    await page.click(await page.locator('#register-button'));

    // Wait for the user to be redirected to the home page
    await page.waitForNavigation();

    // Navigate to the Books menu or link to access the book list
    await page.goto('https://demowebshop.tricentis.com/books');

    // Locate and click on the Health Book to open its details page
    await page.click(await page.locator('#health-book'));

    // Verify that the user is logged in after registration
    await page.waitForNavigation();

    // Navigate to the shopping cart to check the added item
    await page.goto('https://demowebshop.tricentis.com/cart');

    // Locate and click on the Health Book to open its details page
    await page.click(await page.locator('#health-book'));

    // Verify that the user is logged in after registration
    await page.waitForNavigation();
  });
});
