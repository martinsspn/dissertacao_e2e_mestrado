import { test, expect } from '../../../../runtime/playwright/fixture.ts';

test.describe('Institutional Information', () => {
  test('User opens the About us page from footer', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // 1. Access the Demo Web Shop home page
    await page.goto(baseUrl);

    // 2. In the Information section of the footer, select About us
    const footer = page.locator('.footer');
    const aboutUsLink = footer.getByRole('link', { name: 'About us' });
    await expect(aboutUsLink).toBeVisible();
    await aboutUsLink.click();

    // 3. Verify the About us page and heading are displayed
    await expect(page).toHaveURL(/.*about-us/);
    const heading = page.getByRole('heading', { name: 'About us' });
    await expect(heading).toBeVisible();
  });
});
