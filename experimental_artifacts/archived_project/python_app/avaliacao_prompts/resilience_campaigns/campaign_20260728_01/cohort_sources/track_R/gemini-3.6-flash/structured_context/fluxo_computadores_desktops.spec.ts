import { test, expect } from '@playwright/test';

test.describe('Fluxo Computadores Desktops', () => {
  test('The user accesses the Digital downloads category and validates page visibility', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    await page.getByText("Digital downloads", { exact: true }).first().click();

    await expect(page).toHaveURL('https://demowebshop.tricentis.com/digital-downloads');
    await expect(page.getByRole('heading', { name: 'Digital downloads', exact: true })).toBeVisible();
    await expect(page.locator('.product-grid')).toBeVisible();
    await expect(page.locator('.product-item').first()).toBeVisible();
  });
});
