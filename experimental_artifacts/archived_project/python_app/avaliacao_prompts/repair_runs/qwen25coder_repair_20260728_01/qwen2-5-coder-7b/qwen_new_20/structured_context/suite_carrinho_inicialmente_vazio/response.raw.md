```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Carrinho Inicialmente Vazio', () => {
  test('Viewing an empty shopping cart', async ({ page }) => {
    // Etapa 1: Acessar a página do carrinho de compras
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 2: Verificar que o carrinho está vazio
    await expect(page.locator('h1')).toHaveText('Shopping cart');
    await expect(page.getByRole('heading', { name: 'No items added to your shopping cart' })).toBeVisible();
  });
});
```