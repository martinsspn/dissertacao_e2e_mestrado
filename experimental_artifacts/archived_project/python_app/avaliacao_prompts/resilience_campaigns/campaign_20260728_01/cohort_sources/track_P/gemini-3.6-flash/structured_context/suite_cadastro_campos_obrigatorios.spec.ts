import { test, expect } from '@playwright/test';

test.describe('Suite Cadastro Campos Obrigatorios', () => {
  test('Deve validar mensagens de erro ao submeter formulario de cadastro com campos obrigatorios vazios', async ({ page }) => {
    // Etapa 1: Acesse a pagina de registro do Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Register", { exact: true }).first().click();
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Garantir que os campos obrigatorios fiquem vazios
    await page.getByLabel("First name:", { exact: true }).clear();
    await page.getByLabel("Last name:", { exact: true }).clear();
    await page.getByLabel("Email:", { exact: true }).clear();
    await page.getByLabel("Password:", { exact: true }).clear();

    // Etapa 3: Submeter o formulario com o botao Register
    await page.locator("[id=\"register-button\"]").click();

    // Etapa 4: Verificar que o cadastro nao e concluido e as 5 mensagens de validacao sao exibidas
    await expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
    await expect(page.locator('.field-validation-error')).toHaveCount(5);
    await expect(page.getByText('First name is required.', { exact: true })).toBeVisible();
    await expect(page.getByText('Last name is required.', { exact: true })).toBeVisible();
    await expect(page.getByText('Email is required.', { exact: true })).toBeVisible();
    await expect(page.getByText('Password is required.', { exact: true }).first()).toBeVisible();
  });
});
