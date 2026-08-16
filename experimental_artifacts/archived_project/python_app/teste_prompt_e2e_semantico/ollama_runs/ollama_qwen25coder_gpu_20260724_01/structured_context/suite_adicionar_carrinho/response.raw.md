```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Carrinho', () => {
  test('Adicionar Blue Jeans ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Pesquisa por Blue Jeans
    await page.fill('#small-searchterms', 'Blue Jeans');
    await page.click('role_name:Search');

    // Etapa 2: Abre a página do produto Blue Jeans
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');
    await expect(page.locator('h1')).toHaveText('Blue Jeans');

    // Etapa 3: Adiciona o produto ao carrinho
    await page.click('#add-to-cart-button-36');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Etapa 5: Acessa o carrinho de compras
    await page.click('page.getByRole("link", { name: "Shopping cart", exact: true })');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1')).toHaveText('Shopping cart');

    // Verifica se Blue Jeans está no carrinho
    await expect(page.locator('td.item').filter({ hasText: 'Blue Jeans' })).toBeVisible();
  });
});
```