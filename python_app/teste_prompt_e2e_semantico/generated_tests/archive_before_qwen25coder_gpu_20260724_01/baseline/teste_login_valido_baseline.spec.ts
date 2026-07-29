import { test, expect } from '@playwright/test';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

test('Login with valid credentials', async ({ page }) => {
  const email = requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL');
  const password = requireEnvironmentVariable('DEMO_WEB_SHOP_PASSWORD');

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in', exact: true }).click();

  await expect(
    page.getByRole('heading', {
      name: 'Welcome, Please Sign In!',
      exact: true,
    }),
  ).toBeVisible();

  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(password);
  await page.locator('input.login-button').click();

  await expect(
    page.getByRole('link', {
      name: email,
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
