import { test, expect } from '@playwright/test';

test.describe('Suite Carrinho Inicialmente Vazio', () => {
  test('Viewing an empty shopping cart', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.getByRole('heading', { name: 'Shopping cart', exact: true })).toBeVisible();
    await expect(page.getByText('Your Shopping Cart is empty!')).toBeVisible();
  });
});
