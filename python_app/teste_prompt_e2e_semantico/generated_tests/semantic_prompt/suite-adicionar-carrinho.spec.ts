import { test, expect } from '@playwright/test';

test.describe('Suite Adicionar Carrinho', () => {
  test('adiciona Blue Jeans ao carrinho', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    const searchField = page.locator('#small-searchterms');
    await expect(searchField).toBeVisible();
    await searchField.fill('Blue Jeans');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const blueJeansLink = page.getByRole('link', {
      name: 'Blue Jeans',
      exact: true,
    });
    await expect(blueJeansLink).toBeVisible();
    await blueJeansLink.click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/blue-jeans',
    );
    await expect(
      page.getByRole('heading', { name: 'Blue Jeans', exact: true }),
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
      page.getByRole('heading', { name: 'Shopping cart', exact: true }),
    ).toBeVisible();

    const cartItem = page.locator('.cart-item-row').filter({
      has: page.getByRole('link', { name: 'Blue Jeans', exact: true }),
    });

    await expect(cartItem).toBeVisible();
    await expect(
      cartItem.getByRole('link', { name: 'Blue Jeans', exact: true }),
    ).toBeVisible();
  });
});