import { test, expect } from '../../../playwright_resilience/fixture.ts';

test('Searching and opening the Blue Jeans product', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  const searchField = page.locator('#small-searchterms');
  await expect(searchField).toBeVisible();
  await searchField.fill('Blue Jeans');

  await page.locator('input.search-box-button').click();

  const blueJeansProduct = page
    .locator('.product-item')
    .filter({
      has: page.getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      }),
    });

  await expect(blueJeansProduct).toBeVisible();
  await expect(
    blueJeansProduct.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  ).toBeVisible();

  await blueJeansProduct
    .getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Blue Jeans',
      exact: true,
    }),
  ).toBeVisible();
});
