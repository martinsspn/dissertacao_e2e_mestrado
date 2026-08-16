import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Wishlist', () => {
  test('Adicionar produto à wishlist', async ({ page }) => {
    // Etapa 1: Autenticação (não implementada no contexto fornecido)
    
    // Etapa 2: Pesquisa por Camera
    await page.goto('https://demowebshop.tricentis.com/');
    await page.locator("[id=\"small-searchterms\"]").fill('Camera');
    await page.getByRole("button", { name: "Search", exact: true }).click();
    
    // Etapa 3: Abertura do produto Camera
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/search?q=Camera');
    const cameraProduct = page.locator("[href=\"/digital-slr-camera\"]");
    await cameraProduct.click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/digital-slr-camera');
    
    // Etapa 4: Adicionar ao carrinho
    await page.locator("[id=\"add-to-wishlist-button-18\"]").click();
    await expect(page.getByText("The product has been added to your wishlist.")).toBeVisible();
    
    // Etapa 6: Acessar Wishlist
    await page.getByRole("link", { name: "Wishlist", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');
    
    // Verificação final: Produto Camera na wishlist
    await expect(cameraProduct).toBeVisible();
  });
});
