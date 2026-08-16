import { test, expect } from '../../../../runtime/playwright/fixture.ts';

test.describe('Suite Limpar Carrinho', () => {
  test('remove Blue Jeans e exibe o carrinho vazio', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page.locator('#small-searchterms').fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const blueJeansResult = page
      .locator('.product-item')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansResult).toBeVisible();

    await blueJeansResult
      .getByRole('link', {
        name: 'Blue Jeans',
        exact: true,
      })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/blue-jeans',
    );
    await expect(
      page.getByRole('heading', {
        name: 'Blue Jeans',
        exact: true,
      }),
    ).toBeVisible();

    await page.locator('#add-to-cart-button-36').click();

    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your shopping cart',
    );

    await page
      .getByRole('link', { name: 'Shopping cart', exact: true })
      .click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    await expect(
      page.getByRole('heading', {
        name: 'Shopping cart',
        exact: true,
      }),
    ).toBeVisible();

    const blueJeansCartItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: 'Blue Jeans',
          exact: true,
        }),
      });

    await expect(blueJeansCartItem).toBeVisible();

    const removeCheckbox = blueJeansCartItem.locator(
      'input[type="checkbox"][name="removefromcart"]',
    );

    await removeCheckbox.check();
    await expect(removeCheckbox).toBeChecked();

    await page
      .getByRole('button', {
        name: 'Update shopping cart',
        exact: true,
      })
      .click();

    await expect(
      page.getByText('Your Shopping Cart is empty!', {
        exact: true,
      }),
    ).toBeVisible();

    await expect(blueJeansCartItem).toHaveCount(0);
  });
});
