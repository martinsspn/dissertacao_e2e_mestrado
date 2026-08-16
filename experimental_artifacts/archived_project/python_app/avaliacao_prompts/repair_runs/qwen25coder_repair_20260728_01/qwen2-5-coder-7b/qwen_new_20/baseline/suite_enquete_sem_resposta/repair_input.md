Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Attempting to vote without selecting an answer: The user accesses the Demo Web Shop home page in a new browser context. In the Community poll titled Do you like nopCommerce?, the user does not select any answer and selects Vote. The system prevents the vote and informs the user to select an answer.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Community Poll Voting', () => {
  test('should prevent voting without selecting an answer', async ({ page }) => {
    // Access the Demo Web Shop home page in a new browser context
    await page.goto('https://demowebshop.tricentis.com/');

    // Navigate to the Community poll titled "Do you like nopCommerce?"
    await page.click('text="Community polls"');
    await page.click('text="Do you like nopCommerce?"');

    // Attempt to vote without selecting an answer
    await page.click('button:has-text("Vote")');

    // Verify that the system prevents the vote and informs the user to select an answer
    const alertText = await page.textContent('.alert.alert-danger');
    expect(alertText).toContain('Please select an answer before voting.');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('text="Community polls"')

DIAGNÓSTICO DA REVISÃO:
A intenção está correta, mas inventa navegação e um alerta inline diferente do controle real.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.