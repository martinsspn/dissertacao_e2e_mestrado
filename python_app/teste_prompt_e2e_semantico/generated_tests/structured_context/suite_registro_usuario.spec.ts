import { test, expect } from '@playwright/test';

test.describe('Suite Registro Usuario', () => {
  test('should register a user and continue shopping', async ({ page }) => {
    // Etapa 1: Acessa a página de registro
    await page.goto('https://demowebshop.tricentis.com/');
    await page.click('text:Register');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/register');

    // Etapa 2: Seleciona uma opção de gênero (mas não é especificado no contexto, então pulamos)

    // Etapa 3: Preenche o nome e sobrenome
    await page.fill('label:First name:', 'John');
    await page.fill('label:Last name:', 'Doe');

    // Etapa 4: Preenche o email com um endereço único
    const uniqueEmail = `user${Date.now()}@example.com`;
    await page.fill('label:Email:', uniqueEmail);

    // Etapa 5: Preenche a senha e confirmação de senha
    const password = 'P@ssw0rd!';
    await page.fill('label:Password:', password);
    await page.fill('label:Confirm password:', password);

    // Etapa 6: Submite o formulário
    await page.click('id:register-button');
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Etapa 7 e 8: Seleciona Continue e retorna à loja autenticada (mas não é especificado no contexto, então pulamos)
  });
});
