import { test, expect } from '../../../playwright_resilience/fixture.ts';

test.describe('Suite Registro Usuario', () => {
  test('registra um novo usuario e retorna autenticado para a loja', async ({
    page,
  }) => {
    const uniqueEmail = `playwright.${Date.now()}@example.com`;
    const password = 'ValidPassword123!';

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Register', exact: true }).click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/register',
    );
    await expect(
      page.getByRole('heading', { name: 'Register', exact: true }),
    ).toBeVisible();

    const genderOption = page.locator('#gender-male');
    await genderOption.check();
    await expect(genderOption).toBeChecked();

    await page.getByLabel('First name:').fill('Playwright');
    await page.getByLabel('Last name:').fill('User');
    await page.getByLabel('Email:').fill(uniqueEmail);
    await page.getByLabel('Password:', { exact: true }).fill(password);
    await page.getByLabel('Confirm password:').fill(password);

    await page.locator('#register-button').click();

    await expect(
      page.getByText('Your registration completed', { exact: true }),
    ).toBeVisible();

    await expect(
      page.getByRole('link', { name: uniqueEmail, exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log out', exact: true }),
    ).toBeVisible();

    await page.getByRole('link', { name: 'Continue', exact: true }).click();

    await expect(
      page.getByRole('link', { name: uniqueEmail, exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log out', exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole('link', { name: 'Log in', exact: true }),
    ).toHaveCount(0);
  });
});
