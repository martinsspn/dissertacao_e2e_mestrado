import { test, expect } from '@playwright/test';

test('Cadastro com senha curta deve exibir mensagem de erro', async ({ page }) => {
  // 1. Access the Register page
  await page.goto('https://demowebshop.tricentis.com/');
  await page.getByText("Register", { exact: true }).first().click();
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

  // 2. Fill in First name, Last name and unique Email
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  await page.getByLabel("First name:", { exact: true }).fill('John');
  await page.getByLabel("Last name:", { exact: true }).fill('Doe');
  await page.getByLabel("Email:", { exact: true }).fill(uniqueEmail);

  // 3. Fill Password and Confirm password with fewer than 6 characters
  await page.getByLabel("Password:", { exact: true }).fill('12345');
  await page.getByLabel("Confirm password:", { exact: true }).fill('12345');

  // 4. Submit form using the Register button
  await page.locator("[id=\"register-button\"]").click();

  // 5. Verify system does not register user and displays validation error for short password
  await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
  const validationError = page.locator('.field-validation-error');
  await expect(validationError).toBeVisible();
  await expect(validationError).toContainText('6 characters');
});
