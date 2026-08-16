Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Changing the number of books displayed per page: The user accesses the Books category. The user selects 4 in the Display control. The system keeps the Books category visible and displays no more than four product items on the current page.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Books Category Display Control', () => {
  test('should keep Books visible and display no more than 4 items when 4 is selected', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Access the home page
    await page.goto(baseUrl);

    // Access the Books category
    const booksLink = page.getByRole('link', { name: 'Books', exact: true }).first();
    await expect(booksLink).toBeVisible();
    await booksLink.click();

    // Verify the Books category heading is visible
    const booksHeading = page.getByRole('heading', { name: 'Books' }).first();
    await expect(booksHeading).toBeVisible();

    // Locate the Display control select element
    const displayControl = page
      .getByLabel(/display/i)
      .or(page.getByRole('combobox', { name: /display/i }))
      .or(page.locator('#products-pagesize'))
      .first();

    await expect(displayControl).toBeVisible();

    // Select 4 in the Display control
    await displayControl.selectOption({ label: '4' }).catch(async () => {
      await displayControl.selectOption('4');
    });

    // Ensure the page state updates
    await page.waitForLoadState('networkidle');

    // Verify the Books category remains visible
    await expect(booksHeading).toBeVisible();

    // Verify no more than four product items are displayed on the current page
    const productItems = page.locator('.product-item, .item-box, [data-testid="product-item"]');
    const count = await productItems.count();

    expect(count).toBeGreaterThan(0);
    expect(count).toBeLessThanOrEqual(4);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(received).toBeLessThanOrEqual(expected)

Expected: <= 4
Received:    8

DIAGNÓSTICO DA REVISÃO:
Seleciona 4, mantém Books visível e valida limite e presença de produtos.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.