Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Changing the number of books displayed per page: The user accesses the Books category. The user selects 4 in the Display control. The system keeps the Books category visible and displays no more than four product items on the current page.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Books Category Display Control', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/books');
  });

  test('displays no more than four product items when 4 is selected in the Display control', async ({ page }) => {
    // Select 4 in the Display control
    await page.locator('#display-control').selectOption('4');

    // Wait for the products to update
    await page.waitForSelector('.product-item');

    // Get all product items on the current page
    const productItems = await page.locator('.product-item').all();

    // Expect no more than four product items to be displayed
    expect(productItems.length).toBeLessThanOrEqual(4);
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: locator.selectOption: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('#display-control')

DIAGNÓSTICO DA REVISÃO:
Seleciona quatro e conta produtos, mas o identificador do controle Display é inventado.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.