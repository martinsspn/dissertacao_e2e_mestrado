Condição experimental: baseline

ESPECIFICAÇÃO ORIGINAL:
Viewing an empty shopping cart: In a new browser context, the user accesses Shopping cart without adding any product. The system displays the Shopping cart page, shows a zero item count, and informs that the shopping cart is empty.


ARQUIVO GERADO QUE DEVE SER REPARADO:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Viewing an empty shopping cart', () => {
  test('should display the shopping cart page with zero items and an empty message', async ({ page }) => {
    // Navigate to the shopping cart page
    await page.goto('/shopping-cart');

    // Check if the item count is displayed as zero
    const itemCount = await page.textContent('.item-count');
    expect(itemCount).toBe('0');

    // Check if the empty cart message is displayed
    const emptyCartMessage = await page.textContent('.empty-cart-message');
    expect(emptyCartMessage).toContain('The shopping cart is empty.');
  });
});

```

EVIDÊNCIA DA FALHA DE EXECUÇÃO:
TimeoutError: page.textContent: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('.item-count')

DIAGNÓSTICO DA REVISÃO:
Representa o estado vazio em rota e classes inexistentes.

Faça uma única tentativa de reparo. Mantenha todas as verificações exigidas e devolva o arquivo TypeScript completo.