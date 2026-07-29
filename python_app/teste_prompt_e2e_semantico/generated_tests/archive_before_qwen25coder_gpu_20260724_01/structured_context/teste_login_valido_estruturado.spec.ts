import { test, expect } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

test.describe('Suite Login Valido', () => {
  test('autentica o usuario com credenciais validas', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com credenciais validas.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/login',
    );
    await expect(
      page.getByRole('heading', {
        name: 'Welcome, Please Sign In!',
        exact: true,
      }),
    ).toBeVisible();

    await page.getByLabel('Email:').fill(email!);
    await page.getByLabel('Password:').fill(password!);

    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(
      page.getByRole('link', {
        name: email!,
        exact: true,
      }),
    ).toBeVisible();

    await expect(
      page.getByRole('link', {
        name: 'Log out',
        exact: true,
      }),
    ).toBeVisible();

    await expect(
      page.getByRole('link', {
        name: 'Log in',
        exact: true,
      }),
    ).toHaveCount(0);
  });
});
