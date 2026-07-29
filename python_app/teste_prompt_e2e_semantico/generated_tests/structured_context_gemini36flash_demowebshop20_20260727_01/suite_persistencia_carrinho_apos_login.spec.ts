import { test, expect } from '@playwright/test';

test('Suite Persistencia Carrinho Apos Login', async ({ page }) => {
  const email = process.env.E2E_EMAIL || 'test@example.com';
  const password = process.env.E2E_PASSWORD || 'Password123';

  // 1. The user accesses the application and authenticates
  await page.goto('https://demowebshop.tricentis.com/');

  const loginLink = page.getByText("Log in", { exact: true }).first();
  if (await loginLink.isVisible()) {
    await loginLink.click();
    await page.getByLabel('Email:', { exact: true }).fill(email);
    await page.getByLabel('Password:', { exact: true }).fill(password);
    await page.getByRole('button', { name: 'Log in' }).click();
  }

  // 2. Ensure cart does not contain Computing and Internet and then add that product
  await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();

  const existingProduct = page.getByRole('link', { name: 'Computing and Internet', exact: true });
  if (await existingProduct.isVisible()) {
    const row = page.locator('tr').filter({ hasText: 'Computing and Internet' });
    await row.getByRole('checkbox').check();
    await page.getByRole('button', { name: 'Update shopping cart' }).click();
  }

  await page.getByRole('link', { name: 'Books' }).first().click();
  const productCard = page.locator('.product-item').filter({ hasText: 'Computing and Internet' });
  await productCard.getByRole('button', { name: 'Add to cart' }).click();
  await expect(page.getByText('The product has been added to your shopping cart')).toBeVisible();

  // 3. Log out and log in again with the same account
  await page.getByRole('link', { name: 'Log out' }).click();
  await page.getByText("Log in", { exact: true }).first().click();
  await page.getByLabel('Email:', { exact: true }).fill(email);
  await page.getByLabel('Password:', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Log in' }).click();

  // 4. Access Shopping cart
  await page.getByRole("link", { name: "Shopping cart", exact: true }).click();

  // 5. System still displays Computing and Internet in the cart
  await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Computing and Internet', exact: true })).toBeVisible();

  // 6. At the end, remove the product to restore account state
  const cartRow = page.locator('tr').filter({ hasText: 'Computing and Internet' });
  await cartRow.getByRole('checkbox').check();
  await page.getByRole('button', { name: 'Update shopping cart' }).click();
  await expect(page.getByRole('link', { name: 'Computing and Internet', exact: true })).not.toBeVisible();
});
