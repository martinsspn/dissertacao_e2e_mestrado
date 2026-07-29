import { test, expect } from '@playwright/test';

test.describe('Demo Web Shop - Registration Validation', () => {
  test('should display required-field validation messages when submitting empty form', async ({ page }) => {
    // 1. Access the Register page of the Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/register');

    // Verify the page is loaded correctly
    await expect(page.getByRole('heading', { name: 'Register' })).toBeVisible();

    // 2. Submit the registration form with empty fields
    const registerButton = page.getByRole('button', { name: 'Register', exact: true });
    await registerButton.click();

    // 3. Verify user is not registered and remains on the Register page
    await expect(page).toHaveURL(/.*\/register/);

    // 4. Verify required-field validation messages for all five mandatory fields
    await expect(page.getByText('First name is required.')).toBeVisible();
    await expect(page.getByText('Last name is required.')).toBeVisible();
    await expect(page.getByText('Email is required.')).toBeVisible();
    
    // Password and Confirm Password both output 'Password is required.' validation text
    const passwordValidationMessages = page.getByText('Password is required.');
    await expect(passwordValidationMessages).toHaveCount(2);

    // Ensure exactly 5 required field validation error messages are displayed
    const validationErrors = page.locator('.field-validation-error');
    await expect(validationErrors).toHaveCount(5);
  });
});
