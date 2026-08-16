import { test, expect } from '../../../playwright_resilience/fixture.ts';

test('Consulting Fiction product details', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  const searchField = page.locator('#small-searchterms');
  await expect(searchField).toBeVisible();
  await searchField.fill('Fiction');

  await page.locator('input.search-box-button').click();

  const fictionProduct = page.locator('.product-item').filter({
    has: page.getByRole('link', {
      name: 'Fiction',
      exact: true,
    }),
  });

  await expect(fictionProduct).toBeVisible();

  await fictionProduct
    .getByRole('link', {
      name: 'Fiction',
      exact: true,
    })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Fiction',
      exact: true,
    }),
  ).toBeVisible();

  const productPrice = page.locator(
    '.product-details-page .product-price span',
  );

  await expect(productPrice).toBeVisible();
  await expect(productPrice).not.toHaveText('');
});
