import { test, expect } from '@playwright/test';

test.describe('User Registration', () => {
  test('should register a new user successfully', async ({ page }) => {
    // Access the Register page of the Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/register');

    // Select a Gender option
    await page.locator('#gender-male').check();

    // Fill in First name and Last name with valid data
    await page.fill('#FirstName', 'John');
    await page.fill('#LastName', 'Doe');

    // Fill in Email with a unique address generated for this execution
    const email = `user${Date.now()}@example.com`;
    await page.fill('#Email', email);

    // Fill in Password and Confirm password with the same valid password
    const password = 'P@ssw0rd';
    await page.fill('#Password', password);
    await page.fill('#ConfirmPassword', password);

    // Submit the form using the Register button
    await page.click('#register-button');

    // System confirms that the registration has been completed
    await expect(page.locator('.result')).toHaveText('Your registration completed');

    // User selects Continue and returns to the store authenticated
    await page.click('a[href="/logout"]');
    await page.fill('#Email', email);
    await page.fill('#Password', password);
    await page.click('#login-button');
    await expect(page.locator('.account')).toContainText(email);
  });
});
