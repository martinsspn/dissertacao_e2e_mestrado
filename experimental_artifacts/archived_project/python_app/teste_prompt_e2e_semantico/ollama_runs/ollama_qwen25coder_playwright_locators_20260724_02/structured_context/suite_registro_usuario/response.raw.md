```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Registro Usuario', () => {
  test('should register a user and continue shopping', async ({ page }) => {
    // Etapa 1: Acessa a página de registro
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Register", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Seleciona uma opção de gênero (presumindo que seja o primeiro disponível)
    await page.locator('[name="Gender"]').nth(0).check();

    // Etapa 3: Preenche os campos de nome e sobrenome
    const firstName = 'John';
    const lastName = 'Doe';
    await page.getByLabel("First name:", { exact: true }).fill(firstName);
    await page.getByLabel("Last name:", { exact: true }).fill(lastName);

    // Etapa 4: Preenche o campo de e-mail com um endereço único
    const email = `user${Date.now()}@example.com`;
    await page.getByLabel("Email:", { exact: true }).fill(email);

    // Etapa 5: Preenche os campos de senha e confirmação de senha
    const password = 'P@ssw0rd!';
    await page.getByLabel("Password:", { exact: true }).fill(password);
    await page.getByLabel("Confirm password:", { exact: true }).fill(password);

    // Etapa 6: Submite o formulário
    await page.locator("[id=\"register-button\"]").click();

    // Etapa 7: Confirma que a registro foi concluído (presumindo uma mensagem de sucesso)
    expect(page).toHaveURL('https://demowebshop.tricentis.com/registerresult');
    await expect(page.getByText("Your registration completed")).toBeVisible();

    // Etapa 8: Seleciona Continue e retorna à loja autenticada
    await page.getByRole('button', { name: 'Continue' }).click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');
  });
});
```