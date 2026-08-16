import { test, expect } from '../../../playwright_resilience/fixture.ts';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const invalidPassword = process.env.DEMO_WEB_SHOP_INVALID_PASSWORD;

test.describe('Suite Login Invalido', () => {
  test('mantem o usuario nao autenticado ao informar senha invalida', async ({
    page,
  }) => {
    test.skip(
      !email || !invalidPassword,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_INVALID_PASSWORD.',
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
    await page.getByLabel('Password:').fill(invalidPassword!);

    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/login',
    );
    await expect(page.locator('.validation-summary-errors')).toBeVisible();
    await expect(page.locator('.validation-summary-errors')).toContainText(
      'Login was unsuccessful. Please correct the errors and try again.',
    );
    await expect(
      page.getByRole('link', { name: 'Log in', exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: email!, exact: true }),
    ).toHaveCount(0);
  });
});
