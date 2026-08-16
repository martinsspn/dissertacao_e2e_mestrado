import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Wishlist', () => {
  test('Adicionar produto à wishlist', async ({ page }) => {
    // Etapa 1: Autenticação (presumida já realizada pelo ambiente de teste)

    // Etapa 2: Pesquisa por Camera
    await page.goto('https://demowebshop.tricentis.com/');
    await page.fill('#small-searchterms', 'Camera');
    await page.click('role_name:Search');

    // Etapa 3: Abertura do produto Camera
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/digital-slr-camera');
    await expect(page.locator('h1')).toContainText('Digital SLR Camera 12.2 Mpixel');

    // Etapa 4: Adicionar ao Wishlist
    await page.click('#add-to-wishlist-button-18');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/digital-slr-camera');

    // Etapa 5: Confirmação de adição ao Wishlist (presumida por mensagem visível)

    // Etapa 6: Acessar Wishlist
    await page.click('page.getByRole("link", { name: "Wishlist", exact: true })');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');

    // Etapa 7: Verificação do produto na Wishlist
    await expect(page.locator('h1')).toContainText('Wishlist');
    await expect(page.locator('li.product-item')).toContainText('Digital SLR Camera 12.2 Mpixel');
  });
});
