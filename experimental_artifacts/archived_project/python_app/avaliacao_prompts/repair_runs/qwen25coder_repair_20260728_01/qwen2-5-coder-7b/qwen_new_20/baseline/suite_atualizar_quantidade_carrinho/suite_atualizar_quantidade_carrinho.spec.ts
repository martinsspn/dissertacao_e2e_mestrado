import { test, expect } from '@playwright/test';

test.describe('Updating a product quantity in the cart', () => {
  test('should update the quantity of Computing and Internet to two and keep it in the cart', async ({ page }) => {
    // Add Computing and Internet to the cart
    await page.goto('/products');
    await page.click('text=Computing and Internet');
    await page.click('button=add-to-cart');

    // Access Shopping cart
    await page.click('text=Shopping Cart');

    // Change the quantity of Computing and Internet from one to two
    const input = page.locator('input[name="quantity"]');
    await input.clear();
    await input.fill('2');

    // Select Update shopping cart
    await page.click('button=Update shopping cart');

    // Verify that the product is in the cart with quantity two
    const productQuantity = await page.textContent('text=Computing and Internet');
    expect(productQuantity).toContain('x 2');

    // Verify that the subtotal is updated consistently with the displayed unit price
    const subtotal = await page.textContent('text=Subtotal');
    expect(subtotal).toContain('$10.00'); // Assuming the unit price is $5.00 and quantity is now 2
  });
});
