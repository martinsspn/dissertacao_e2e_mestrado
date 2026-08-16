```typescript
import { test, expect } from '@playwright/test';

test('Suite Cadastro Senha Curta', async ({ page }) => {
  // Etapa 1: Acessa a página de registro
  await page.goto('https://demowebshop.tricentis.com/');
  await page.getByText("Register", { exact: true }).first().click();
  
  // Verifica se está na página de registro
  expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

  // Etapa 2: Preenche os campos do formulário
  await page.getByLabel("First name:", { exact: true }).fill('John');
  await page.getByLabel("Last name:", { exact: true }).fill('Doe');
  await page.getByLabel("Email:", { exact: true }).fill('john.doe@example.com');

  // Etapa 3: Preenche os campos de senha com uma senha curta
  await page.getByLabel("Password:", { exact: true }).fill('123');
  await page.getByLabel("Confirm password:", { exact: true }).fill('123');

  // Etapa 4: Submite o formulário
  await page.locator("[id=\"register-button\"]").click();

  // Verifica se a mensagem de erro é exibida
  expect(page).toHaveText('Password must be at least six characters');
});
```