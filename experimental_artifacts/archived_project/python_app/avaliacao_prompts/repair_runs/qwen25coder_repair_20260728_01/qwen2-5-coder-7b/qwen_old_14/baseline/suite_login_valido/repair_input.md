Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Login with valid credentials: The user accesses the Log in page of the Demo Web Shop. The user fills in Email and Password with the valid credentials provided by the testing environment. The user submits the login form. The system authenticates the user and displays the account and Log out links.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Login with valid credentials', () => {
  test('should authenticate user and display account and logout links', async ({ page }) => {
    // Access the Log in page of the Demo Web Shop
    await page.goto('https://demowebshop.tricentis.com/login');

    // Fill in Email and Password with the valid credentials provided by the testing environment
    await page.fill('#Email', process.env.TEST_EMAIL || 'test@example.com');
    await page.fill('#Password', process.env.TEST_PASSWORD || 'password123');

    // Submit the login form
    await page.click('button[type="submit"]');

    // The system authenticates the user and displays the account and Log out links
    await expect(page.locator('.account')).toBeVisible();
    await expect(page.locator('#logoutLink')).toBeVisible();
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('button[type="submit"]')

DIAGNÓSTICO DA REVISÃO:
Usa credenciais do ambiente e campos corretos; botão submit e id de logout estão errados.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.