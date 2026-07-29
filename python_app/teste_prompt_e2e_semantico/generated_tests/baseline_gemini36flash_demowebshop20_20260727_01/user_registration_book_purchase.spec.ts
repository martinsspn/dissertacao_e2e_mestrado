import { test, expect } from '@playwright/test';

test.describe('Book Purchase Flow (Registration + Cart)', () => {
  test('should register a new user, add Health Book to cart, and verify cart contents', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'https://demowebshop.tricentis.com/';
    const userPassword = process.env.USER_PASSWORD || process.env.TEST_USER_PASSWORD || 'SecurePassword123!';
    const uniqueEmail = `testuser_${Date.now()}@example.com`;

    // Step 1: Access the Demo Web Shop website
    await page.goto(baseUrl);

    // Step 2: Click on the Register link
    await page.getByRole('link', { name: 'Register' }).click();

    // Step 3: Verify the registration form is displayed
    await expect(page.getByRole('heading', { name: 'Register' })).toBeVisible();

    // Steps 4-8: Fill in the registration form fields
    await page.getByLabel('First name:').fill('John');
    await page.getByLabel('Last name:').fill('Doe');
    await page.getByLabel('Email:').fill(uniqueEmail);
    await page.getByLabel('Password:', { exact: true }).fill(userPassword);
    await page.getByLabel('Confirm password:').fill(userPassword);

    // Step 9: Click on the Register button
    await page.getByRole('button', { name: 'Register' }).click();

    // Step 10: Verify registration completed message and logged-in state
    await expect(page.getByText('Your registration completed')).toBeVisible();
    await expect(page.locator('.header-links')).toContainText(uniqueEmail);

    // Step 11: Continue to home page
    await page.getByRole('button', { name: 'Continue' }).click();

    // Steps 12-13: Access the Books category and display book catalog
    await page.locator('.top-menu').getByRole('link', { name: 'Books' }).first().click();
    await expect(page.getByRole('heading', { name: 'Books' })).toBeVisible();

    // Steps 14-15: Open details page for 'Health Book'
    await page.getByRole('link', { name: 'Health Book' }).first().click();
    await expect(page.getByRole('heading', { name: 'Health Book' })).toBeVisible();

    // Step 16: Click on Add to cart
    await page.getByRole('button', { name: 'Add to cart' }).click();

    // Step 17: Confirm success notification for adding to cart
    const notification = page.locator('#bar-notification');
    await expect(notification).toBeVisible();
    await expect(notification).toContainText('The product has been added to your shopping cart');

    // Step 18: Navigate to the shopping cart
    await page.getByRole('link', { name: 'Shopping cart' }).first().click();

    // Steps 19-20: Verify cart contains Health Book with details
    await expect(page).toHaveURL(/.*cart/);
    const cartTable = page.locator('.cart');
    await expect(cartTable).toContainText('Health Book');
    await expect(cartTable.getByRole('link', { name: 'Health Book' })).toBeVisible();
  });
});
