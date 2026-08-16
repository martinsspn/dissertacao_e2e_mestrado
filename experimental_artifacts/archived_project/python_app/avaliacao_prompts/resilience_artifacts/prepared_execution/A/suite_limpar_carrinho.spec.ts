import { test, expect } from '../../../playwright_resilience/fixture.ts';

test('Removal of all products from the cart', async ({ page }) => {
  await page.goto('https://demowebshop.tricentis.com/');

  const searchField = page.locator('#small-searchterms');
  await expect(searchField).toBeVisible();
  await searchField.fill('Blue Jeans');

  await page.locator('input.search-box-button').click();

  const blueJeansProduct = page.locator('.product-item').filter({
    has: page.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  });

  await expect(blueJeansProduct).toBeVisible();

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

  await page.locator('input[value="Add to cart"]').click();

  const successNotification = page.locator('#bar-notification');
  await expect(successNotification).toBeVisible();
  await expect(successNotification).toContainText(
    'The product has been added to your shopping cart',
  );

  await page.locator('#topcartlink').getByRole('link').click();

  const blueJeansCartItem = page.locator('.cart-item-row').filter({
    has: page.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    }),
  });

  await expect(blueJeansCartItem).toBeVisible();

  await blueJeansCartItem.locator('input[name^="removefromcart"]').check();
  await page.locator('input[name="updatecart"]').click();

  await expect(
    page.getByText('Your Shopping Cart is empty!', {
      exact: true,
    }),
  ).toBeVisible();
});
