import { test, expect } from '@playwright/test';

test('User Registration and Book Purchase Flow', async ({ page }) => {
  const email = process.env.TEST_EMAIL || `testuser_${Date.now()}@example.com`;
  const password = process.env.TEST_PASSWORD || 'Password123!';
  const firstName = process.env.TEST_FIRST_NAME || 'John';
  const lastName = process.env.TEST_LAST_NAME || 'Doe';

  // Step 1: Access the Demo Web Shop website
  await page.goto('https://demowebshop.tricentis.com/');
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/');

  // Step 2: Click on the Register link
  await page.getByText("Register", { exact: true }).first().click();
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

  // Step 3: System displays the registration form
  await expect(page.getByRole('heading', { name: 'Register' })).toBeVisible();

  // Step 4: Fill in the email field
  await page.getByLabel("Email:", { exact: true }).fill(email);

  // Step 5: Fill in the password field
  await page.getByLabel("Password:", { exact: true }).fill(password);

  // Step 6: Confirm the password
  await page.getByLabel("Confirm password:", { exact: true }).fill(password);

  // Step 7: Fill in the First Name field
  await page.getByLabel("First name:", { exact: true }).fill(firstName);

  // Step 8: Fill in the Last Name field
  await page.getByLabel("Last name:", { exact: true }).fill(lastName);

  // Step 9: Click on the Register button
  await page.locator("[id=\"register-button\"]").click();

  // Steps 10-12: System validates registration and user remains logged in
  await expect(page.getByText('Your registration completed')).toBeVisible();
  await expect(page.getByText(email, { exact: false })).toBeVisible();

  // Step 13: Click on the Books menu
  await page.getByText("Books", { exact: true }).first().click();

  // Step 14: System displays catalog page of available books
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/books');
  await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

  // Step 15: Locate and click on Health Book
  await page.getByText("Health Book", { exact: true }).first().click();

  // Step 16: System displays product page with description and purchase options
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/health');
  await expect(page.getByRole('heading', { name: 'Health Book' })).toBeVisible();

  // Step 17: Click on Add to cart button
  await page.locator("[id=\"add-to-cart-button-22\"]").click();

  // Step 18: Confirm success notification
  await expect(page.locator('#bar-notification')).toBeVisible();

  // Step 19: Navigate to shopping cart
  await page.getByRole("link", { name: "Shopping cart", exact: true }).click();

  // Steps 20-21: System displays cart containing Health Book and verify inclusion
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/cart');
  await expect(page.getByRole('heading', { name: 'Shopping cart' })).toBeVisible();
  await expect(page.locator('.shopping-cart-page')).toContainText('Health Book');
});
