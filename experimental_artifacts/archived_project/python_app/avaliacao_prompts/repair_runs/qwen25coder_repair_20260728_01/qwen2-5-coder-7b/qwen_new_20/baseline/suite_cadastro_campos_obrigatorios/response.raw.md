```typescript
import { test, expect } from '@playwright/test';

test.describe('Validation of required registration fields', () => {
  test('should display validation messages for empty fields', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/register');

    // Leave all fields empty
    await page.click('input[name="FirstName"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="LastName"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="Email"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="Password"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="ConfirmPassword"]');

    // Submit the form
    await page.click('button[type="submit"]');

    // Check for validation messages
    await expect(page.locator('.message-error')).toHaveText('First name is required.');
    await expect(page.locator('.message-error')).toHaveText('Last name is required.');
    await expect(page.locator('.message-error')).toHaveText('Email is required.');
    await expect(page.locator('.message-error')).toHaveText('Password is required.');
    await expect(page.locator('.message-error')).toHaveText('Confirm password is required.');
  });
});
```