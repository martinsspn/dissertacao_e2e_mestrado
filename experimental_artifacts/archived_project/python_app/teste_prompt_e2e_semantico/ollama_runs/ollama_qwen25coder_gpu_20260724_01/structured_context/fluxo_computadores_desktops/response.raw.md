```typescript
import { test, expect } from '@playwright/test';

test.describe('Fluxo Computadores Desktops', () => {
  test('The user must access the Digital downloads category, view the available digital items, and validate that the digital downloads page is visible.', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1 (R1)
    const digitalDownloadsLink = page.locator('a', { hasText: 'Digital downloads' });
    await expect(digitalDownloadsLink).toBeVisible();
    await digitalDownloadsLink.click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/digital-downloads');

    // Verificar que a página de downloads digitais está visível
    const title = page.locator('h1', { hasText: 'Digital downloads' });
    await expect(title).toBeVisible();
  });
});
```