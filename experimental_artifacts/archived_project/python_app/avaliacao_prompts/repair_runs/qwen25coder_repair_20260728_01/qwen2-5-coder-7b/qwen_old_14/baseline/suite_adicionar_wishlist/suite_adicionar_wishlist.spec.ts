import { test, expect } from '@playwright/test';

test.describe('Add a product to the wishlist', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming there's a fixture for authentication with valid credentials
    await page.goto('https://demowebshop.tricentis.com/login');
    await page.fill('#Email', process.env.DEMO_WEB_SHOP_USERNAME);
    await page.fill('#Password', process.env.DEMO_WEB_SHOP_PASSWORD);
    await page.click('input[type="submit"]');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/');
  });

  test('should add product to wishlist and display it', async ({ page }) => {
    // Search for Camera
    await page.fill('#small-search-box', 'Camera');
    await page.keyboard.press('Enter');

    // Open a Camera product
    const cameraProduct = page.locator('.product-item:has-text("Camera")');
    await cameraProduct.click();
    await expect(page).toHaveURL(/\/products\/\d+/);

    // Add to wishlist
    await page.click('#add-to-wishlist-button');
    await expect(page.locator('#bar-notification')).toContainText('The product has been added to your wishlist');

    // Access Wishlist
    await page.goto('/wishlist');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');

    // Verify Camera product is in the wishlist
    const wishlistItem = page.locator('.product-item:has-text("Camera")');
    await expect(wishlistItem).toBeVisible();
  });
});
