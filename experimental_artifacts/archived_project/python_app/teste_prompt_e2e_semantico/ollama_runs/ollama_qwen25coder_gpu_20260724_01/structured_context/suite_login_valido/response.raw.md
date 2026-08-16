```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Login Valido', () => {
  test('should log in with valid credentials and display account links', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/');

    // Etapa 1: Acessar a página de login
    const loginLink = page.locator('text=Log in');
    await loginLink.click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/login');

    // Etapa 2: Preencher o formulário de login
    const emailInput = page.locator('#Email');
    await emailInput.fill(process.env.EMAIL || 'test@example.com');

    const passwordInput = page.locator('#Password');
    await passwordInput.fill(process.env.PASSWORD || 'password123');

    // Etapa 3: Submeter o formulário de login
    const loginButton = page.locator('role=button[name="Log in"]');
    await loginButton.click();

    // Verificar que a página foi redirecionada para a conta do usuário
    expect(page).toHaveURL('https://demowebshop.tricentis.com/Account/Manage');

    // Verificar que os links de conta e logout estão presentes
    const accountLink = page.locator('text=Welcome, Please Sign In!');
    await expect(accountLink).toBeVisible();

    const logoutLink = page.locator('text=Log out');
    await expect(logoutLink).toBeVisible();
  });
});
```