import { test, expect } from '@playwright/test';

test.describe('Add a product to the wishlist', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming there's a fixture for authentication with valid credentials
    await page.goto('/login');
    await page.fill('#username', 'validUsername');
    await page.fill('#password', 'validPassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('should add product to wishlist and display it', async ({ page }) => {
    // Search for Camera
    await page.fill('#search-input', 'Camera');
    await page.keyboard.press('Enter');

    // Open a Camera product
    const cameraProduct = page.locator('.product-item:has-text("Camera")');
    await cameraProduct.click();
    await expect(page).toHaveURL(/\/products\/\d+/);

    // Add to wishlist
    await page.click('#add-to-wishlist-button');
    await expect(page.locator('#wishlist-notification')).toContainText('Product added to wishlist');

    // Access Wishlist
    await page.goto('/wishlist');
    await expect(page).toHaveURL('/wishlist');

    // Verify Camera product is in the wishlist
    const wishlistItem = page.locator('.wishlist-item:has-text("Camera")');
    await expect(wishlistItem).toBeVisible();
  });
});
