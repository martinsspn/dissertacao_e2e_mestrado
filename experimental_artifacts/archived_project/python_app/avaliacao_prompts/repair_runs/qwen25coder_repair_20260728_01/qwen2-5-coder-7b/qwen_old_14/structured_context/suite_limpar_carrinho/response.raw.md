```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Limpar Carrinho', () => {
  test('should clear the cart after removing an item', async ({ page }) => {
    // Etapa 1: Adicionar o produto Blue Jeans ao carrinho
    await page.goto('https://demowebshop.tricentis.com/blue-jeans');
    await page.locator("[id=\"add-to-cart-button-36\"]").click();

    // Etapa 2: Acessar Carrinho de Compras
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 3: Marcar Blue Jeans para remoção
    await page.locator("[name=\"removefromcart_1\"]").click();

    // Etapa 4: Selecionar Atualizar Carrinho
    await page.getByRole("button", { name: "Update shopping cart" }).click();

    // Etapa 5: Sistema exibe carrinho vazio
    await expect(page.locator("[class=\"empty-cart\"]")).toBeVisible();
  });
});
```