```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Exibir Quatro Livros', () => {
  test('The user accesses the Books category and displays no more than four product items on the current page', async ({ page }) => {
    // Etapa 1: Access the Books category
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Etapa 3: Verify no more than four product items are displayed
    const productItems = page.locator('.product-item');
    await expect(productItems).toHaveCount(4);
  });
});
```