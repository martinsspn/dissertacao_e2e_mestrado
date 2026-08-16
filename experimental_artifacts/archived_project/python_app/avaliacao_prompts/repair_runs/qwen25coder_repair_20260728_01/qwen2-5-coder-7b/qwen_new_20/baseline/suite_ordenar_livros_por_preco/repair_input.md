Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Sorting books by ascending price: The user accesses the Books category. The user selects Price: Low to High in the Sort by control. The system keeps the Books category visible and displays the products in nondecreasing order according to their current sale prices.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Sorting books by ascending price', () => {
  test('should sort books by ascending price', async ({ page }) => {
    // Access the Books category
    await page.goto('/books');

    // Select Price: Low to High in the Sort by control
    await page.click('text=Sort by');
    await page.click('text=Price: Low to High');

    // The system keeps the Books category visible and displays the products in nondecreasing order according to their current sale prices
    const productPrices = await page.locator('.product-price').allTextContents();
    for (let i = 0; i < productPrices.length - 1; i++) {
      expect(parseFloat(productPrices[i])).toBeLessThanOrEqual(parseFloat(productPrices[i + 1]));
    }
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('text=Price: Low to High')
    - locator resolved to <option value="https://demowebshop.tricentis.com/books?orderby=10">Price: Low to High</option>
  - attempting click action
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
    - waiting 20ms
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
      - waiting 100ms
    19 × waiting for element to be visible, enabled and stable
       - element is not visible
     - retrying click action
       - waiting 500ms

DIAGNÓSTICO DA REVISÃO:
Compara preços em ordem, mas modela o seletor de ordenação e a classe de preço incorretamente.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.