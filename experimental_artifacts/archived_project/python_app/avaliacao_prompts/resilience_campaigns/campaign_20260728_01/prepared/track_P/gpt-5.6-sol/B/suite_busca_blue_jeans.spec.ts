import { test, expect } from '../../../../runtime/playwright/fixture.ts';

test.describe('Suite Busca Blue Jeans', () => {
  test('busca e abre os detalhes do produto Blue Jeans', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page.locator('#small-searchterms').fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const blueJeansResult = page
      .locator('.product-item')
      .filter({
        has: page
          .locator('h2.product-title')
          .getByRole('link', { name: 'Blue Jeans', exact: true }),
      });

    await expect(blueJeansResult).toBeVisible();
    await expect(
      blueJeansResult
        .locator('h2.product-title')
        .getByRole('link', { name: 'Blue Jeans', exact: true }),
    ).toBeVisible();

    await blueJeansResult
      .locator('h2.product-title')
      .getByRole('link', { name: 'Blue Jeans', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/blue-jeans',
    );
    await expect(
      page.getByRole('heading', { name: 'Blue Jeans', exact: true }),
    ).toBeVisible();
  });
});
