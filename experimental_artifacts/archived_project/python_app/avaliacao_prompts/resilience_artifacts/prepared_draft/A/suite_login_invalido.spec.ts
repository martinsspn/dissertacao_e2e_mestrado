import { test, expect } from '../../../playwright_resilience/fixture.ts';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

test('Login attempt with an invalid password', async ({ page }) => {
  const email = requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL');
  const invalidPassword = requireEnvironmentVariable(
    'DEMO_WEB_SHOP_INVALID_PASSWORD',
  );

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in', exact: true }).click();

  await expect(
    page.getByRole('heading', { name: 'Welcome, Please Sign In!', exact: true }),
  ).toBeVisible();

  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(invalidPassword);
  await page.locator('input.login-button').click();

  await expect(
    page.getByText('Login was unsuccessful. Please correct the errors and try again.', {
      exact: true,
    }),
  ).toBeVisible();

  await expect(
    page.getByText('The credentials provided are incorrect', {
      exact: true,
    }),
  ).toBeVisible();

  await expect(
    page.getByRole('link', { name: 'Log in', exact: true }),
  ).toBeVisible();

  await expect(
    page.getByRole('link', { name: email, exact: true }),
  ).toHaveCount(0);
});
