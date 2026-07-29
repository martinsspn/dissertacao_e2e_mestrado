import { test, expect } from '@playwright/test';

test.describe('Suite Cadastro Confirmacao Senha', () => {
  test('should not register user with mismatched passwords', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Acessa a página de Registro
    await page.getByText("Register", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Preenche os campos do formulário
    const firstName = 'John';
    const lastName = 'Doe';
    const email = `test${Date.now()}@example.com`;
    await page.getByLabel("First name:", { exact: true }).fill(firstName);
    await page.getByLabel("Last name:", { exact: true }).fill(lastName);
    await page.getByLabel("Email:", { exact: true }).fill(email);

    // Etapa 3: Preenche os campos de senha
    const password = 'P@ssw0rd';
    const confirmPassword = 'DifferentPassword';
    await page.getByLabel("Password:", { exact: true }).fill(password);
    await page.getByLabel("Confirm password:", { exact: true }).fill(confirmPassword);

    // Etapa 4: Submite o formulário
    await page.locator("[id=\"register-button\"]").click();

    // Verifica se a mensagem de erro é exibida
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
    await expect(page.getByText("The specified passwords do not match.")).toBeVisible();
  });
});
