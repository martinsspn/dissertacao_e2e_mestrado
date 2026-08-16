
```typescript
import { test } from '@playwright/test';

describe('Login Invalido', () => {
  it('Login with invalid email and password', async () => {
    const page = await playwright.chromium.launch();

    await page.goto('https://demowebshop.tricentis.com/');

    // Step 1: Access the login page
    const control = await page.locator('#email');
    await control.click();

    // Step 2: Fill in email and password fields with invalid values
    const inputEmail = await page.locator('#email').query({ value: 'invalid@example.com' });
    await inputEmail.fill('Invalid Email');

    const inputPassword = await page.locator('#password').query({ value: 'weakpassword' });
    await inputPassword.fill('Weak Password');

    // Step 3: Submit the login form
    const submitButton = await page.locator('#submit-btn');
    await submitButton.click();

    // Step 4: Verify that the user is unauthenticated and informed of an error message
    const errorMessage = await page.locator('#error-message').query({ text: 'Login was not completed' });
    expect(errorMessage).toBeInTheDocument();
  });
});
```