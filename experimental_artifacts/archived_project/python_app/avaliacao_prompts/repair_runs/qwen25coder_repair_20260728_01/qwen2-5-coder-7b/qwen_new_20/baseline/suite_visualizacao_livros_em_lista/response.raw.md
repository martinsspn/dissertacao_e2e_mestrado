```typescript
import { test, expect } from '@playwright/test';

test.describe('Changing the book catalog view', () => {
  test('should switch to list view when user selects List in the View as control', async ({ page }) => {
    // Navigate to the Books category
    await page.goto('/books');

    // Verify initial Grid view
    const gridView = page.locator('.product-grid');
    expect(await gridView.isVisible()).toBe(true);

    // Select List view
    await page.click('button.view-as-list');

    // Verify List view is displayed
    const listView = page.locator('.product-list');
    expect(await listView.isVisible()).toBe(true);
  });
});
```