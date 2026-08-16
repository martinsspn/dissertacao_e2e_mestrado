Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Viewing the product history: In a new browser context, the user opens the Fiction product page and then opens the Blue Jeans product page. The user selects Recently viewed products in the Customer service section. The system displays the Recently viewed products page containing both Blue Jeans and Fiction, with Blue Jeans presented before Fiction because it was viewed most recently.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Product History - Recently Viewed Products', () => {
  test('displays recently viewed products in reverse chronological order', async ({ browser }) => {
    // In a new browser context
    const context = await browser.newContext();
    const page = await context.newPage();

    const baseUrl = process.env.BASE_URL || 'https://demo.nopcommerce.com';

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
    const pageText = await page.locator('body').innerText();
    const blueJeansIndex = pageText.indexOf('Blue Jeans');
    const fictionIndex = pageText.indexOf('Fiction');

    expect(blueJeansIndex).toBeGreaterThan(-1);
    expect(fictionIndex).toBeGreaterThan(-1);
    expect(blueJeansIndex).toBeLessThan(fictionIndex);

    await context.close();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.click: Timeout 10000ms exceeded.
Call log:
  - waiting for getByRole('link', { name: 'Fiction' }).first()

DIAGNÓSTICO DA REVISÃO:
Fluxo e ordem completos, mas o domínio padrão é outra instalação nopCommerce.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.