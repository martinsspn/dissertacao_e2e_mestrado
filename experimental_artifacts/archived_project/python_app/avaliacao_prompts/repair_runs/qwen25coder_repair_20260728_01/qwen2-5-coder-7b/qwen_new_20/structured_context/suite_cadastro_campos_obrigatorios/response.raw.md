```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Cadastro Campos Obrigatorios', () => {
  test('The user accesses the Register page of the Demo Web Shop and submits the form with empty fields', async ({ page }) => {
    // Etapa 1: Acessa a página de Registro
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Register", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Deixa os campos obrigatórios em branco
    await page.getByLabel("First name:", { exact: true }).fill('');
    await page.getByLabel("Last name:", { exact: true }).fill('');
    await page.getByLabel("Email:", { exact: true }).fill('');
    await page.getByLabel("Password:", { exact: true }).fill('');

    // Etapa 3: Submite o formulário
    await page.locator("[id=\"register-button\"]").click();

    // Verificações após a submissão do formulário
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');
    await expect(page.getByText("First name is required")).toBeVisible();
    await expect(page.getByText("Last name is required")).toBeVisible();
    await expect(page.getByText("Email is required")).toBeVisible();
    await expect(page.getByText("Password is required")).toBeVisible();
    await expect(page.getByText("Confirm password is required")).toBeVisible();
  });
});
```