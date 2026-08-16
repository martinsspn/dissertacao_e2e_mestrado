import { test, expect } from '../../../playwright_resilience/fixture.ts';

test('Configuration of a computer before purchase', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  await page
    .getByRole('link', { name: 'Computers', exact: true })
    .first()
    .click();

  await expect(
    page.getByRole('heading', { name: 'Computers', exact: true }),
  ).toBeVisible();

  await page
    .getByRole('link', { name: 'Desktops', exact: true })
    .first()
    .click();

  await expect(
    page.getByRole('heading', { name: 'Desktops', exact: true }),
  ).toBeVisible();

  const configurableDesktop = page.locator('.product-item').filter({
    has: page.getByRole('link', {
      name: 'Build your own cheap computer',
      exact: true,
    }),
  });

  await expect(configurableDesktop).toBeVisible();

  await configurableDesktop
    .getByRole('link', {
      name: 'Build your own cheap computer',
      exact: true,
    })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Build your own cheap computer',
      exact: true,
    }),
  ).toBeVisible();

  await page.getByLabel('Fast', { exact: true }).check();
  await page.getByLabel('4 GB', { exact: true }).check();
  await page.getByLabel('400 GB', { exact: true }).check();
  await page.getByLabel('Office Suite', { exact: true }).check();

  await page.locator('input[value="Add to cart"]').click();

  const successNotification = page.locator('#bar-notification');

  await expect(successNotification).toBeVisible();
  await expect(successNotification).toContainText(
    'The product has been added to your shopping cart',
  );

  await page.locator('#topcartlink').getByRole('link').click();

  const configuredDesktop = page.locator('.cart-item-row').filter({
    has: page.getByRole('link', {
      name: 'Build your own cheap computer',
      exact: true,
    }),
  });

  await expect(configuredDesktop).toBeVisible();
  await expect(configuredDesktop).toContainText('Fast');
  await expect(configuredDesktop).toContainText('4 GB');
  await expect(configuredDesktop).toContainText('400 GB');
  await expect(configuredDesktop).toContainText('Office Suite');
});
