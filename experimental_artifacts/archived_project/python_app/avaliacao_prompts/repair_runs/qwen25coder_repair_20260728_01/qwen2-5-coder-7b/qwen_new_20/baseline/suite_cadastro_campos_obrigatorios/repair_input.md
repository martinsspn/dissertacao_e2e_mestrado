Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Validation of required registration fields: The user accesses the Register page of the Demo Web Shop. The user leaves First name, Last name, Email, Password, and Confirm password empty. The user submits the form using the Register button. The system does not register the user and displays a required-field validation message for each of the five empty fields.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Validation of required registration fields', () => {
  test('should display validation messages for empty fields', async ({ page }) => {
    await page.goto('https://demowebshop.tricentis.com/register');

    // Leave all fields empty
    await page.click('input[name="FirstName"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="LastName"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="Email"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="Password"]');
    await page.keyboard.press('Tab');
    await page.click('input[name="ConfirmPassword"]');

    // Submit the form
    await page.click('button[type="submit"]');

    // Check for validation messages
    await expect(page.locator('.message-error')).toHaveText('First name is required.');
    await expect(page.locator('.message-error')).toHaveText('Last name is required.');
    await expect(page.locator('.message-error')).toHaveText('Email is required.');
    await expect(page.locator('.message-error')).toHaveText('Password is required.');
    await expect(page.locator('.message-error')).toHaveText('Confirm password is required.');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('button[type="submit"]')

DIAGNÓSTICO DA REVISÃO:
Submete campos vazios, mas usa um único locator incompatível para cinco mensagens distintas.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.