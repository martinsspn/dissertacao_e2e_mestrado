import { test, expect } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

test.describe('Suite Logout', () => {
  test('encerra a sessao do usuario autenticado', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com credenciais validas.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();

    await page.locator('#Email').fill(email!);
    await page.locator('#Password').fill(password!);
    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    const accountLink = page.getByRole('link', {
      name: email!,
      exact: true,
    });
    const logoutLink = page.getByRole('link', {
      name: 'Log out',
      exact: true,
    });

    await expect(accountLink).toBeVisible();
    await expect(logoutLink).toBeVisible();

    await logoutLink.click();

    await expect(
      page.getByRole('link', {
        name: 'Log in',
        exact: true,
      }),
    ).toBeVisible();

    await expect(
      page.getByRole('link', {
        name: 'Log out',
        exact: true,
      }),
    ).toHaveCount(0);

    await expect(accountLink).toHaveCount(0);
  });
});
