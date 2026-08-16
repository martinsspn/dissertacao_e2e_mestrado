```typescript
import { test, expect } from '@playwright/test';

test.describe('Product History - Recently Viewed Products', () => {
  test('displays recently viewed products in reverse chronological order', async ({ browser }) => {
    // In a new browser context
    const context = await browser.newContext();
    const page = await context.newPage();

    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // 1. Open the Fiction product page
    await page.goto(baseUrl);

    const searchBox = page.getByPlaceholder('Search store').or(page.getByRole('searchbox'));
    if (await searchBox.isVisible()) {
      await searchBox.fill('Fiction');
      await searchBox.press('Enter');
      await page.getByRole('link', { name: 'Fiction', exact: true }).first().click();
    } else {
      await page.getByRole('link', { name: 'Fiction' }).first().click();
    }

    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();

    // 2. Open the Blue Jeans product page
    if (await searchBox.isVisible()) {
      await searchBox.fill('Blue Jeans');
      await searchBox.press('Enter');
      await page.getByRole('link', { name: /Blue Jeans/i }).first().click();
    } else {
      await page.getByRole('link', { name: /Blue Jeans/i }).first().click();
    }

    await expect(page.getByRole('heading', { name: /Blue Jeans/i })).toBeVisible();

    // 3. Select Recently viewed products in Customer service section
    const recentlyViewedLink = page.getByRole('link', { name: /Recently viewed products/i });
    await recentlyViewedLink.first().click();

    // Verify Recently viewed products page heading
    await expect(page.getByRole('heading', { name: /Recently viewed products/i })).toBeVisible();

    // 4. Verify both Blue Jeans and Fiction are present
    const blueJeansLocator = page.getByRole('link', { name: /Blue Jeans/i }).first();
    const fictionLocator = page.getByRole('link', { name: 'Fiction' }).first();

    await expect(blueJeansLocator).toBeVisible();
    await expect(fictionLocator).toBeVisible();

    // 5. Verify Blue Jeans is presented before Fiction (viewed most recently)
    const blueJeansIndex = await page.textContent().then(text => text.indexOf('Blue Jeans'));
    const fictionIndex = await page.textContent().then(text => text.indexOf('Fiction'));

    expect(blueJeansIndex).toBeGreaterThan(-1);
    expect(fictionIndex).toBeGreaterThan(-1);
    expect(blueJeansIndex).toBeLessThan(fictionIndex);

    await context.close();
  });
});
```