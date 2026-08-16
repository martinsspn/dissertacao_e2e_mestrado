```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Cadastro Senha Curta', () => {
  test('should not register user with short password', async ({ page }) => {
    // Etapa 1: Acessa a página de Registro
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Register", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Preenche os campos de nome, sobrenome e email
    const firstName = 'John';
    const lastName = 'Doe';
    const email = `test${Date.now()}@example.com`;
    await page.getByLabel("First name:", { exact: true }).fill(firstName);
    await page.getByLabel("Last name:", { exact: true }).fill(lastName);
    await page.getByLabel("Email:", { exact: true }).fill(email);

    // Etapa 3: Preenche os campos de senha e confirmação com uma senha curta
    const shortPassword = '123';
    await page.getByLabel("Password:", { exact: true }).fill(shortPassword);
    await page.getByLabel("Confirm password:", { exact: true }).fill(shortPassword);

    // Etapa 4: Submite o formulário
    await page.locator("[id=\"register-button\"]").click();

    // Verifica se a mensagem de erro é exibida
    const errorMessage = 'Password must have at least six characters';
    expect(page).toHaveText(errorMessage);
  });
});
```