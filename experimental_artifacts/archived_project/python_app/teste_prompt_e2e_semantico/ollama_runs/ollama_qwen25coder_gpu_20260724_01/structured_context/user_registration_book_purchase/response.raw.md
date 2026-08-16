```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Book Purchase', () => {
  test('should register user and purchase book', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Step 2: Click on the Register link
    await page.click('tag=a, text=Register, href=/register');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Step 4: Fill in the email field
    await page.fill('label:Email:', 'testuser@example.com');

    // Step 5: Fill in the password field
    await page.fill('label:Password:', 'P@ssw0rd!');

    // Step 6: Confirm the password
    await page.fill('label:Confirm password:', 'P@ssw0rd!');

    // Step 7: Fill in the First Name field
    await page.fill('label:First name:', 'John');

    // Step 8: Fill in the Last Name field
    await page.fill('label:Last name:', 'Doe');

    // Step 9: Click on the Register button
    await page.click('id=register-button');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Step 13: Click on the Books menu
    await page.click('tag=a, text=Books, href=/books');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/books');

    // Step 15: Click on the Health Book
    await page.click('tag=a, text=Health Book, href=/health');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/health');

    // Step 17: Add to cart
    await page.click('id:add-to-cart-button-22');
    expect(page.locator('#bar-notification').textContent()).toContain('The product has been added to your shopping cart');

    // Step 19: Navigate to the shopping cart
    await page.click('page.getByRole("link", { name: "Shopping cart", exact: true })');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');

    // Step 20: Verify the added item
    expect(page.locator('#cart-item-22').textContent()).toContain('Health Book');
  });
});
```