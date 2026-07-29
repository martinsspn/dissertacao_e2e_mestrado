import { test, expect } from '@playwright/test';

test('Suite Adicionar Dois Produtos Carrinho', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  await page.goto('https://demowebshop.tricentis.com/computing-and-internet');
  await page.locator("[id=\"add-to-cart-button-13\"]").click();

  await page.getByText("Fiction", { exact: true }).first().click();
  await page.getByRole('button', { name: 'Add to cart' }).click();

  await page.getByRole("link", { name: "Shopping cart", exact: true }).click();

  await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
  await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();
  await expect(page.locator('.cart')).toContainText('Computing and Internet');
  await expect(page.locator('.cart')).toContainText('Fiction');
});
