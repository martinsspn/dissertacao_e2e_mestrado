import { test, expect } from '@playwright/test';

test.describe('Suite Limpar Wishlist', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');
    // Assume que o usuário já está autenticado com as credenciais fornecidas pelo ambiente de teste
  });

  test('should clear the wishlist', async ({ page }) => {
    // Etapa 3: Acessa a Wishlist
    await page.getByRole('link', { name: 'Wishlist', exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');

    // Etapa 4: Marca o produto Camera para remoção
    const cameraProduct = page.locator('.product-item-name', { hasText: 'Camera' });
    await cameraProduct.click();
    await expect(cameraProduct).toBeVisible();

    // Etapa 5: Seleciona Atualizar Wishlist
    await page.getByRole('button', { name: 'Update wishlist' }).click();

    // Etapa 6: O sistema exibe a wishlist vazia
    await expect(page.locator('.no-data')).toBeVisible();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');
  });
});
