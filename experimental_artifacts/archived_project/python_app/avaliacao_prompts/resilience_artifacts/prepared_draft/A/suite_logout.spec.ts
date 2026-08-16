import { test, expect } from '../../../playwright_resilience/fixture.ts';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

test('User session termination', async ({ page }) => {
  const email = requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL');
  const password = requireEnvironmentVariable('DEMO_WEB_SHOP_PASSWORD');

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in', exact: true }).click();

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

  await page.getByRole('link', { name: 'Log out', exact: true }).click();

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

  await expect(
    page.getByRole('link', {
      name: email,
      exact: true,
    }),
  ).toHaveCount(0);
});
