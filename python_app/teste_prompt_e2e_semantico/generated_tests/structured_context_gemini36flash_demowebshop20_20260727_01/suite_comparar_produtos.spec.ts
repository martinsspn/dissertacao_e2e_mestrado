import { test, expect } from '@playwright/test';

test.describe('Suite Comparar Produtos', () => {
  test('Deve adicionar produtos a lista de comparacao e depois limpar a lista', async ({ page }) => {
    // Inicia na pagina principal
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Acessa a pagina do produto Computing and Internet e adiciona a lista de comparacao
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await expect(page.getByRole('heading', { name: 'Computing and Internet' })).toBeVisible();
    await page.getByRole('button', { name: 'Add to compare list' }).click();

    // Etapa 2: Acessa a pagina do produto Fiction e adiciona a lista de comparacao
    await page.getByText("Fiction", { exact: true }).first().click();
    await expect(page.getByRole('heading', { name: 'Fiction' })).toBeVisible();
    await page.getByRole('button', { name: 'Add to compare list' }).click();

    // Etapa 3: Exibe a pagina de comparacao contendo Computing and Internet e Fiction
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/compareproducts');
    await expect(page.getByRole('heading', { name: 'Compare products' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Computing and Internet' }).last()).toBeVisible();
    await expect(page.getByRole('link', { name: 'Fiction' }).last()).toBeVisible();

    // Etapa 4: Limpa a lista de comparacao
    await page.getByRole('button', { name: 'Clear list' }).click();
    await expect(page.getByText('You have no items to compare.')).toBeVisible();
  });
});
