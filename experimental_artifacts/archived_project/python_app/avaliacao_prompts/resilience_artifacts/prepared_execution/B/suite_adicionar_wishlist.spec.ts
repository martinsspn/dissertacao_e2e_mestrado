import { test, expect } from '../../../playwright_resilience/fixture.ts';

test.describe('Suite Adicionar Wishlist', () => {
  test('adiciona um produto Camera à wishlist', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    const loginLink = page.getByRole('link', { name: 'Log in', exact: true });

    if (await loginLink.isVisible()) {
      const email = process.env.DEMO_WEB_SHOP_EMAIL;
      const password = process.env.DEMO_WEB_SHOP_PASSWORD;

      if (!email || !password) {
        throw new Error(
          'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com credenciais válidas do ambiente de testes.',
        );
      }

      await loginLink.click();

      await page.locator('#Email').fill(email);
      await page.locator('#Password').fill(password);
      await page.getByRole('button', { name: 'Log in', exact: true }).click();
    }

    await expect(
      page.getByRole('link', { name: 'Log out', exact: true }),
    ).toBeVisible();

    await page.locator('#small-searchterms').fill('Camera');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const productName = 'Digital SLR Camera 12.2 Mpixel';
    const productLink = page.getByRole('link', {
      name: productName,
      exact: true,
    });

    await expect(productLink).toBeVisible();
    await productLink.click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/digital-slr-camera',
    );
    await expect(
      page.getByRole('heading', { name: productName, exact: true }),
    ).toBeVisible();

    await page.locator('#add-to-wishlist-button-18').click();

    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText(
      'The product has been added to your wishlist',
    );

    await page
      .getByRole('link', { name: 'Wishlist', exact: true })
      .click();

    await expect(page).toHaveURL(
      'https://demowebshop.tricentis.com/wishlist',
    );
    await expect(
      page.getByRole('heading', { name: 'Wishlist', exact: true }),
    ).toBeVisible();

    const wishlistItem = page.locator('.wishlist-content .cart-item-row').filter({
      has: page.getByRole('link', {
        name: productName,
        exact: true,
      }),
    });

    await expect(wishlistItem).toBeVisible();
    await expect(
      wishlistItem.getByRole('link', {
        name: productName,
        exact: true,
      }),
    ).toBeVisible();
  });
});
