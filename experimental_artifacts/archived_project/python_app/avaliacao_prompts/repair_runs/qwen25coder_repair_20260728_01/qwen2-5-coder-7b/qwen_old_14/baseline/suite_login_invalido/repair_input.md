Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Login attempt with an invalid password: The user accesses the Log in page of the Demo Web Shop. The user fills in Email with the email of an existing account and Password with an invalid password provided by the testing environment. The user submits the login form. The system keeps the user unauthenticated and informs that the login was not completed.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Login attempt with an invalid password', () => {
  test('should keep the user unauthenticated and inform of failed login', async ({ page }) => {
    // Access the Log in page
    await page.goto('https://demowebshop.tricentis.com/login');

    // Fill in Email with an existing account's email
    await page.fill('#Email', 'existing@example.com');

    // Fill in Password with an invalid password provided by the testing environment
    await page.fill('#Password', process.env.INVALID_PASSWORD);

    // Submit the login form
    await page.click('#login-button');

    // Verify that the user is kept unauthenticated and informed of failed login
    const errorMessage = await page.textContent('.message-error');
    expect(errorMessage).toContain('Login was unsuccessful. Please correct the errors and try again.');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('#login-button')

DIAGNÓSTICO DA REVISÃO:
Campos e oráculo são adequados; botão de login não existe e o email não vem do ambiente.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.