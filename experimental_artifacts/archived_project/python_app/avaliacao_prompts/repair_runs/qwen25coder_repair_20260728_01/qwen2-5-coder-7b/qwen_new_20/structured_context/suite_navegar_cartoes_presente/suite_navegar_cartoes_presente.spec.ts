import { test, expect } from '@playwright/test';

test.describe('Suite Navegar Cartoes Presente', () => {
  test('The user accesses the Demo Web Shop home page', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');
    await expect(page).toHaveTitle('Demo Web Shop');
  });

  test('The user selects Gift Cards in the main category menu', async ({ page }) => {
    await page.getByText("Gift Cards", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/gift-cards');
  });

  test('The system displays the Gift Cards category page, its breadcrumb, and the available gift card products', async ({ page }) => {
    await expect(page.locator('h1')).toHaveText('Gift Cards');
  });
});
