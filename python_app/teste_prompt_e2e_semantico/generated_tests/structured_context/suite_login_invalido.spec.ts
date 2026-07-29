import { test, expect } from '@playwright/test';

test.describe('Suite Login Invalido', () => {
  test('The user accesses the Log in page of the Demo Web Shop and submits an invalid login form', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Navega para a página de login
    const loginLink = page.locator('text=Log in');
    await loginLink.click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/login');

    // Etapa 2: Preenche o formulário de login com email válido e senha inválida
    const emailInput = page.locator('#Email');
    await emailInput.fill('existing@example.com');

    const passwordInput = page.locator('#Password');
    await passwordInput.fill('invalidpassword');

    // Etapa 3: Submite o formulário de login
    const loginButton = page.locator('role=button[name="Log in"]');
    await loginButton.click();

    // Verifica que o usuário permanece desautenticado e é informado que o login não foi concluído
    expect(page).toHaveURL('https://demowebshop.tricentis.com/login');
    const errorMessage = page.locator('#message-error');
    await expect(errorMessage).toContainText('Login was unsuccessful. Please correct the errors and try again.');
  });
});
