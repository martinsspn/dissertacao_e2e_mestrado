```typescript
import { test, expect } from '@playwright/test';

test.describe('Validation of mismatched registration passwords', () => {
  test('should inform when password and confirmation password do not match', async ({ page }) => {
    // Access the Register page
    await page.goto('/register');

    // Fill in First name and Last name with valid data
    await page.fill('#firstName', 'John');
    await page.fill('#lastName', 'Doe');

    // Fill in Email with a unique address generated for this execution
    const email = `test${Date.now()}@example.com`;
    await page.fill('#email', email);

    // Fill in Password with a valid password and Confirm password with a different value
    const password = 'ValidPassword123';
    await page.fill('#password', password);
    await page.fill('#confirmPassword', 'DifferentPassword123');

    // Submit the form using the Register button
    await page.click('#registerButton');

    // The system does not register the user and informs that the password and confirmation password do not match
    const errorMessage = await page.textContent('.error-message');
    expect(errorMessage).toContain('Passwords do not match');
  });
});
```