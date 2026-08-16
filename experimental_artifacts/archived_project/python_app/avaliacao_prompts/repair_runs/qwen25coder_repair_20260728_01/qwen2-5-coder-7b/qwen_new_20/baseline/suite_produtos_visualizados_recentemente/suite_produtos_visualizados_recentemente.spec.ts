import { test, expect } from '@playwright/test';

test.describe('Product History', () => {
  test('displays recently viewed products in the correct order', async ({ page }) => {
    // Open a new browser context
    const context = await page.context();
    const newPage = await context.newPage();

    // Navigate to Fiction product page
    await newPage.goto('https://demowebshop.tricentis.com/fiction-product');

    // Navigate to Blue Jeans product page
    await newPage.goto('https://demowebshop.tricentis.com/blue-jeans-product');

    // Select Recently viewed products in the Customer service section
    await newPage.click('text=Customer Service');
    await newPage.click('text=Recently Viewed Products');

    // Check if both products are displayed
    const recentlyViewedProducts = await newPage.textContent('.recently-viewed-products');
    expect(recentlyViewedProducts).toContain('Blue Jeans');
    expect(recentlyViewedProducts).toContain('Fiction');

    // Verify the order of products
    const productOrder = await newPage.textContent('.product-order');
    expect(productOrder).toBe('Blue Jeans, Fiction');
  });
});
