Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Opening the institutional information page: The user accesses the Demo Web Shop home page. In the Information section of the footer, the user selects About us. The system displays the About us page and its corresponding heading.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Institutional Information Page', () => {
  test('should display the About us page and its corresponding heading', async ({ page }) => {
    // Access the Demo Web Shop home page
    await page.goto('https://demo.webshopapp.com');

    // Select About us in the Information section of the footer
    await page.click('footer a:has-text("Information")');
    await page.click('a:has-text("About us")');

    // Verify that the About us page is displayed
    expect(page.url()).toContain('/about-us');

    // Verify that the corresponding heading is displayed
    const heading = await page.locator('h1').textContent();
    expect(heading).toBe('About Us');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('footer a:has-text("Information")')

DIAGNÓSTICO DA REVISÃO:
Intenção e heading presentes, mas o domínio e a interação com a seção Information são inventados.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.