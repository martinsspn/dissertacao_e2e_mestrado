```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Book Purchase', () => {
  test('should register user and purchase book', async ({ page }) => {
    // Step 1: Access the Demo Web Shop website
    await page.goto('https://demowebshop.tricentis.com/');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Step 2: Click on the Register link to access the registration page
    await page.getByText("Register", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
    expect(page.locator('h1')).toContainText('Register');

    // Step 4: Fill in the email field with a valid email
    await page.getByLabel("Email:", { exact: true }).fill('test@example.com');

    // Step 5: Fill in the password field with a secure password
    await page.getByLabel("Password:", { exact: true }).fill('P@ssw0rd!');

    // Step 6: Confirm the password by typing it again
    await page.getByLabel("Confirm password:", { exact: true }).fill('P@ssw0rd!');

    // Step 7: Fill in the First Name field with their first name
    await page.getByLabel("First name:", { exact: true }).fill('John');

    // Step 8: Fill in the Last Name field with their last name
    await page.getByLabel("Last name:", { exact: true }).fill('Doe');

    // Step 9: Click on the Register button to complete the registration
    await page.locator("[id=\"register-button\"]").click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Step 13: Click on the Books menu or link to access the book list
    await page.getByText("Books", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
    expect(page.locator('h1')).toContainText('Books');

    // Step 15: Locate and click on the book Health Book to open its details page
    await page.getByText("Health Book", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/health');
    expect(page.locator('h1')).toContainText('Health Book');

    // Step 17: Click on the Add to cart button to add the book to the cart
    await page.locator("[id=\"add-to-cart-button-22\"]").click();
    expect(page.locator('.content')).toContainText('The product has been added to your shopping cart');

    // Step 19: Navigate to the shopping cart to check the added item
    await page.getByRole("link", { name: "Shopping cart", exact: true }).click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
    expect(page.locator('h1')).toContainText('Shopping cart');

    // Step 20: The system displays the cart containing the book Health Book with quantity and price
    expect(page.locator('.cart-item-name')).toContainText('Health Book');
  });
});
```