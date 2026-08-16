import { test, expect } from '@playwright/test';

test.describe('Suite Detalhes Fiction', () => {
  test('The user searches for the product Fiction in the Search store field and opens its details page', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Pesquisa pelo produto Fiction
    const searchInput = page.locator('#small-searchterms');
    await searchInput.fill('Fiction');
    const searchButton = page.locator('role=Search');
    await searchButton.click();

    // Verifica se a URL contém '/fiction'
    await expect(page).toHaveURL(/\/fiction/);

    // Etapa 2: Confirma que a página de detalhes do produto Fiction é exibida
    const productTitle = page.locator('h1');
    await expect(productTitle).toHaveText('Fiction');

    // Etapa 3: Verifica se as informações de preço estão disponíveis
    const priceInfo = page.locator('.price-value-std');
    await expect(priceInfo).toBeVisible();
  });
});
