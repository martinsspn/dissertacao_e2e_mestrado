import { test, expect } from '@playwright/test';

test.describe('Suite Persistencia Carrinho Apos Login', () => {
  test('should persist cart items after login', async ({ page }) => {
    // Etapa 1: Autenticação com credenciais válidas
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log in", { exact: true }).first().click();
    await page.fill('input[name="Email"]', process.env.TEST_EMAIL);
    await page.fill('input[name="Password"]', process.env.TEST_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Etapa 2: Adicionar produto ao carrinho
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByRole('link', { name: 'Computing and Internet' }).click();
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 3: Logout e login novamente
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log out", { exact: true }).click();
    await page.fill('input[name="Email"]', process.env.TEST_EMAIL);
    await page.fill('input[name="Password"]', process.env.TEST_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Etapa 4: Acessar carrinho
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByRole('link', { name: 'Shopping cart' }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Etapa 5: Verificar persistência do carrinho
    await expect(page.getByText('Computing and Internet')).toBeVisible();

    // Etapa 6: Remover produto para restaurar o estado da conta
    await page.click('button[name="removefromcart"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(page.getByText('Computing and Internet')).not.toBeVisible();
  });
});
