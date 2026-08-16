import { test } from '@playwright/test';

describe('Suite Registro Usuario', () => {
  it('should register user successfully', async () => {
    const page = await playwright.chromium.launch();

    await page.goto('https://demowebshop.tricentis.com/');

    // Step 1: The user accesses the Register page of the Demo Web Shop
    const registerLink = await page.locator('#register-button');
    await registerLink.click();

    // Step 2: The user selects a Gender option
    const genderSelect = await page.locator('#gender-select');
    await genderSelect.focus();

    // Step 3: The user fills in First name and Last name with valid data
    const firstNameInput = await page.locator('#first-name-input');
    await firstNameInput.fill('John Doe');
    const lastNameInput = await page.locator('#last-name-input');
    await lastNameInput.fill('Doe');

    // Step 4: The user fills in Email with a unique address generated for this execution
    const emailInput = await page.locator('#email-input');
    const email = 'johndoe@example.com';
    await emailInput.fill(email);

    // Step 5: The user fills in Password and Confirm password with the same valid password
    const passwordInput = await page.locator('#password-input');
    const confirmPasswordInput = await page.locator('#confirm-password-input');
    await passwordInput.fill('password123');
    await confirmPasswordInput.fill('password123');

    // Step 6: The user submits the form using the Register button
    await registerLink.click();

    // Step 7: The system confirms that the registration has been completed
    const confirmationMessage = await page.locator('#confirmation-message');
    expect(confirmationMessage).toBeInTheDocument();

    // Step 8: The user selects Continue and returns to the store authenticated
    await page.locator('#continue-button').click();
  });
});
