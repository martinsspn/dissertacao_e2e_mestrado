```typescript
import { test, expect } from '@playwright/test';

function requireEnvironmentVariable(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`The environment variable ${name} is required.`);
  }

  return value;
}

test('Removal of all products from the wishlist', async ({ page }) => {
  const email = requireEnvironmentVariable('DEMO_WEB_SHOP_EMAIL');
  const password = requireEnvironmentVariable('DEMO_WEB_SHOP_PASSWORD');

  await page.goto('https://demowebshop.tricentis.com/');

  await page.getByRole('link', { name: 'Log in', exact: true }).click();

  await page.locator('#Email').fill(email);
  await page.locator('#Password').fill(password);
  await page.locator('input.login-button').click();

  await expect(
    page.getByRole('link', { name: email, exact: true }),
  ).toBeVisible();

  const searchField = page.locator('#small-searchterms');
  await expect(searchField).toBeVisible();
  await searchField.fill('Camera');

  await page.locator('input.search-box-button').click();

  const cameraProduct = page.locator('.product-item').filter({
    has: page.getByRole('link', {
      name: 'Digital SLR Camera 12.2 Mpixel',
      exact: true,
    }),
  });

  await expect(cameraProduct).toBeVisible();

  await cameraProduct
    .getByRole('link', {
      name: 'Digital SLR Camera 12.2 Mpixel',
      exact: true,
    })
    .click();

  await expect(
    page.getByRole('heading', {
      name: 'Digital SLR Camera 12.2 Mpixel',
      exact: true,
    }),
  ).toBeVisible();

  await page.locator('input[value="Add to wishlist"]').click();

  const successNotification = page.locator('#bar-notification');
  await expect(successNotification).toBeVisible();
  await expect(successNotification).toContainText(
    'The product has been added to your wishlist',
  );

  await page
    .getByRole('link', {
      name: /Wishlist/,
    })
    .first()
    .click();

  const cameraWishlistItem = page.locator('.cart-item-row').filter({
    has: page.getByRole('link', {
      name: 'Digital SLR Camera 12.2 Mpixel',
      exact: true,
    }),
  });

  await expect(cameraWishlistItem).toBeVisible();

  await cameraWishlistItem
    .locator('input[name^="removefromcart"]')
    .check();

  await page.locator('input[name="updatecart"]').click();

  await expect(
    page.getByText('The wishlist is empty!', {
      exact: true,
    }),
  ).toBeVisible();
});
```