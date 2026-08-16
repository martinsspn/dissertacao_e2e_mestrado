import { test, expect } from '@playwright/test';

test.describe('Desktop Configuration Test', () => {
  test('should configure and add a desktop to the cart', async ({ page }) => {
    // Access Computers and open the Desktops category
    await page.goto('/computers');
    await page.click('text=Desktops');

    // Open a desktop that allows choosing its configuration
    await page.click('text=Configure this desktop');

    // Select options for Fast processor, 4 GB memory, 400 GB disk, and Office Suite software
    await page.selectOption('#processor', 'Fast');
    await page.fill('#memory', '4GB');
    await page.fill('#disk', '400GB');
    await page.click('text=Office Suite');

    // Select Add to cart
    await page.click('text=Add to cart');

    // System informs that the product has been added to the cart
    await expect(page.locator('.cart-notification')).toContainText('Product added to cart');

    // Access Shopping cart
    await page.click('text=Shopping cart');

    // System displays the configured desktop among the items in the cart
    await expect(page.locator('.cart-item')).toContainText('Configured Desktop');
  });
});
