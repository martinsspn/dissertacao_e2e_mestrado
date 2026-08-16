```typescript
import { test, expect } from '@playwright/test';

test.describe('Community Poll Voting', () => {
  test('should prevent voting without selecting an answer', async ({ page }) => {
    // Access the Demo Web Shop home page in a new browser context
    await page.goto('https://demowebshop.tricentis.com/');

    // Navigate to the Community poll titled "Do you like nopCommerce?"
    await page.click('text="Community polls"');
    await page.click('text="Do you like nopCommerce?"');

    // Attempt to vote without selecting an answer
    await page.click('button:has-text("Vote")');

    // Verify that the system prevents the vote and informs the user to select an answer
    const alertText = await page.textContent('.alert.alert-danger');
    expect(alertText).toContain('Please select an answer before voting.');
  });
});
```