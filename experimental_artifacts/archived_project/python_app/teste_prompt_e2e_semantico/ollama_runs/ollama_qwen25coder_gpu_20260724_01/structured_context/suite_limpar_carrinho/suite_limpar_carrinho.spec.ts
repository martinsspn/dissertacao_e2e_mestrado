import { test, expect } from '@playwright/test';

test.describe('Suite Limpar Carrinho', () => {
  test('should clear the cart after removing an item', async ({ page }) => {
    // Etapa 1: Adicionar o produto Blue Jeans ao carrinho
    await page.goto('https://demowebshop.tricentis.com/blue-jeans');
    await page.click('#add-to-cart-button-36');

    // Etapa 2: Acessar o carrinho de compras
    await page.getByRole('link', { name: 'Shopping cart', exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1')).toContainText('Shopping cart');

    // Etapa 3: Marcar Blue Jeans para remoção
    await page.click('input[name="removefromcart_36"]');

    // Etapa 4: Selecionar Atualizar carrinho
    await page.click('button[name="updatecart"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.locator('h1')).toContainText('Shopping cart');

    // Verificação final: Carrinho deve estar vazio
    await expect(page.locator('.empty-cart')).toBeVisible();
  });
});
