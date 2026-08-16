Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
The user must access the Digital downloads category, view the available digital items, and validate that the digital downloads page is visible.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Digital Downloads Page', () => {
  test('should display the digital downloads page', async ({ page }) => {
    // Navigate to the Digital downloads category
    await page.goto('/digital-downloads');

    // Wait for the digital items to be visible
    const digitalItems = page.locator('.digital-item');
    await expect(digitalItems).toBeVisible();

    // Validate that the digital downloads page is visible
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toHaveText('Digital Downloads');

    // Optionally, you can add more specific validations here
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
Error: expect(locator).toBeVisible() failed

Locator: locator('.digital-item')
Expected: visible
Timeout: 7000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 7000ms
  - waiting for locator('.digital-item')

DIAGNÓSTICO DA REVISÃO:
Rota correta, mas inventa .digital-item e usa capitalização incorreta no título.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.