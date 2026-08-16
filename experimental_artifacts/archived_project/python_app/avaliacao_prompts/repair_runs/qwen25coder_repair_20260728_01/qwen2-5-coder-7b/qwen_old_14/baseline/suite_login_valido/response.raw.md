```typescript
import { test, expect } from '@playwright/test';

test.describe('Login with valid credentials', () => {
  test('should authenticate user and display account and logout links', async ({ page }) => {
    // Access the Log in page of the Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/login');

    // Fill in Email and Password with the valid credentials provided by the testing environment
    await page.fill('#Email', process.env.TEST_EMAIL || 'test@example.com');
    await page.fill('#Password', process.env.TEST_PASSWORD || 'password123');

    // Submit the login form
    await page.click('input[type="submit"]');

    // The system authenticates the user and displays the account and Log out links
    await expect(page.locator('.account')).toBeVisible();
    await expect(page.locator('#logoutLink')).toBeVisible();
  });
});
```