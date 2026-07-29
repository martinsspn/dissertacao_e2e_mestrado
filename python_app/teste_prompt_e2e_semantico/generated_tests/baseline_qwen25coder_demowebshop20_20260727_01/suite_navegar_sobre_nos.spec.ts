import { test, expect } from '@playwright/test';

test.describe('Institutional Information Page', () => {
  test('should display the About us page and its corresponding heading', async ({ page }) => {
    // Access the Demo Web Shop home page
    await page.goto('https://demo.webshopapp.com');

    // Select About us in the Information section of the footer
    await page.click('footer a:has-text("Information")');
    await page.click('a:has-text("About us")');

    // Verify that the About us page is displayed
    expect(page.url()).toContain('/about-us');

    // Verify that the corresponding heading is displayed
    const heading = await page.locator('h1').textContent();
    expect(heading).toBe('About Us');
  });
});
