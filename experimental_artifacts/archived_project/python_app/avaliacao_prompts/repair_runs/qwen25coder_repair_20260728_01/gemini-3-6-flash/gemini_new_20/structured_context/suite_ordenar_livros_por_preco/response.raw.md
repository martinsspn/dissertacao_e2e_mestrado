```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Ordenar Livros Por Preco', () => {
  test('Deve ordenar livros por preco do menor para o maior', async ({ page }) => {
    // Etapa 1: Navegar para a categoria Books
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    // Etapa 2: Selecionar "Price: Low to High" no controle de ordenacao
    await page.locator('#sortOrder').selectOption({ label: 'Price: Low to High' });

    // Etapa 3: Verificar que a categoria Books continua visivel e os produtos estao ordenados por preco crescente
    await expect(page.getByRole('heading', { name: 'Books', exact: true })).toBeVisible();

    const priceElements = page.locator('.actual-price');
    await expect(priceElements.first()).toBeVisible();

    const priceTexts = await priceElements.allInnerTexts();
    const prices = priceTexts.map(text => parseFloat(text.replace(/[^0-9.]/g, '')));

    expect(prices.length).toBeGreaterThan(0);
    for (let i = 0; i < prices.length - 1; i++) {
      expect(prices[i]).toBeLessThanOrEqual(prices[i + 1]);
    }
  });
});
```