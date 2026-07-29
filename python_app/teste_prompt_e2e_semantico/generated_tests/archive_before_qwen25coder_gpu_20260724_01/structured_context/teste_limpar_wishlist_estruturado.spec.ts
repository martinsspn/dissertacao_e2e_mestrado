import { test, expect } from '@playwright/test';

const email = process.env.DEMO_WEB_SHOP_EMAIL;
const password = process.env.DEMO_WEB_SHOP_PASSWORD;

test.describe('Suite Limpar Wishlist', () => {
  test('remove o produto Camera e exibe a wishlist vazia', async ({ page }) => {
    test.skip(
      !email || !password,
      'Defina DEMO_WEB_SHOP_EMAIL e DEMO_WEB_SHOP_PASSWORD com credenciais válidas.',
    );

    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByRole('link', { name: 'Log in', exact: true }).click();
    await page.locator('#Email').fill(email!);
    await page.locator('#Password').fill(password!);
    await page.getByRole('button', { name: 'Log in', exact: true }).click();

    await expect(
      page.getByRole('link', { name: email!, exact: true }),
    ).toBeVisible();

    await page.locator('#small-searchterms').fill('Camera');
    await page.getByRole('button', { name: 'Search', exact: true }).click();

    const cameraProductLink = page
      .locator('h2.product-title')
      .getByRole('link')
      .filter({ hasText: 'Camera' });

    await expect(cameraProductLink).toHaveCount(1);
    await expect(cameraProductLink).toBeVisible();

    const cameraProductName = (
      await cameraProductLink.textContent()
    )?.trim();

    expect(cameraProductName).toBeTruthy();

    await cameraProductLink.click();

    await expect(
      page.getByRole('heading', {
        name: cameraProductName!,
        exact: true,
      }),
    ).toBeVisible();

    await page
      .getByRole('button', { name: 'Add to wishlist', exact: true })
      .click();

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

    const cameraWishlistItem = page
      .locator('tr.cart-item-row')
      .filter({
        has: page.getByRole('link', {
          name: cameraProductName!,
          exact: true,
        }),
      });

    await expect(cameraWishlistItem).toBeVisible();

    const removeCheckbox = cameraWishlistItem.locator(
      'input[type="checkbox"][name="removefromcart"]',
    );

    await removeCheckbox.check();
    await expect(removeCheckbox).toBeChecked();

    await page
      .getByRole('button', {
        name: 'Update wishlist',
        exact: true,
      })
      .click();

    await expect(
      page.getByText('The wishlist is empty!', { exact: true }),
    ).toBeVisible();

    await expect(cameraWishlistItem).toHaveCount(0);
  });
});
