import { test, expect } from '@playwright/test';

test.describe('Short registration password validation', () => {
  test('should prevent registration with short password', async ({ page }) => {
    // Access the Register page
    await page.goto('/register');

    // Fill in First name and Last name with valid data
    await page.fill('#firstName', 'John');
    await page.fill('#lastName', 'Doe');

    // Fill in Email with a unique address generated for this execution
    const email = `test${Date.now()}@example.com`;
    await page.fill('#email', email);

    // Fill in Password and Confirm password with the same value containing fewer than six characters
    const shortPassword = '123';
    await page.fill('#password', shortPassword);
    await page.fill('#confirmPassword', shortPassword);

    // Submit the form using the Register button
    await page.click('#registerButton');

    // The system does not register the user and informs that the password must contain at least six characters
    const errorMessage = 'Password must be at least 6 characters long';
    await expect(page.locator('.error-message')).toHaveText(errorMessage);
  });
});
