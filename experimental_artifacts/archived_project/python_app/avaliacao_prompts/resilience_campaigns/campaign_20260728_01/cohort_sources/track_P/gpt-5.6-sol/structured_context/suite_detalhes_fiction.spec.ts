import { test, expect } from '@playwright/test';

test.describe('Suite Detalhes Fiction', () => {
  test('exibe os detalhes e o preço disponível do produto Fiction', async ({
    page,
  }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page.locator('#small-searchterms').fill('Fiction');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const fictionResult = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: 'Fiction',
          exact: true,
        }),
      });

    await expect(fictionResult).toBeVisible();

    const fictionResultLink = fictionResult.getByRole('link', {
      name: 'Fiction',
      exact: true,
    });

    await expect(fictionResultLink).toBeVisible();
    await fictionResultLink.click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/fiction',
    );

    await expect(
      page.getByRole('heading', {
        name: 'Fiction',
        exact: true,
      }),
    ).toBeVisible();

    const productPrice = page
      .locator('.product-essential')
      .locator('.prices');

    await expect(productPrice).toBeVisible();
    await expect(productPrice).not.toHaveText('');
  });
});
