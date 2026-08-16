
```typescript
import { test } from '@playwright/test';

describe('Login Valido', () => {
  it('Login valido', async () => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Step 1: The user accesses the Log in page of the Demo Web Shop
    const loginControl = await page.locator('#login-control');
    await loginControl.click();

    // Step 2: The user fills in Email and Password with the valid credentials provided by the testing environment
    const emailInput = await page.locator('#email-input');
    await emailInput.fill('test@example.com');
    const passwordInput = await page.locator('#password-input');
    await passwordInput.fill('test1234567890');

    // Step 3: The user submits the login form
    const loginButton = await page.locator('#login-button');
    await loginButton.click();

    // Step 4: The system authenticates the user and displays the account and Log out links
    const accountLink = await page.locator('#account-link');
    await accountLink.click();
    const logoutLink = await page.locator('#logout-link');
  });
});
```