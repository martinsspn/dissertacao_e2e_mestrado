import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Sobre Nos', () => {
  test('Deve navegar para a pagina About us a partir do rodape', async ({ page }) => {
    // Etapa 1: O usuario acessa a pagina inicial do Demo Web Shop.
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 2: Na secao Information do rodape, o usuario seleciona About us.
    await page.getByText("About us", { exact: true }).first().click();

    // Etapa 3: O sistema exibe a pagina About us e seu titulo correspondente.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/about-us');
    await expect(page.getByRole('heading', { name: 'About us', exact: true })).toBeVisible();
  });
});
