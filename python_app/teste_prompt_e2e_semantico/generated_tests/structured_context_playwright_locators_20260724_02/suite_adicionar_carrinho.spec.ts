import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Carrinho', () => {
  test('Adicionar Blue Jeans ao carrinho', async ({ page }) => {
    // Etapa 1: Pesquisa por Blue Jeans
    await page.goto('https://demowebshop.tricentis.com/');
    await page.locator("[id=\"small-searchterms\"]").fill('Blue Jeans');
    await page.getByRole("button", { name: "Search", exact: true }).click();

    // Etapa 2: Abre a página do produto Blue Jeans
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/blue-jeans');

    // Etapa 3: Adiciona o produto ao carrinho
    await page.locator("[id=\"add-to-cart-button-36\"]").click();

    // Verifica a mensagem de sucesso
    await expect(page.getByText('The product has been added to your shopping cart')).toBeVisible();

    // Etapa 5: Acessa o carrinho
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Verifica que Blue Jeans está no carrinho
    await expect(page.getByText('Blue Jeans')).toBeVisible();
  });
});
