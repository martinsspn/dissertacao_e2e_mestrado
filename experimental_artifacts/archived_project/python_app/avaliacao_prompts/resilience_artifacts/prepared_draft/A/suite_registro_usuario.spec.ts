import { test, expect } from '../../../playwright_resilience/fixture.ts';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

test('Registration of a new user', async ({ page }) => {
  const firstName = requireEnvironmentVariable(
    'DEMO_WEB_SHOP_FIRST_NAME',
  );
  const lastName = requireEnvironmentVariable(
    'DEMO_WEB_SHOP_LAST_NAME',
  );
  const password = requireEnvironmentVariable(
    'DEMO_WEB_SHOP_PASSWORD',
  );

  const uniqueEmail = `playwright.${Date.now()}.${Math.random()
    .toString(36)
    .slice(2, 10)}@example.com`;

  await page.goto('https://demowebshop.tricentis.com/');

  await page
    .getByRole('link', { name: 'Register', exact: true })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Register',
      exact: true,
    }),
  ).toBeVisible();

  await page.locator('#gender-male').check();
  await page.locator('#FirstName').fill(firstName);
  await page.locator('#LastName').fill(lastName);
  await page.locator('#Email').fill(uniqueEmail);
  await page.locator('#Password').fill(password);
  await page.locator('#ConfirmPassword').fill(password);

  await page.locator('#register-button').click();

  await expect(
    page.getByText('Your registration completed', {
      exact: true,
    }),
  ).toBeVisible();

  await page
    .getByRole('button', { name: 'Continue', exact: true })
    .click();

  await expect(
    page.getByRole('link', {
      name: uniqueEmail,
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
