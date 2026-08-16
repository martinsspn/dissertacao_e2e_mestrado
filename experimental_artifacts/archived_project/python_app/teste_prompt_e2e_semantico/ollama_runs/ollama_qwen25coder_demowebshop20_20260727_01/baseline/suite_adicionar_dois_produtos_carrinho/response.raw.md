```typescript
import { test, expect } from '@playwright/test';

test.describe('Cart Test', () => {
  test('Adding two different products to the cart', async ({ page }) => {
    // Navigate to the store homepage
    await page.goto('https://examplestore.com');

    // Add Computing product to the cart
    await page.click('#computing-product');
    await page.click('#add-to-cart-computing');

    // Add Fiction product to the cart
    await page.click('#fiction-product');
    await page.click('#add-to-cart-fiction');

    // Access Shopping cart
    await page.click('#shopping-cart-link');

    // Verify both products are in the cart
    const computingItem = await page.locator('.cart-item', { hasText: 'Computing' });
    expect(computingItem).toBeVisible();
    const fictionItem = await page.locator('.cart-item', { hasText: 'Fiction' });
    expect(fictionItem).toBeVisible();

    // Verify quantity and price for each product
    const computingQuantity = await page.locator('.cart-quantity', { hasText: '1' }).textContent();
    expect(computingQuantity).toBe('1');
    const fictionPrice = await page.locator('.cart-price', { hasText: '$20.00' }).textContent();
    expect(fictionPrice).toBe('$20.00');

    // Optionally, verify total price
    const totalPrice = await page.locator('.total-price').textContent();
    expect(totalPrice).toBe('$40.00');
  });
});
```