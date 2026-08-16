import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Cartoes Presente', () => {
  test('Navegar para a categoria de Cartões de Presente e verificar produtos', async ({ page }) => {
    // Etapa 1: O usuário acessa a página inicial do Demo Web Shop.
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: O usuário seleciona Gift Cards no menu principal de categorias.
    await page.getByText("Gift Cards", { exact: true }).first().click();

    // Etapa 3: O sistema exibe a página da categoria Gift Cards, seu breadcrumb e os produtos disponíveis.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/gift-cards');
    await expect(page.getByRole('heading', { name: 'Gift Cards', exact: true })).toBeVisible();
    await expect(page.locator('.breadcrumb')).toBeVisible();

    // Verificar a presença de pelo menos um produto
    const productItems = page.locator('.product-item');
    await expect(productItems).toHaveCount(1);
  });
});
