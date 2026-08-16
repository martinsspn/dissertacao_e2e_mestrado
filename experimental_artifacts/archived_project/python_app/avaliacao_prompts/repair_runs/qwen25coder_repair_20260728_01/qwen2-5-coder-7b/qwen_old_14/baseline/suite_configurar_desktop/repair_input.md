Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Configuration of a computer before purchase: The user accesses Computers and opens the Desktops category. The user opens a desktop that allows choosing its configuration. The user selects the options for a Fast processor, 4 GB memory, 400 GB disk, and Office Suite software. The user selects Add to cart. The system informs that the product has been added to the cart. The user accesses Shopping cart. The system displays the configured desktop among the items in the cart.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Desktop Configuration Test', () => {
  test('should configure and add a desktop to the cart', async ({ page }) => {
    // Access Computers and open the Desktops category
    await page.goto('/computers');
    await page.click('text=Desktops');

    // Open a desktop that allows choosing its configuration
    await page.click('text=Configure this desktop');

    // Select options for Fast processor, 4 GB memory, 400 GB disk, and Office Suite software
    await page.selectOption('#processor', 'Fast');
    await page.fill('#memory', '4GB');
    await page.fill('#disk', '400GB');
    await page.click('text=Office Suite');

    // Select Add to cart
    await page.click('text=Add to cart');

    // System informs that the product has been added to the cart
    await expect(page.locator('.cart-notification')).toContainText('Product added to cart');

    // Access Shopping cart
    await page.click('text=Shopping cart');

    // System displays the configured desktop among the items in the cart
    await expect(page.locator('.cart-item')).toContainText('Configured Desktop');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('text=Desktops')
    - locator resolved to 4 elements. Proceeding with the first one: <a href="/desktops">Desktops↵        </a>
  - attempting click action
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
    - waiting 20ms
    2 × waiting for element to be visible, enabled and stable
      - element is not visible
    - retrying click action
      - waiting 100ms
    19 × waiting for element to be visible, enabled and stable
       - element is not visible
     - retrying click action
       - waiting 500ms

DIAGNÓSTICO DA REVISÃO:
Segue o fluxo, mas inventa controles de configuração e regiões de confirmação/carrinho.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.