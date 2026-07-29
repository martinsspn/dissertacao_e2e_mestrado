import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Dois Produtos Carrinho', () => {
  test('Adicionar Computing and Internet ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.locator("[id=\"add-to-cart-button-13\"]").click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/computing-and-internet');
  });

  test('Adicionar Fiction ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
    await page.getByText("Fiction", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/fiction');
  });

  test('Acessar carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/fiction');
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
  });

  test('Verificar itens no carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/cart');
    await expect(page.getByText("Computing and Internet")).toBeVisible();
    await expect(page.getByText("Fiction")).toBeVisible();
  });
});
