import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Sobre Nos', () => {
  test('The user accesses the Demo Web Shop home page and navigates to About us page', async ({ page }) => {
    // Etapa 1: Acessar a página inicial do Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');

    // Etapa 2: Navegar para a página "About us"
    const aboutUsLink = page.getByText("About us", { exact: true }).first();
    await aboutUsLink.click();

    // Verificar se foi redirecionado para a página "About us"
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/about-us');
  });
});
