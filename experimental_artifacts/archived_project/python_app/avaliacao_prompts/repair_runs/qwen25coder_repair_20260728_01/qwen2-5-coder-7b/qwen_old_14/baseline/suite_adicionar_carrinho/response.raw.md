```typescript
import { test, expect } from '@playwright/test';

test.describe('Adding a product to the cart', () => {
  test('should add Blue Jeans to the cart and display it in the shopping cart', async ({ page }) => {
    // Step 1: Search for the product "Blue Jeans"
    await page.goto('https://demowebshop.tricentis.com');
    await page.fill('[data-test="search-input"]', 'Blue Jeans');
    await page.click('[data-test="search-button"]');
    
    // Step 2: Open the product "Blue Jeans" in search results
    const blueJeansLink = await page.locator('a[href*="/productdetails/1"]').first();
    await blueJeansLink.click();

    // Step 3: Select Add to cart on the product page
    await page.click('[data-test="add-to-cart-button"]');
    
    // Step 4: System informs that the product has been added to the cart
    const addToCartConfirmation = await page.locator('[data-test="cart-confirmation"]').textContent();
    expect(addToCartConfirmation).toContain('Blue Jeans has been added to your cart');

    // Step 5: Access Shopping cart
    await page.click('[data-test="shopping-cart-link"]');
    
    // Step 6: System displays Blue Jeans among the items in the cart
    const cartItems = await page.locator('[data-test="cart-item"]').allTextContents();
    expect(cartItems).toContain('Blue Jeans');
  });
});
```