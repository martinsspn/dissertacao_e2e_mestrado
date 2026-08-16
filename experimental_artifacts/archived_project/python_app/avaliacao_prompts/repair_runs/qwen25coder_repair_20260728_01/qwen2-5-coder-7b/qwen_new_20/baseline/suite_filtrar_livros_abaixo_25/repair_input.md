Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Filtering books by price: The user accesses the Books category. The user selects the Under 25.00 price filter. The system keeps the Books category visible and displays only products whose current sale price is below 25.00.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Filtering books by price', () => {
  test('should keep the Books category visible and display only products under 25.00', async ({ page }) => {
    // Access the Books category
    await page.goto('/books');

    // Select the Under 25.00 price filter
    await page.click('text=Under 25.00');

    // Verify that the Books category is still visible
    expect(await page.isVisible('text=Books')).toBe(true);

    // Verify that only products under 25.00 are displayed
    const productPrices = await page.textContent('.product-price');
    expect(productPrices).not.toContain('Over 25.00');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.textContent: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('.product-price')

DIAGNÓSTICO DA REVISÃO:
Aciona o filtro, mas o oráculo apenas procura a frase Over 25.00 e não inspeciona preços.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.