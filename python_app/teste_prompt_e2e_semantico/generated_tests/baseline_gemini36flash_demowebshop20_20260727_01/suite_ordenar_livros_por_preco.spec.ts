import { test, expect } from '@playwright/test';

test.describe('Books Category - Price Sorting', () => {
  test('should display books sorted by ascending price when Price: Low to High is selected', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Access the homepage and navigate to Books category
    await page.goto(baseUrl);

    const booksCategoryLink = page.getByRole('link', { name: /^books$/i }).first();
    if (await booksCategoryLink.isVisible()) {
      await booksCategoryLink.click();
    } else {
      await page.goto(`${baseUrl}/books`);
    }

    // Verify the Books category heading is visible
    const categoryHeader = page.getByRole('heading', { name: /books/i }).first();
    await expect(categoryHeader).toBeVisible();

    // Select 'Price: Low to High' in the Sort by control
    const sortByDropdown = page.getByLabel(/sort by/i).first();
    await expect(sortByDropdown).toBeVisible();
    await sortByDropdown.selectOption({ label: 'Price: Low to High' });

    // Verify the Books category header remains visible after sorting
    await expect(categoryHeader).toBeVisible();

    // Retrieve product prices
    const priceElements = page.locator('.actual-price, .product-price, .price');
    await expect(priceElements.first()).toBeVisible();

    const priceTexts = await priceElements.allInnerTexts();
    const prices = priceTexts
      .map(text => {
        const cleanText = text.replace(/[^0-9.]/g, '');
        return parseFloat(cleanText);
      })
      .filter(val => !isNaN(val));

    expect(prices.length).toBeGreaterThan(1);

    // Verify prices are in nondecreasing order
    for (let i = 0; i < prices.length - 1; i++) {
      expect(prices[i]).toBeLessThanOrEqual(prices[i + 1]);
    }
  });
});
