import { test, expect } from '@playwright/test';

test.describe('Suite Limpar Wishlist', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');
    // Assume user is authenticated with valid credentials provided by the testing environment
  });

  test('should clear the wishlist', async ({ page }) => {
    // Step 3: The user accesses Wishlist
    await page.getByRole("link", { name: "Wishlist", exact: true }).click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');

    // Step 4: The user marks the Camera product for removal
    await page.getByText('Camera').getByRole("button", { name: "Remove from Wishlist" }).click();

    // Step 5: The user selects Update wishlist
    await page.getByRole("button", { name: "Update Wishlist" }).click();

    // Step 6: The system displays the empty wishlist
    await expect(page.locator('h1')).toHaveText('Wishlist');
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/wishlist');
  });
});
