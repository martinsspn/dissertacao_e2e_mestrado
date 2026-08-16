```typescript
import { test, expect } from '@playwright/test';

test.describe('Changing the book catalog view', () => {
  test('should switch to list view when user selects List in the View as control', async ({ page }) => {
    // Navigate to the Books category
    await page.goto('/books');

    // Verify initial Grid view
    const gridView = page.locator('.grid-view');
    expect(gridView).toBeVisible();

    // Select List view
    await page.click('button.view-as-list');

    // Verify List view is displayed
    const listView = page.locator('.list-view');
    expect(listView).toBeVisible();
  });
});
```