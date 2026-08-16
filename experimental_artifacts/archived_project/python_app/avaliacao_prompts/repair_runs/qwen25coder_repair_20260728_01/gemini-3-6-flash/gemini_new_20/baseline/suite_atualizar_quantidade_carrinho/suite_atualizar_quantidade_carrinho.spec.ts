import { test, expect } from '@playwright/test';

test.describe('Shopping Cart Quantity Update', () => {
  test('should update product quantity in cart and reflect correct subtotal', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com';

    // Navigate to the store
    await page.goto(baseUrl);

    // Search for "Computing and Internet"
    const searchInput = page.getByPlaceholder('Search store');
    await searchInput.fill('Computing and Internet');
    await page.keyboard.press('Enter');

    // Open the product page
    await page.locator('.product-box a').first().click();

    // Add product to cart to prepare scenario
    const addToCartButton = page.getByRole('button', { name: 'Add to cart' }).first();
    await addToCartButton.click();

    // Wait for the notification bar confirming addition
    const notification = page.locator('.bar-notification.success');
    await expect(notification).toBeVisible();

    // Access Shopping cart
    await page.getByRole('link', { name: 'Shopping cart', exact: false }).first().click();
    await expect(page).toHaveURL(/.*cart/);

    // Locate the row for "Computing and Internet"
    const cartRow = page.locator('tr').filter({ hasText: 'Computing and Internet' });
    await expect(cartRow).toBeVisible();

    // Change the quantity from one to two
    const qtyInput = cartRow.locator('input.qty-input, input[name^="itemquantity"]').first();
    await qtyInput.fill('2');

    // Select "Update shopping cart"
    const updateCartBtn = page.getByRole('button', { name: 'Update shopping cart' })
      .or(page.getByRole('button', { name: 'Update cart' }));
    await updateCartBtn.first().click();

    // Verify product quantity remains two
    await expect(qtyInput).toHaveValue('2');

    // Read unit price and subtotal elements to assert mathematical consistency
    const unitPriceElement = cartRow.locator('.product-unit-price, .unit-price').first();
    const subtotalElement = cartRow.locator('.product-subtotal, .subtotal').first();

    await expect(unitPriceElement).toBeVisible();
    await expect(subtotalElement).toBeVisible();

    const unitPriceText = await unitPriceElement.innerText();
    const subtotalText = await subtotalElement.innerText();

    const parsePrice = (priceStr: string) => {
      const match = priceStr.replace(/[^0-9.]/g, '');
      return parseFloat(match);
    };

    const unitPrice = parsePrice(unitPriceText);
    const subtotal = parsePrice(subtotalText);

    expect(unitPrice).toBeGreaterThan(0);
    expect(subtotal).toBeCloseTo(unitPrice * 2, 2);
  });
});
