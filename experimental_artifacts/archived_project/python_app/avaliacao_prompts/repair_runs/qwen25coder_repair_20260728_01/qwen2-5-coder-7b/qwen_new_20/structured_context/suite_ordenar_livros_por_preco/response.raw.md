```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Ordenar Livros Por Preco', () => {
  test('Ordenar livros por preço baixo para alto', async ({ page }) => {
    // Etapa 1: Acessa a categoria de Livros
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Etapa 2: Seleciona a opção de ordenar por preço baixo para alto
    await page.locator('#sorter-options').selectOption('Price: Low to High');

    // Verifica se os livros estão em ordem crescente de preço
    const prices = await page.locator('.product-box .price').allTextContents();
    for (let i = 0; i < prices.length - 1; i++) {
      expect(parseFloat(prices[i].replace('$', ''))).toBeLessThanOrEqual(parseFloat(prices[i + 1].replace('$', '')));
    }
  });
});
```