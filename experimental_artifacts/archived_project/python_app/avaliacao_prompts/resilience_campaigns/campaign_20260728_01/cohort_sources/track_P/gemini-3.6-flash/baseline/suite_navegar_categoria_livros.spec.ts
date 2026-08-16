import { test, expect } from '@playwright/test';

test.describe('Browsing the Books category', () => {
  test('user can navigate to Books category and view available book products', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com/';

    // Access the Demo Web Shop home page
    await page.goto(baseUrl);

    // Select Books in the main category menu
    const booksCategoryLink = page.locator('.top-menu').getByRole('link', { name: 'Books', exact: true });
    await expect(booksCategoryLink).toBeVisible();
    await booksCategoryLink.click();

    // Verify navigation to Books category page
    await expect(page).toHaveURL(/.*\/books/);
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

    // Verify breadcrumb displays navigation hierarchy
    const breadcrumb = page.locator('.breadcrumb');
    await expect(breadcrumb).toBeVisible();
    await expect(breadcrumb).toContainText('Books');

    // Verify available book products are displayed
    const computingAndInternetProduct = page.getByRole('link', { name: 'Computing and Internet', exact: true });
    const fictionProduct = page.getByRole('link', { name: 'Fiction', exact: true });
    const healthBookProduct = page.getByRole('link', { name: 'Health Book', exact: true });

    await expect(computingAndInternetProduct.first()).toBeVisible();
    await expect(fictionProduct.first()).toBeVisible();
    await expect(healthBookProduct.first()).toBeVisible();
  });
});
