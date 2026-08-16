import { test, expect } from '@playwright/test';

test.describe('Login attempt with an invalid password', () => {
  test('should keep the user unauthenticated and inform of failed login', async ({ page }) => {
    // Access the Log in page
    await page.goto('https://demowebshop.tricentis.com/login');

    // Fill in Email with an existing account's email
    await page.fill('#Email', 'existing@example.com');

    // Fill in Password with an invalid password provided by the testing environment
    await page.fill('#Password', process.env.INVALID_PASSWORD);

    // Submit the login form
    await page.click('#login-button');

    // Verify that the user is kept unauthenticated and informed of failed login
    const errorMessage = await page.textContent('.message-error');
    expect(errorMessage).toContain('Login was unsuccessful. Please correct the errors and try again.');
  });
});
