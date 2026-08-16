import { test, expect } from '@playwright/test';

test.describe('Registration - Mismatched Password Validation', () => {
  test('should display error when password and confirm password do not match', async ({ page }) => {
    const uniqueEmail = `testuser_${Date.now()}@example.com`;

    // Access the Register page
    await page.goto('/register');

    // Fill in First name and Last name with valid data
    await page.getByLabel(/first name/i).fill('Jane');
    await page.getByLabel(/last name/i).fill('Doe');

    // Fill in Email with unique address
    await page.getByLabel(/email/i).fill(uniqueEmail);

    // Fill in Password with a valid password and Confirm password with a different value
    await page.getByLabel(/^password/i).first().fill('ValidPassword123!');
    await page.getByLabel(/confirm password/i).fill('DifferentPassword123!');

    // Submit the form using the Register button
    await page.getByRole('button', { name: /register|sign up/i }).click();

    // Verify system does not register and informs that the passwords do not match
    const mismatchMessage = page.getByText(/password.*match|passwords do not match/i);
    await expect(mismatchMessage).toBeVisible();

    // Verify user remains on the register page
    await expect(page).toHaveURL(/.*register.*/i);
  });
});
