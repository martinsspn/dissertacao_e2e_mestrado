```typescript
import { test, expect } from '@playwright/test';

test.describe('Suite Login Valido', () => {
  test('should log in with valid credentials and display account links', async ({ page }) => {
    // Etapa 1: Acessar a página de login
    await page.goto('https://demowebshop.tricentis.com/');
    await page.getByText("Log in", { exact: true }).first().click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/login');
    expect(await page.textContent('.title')).toBe('Welcome, Please Sign In!');

    // Etapa 2: Preencher os campos de email e senha
    await page.getByLabel("Email:", { exact: true }).fill(process.env.EMAIL || 'test@example.com');
    await page.getByLabel("Password:", { exact: true }).fill(process.env.PASSWORD || 'password123');

    // Etapa 3: Submeter o formulário de login
    await page.getByRole("button", { name: "Log in", exact: true }).click();
    expect(page).toHaveURL('https://demowebshop.tricentis.com/');

    // Verificar se os links da conta e logout estão presentes
    expect(await page.isVisible('.account')).toBe(true);
    expect(await page.isVisible('a[href="/logout"]')).toBe(true);
  });
});
```