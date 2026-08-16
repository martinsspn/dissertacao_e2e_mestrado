import { test, expect } from '../../../../runtime/playwright/fixture.ts';

test.describe('Suite Cadastro Confirmacao Senha', () => {
  test('Deve exibir erro ao tentar cadastrar com senhas divergentes', async ({ page }) => {
    // 1. The user accesses the Register page.
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Register", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // 2. The user fills in First name and Last name with valid data and Email with a unique address generated for this execution.
    const uniqueEmail = `user_${Date.now()}@example.com`;
    await page.getByLabel("First name:", { exact: true }).fill('FirstName');
    await page.getByLabel("Last name:", { exact: true }).fill('LastName');
    await page.getByLabel("Email:", { exact: true }).fill(uniqueEmail);

    // 3. The user fills in Password with a valid password and Confirm password with a different value.
    await page.getByLabel("Password:", { exact: true }).fill('Password123!');
    await page.getByLabel("Confirm password:", { exact: true }).fill('Different123!');

    // 4. The user submits the form using the Register button.
    await page.locator("[id=\"register-button\"]").click();

    // 5. The system does not register the user and informs that the password and confirmation password do not match.
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
    await expect(page.getByText('The password and confirmation password do not match.')).toBeVisible();
  });
});
