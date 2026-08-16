```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Filtrar Livros Abaixo 25', () => {
  test('Filtrar livros abaixo de 25.00', async ({ page }) => {
    // Etapa 1: Acessar a categoria Books
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Etapa 2: Selecionar o filtro Under 25.00
    await page.getByText("Under 25.00", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books?price=-25');

    // Etapa 3: Verificar que apenas livros abaixo de 25.00 são exibidos
    const products = page.locator('.product-item');
    for (let product of await products.all()) {
      const priceText = await product.getByRole('button', { name: 'Add to cart' }).first().textContent();
      expect(parseFloat(priceText.replace('$', ''))).toBeLessThan(25);
    }
  });
});
```