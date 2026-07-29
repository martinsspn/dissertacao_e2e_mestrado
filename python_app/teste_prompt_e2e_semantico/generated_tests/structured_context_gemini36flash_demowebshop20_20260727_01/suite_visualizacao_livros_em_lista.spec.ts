import { test, expect } from '@playwright/test';

test.describe('Suite Visualizacao Livros Em Lista', () => {
  test('deve alternar a exibição da categoria Books para o modo lista', async ({ page }) => {
    // Etapa 1: O usuário acessa a categoria Books
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Books", { exact: true }).first().click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

    // Etapa 2: O usuário seleciona List no controle View as
    await page.getByLabel('View as').selectOption({ label: 'List' });

    // Etapa 3: O sistema mantém a categoria Books visível e apresenta os produtos em lista
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();
    await expect(page.locator('.product-list')).toBeVisible();
  });
});
