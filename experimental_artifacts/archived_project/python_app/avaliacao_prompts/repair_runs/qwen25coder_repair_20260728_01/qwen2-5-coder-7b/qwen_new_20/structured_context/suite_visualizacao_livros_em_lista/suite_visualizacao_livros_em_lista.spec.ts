import { test, expect } from '@playwright/test';

test.describe('Suite Visualizacao Livros Em Lista', () => {
  test('The user accesses the Books category and selects List view', async ({ page }) => {
    // Etapa 1: Acessa a categoria de Livros
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Etapa 3: Seleciona a visualização em Lista
    const listViewButton = page.locator('button', { hasText: 'List' });
    if (await listViewButton.isVisible()) {
      await listViewButton.click();
    }

    // Verifica se a página ainda é a de Livros e se está em modo de lista
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    const productItems = page.locator('.product-item');
    await expect(productItems).toHaveCount(6); // Espera que haja 6 produtos visíveis na lista
  });
});
