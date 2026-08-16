import { test, expect } from '@playwright/test';

test.describe('Gift Cards Category Navigation', () => {
  test('should navigate to Gift Cards category and display breadcrumb and products', async ({ page }) => {
    // Access the Demo Web Shop home page
    await page.goto('https://demowebshop.tricentis.com/');

    // Select Gift Cards from the main top category menu
    const topMenu = page.locator('.top-menu');
    const giftCardsLink = topMenu.getByRole('link', { name: 'Gift Cards', exact: true });
    await giftCardsLink.click();

    // Verify URL reflects the Gift Cards category page
    await expect(page).toHaveURL(/.*\/gift-cards/);

    // Verify page heading
    const pageHeading = page.getByRole('heading', { name: 'Gift Cards', level: 1 });
    await expect(pageHeading).toBeVisible();

    // Verify breadcrumb navigation
    const breadcrumb = page.locator('.breadcrumb');
    await expect(breadcrumb).toBeVisible();
    await expect(breadcrumb).toContainText('Gift Cards');

    // Verify available gift card products are displayed
    const productItems = page.locator('.product-grid .item-box');
    await expect(productItems.first()).toBeVisible();
    const itemCount = await productItems.count();
    expect(itemCount).toBeGreaterThan(0);
  });
});
